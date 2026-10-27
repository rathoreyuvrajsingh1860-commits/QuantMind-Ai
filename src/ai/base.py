from abc import ABC, abstractmethod

from src.ai.models import AIMessage


class AIProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, *, system_prompt: str, user_prompt: str) -> AIMessage:
        raise NotImplementedError


class AIProviderError(RuntimeError):
    """Base error raised by an AI provider."""

    def __init__(self, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.retryable = retryable


class AIProviderAuthenticationError(AIProviderError):
    """Authentication or permission failure; do not retry with another model."""


class AIProviderRequestError(AIProviderError):
    """Invalid request or unsupported request configuration."""


class AIProviderUnavailableError(AIProviderError):
    """Temporary network, rate-limit, or upstream server failure."""

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=True)
