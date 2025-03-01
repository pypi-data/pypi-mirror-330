import abc
import json

import msgpack
import cloudpickle


class Serializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, data: dict) -> bytes:
        pass

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> dict:
        pass


class DefaultSerializer(Serializer):
    def serialize_pyobj(self, data: object) -> bytes:
        return cloudpickle.dumps(data)

    def deserialize_pyobj(self, data: bytes) -> object:
        return cloudpickle.loads(data)

    def mixed_serialize(self, data: dict) -> bytes:
        """Try to serialize the data as msgpack, if that fails, serialize as pyobj"""
        try:
            method = "msgpack"
            payload = msgpack.packb(data)
        except:
            method = "cloudpickle"
            payload = self.serialize_pyobj(data)
        return msgpack.packb({"method": method, "payload": payload})

    def mixed_deserialize(self, data: bytes) -> dict:
        """Try to deserialize the data as msgpack, if that fails, deserialize as pyobj"""
        data = msgpack.unpackb(data)
        method = data["method"]
        payload = data["payload"]
        if method == "msgpack":
            return msgpack.unpackb(payload)
        elif method == "cloudpickle":
            return self.deserialize_pyobj(payload)

    def serialize(self, data: dict) -> bytes:
        action = data.get("action")
        if action == "invoke_service":
            parameters = data["parameters"]
            ser_parameters = {}
            for key, value in parameters.items():
                ser_parameters[key] = self.mixed_serialize(value)
            return msgpack.packb({**data, "parameters": ser_parameters})
        elif action == "worker_response":
            result = data.pop("result")
            ser_result = self.mixed_serialize(result)
            return msgpack.packb({**data, "result": ser_result})
        return msgpack.packb(data)

    def deserialize(self, data: bytes) -> dict:
        res: dict = msgpack.unpackb(data)
        if not ("action" in res):
            return res
        action = res["action"]
        if action == "invoke_service":
            ser_parameters = res.pop("parameters")
            parameters = {}
            for key, value in ser_parameters.items():
                parameters[key] = self.mixed_deserialize(value)
            res["parameters"] = parameters
        elif action == "worker_response":
            result = res.pop("result")
            ser_result = self.mixed_deserialize(result)
            res["result"] = ser_result
        return res
