from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, List, Optional, Union

from fastapi import HTTPException
from openai.types.chat import ChatCompletion

from briton.async_util import map_generator, tap_generator, try_advance_generator
from briton.backend.utils import collect_text
from briton.constants import BRITON_DEFAULT_MAX_TOKENS
from briton.error_handling import grpc_error_handling
from briton.lora_cache import LoraNotFoundException
from briton.openai import create_completion, create_completion_chunks
from briton.proto import InferenceAnswerPart, InferenceRequest
from briton.schema import ModelInput


async def model_input_to_briton_request(
    request_id: int,
    model_input: ModelInput,
    input_ids: List[int],
    tokenizer_eos_token_id: Optional[int],
    tokenizer_pad_token_id: Optional[int],
    add_schema_to_cache: Callable[[Dict[str, Any]], Awaitable[str]],
    resolve_lora: Optional[Callable[[str], Optional[int]]],
    default_max_tokens: Optional[int],
    max_seq_len: int,
) -> InferenceRequest:
    """
    Convert ModelInput to Briton inference request.

    :param model_input: model input
    :return: InferRequest
    """
    request = InferenceRequest(
        request_id=request_id,
        input_ids=input_ids,
    )
    num_input_ids = len(input_ids)

    # end_id, pad_id
    end_id = model_input.end_id or tokenizer_eos_token_id
    if end_id is not None:
        request.end_id = end_id
    pad_id = model_input.pad_id or tokenizer_pad_token_id
    if pad_id is not None:
        request.pad_id = pad_id

    schema = model_input.output_json_schema
    if schema is not None:
        request.output_schema_hash = await add_schema_to_cache(schema)
        force_tools = model_input.force_tools
        if force_tools is not None:
            request.force_tools = force_tools

    if model_input.model is not None and len(model_input.model) > 0 and resolve_lora is not None:
        try:
            lora_task_id = resolve_lora(model_input.model)
        except LoraNotFoundException:
            raise HTTPException(status_code=404, detail=f"Model {model_input.model} not found.")
        if lora_task_id is not None:
            request.lora_task_id = lora_task_id

    # max tokens
    request.request_output_len = calc_request_output_len(
        model_input.max_tokens,
        num_input_ids,
        default_max_tokens,
        max_seq_len,
    )

    # beam width
    if model_input.beam_width is not None:
        request.beam_width = model_input.beam_width

    # repetition penalty
    if model_input.repetition_penalty is not None:
        request.repetition_penalty = model_input.repetition_penalty

    # presence_penalty
    if model_input.presence_penalty is not None:
        request.presence_penalty = model_input.presence_penalty

    # length penalty
    if model_input.length_penalty is not None:
        request.len_penalty = model_input.length_penalty

    # temperature
    if model_input.temperature is not None:
        request.temperature = model_input.temperature

    # length_penalty
    if model_input.length_penalty is not None:
        request.len_penalty = model_input.length_penalty

    # frequency_penalty
    if model_input.frequency_penalty is not None:
        # TODO(pankaj) Implement this in Briton
        # request.frequency_penalty = model_input.frequency_penalty
        pass

    # top_k
    if model_input.top_k is not None:
        request.runtime_top_k = model_input.top_k

    # top_p
    if model_input.top_p is not None:
        request.runtime_top_p = model_input.top_p

    # random seed
    # Note that model_input always has a seed. If seed is not supplied in input
    # then a random value is picked.
    request.random_seed = model_input.seed

    # stop words
    if model_input.stop is not None:
        request.stop_words.extend(model_input.stop)

    # bad words
    if model_input.bad_words is not None:
        request.bad_words.extend(model_input.bad_words)

    return request


def calc_request_output_len(
    model_input_max_tokens: Optional[int],
    num_input_ids: int,
    default_max_tokens: Optional[int],
    max_seq_len: int,
) -> int:
    if num_input_ids > max_seq_len:
        raise HTTPException(
            status_code=400,
            detail=f"Number of input tokens {num_input_ids} exceeds max sequence length {max_seq_len}",
        )
    model_max_allowed_tokens = max_seq_len - num_input_ids
    max_tokens = model_input_max_tokens or default_max_tokens or BRITON_DEFAULT_MAX_TOKENS
    return min(model_max_allowed_tokens, max_tokens)


async def openai_spec_response(
    resp_iters: List[AsyncGenerator[InferenceAnswerPart, None]],
    request_id: str,
    num_input_ids: int,
    streaming: bool,
    eos_token: str,
    tool_call_token: Optional[str],
    use_vllm_tool_call_id_style: Optional[bool],
    model_name: str,
    include_stream_usage: bool,
    stop_words: Optional[List[str]],
    skip_special_tokens: Optional[List[str]],
) -> Union[AsyncGenerator[str, None], ChatCompletion]:
    with grpc_error_handling():
        if streaming:
            completion_tokens = 0

            def get_completion_tokens():
                nonlocal completion_tokens
                return completion_tokens

            def set_completion_tokens(item: InferenceAnswerPart):
                nonlocal completion_tokens
                completion_tokens += len(item.output_ids)

            sequences = [
                map_generator(
                    tap_generator(try_advance_generator(resp_iter), set_completion_tokens),
                    lambda x: x.output_text,
                )
                for resp_iter in resp_iters
            ]

            return create_completion_chunks(
                req_id=request_id,
                model=model_name,
                sequences=sequences,
                eos_token=eos_token,
                tool_token=tool_call_token,
                use_vllm_tool_call_id_style=use_vllm_tool_call_id_style,
                prompt_tokens=(num_input_ids if include_stream_usage else None),
                completion_tokens_fn=(get_completion_tokens if include_stream_usage else None),
                stop_words=stop_words,
                skip_special_tokens=skip_special_tokens,
            )
        else:
            total_completion_tokens = 0
            sequences = []
            for resp_iter in resp_iters:
                generation_text, completion_tokens = await collect_text(resp_iter)
                sequences.append(generation_text)
                total_completion_tokens += completion_tokens
            return create_completion(
                req_id=request_id,
                model=model_name,
                sequences=sequences,
                eos_token=eos_token,
                tool_token=tool_call_token,
                use_vllm_tool_call_id_style=use_vllm_tool_call_id_style,
                prompt_tokens=num_input_ids,
                completion_tokens=total_completion_tokens,
                stop_words=stop_words,
                skip_special_tokens=skip_special_tokens,
            )
