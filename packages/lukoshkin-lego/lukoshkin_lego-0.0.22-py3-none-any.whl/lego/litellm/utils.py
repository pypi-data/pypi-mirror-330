import asyncio

from litellm import Router

from lego.litellm.settings import (
    CustomLLMChatSettings,
    LiteLLMProxyModel,
    LiteLLMSettings,
)
from lego.settings import AmazonAccess


def build_bedrock_model(
    model: str,
    model_alias: str = "default",
    model_settings: dict[str, str | int | float] | None = None,
    proxy_settings: dict[str, str | int] | None = None,
) -> LiteLLMProxyModel:
    """Build a snapshot of a Bedrock model."""
    return LiteLLMProxyModel(
        provider=AmazonAccess(),
        model_settings=CustomLLMChatSettings(
            model=model, **(model_settings or {})
        ),
        proxy_settings=LiteLLMSettings(
            model_alias=model_alias, **(proxy_settings or {})
        ),
    )


class LiteLLMRouter(Router):
    """
    A compatibility wrapper around the `Router` class.

    FIXME: I need to come up with something better than this.
    I mean, it's OK for sync tasks, but when switching to async,
    I'll need to restructure it a bit.
    """

    def __init__(
        self,
        models: list[LiteLLMProxyModel],
        default_model_choice: str = "default",
        **kwargs,
    ):
        super().__init__(
            model_list=[model.serialize() for model in models],
            **kwargs,
        )
        self.default_model_choice = default_model_choice

    async def __call__(self, messages: list[dict[str, str]], **kwargs):
        model = kwargs.pop("model", None) or self.default_model_choice
        return await self.acompletion(model=model, messages=messages, **kwargs)

    def sync_call(self, messages: list[dict[str, str]], **kwargs):
        model = kwargs.pop("model", None) or self.default_model_choice
        return self.completion(model=model, messages=messages, **kwargs)


def build_litellm_router(
    models: list[LiteLLMProxyModel],
    default_model_choice: str = "default",
    **kwargs,
) -> Router:
    """Build a Bedrock model from a Pydantic model."""
    return LiteLLMRouter(
        models=models,
        default_model_choice=default_model_choice,
        **kwargs,
    )


if __name__ == "__main__":
    router = build_litellm_router(
        [
            build_bedrock_model(
                "anthropic.claude-3-haiku-20240307-v1:0",
                model_settings={"temperature": 0.2},
                proxy_settings={"num_retries": 2},
            )
        ],
        num_retries=1,
        set_verbose=True,
        debug_level="DEBUG",
    )
    messages = [{"role": "user", "content": "Hello, world!"}]

    async def test_call():
        print(await router(messages=messages, temperature=0))

    asyncio.run(test_call())
