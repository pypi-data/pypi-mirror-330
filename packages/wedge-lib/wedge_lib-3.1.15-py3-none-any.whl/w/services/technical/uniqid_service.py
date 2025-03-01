from abc import ABC, abstractmethod
from typing import Type
from uuid import uuid4

from w.services.abstract_service import AbstractService


class AbstractUniqIdGenerator(ABC):
    @classmethod
    @abstractmethod
    def next_id(cls) -> str: ...  # pragma: no cover


class FakeGenerator(AbstractUniqIdGenerator):
    start: str = "000000000000000000000000"
    _last_uuid: str = "000000000000000000000000"

    @classmethod
    def next_id(cls) -> str:
        cls._last_uuid = cls._increment_id(cls._last_uuid)
        return cls._last_uuid

    @classmethod
    def reset(cls, last_id=None):
        cls.start = last_id or "000000000000000000000000"
        cls._last_uuid = cls.start

    @staticmethod
    def _increment_id(str_id):
        str_id = str(int(str_id) + 1)
        return "0" * (24 - len(str_id)) + str_id


class UuidGenerator(AbstractUniqIdGenerator):
    @classmethod
    def next_id(cls) -> str:
        return str(uuid4())


class UniqIdService(AbstractService):
    _generator: Type[AbstractUniqIdGenerator] = UuidGenerator

    @classmethod
    def get(cls):
        return cls._generator.next_id()

    @classmethod
    def set_fake_generator(cls):
        FakeGenerator.reset()
        cls._generator = FakeGenerator

    @classmethod
    def clear(cls):
        cls._generator = UuidGenerator
