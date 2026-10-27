import httpx

from src.ai.base import (
    AIProvider,
    AIProviderAuthenticationError,
    AIProviderError,
    AIProviderRequestError,
    AIProviderUnavailableError,
)
from src.ai.models import AIMessage


class OpenAICompatibleProvider(AIProvider):
    """
    Provider adapter for APIs exposing an OpenAI-compatible
    /chat/completions endpoint.

    This supports OpenAI-compatible services such as OpenRouter
    without coupling QuantMind's core architecture to one vendor.
    """

    name = "openai_compatible"

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 60.0,
    ) -> None:
        if not api_key:
            raise ValueError("AI API key is required")
        if not model:
            raise ValueError("AI model is required")

        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, *, system_prompt: str, user_prompt: str) -> AIMessage:
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": 0.1,
            "response_format": {
                "type": "json_object",
            },
        }

        try:
            response = httpx.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=httpx.Timeout(self.timeout, connect=10.0),
            )
        except httpx.TimeoutException as exc:
            raise AIProviderUnavailableError("AI provider request timed out") from exc
        except httpx.HTTPError as exc:
            raise AIProviderUnavailableError(
                f"AI provider network request failed: {type(exc).__name__}"
            ) from exc

        if response.status_code in (401, 403):
            raise AIProviderAuthenticationError(
                f"AI provider authentication/permission failure "
                f"(HTTP {response.status_code})"
            )

        if response.status_code == 429 or response.status_code >= 500:
            raise AIProviderUnavailableError(
                f"AI provider temporarily unavailable (HTTP {response.status_code})"
            )

        if response.status_code >= 400:
            raise AIProviderRequestError(
                f"AI provider rejected the request (HTTP {response.status_code})"
            )

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise AIProviderError("AI provider returned an invalid response") from exc

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and item.get("text"):
                    parts.append(str(item["text"]))
            content = "\n".join(parts)

        if not isinstance(content, str) or not content.strip():
            raise AIProviderError("AI provider returned empty content")

        return AIMessage(
            content=content.strip(),
            model=self.model,
            provider=self.name,
        )
