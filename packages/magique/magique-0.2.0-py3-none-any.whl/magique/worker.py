import typing as T
import asyncio
import uuid
import functools
import traceback

import websockets
from funcdesc import parse_func
from executor.engine import Engine, EngineSetting
from executor.engine.launcher import launcher

from .utils.log import logger
from .utils.network import get_free_port, get_ip_addresses
from .protocol import (
    ServiceInfo, RegisterServiceRequest,
    InvokeServiceRequest, InvokeServiceResponse,
    InvokeFuture, GetFutureResultRequest, FutureResponse,
)
from .ser import DefaultSerializer
from .utils.network import ws_connect, ws_serve
from .base import NetworkObject

if T.TYPE_CHECKING:
    from .client import ServiceProxy


class MagiqueWorker(NetworkObject):
    def __init__(
        self,
        service_name: str,
        server_host: str = "magique.spateo.aristoteleo.com",
        server_port: int = 80,
        link_to_server: bool = True,
        serializer: T.Optional[DefaultSerializer] = None,
        use_worker_server: bool = True,
        self_host: str = "localhost",
        self_port: T.Optional[int] = None,
        engine_setting: T.Optional[EngineSetting] = None,
        need_auth: bool = False,
    ):
        super().__init__(serializer or DefaultSerializer())
        self.server_host = server_host
        self.server_port = server_port
        self.server_uri = f"ws://{server_host}:{server_port}/ws"
        self.link_to_server = link_to_server
        self.service_name = service_name
        self.description = ""
        self.functions = {}
        self.service_id = str(uuid.uuid4())
        self.self_host = self_host
        self.self_port = self_port or get_free_port()
        self.use_worker_server = use_worker_server
        self.self_uri = f"ws://{self.self_host}:{self.self_port}"
        self.actions = {}
        self.engine = Engine(setting=engine_setting)
        self._invokeid_to_jobid = {}
        self.need_auth = need_auth

    async def handle_request(self, message: bytes, websocket):
        request = self.serializer.deserialize(message)
        logger.info(f"Received request:\n{request}")
        action = request.get("action")
        if action == "invoke_service":
            await self.handle_invoke_function(request, websocket)
        elif action == "get_service_info":
            service_info = self.get_service_info()
            await self.send_message(websocket, service_info.encode())
        elif action == "get_future_result":
            await self.handle_get_future_result(request, websocket)
        elif action == "ping":
            response = {"status": "success", "message": "pong"}
            await self.send_message(websocket, response)
        elif action in self.actions:
            await self.actions[action](websocket, request)
        elif action == "auth":
            await self.handle_auth(request, websocket)
        else:
            logger.error(f"Unknown action: {action}")

    async def handle_invoke_function(self, request: dict, websocket):
        invoke_request = InvokeServiceRequest.decode(request)
        if invoke_request.function_name not in self.functions:
            await self.send_message(
                websocket,
                InvokeServiceResponse(
                    invoke_id=invoke_request.invoke_id,
                    status="error",
                    result="Function not found",
                ).encode(),
            )
            return
        function, job_type = self.functions[invoke_request.function_name]
        f_launcher = launcher(
            function, engine=self.engine, job_type=job_type,
            async_mode=True)
        parameters = await self.resolve_parameters(invoke_request.parameters)
        if "__client_id__" in function.__code__.co_varnames:
            # inject client_id into the function
            parameters["__client_id__"] = invoke_request.client_id
        job = await f_launcher.submit(**parameters)
        self._invokeid_to_jobid[invoke_request.invoke_id] = job.id
        if invoke_request.return_future:
            future = InvokeFuture(
                invoke_id=invoke_request.invoke_id,
                service_id=self.service_id,
            )
            future_response = FutureResponse(future)
            await self.send_message(websocket, future_response.encode())
        else:
            await self._wait_and_send_job(
                job, websocket, invoke_request.invoke_id)

    async def handle_get_future_result(self, request: dict, websocket):
        get_future_result_request = GetFutureResultRequest.decode(request)
        future = get_future_result_request.future
        job_id = self._invokeid_to_jobid.get(future.invoke_id)
        if job_id is None:
            logger.error(f"Job not found: id={job_id}")
            response = InvokeServiceResponse(
                invoke_id=future.invoke_id,
                status="error",
                result="Job not found",
            )
            await self.send_message(websocket, response.encode())
            return
        job = self.engine.jobs.get_job_by_id(job_id)
        await self._wait_and_send_job(job, websocket, future.invoke_id)

    async def _wait_and_send_job(self, job, websocket, invoke_id):
        await job.join()
        if job.status == "done":
            result = job.result()
            status = "success"
        else:
            e = job.exception()
            result = "\n".join(traceback.format_exception(e))
            status = "error"
        response = InvokeServiceResponse(
            invoke_id=invoke_id,
            status=status,
            result=result,
        ).encode()
        await self.send_message(websocket, response)

    async def resolve_parameters(self, parameters: dict):
        for key, value in parameters.items():
            if isinstance(value, InvokeFuture):
                # wait for the future result
                future = value
                if future.service_id != self.service_id:
                    logger.info(
                        f"Future from other service: id={future.service_id}"
                        f"Connecting to the server at {self.server_uri}"
                    )
                    service = await self.get_another_service(future.service_id)
                    result = await service.fetch_future_result(future)
                else:
                    job_id = self._invokeid_to_jobid.get(future.invoke_id)
                    if job_id is None:
                        logger.error(f"Job not found: id={job_id}")
                        raise ValueError(f"Job not found: id={job_id}")
                    job = self.engine.jobs.get_job_by_id(job_id)
                    await job.join()
                    if job.status == "done":
                        result = job.result()
                    else:
                        raise RuntimeError(f"Job failed: id={job_id}")
                parameters[key] = result
        return parameters

    async def get_another_service(self, service_id: str) -> "ServiceProxy":
        if not self.link_to_server:
            raise ValueError(
                "Cannot resolve future from other service"
                "without linking to the server")
        from .client import connect_to_server
        server = await connect_to_server(
            self.server_host, self.server_port)
        service = await server.get_service(service_id)
        return service

    def get_service_info(self):
        potential_ip_addresses = [
            "127.0.0.1",
        ] + [
            v for v in get_ip_addresses(ipv6=False).values()
            if v != "127.0.0.1"
        ]
        service_info = ServiceInfo(
            service_name=self.service_name,
            service_id=self.service_id,
            description=self.description,
            functions_description={
                name: parse_func(func)
                for name, (func, _) in self.functions.items()
            },
            use_worker_server=self.use_worker_server,
            worker_server_port=self.self_port,
            potential_ip_addresses=potential_ip_addresses,
            need_auth=self.need_auth,
        )
        return service_info

    async def register_to_server(self, websocket):
        logger.info(f"Connected to the server at {self.server_uri}")
        service_info = self.get_service_info()
        registration = RegisterServiceRequest(service_info).encode()
        logger.info(f"Sending registration request:\n{registration}")
        await self.send_message(websocket, registration)
        response = await self.receive_message(websocket)
        logger.info(f"Received registration response:\n{response}")

    async def handle_server_requests(self, websocket):
        async for message in websocket:
            await self.handle_request(message, websocket)

    async def handle_client_request(self, websocket):
        try:
            async for message in websocket:
                await self.handle_request(message, websocket)
        except websockets.exceptions.ConnectionClosed:
            logger.debug("Client connection closed")

    async def start_worker_server(self):
        worker_server = await ws_serve(
            self.handle_client_request,
            self.self_host,
            self.self_port,
        )
        logger.info(f"Worker server started at {self.self_uri}")
        await worker_server.wait_closed()

    async def register_and_handle_server_requests(self):
        async with ws_connect(self.server_uri) as websocket:
            await self.register_to_server(websocket)
            await self.handle_server_requests(websocket)

    async def run(self):
        coroutines = []
        if self.link_to_server:
            coroutines.append(self.register_and_handle_server_requests())
        if self.use_worker_server:
            coroutines.append(self.start_worker_server())
        await asyncio.gather(*coroutines)

    def register(self, function: T.Optional[T.Callable] = None, **kwargs):
        if function is None:
            return functools.partial(self.register, **kwargs)
        job_type = kwargs.get("job_type", "local")
        self.functions[function.__name__] = (function, job_type)
        return function

    def register_action(self, action: str):
        def _register_action(
                function: T.Callable[[dict, object], T.Coroutine]):
            self.actions[action] = function
            return function
        return _register_action

    async def handle_auth(self, request: dict, websocket):
        user_info = request.get("user_info")
        auth_id = request.get("auth_id")
        resp = {
            "action": "worker_auth_response",
            "status": "failed",
            "auth_id": auth_id,
        }
        if self.auth_function(user_info):
            resp["status"] = "success"
        await self.send_message(websocket, resp)

    def auth_function(self, user_info: dict) -> bool:
        return True

    def register_auth(self, function: T.Callable[[dict], bool]):
        self.auth_function = function
        return function


def main():
    worker = MagiqueWorker("test_worker")
    asyncio.run(worker.run())


if __name__ == "__main__":
    main()
