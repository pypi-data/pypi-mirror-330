import asyncio
import uuid
from collections import defaultdict
import typing as T

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fire import Fire

from .utils.log import logger
from .protocol import (
    ServiceInfo, RegisterServiceRequest,
    InvokeServiceRequest, InvokeServiceResponse,
    GetFutureResultRequest, FutureResponse,
)
from .ser import DefaultSerializer
from .auth import AuthManager


class MagiqueServer:
    def __init__(
        self, host: str = "localhost", port: int = 8765,
        serializer: T.Optional[DefaultSerializer] = None,
    ):
        self.host = host
        self.port = port
        self.app = FastAPI(title="Magique Server")
        self.service_registry: T.Dict[str, ServiceInfo] = {}
        self.pending_requests: T.Dict[str, asyncio.Future] = defaultdict(
            asyncio.Future
        )
        self.auth = AuthManager(
            redirect_uri=f"http://{host}:{port}/auth_callback"
        )
        self._setup_routes()
        self.serializer = serializer or DefaultSerializer()
        self.worker_auth_futures: T.Dict[str, asyncio.Future] = {}

    async def send_message(self, websocket: WebSocket, message: dict):
        ser_message = self.serializer.serialize(message)
        await websocket.send_bytes(ser_message)

    async def receive_message(self, websocket: WebSocket) -> dict:
        message = await websocket.receive_bytes()
        return self.serializer.deserialize(message)

    def _setup_routes(self):
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            try:
                await self._handle_websocket(websocket)
            except WebSocketDisconnect:
                # Clean up any services registered by this websocket
                self._cleanup_disconnected_service(websocket)

        self.app.get("/auth_callback")(self.auth.auth_callback)

    def _cleanup_disconnected_service(self, websocket: WebSocket):
        # Remove any services associated with the disconnected websocket
        disconnected_services = [
            service_id for service_id, info in self.service_registry.items()
            if info.websocket == websocket
        ]
        for service_id in disconnected_services:
            del self.service_registry[service_id]
            logger.info(
                f"Service {service_id} disconnected and removed from registry")

    async def _handle_websocket(self, websocket: WebSocket) -> None:
        try:
            request = await self.receive_message(websocket)
            action = request.get("action")
            logger.info(
                f"Received action: {action} from {websocket.client.host}")
            response: T.Optional[dict] = None

            # handle actions from the client or worker's registration
            if action == "invoke_service":
                response = await self.handle_invoke_service(request)
            elif action == "register_service":  # from worker
                await self.handle_register_service(request, websocket)
            elif action == "get_services":
                response = await self.handle_get_services(request, websocket)
            elif action == "get_future_result":
                response = await self.handle_get_future_result(request)
            elif action == "ping":
                response = {"status": "success", "message": "pong"}
            elif action == "login":
                response = await self.handle_login(websocket)
            else:
                response = {
                    "status": "error",
                    "message": "Unknown action."
                }

            if response:
                await self.send_message(websocket, response)

        except Exception as e:
            logger.error(f"Error handling websocket:\n{e}")
            import traceback
            traceback.print_exc()
            response = {"status": "error", "message": str(e)}
            await self.send_message(websocket, response)

    async def handle_login(self, websocket: WebSocket) -> dict:
        auth_url = self.auth.get_auth_url()
        await self.send_message(websocket, {"auth_url": auth_url})
        timeout = self.auth.login_timeout  # seconds
        time_delta = 0.5
        while True:
            # wait for the user to login
            if self.auth._auth_response is not None:
                break

            await asyncio.sleep(time_delta)
            timeout -= time_delta
            if timeout <= 0:
                logger.error("Login timeout.")
                return {"status": "error", "message": "Login timeout."}
        try:
            await self.auth.fetch_token()
            user_info = await self.auth.get_user_info()
            logger.info(f"User logged in:\n{user_info}")
        except Exception as e:
            logger.error(f"Failed to fetch token or get user info:\n{e}")
            return {"status": "error", "message": str(e)}
        jwt = self.auth.create_jwt(user_info)
        return {"status": "success", "jwt": jwt}

    async def handle_register_service(
        self, request: dict, websocket,
    ) -> dict:
        try:
            register_request = RegisterServiceRequest.decode(request)
            service_info = register_request.service_info
            service_info.websocket = websocket
        except Exception as e:
            logger.error(f"Error registering service:\n{e}")
            return {"status": "error", "message": str(e)}
        self.service_registry[service_info.service_id] = service_info
        resp = {
            "status": "success",
            "message": (
                f"Service '{service_info.service_name}'"
                f"({service_info.service_id}) registered successfully."
            ),
        }
        await self.send_message(websocket, resp)

        while True:
            # loop for listening the worker's message
            try:
                request = await self.receive_message(websocket)
                logger.info(f"Received request from worker: {request}")
                # handle actions from worker
                action = request.get("action")
                if action == "worker_response":
                    await self.handle_worker_response(request)
                elif action == "future_response":
                    await self.handle_future_response(request)
                elif action == "worker_auth_response":
                    await self.handle_worker_auth_response(request)
            except WebSocketDisconnect:
                logger.info("Websocket disconnected")
                # unregister services
                del self.service_registry[service_info.service_id]
                break

    async def handle_worker_auth_response(self, request: dict) -> None:
        auth_id = request.get("auth_id")
        success = request.get("status") == "success"
        if auth_id in self.worker_auth_futures:
            f = self.worker_auth_futures[auth_id]
            f.set_result(success)
            del self.worker_auth_futures[auth_id]

    async def handle_get_services(self, request: dict, websocket: WebSocket) -> dict:
        jwt = request.get("jwt")
        user_info = None
        if jwt is not None:
            user_info = self.auth.decode_jwt(jwt)
            logger.info(f"User info:\n{user_info}")
        services = list(self.service_registry.values())
        encoded_services = []
        for service in services:
            if service.need_auth:
                if user_info is not None:
                    auth_id = str(uuid.uuid4())
                    await self.send_message(
                        service.websocket,
                        {
                            "action": "auth",
                            "user_info": user_info,
                            "auth_id": auth_id,
                        }
                    )
                    f = self.worker_auth_futures[auth_id] = asyncio.Future()
                    success = await f
                    if success:
                        encoded_services.append(service.encode())
            else:
                encoded_services.append(service.encode())
        return {
            "status": "success",
            "services": encoded_services,
        }

    async def handle_invoke_service(self, request: dict) -> dict:
        invoke_request = InvokeServiceRequest.decode(request)
        if invoke_request.service_id in self.service_registry:
            service_info = self.service_registry[invoke_request.service_id]
            service_socket = service_info.websocket
            request_id = invoke_request.invoke_id
            self.pending_requests[request_id] = asyncio.Future()

            e = invoke_request.encode()
            await self.send_message(service_socket, e)

            invoke_response = await self.pending_requests[request_id]
            del self.pending_requests[request_id]
            return invoke_response.encode()

        else:
            return {
                "status": "error",
                "message": f"Service '{invoke_request.service_id}' not found.",
            }

    async def handle_get_future_result(self, request: dict) -> dict:
        get_future_result_request = GetFutureResultRequest.decode(request)
        invoke_future = get_future_result_request.future
        if invoke_future.service_id in self.service_registry:
            service_info = self.service_registry[invoke_future.service_id]
            service_socket = service_info.websocket
            request_id = invoke_future.invoke_id
            self.pending_requests[request_id] = asyncio.Future()
            e = get_future_result_request.encode()
            await self.send_message(service_socket, e)

            invoke_response = await self.pending_requests[request_id]
            del self.pending_requests[request_id]
            return invoke_response.encode()
        else:
            return {
                "status": "error",
                "message": f"Service '{invoke_future.service_id}' not found.",
            }

    async def handle_worker_response(self, request: dict) -> None:
        invoke_response = InvokeServiceResponse.decode(request)
        invoke_id = invoke_response.invoke_id
        if invoke_id in self.pending_requests:
            self.pending_requests[invoke_id].set_result(invoke_response)

    async def handle_future_response(self, request: dict) -> None:
        future_response = FutureResponse.decode(request)
        invoke_id = future_response.future.invoke_id
        if invoke_id in self.pending_requests:
            self.pending_requests[invoke_id].set_result(future_response)

    def run(self, **kwargs) -> None:
        uvicorn.run(self.app, host=self.host, port=self.port, **kwargs)


def run_server(host: str = "localhost", port: int = 8765) -> None:
    load_dotenv()
    server = MagiqueServer(host, port)
    server.run()


if __name__ == "__main__":
    Fire(run_server)
