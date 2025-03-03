from typing import Any, Protocol, TypedDict

from openai.types.chat.chat_completion import ChatCompletion


class LegoLLMRouter(Protocol):
    """Protocol for LLM routers available in Lego."""

    def __call__(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,  # type: ignore[misc]
    ) -> Any:
        """Make a ChatCompletion request."""


class _Delta(TypedDict, total=False):
    content: str
    role: str


class _Choice(TypedDict, total=False):
    delta: _Delta
    index: int
    finish_reason: str | None


class StreamChunk(TypedDict, total=False):
    """The protocol for a stream chunk from OpenAI's ChatCompletion."""

    choices: list[_Choice]
