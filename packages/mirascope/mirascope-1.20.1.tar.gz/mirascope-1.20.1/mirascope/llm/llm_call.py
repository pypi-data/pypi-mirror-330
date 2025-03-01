"""This module contains the `call` decorator for making provider-agnostic LLM API calls with a typed function."""

from __future__ import annotations

from collections.abc import AsyncIterable, Awaitable, Callable, Iterable
from enum import Enum
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast, get_args

from pydantic import BaseModel

from ..core import BaseTool
from ..core.base import (
    BaseCallResponse,
    BaseCallResponseChunk,
    BaseStream,
    BaseType,
    CommonCallParams,
)
from ..core.base._utils import fn_is_async
from ..core.base.stream_config import StreamConfig
from ..core.base.types import LocalProvider, Provider
from ._protocols import (
    AsyncLLMFunctionDecorator,
    CallDecorator,
    LLMFunctionDecorator,
    SyncLLMFunctionDecorator,
)
from .call_response import CallResponse
from .stream import Stream

_P = ParamSpec("_P")
_R = TypeVar("_R")
_ParsedOutputT = TypeVar("_ParsedOutputT")
_ResponseModelT = TypeVar("_ResponseModelT", bound=BaseModel | BaseType | Enum)
_AsyncBaseDynamicConfigT = TypeVar("_AsyncBaseDynamicConfigT", contravariant=True)
_BaseDynamicConfigT = TypeVar("_BaseDynamicConfigT", contravariant=True)

_BaseCallResponseT = TypeVar(
    "_BaseCallResponseT", covariant=True, bound=BaseCallResponse
)
_BaseCallResponseChunkT = TypeVar(
    "_BaseCallResponseChunkT", covariant=True, bound=BaseCallResponseChunk
)
_BaseStreamT = TypeVar("_BaseStreamT", covariant=True)
_ResultT = TypeVar("_ResultT")


def _get_local_provider_call(
    provider: LocalProvider,
    client: Any | None,  # noqa: ANN401
) -> tuple[Callable, Any | None]:
    if provider == "ollama":
        from ..core.openai import openai_call

        if client:
            return openai_call, client
        from openai import OpenAI

        client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
        return openai_call, client
    else:  # provider == "vllm"
        from ..core.openai import openai_call

        if client:
            return openai_call, client
        from openai import OpenAI

        client = OpenAI(api_key="ollama", base_url="http://localhost:8000/v1")
        return openai_call, client


def _get_provider_call(provider: Provider) -> Callable:
    """Returns the provider-specific call decorator based on the provider name."""
    if provider == "anthropic":
        from ..core.anthropic import anthropic_call

        return anthropic_call
    elif provider == "azure":
        from ..core.azure import azure_call

        return azure_call
    elif provider == "bedrock":
        from ..core.bedrock import bedrock_call

        return bedrock_call
    elif provider == "cohere":
        from ..core.cohere import cohere_call

        return cohere_call
    elif provider == "gemini":
        from ..core.gemini import gemini_call

        return gemini_call
    elif provider == "google":
        from ..core.google import google_call

        return google_call
    elif provider == "groq":
        from ..core.groq import groq_call

        return groq_call
    elif provider == "litellm":
        from ..core.litellm import litellm_call

        return litellm_call
    elif provider == "mistral":
        from ..core.mistral import mistral_call

        return mistral_call
    elif provider == "openai":
        from ..core.openai import openai_call

        return openai_call
    elif provider == "vertex":
        from ..core.vertex import vertex_call

        return vertex_call
    elif provider == "xai":
        from ..core.xai import xai_call

        return xai_call
    raise ValueError(f"Unsupported provider: {provider}")


def _wrap_result(
    result: BaseCallResponse | BaseStream | _ResultT,
) -> CallResponse | Stream | _ResultT:
    """Wraps the result into a CallResponse or Stream instance.

    Args:
        result: The result returned by the provider-specific decorator.

    Returns:
        A `CallResponse` instance if `result` is a `BaseCallResponse`.
        A `Stream` instance if `result` is a `BaseStream`.

    Raises:
        ValueError: If the result type is not supported.
    """
    if isinstance(result, BaseCallResponse):
        return CallResponse(response=result)  # type: ignore
    elif isinstance(result, BaseStream):
        return Stream(stream=result)  # type: ignore
    else:
        return result


def _call(
    provider: Provider | LocalProvider,
    model: str,
    *,
    stream: bool | StreamConfig = False,
    tools: list[type[BaseTool] | Callable] | None = None,
    response_model: type[_ResponseModelT] | None = None,
    output_parser: Callable[[_BaseCallResponseT], _ParsedOutputT]
    | Callable[[_BaseCallResponseChunkT], _ParsedOutputT]
    | Callable[[_ResponseModelT], _ParsedOutputT]
    | None = None,
    json_mode: bool = False,
    client: Any = None,  # noqa: ANN401
    call_params: CommonCallParams | Any = None,  # noqa: ANN401
) -> (
    AsyncLLMFunctionDecorator[
        _AsyncBaseDynamicConfigT,
        _BaseCallResponseT
        | _ParsedOutputT
        | _BaseStreamT
        | _ResponseModelT
        | AsyncIterable[_ResponseModelT],
    ]
    | SyncLLMFunctionDecorator[
        _BaseDynamicConfigT,
        _BaseCallResponseT
        | _ParsedOutputT
        | _BaseStreamT
        | _ResponseModelT
        | Iterable[_ResponseModelT],
    ]
    | LLMFunctionDecorator[
        _BaseDynamicConfigT,
        _AsyncBaseDynamicConfigT,
        _BaseCallResponseT
        | _ParsedOutputT
        | _BaseStreamT
        | _ResponseModelT
        | Iterable[_ResponseModelT],
        _BaseCallResponseT
        | _ParsedOutputT
        | _BaseStreamT
        | _ResponseModelT
        | AsyncIterable[_ResponseModelT],
    ]
):
    """Decorator for defining a function that calls a language model."""
    if provider in get_args(LocalProvider):
        provider_call, client = _get_local_provider_call(
            cast(LocalProvider, provider), client
        )
    else:
        provider_call = _get_provider_call(cast(Provider, provider))
    _original_args = {
        "model": model,
        "stream": stream,
        "tools": tools,
        "response_model": response_model,
        "output_parser": output_parser,
        "json_mode": json_mode,
        "client": client,
        "call_params": call_params,
    }

    def wrapper(
        fn: Callable[_P, _R | Awaitable[_R]],
    ) -> Callable[
        _P,
        CallResponse | Stream | Awaitable[CallResponse | Stream],
    ]:
        decorated = provider_call(**_original_args)(fn)

        if fn_is_async(decorated):

            @wraps(decorated)
            async def inner_async(
                *args: _P.args, **kwargs: _P.kwargs
            ) -> CallResponse | Stream:
                result = await decorated(*args, **kwargs)
                return _wrap_result(result)

            inner_async._original_args = _original_args  # pyright: ignore [reportAttributeAccessIssue]
            inner_async._original_provider_call = provider_call  # pyright: ignore [reportAttributeAccessIssue]
            inner_async._original_fn = fn  # pyright: ignore [reportAttributeAccessIssue]
            inner_async._original_provider = provider  # pyright: ignore [reportAttributeAccessIssue]

            return inner_async
        else:

            @wraps(decorated)
            def inner(*args: _P.args, **kwargs: _P.kwargs) -> CallResponse | Stream:
                result = decorated(*args, **kwargs)
                return _wrap_result(result)

            inner._original_args = _original_args  # pyright: ignore [reportAttributeAccessIssue]
            inner._original_provider_call = provider_call  # pyright: ignore [reportAttributeAccessIssue]
            inner._original_fn = fn  # pyright: ignore [reportAttributeAccessIssue]
            inner._original_provider = provider  # pyright: ignore [reportAttributeAccessIssue]
            return inner

    return wrapper  # pyright: ignore [reportReturnType]


call = cast(CallDecorator, _call)
"""A decorator for making provider-agnostic LLM API calls with a typed function.

usage docs: learn/calls.md

This decorator enables writing provider-agnostic code by wrapping a typed function 
that can call any supported LLM provider's API. It parses the prompt template of 
the wrapped function as messages and templates the input arguments into each message's 
template.

Example:

```python
from ..llm import call


@call(provider="openai", model="gpt-4o-mini")
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book"


response = recommend_book("fantasy")
print(response.content)
```

Args:
    provider (Provider | LocalProvider): The LLM provider to use
        (e.g., "openai", "anthropic").
    model (str): The model to use for the specified provider (e.g., "gpt-4o-mini").
    stream (bool): Whether to stream the response from the API call.  
    tools (list[BaseTool | Callable]): The tools available for the LLM to use.
    response_model (BaseModel | BaseType): The response model into which the response
        should be structured.
    output_parser (Callable[[CallResponse | ResponseModelT], Any]): A function for
        parsing the call response whose value will be returned in place of the
        original call response.
    json_mode (bool): Whether to use JSON Mode.
    client (object): An optional custom client to use in place of the default client.
    call_params (CommonCallParams): Provider-specific parameters to use in the API call.

Returns:
    decorator (Callable): A decorator that transforms a typed function into a
        provider-agnostic LLM API call that returns standardized response types
        regardless of the underlying provider used.
"""
