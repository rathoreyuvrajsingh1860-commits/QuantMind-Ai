from abc import ABC, abstractmethod

from src.ai.models import AIMessage


class AIProvider(ABC):
    """Provider-neutral interface for QuantMind AI models."""

    name: str

    @abstractmethod
    def generate(self, *, system_prompt: str, user_prompt: str) -> AIMessage:
        """Generate a response from the configured AI provider."""
        raise NotImplementedError


class AIProviderError(RuntimeError):
    """Raised when an AI provider cannot complete a request."""
