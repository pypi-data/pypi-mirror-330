import asyncio

import pytest
from executor.engine import Engine, ProcessJob

from magique.server import MagiqueServer
from magique.client import connect_to_server, connect_to_service, MagiqueError
from magique.worker import MagiqueWorker


TEST_HOST = "localhost"
TEST_PORT = 9000


def start_server():
    server = MagiqueServer(TEST_HOST, TEST_PORT)
    server.run()


def start_worker():
    worker = MagiqueWorker("test_worker", TEST_HOST, TEST_PORT)

    @worker.register(job_type="process")
    def add_numbers(a: int, b: int) -> int:
        return a + b

    @worker.register
    def print_obj(obj: object) -> str:
        print(obj)
        return 'hello'

    @worker.register
    def large_list(n: int) -> list:
        return list(range(n))

    @worker.register
    def raise_error():
        raise Exception("test error")

    @worker.register
    def get_client_id(__client_id__: str) -> str:
        return __client_id__

    asyncio.run(worker.run())


async def test_basic_connection():
    engine = Engine()
    server_job = ProcessJob(start_server)
    await engine.submit_async(server_job)
    await asyncio.sleep(2)
    worker_job = ProcessJob(start_worker)
    await engine.submit_async(worker_job)
    await asyncio.sleep(2)

    server = await connect_to_server(TEST_HOST, TEST_PORT)
    services = await server.list_services()
    assert len(services) == 1
    assert services[0].service_name == "test_worker"
    service = await server.get_service(
        "test_worker", try_direct_connection=False)
    res = await service.invoke("add_numbers", {"a": 1, "b": 2})
    assert res == 3
    res = await service.invoke("add_numbers", {"a": 2, "b": 2})
    assert res == 4

    fut1 = await service.invoke(
        "add_numbers", {"a": 2, "b": 2}, return_future=True)
    fut2 = await service.invoke(
        "add_numbers", {"a": fut1, "b": 2}, return_future=True)
    res = await service.fetch_future_result(fut2)
    assert res == 6

    with pytest.raises(MagiqueError, match="test error"):
        try:
            await service.invoke("raise_error")
        except MagiqueError as e:
            print(e)
            raise

    with pytest.raises(MagiqueError, match="Function not found"):
        await service.invoke("not_exist")

    class TestClass:
        pass

    res = await service.invoke("print_obj", {"obj": TestClass()})
    assert res == "hello"

    size = 1 * int(1e6)  # 1 million, about 5MB
    res = await service.invoke("large_list", {"n": size})
    assert len(res) == size

    res = await service.invoke("get_client_id", {})
    assert res == service.client_id

    await service.close_connection()
    await worker_job.cancel()
    services = await server.list_services()
    assert len(services) == 0
    await server_job.cancel()


async def test_direct_connection():
    engine = Engine()
    server_job = ProcessJob(start_server)
    await engine.submit_async(server_job)
    await asyncio.sleep(2)
    worker_job = ProcessJob(start_worker)
    await engine.submit_async(worker_job)
    await asyncio.sleep(2)

    server = await connect_to_server(TEST_HOST, TEST_PORT)
    service = await server.get_service(
        "test_worker", try_direct_connection=True)
    res = await service.invoke("add_numbers", {"a": 1, "b": 2})
    assert res == 3

    future = await service.invoke(
        "add_numbers", {"a": 1, "b": 2}, return_future=True)
    res = await service.fetch_future_result(future)
    assert res == 3

    size = int(1e6)  # 1 million, about 5MB
    res = await service.invoke("large_list", {"n": size})
    assert len(res) == size

    await service.close_connection()
    await worker_job.cancel()
    await server_job.cancel()


async def test_service_connection():
    def start_worker():
        worker = MagiqueWorker(
            "test_worker",
            link_to_server=False,
            use_worker_server=True,
            self_host=TEST_HOST,
            self_port=TEST_PORT,
        )

        @worker.register
        def add_numbers(a: int, b: int) -> int:
            return a + b

        asyncio.run(worker.run())

    engine = Engine()
    worker_job = ProcessJob(start_worker)
    await engine.submit_async(worker_job)
    await asyncio.sleep(1)

    service = await connect_to_service(TEST_HOST, TEST_PORT)
    res = await service.invoke("add_numbers", {"a": 1, "b": 2})
    assert res == 3
    await service.close_connection()

    await worker_job.cancel()


async def test_future_from_other_service():
    def start_worker1():
        worker = MagiqueWorker("worker1", TEST_HOST, TEST_PORT)

        @worker.register
        def add_numbers(a: int, b: int) -> int:
            return a + b

        asyncio.run(worker.run())

    def start_worker2():
        worker = MagiqueWorker("worker2", TEST_HOST, TEST_PORT)

        @worker.register
        def multiply_numbers(a: int, b: int) -> int:
            return a * b

        asyncio.run(worker.run())

    engine = Engine()
    server_job = ProcessJob(start_server)
    await engine.submit_async(server_job)
    await asyncio.sleep(2)
    worker1_job = ProcessJob(start_worker1)
    worker2_job = ProcessJob(start_worker2)
    await engine.submit_async(worker1_job, worker2_job)
    await asyncio.sleep(2)

    server = await connect_to_server(TEST_HOST, TEST_PORT)
    service1 = await server.get_service("worker1")
    service2 = await server.get_service("worker2")
    fut1 = await service1.invoke(
        "add_numbers", {"a": 1, "b": 2}, return_future=True)
    fut2 = await service2.invoke(
        "multiply_numbers", {"a": fut1, "b": fut1}, return_future=True)
    res = await service2.fetch_future_result(fut2)
    assert res == 9

    await service1.close_connection()
    await service2.close_connection()
    await worker1_job.cancel()
    await worker2_job.cancel()
    await server_job.cancel()
