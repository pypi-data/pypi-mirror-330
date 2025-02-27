from abc import ABC
from abc import abstractmethod


class Provider(ABC):
    """Base class for providers"""

    @abstractmethod
    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict:

        raise NotImplementedError("Method needs to be implemented in subclass")

    @abstractmethod
    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str:

        raise NotImplementedError("Method needs to be implemented in subclass")

    @abstractmethod
    def get_message(self, response: dict) -> str:
        raise NotImplementedError("Method needs to be implemented in subclass")


class AsyncProvider(ABC):
    """Asynchronous base class for providers"""

    @abstractmethod
    async def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict:

        raise NotImplementedError("Method needs to be implemented in subclass")

    @abstractmethod
    async def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str:

        raise NotImplementedError("Method needs to be implemented in subclass")

    @abstractmethod
    async def get_message(self, response: dict) -> str:
        raise NotImplementedError("Method needs to be implemented in subclass")
