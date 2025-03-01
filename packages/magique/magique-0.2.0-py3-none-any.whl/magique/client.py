import typing as T
import asyncio
import uuid

from .protocol import (
    ServiceInfo, InvokeServiceRequest, InvokeServiceResponse,
    InvokeFuture, GetFutureResultRequest,
)
from .utils.log import logger
from .ser import DefaultSerializer
from .utils.network import ws_connect
from .base import NetworkObject


class MagiqueError(Exception):
    pass


class MagiqueFutureError(MagiqueError):
    pass


class LoginError(MagiqueError):
    pass


class ServiceProxy(NetworkObject):
    def __init__(
        self,
        uri: str,
        client_id: T.Optional[str] = None,
        service_info: T.Optional[ServiceInfo] = None,
        serializer: T.Optional[DefaultSerializer] = None,
        jwt: T.Optional[str] = None,
    ):
        super().__init__(serializer or DefaultSerializer())
        self.uri = uri
        self.service_info = service_info
        self.connection = None
        self.client_id = client_id
        if self.client_id is None:
            self.client_id = str(uuid.uuid4())
        self.jwt = jwt
        self.direct_connection = False

    async def ensure_connection(
        self,
        force: bool = False,
        ping_timeout: float = 0.1,
    ):
        if self.connection is None:
            self.connection = await ws_connect(self.uri)
        else:
            if force:
                await self.connection.close()
                self.connection = await ws_connect(self.uri)
            try:
                await asyncio.wait_for(self.ping(), timeout=ping_timeout)
            except Exception:
                self.connection = await ws_connect(self.uri)
        return self.connection

    async def ping(self):
        await self.send_message(self.connection, {"action": "ping"})
        msg = await self.receive_message(self.connection)
        assert msg["message"] == "pong"

    async def invoke(
        self,
        function_name: str,
        parameters: dict | None = None,
        return_future: bool = False,
    ) -> T.Any:
        if parameters is None:
            parameters = {}
        request = InvokeServiceRequest(
            client_id=self.client_id,
            service_id=self.service_info.service_id,
            function_name=function_name,
            parameters=parameters,
            return_future=return_future,
        )
        websocket = await self.ensure_connection()
        await self.send_message(websocket, request.encode())
        resp = await self.receive_message(websocket)
        if return_future:
            return InvokeFuture.decode(resp)
        else:
            response = InvokeServiceResponse.decode(resp)
            if resp.get("status") == "error":
                raise MagiqueError(resp.get("message") or resp.get("result"))
            return response.result

    async def fetch_service_info(self) -> ServiceInfo:
        request = {"action": "get_service_info"}
        websocket = await self.ensure_connection()
        await self.send_message(websocket, request)
        resp = await self.receive_message(websocket)
        response = ServiceInfo.decode(resp)
        self.service_info = response
        return response

    async def fetch_future_result(self, future: InvokeFuture) -> T.Any:
        request = GetFutureResultRequest(future)
        websocket = await self.ensure_connection()
        await self.send_message(websocket, request.encode())
        resp = await self.receive_message(websocket)
        if resp.get("status") == "error":
            raise MagiqueFutureError(resp.get("message"))
        response = InvokeServiceResponse.decode(resp)
        return response.result

    async def try_direct_connection(self, timeout: float = 1.0):
        logger.info(
            f"Trying direct connection to {self.service_info.service_name}")
        port = self.service_info.worker_server_port
        for ip in self.service_info.potential_ip_addresses:
            uri = f"ws://{ip}:{port}"
            try:
                async with ws_connect(
                    uri,
                    ping_timeout=timeout,
                    open_timeout=timeout,
                ):
                    self.uri = uri
                    self.direct_connection = True
                    logger.info(f"Connected to {uri}")
                    return
            except Exception as e:
                logger.info(f"Error connecting to {uri}: {e}")
        logger.warning(
            "Failed to connect to any potential ip address, "
            "using the server as a fallback"
        )

    async def close_connection(self):
        if self.connection is not None:
            await self.connection.close()
            self.connection = None


class ServerProxy(NetworkObject):
    def __init__(
        self,
        host="localhost",
        port=8765,
        serializer: T.Optional[DefaultSerializer] = None,
    ):
        super().__init__(serializer or DefaultSerializer())
        self.uri = f"ws://{host}:{port}/ws"
        self.jwt = None
        self.client_id = str(uuid.uuid4())

    async def list_services(self) -> T.List[ServiceInfo]:
        async with ws_connect(self.uri) as websocket:
            await self.send_message(
                websocket,
                {"action": "get_services", "jwt": self.jwt}
            )
            response = await self.receive_message(websocket)
            services = [
                ServiceInfo.decode(service)
                for service in response["services"]
            ]
            return services

    async def get_service(
        self,
        name_or_id: str,
        try_direct_connection: bool = True,
    ) -> ServiceProxy:
        services = await self.list_services()
        service = None
        for s in services:
            if s.service_id == name_or_id:
                service = s
                break
            elif s.service_name == name_or_id:
                service = s
                logger.info(f"Found service with name {name_or_id}: {service}")
                break
        if service is None:
            raise ValueError(f"Service with id or name {name_or_id} not found")
        proxy = ServiceProxy(self.uri, self.client_id, service, self.serializer, self.jwt)
        if service.use_worker_server and try_direct_connection:
            await proxy.try_direct_connection()
        return proxy

    async def ping(self):
        async with ws_connect(self.uri) as websocket:
            await self.send_message(websocket, {"action": "ping"})
            msg = await self.receive_message(websocket)
            assert msg["message"] == "pong"

    async def login(self):
        if self.jwt is not None:
            logger.info("Already logged in.")
            return
        async with ws_connect(self.uri) as websocket:
            await self.send_message(websocket, {"action": "login"})
            msg = await self.receive_message(websocket)
            auth_url = msg["auth_url"]
            logger.info(f"Open this URL in your browser to log in:\n{auth_url}")
            msg = await self.receive_message(websocket)
            if msg.get("status") == "error":
                raise LoginError(msg.get("message"))
            jwt = msg.get("jwt")
            self.jwt = jwt
            logger.info("Login successful!")


async def connect_to_server(host: str, port: int=80, **kwargs) -> ServerProxy:
    server = ServerProxy(host, port, **kwargs)
    await server.ping()
    return server


async def connect_to_service(host: str, port: int, **kwargs) -> ServiceProxy:
    service_uri = f"ws://{host}:{port}"
    service_proxy = ServiceProxy(service_uri, **kwargs)
    await service_proxy.fetch_service_info()
    return service_proxy
