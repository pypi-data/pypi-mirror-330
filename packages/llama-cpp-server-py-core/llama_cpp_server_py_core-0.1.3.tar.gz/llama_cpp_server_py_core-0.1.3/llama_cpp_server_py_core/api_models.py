from __future__ import annotations

import dataclasses
import time
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union, Type, TypeVar

T = TypeVar("T")

@dataclasses.dataclass
class BaseParameters:
    @classmethod
    def from_dict(cls: Type[T], data: dict, ignore_extra_fields: bool = True) -> T:
        """Create an instance of the dataclass from a dictionary.

        Args:
            data: A dictionary containing values for the dataclass fields.
            ignore_extra_fields: If True, any extra fields in the data dictionary that
                are not part of the dataclass will be ignored.
                If False, extra fields will raise an error. Defaults to False.
        Returns:
            An instance of the dataclass with values populated from the given
                dictionary.

        Raises:
            TypeError: If `ignore_extra_fields` is False and there are fields in the
                           dictionary that aren't present in the dataclass.
        """
        all_field_names = {f.name for f in dataclasses.fields(cls)}
        if ignore_extra_fields:
            data = {key: value for key, value in data.items() if key in all_field_names}
        else:
            extra_fields = set(data.keys()) - all_field_names
            if extra_fields:
                raise TypeError(f"Unexpected fields: {', '.join(extra_fields)}")
        return cls(**data)



@dataclasses.dataclass
class ModelCard(BaseParameters):
    id: str
    object: str = "model"
    created: int = dataclasses.field(default_factory=lambda: int(time.time()))
    owned_by: str = "llamacpp"
    meta: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class ModelList(BaseParameters):
    object: str = "list"
    data: List[ModelCard] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class CompletionRequest(BaseParameters):
    prompt: Union[str, List[Union[str, int]]] = dataclasses.field(
        metadata={
            "help": "Provide the prompt for this completion as a string or as an array of strings or numbers representing tokens."
        }
    )
    temperature: float = dataclasses.field(
        default=0.8,
        metadata={"help": "Adjust the randomness of the generated text. Default: 0.8"},
    )
    dynatemp_range: float = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Dynamic temperature range. The final temperature will be in the range of [temperature - dynatemp_range; temperature + dynatemp_range] Default: 0.0, which is disabled."
        },
    )
    dynatemp_exponent: float = dataclasses.field(
        default=1.0, metadata={"help": "Dynamic temperature exponent. Default: 1.0"}
    )
    top_k: int = dataclasses.field(
        default=40,
        metadata={
            "help": "Limit the next token selection to the K most probable tokens. Default: 40"
        },
    )
    top_p: float = dataclasses.field(
        default=0.95,
        metadata={
            "help": "Limit the next token selection to a subset of tokens with a cumulative probability above a threshold P. Default: 0.95"
        },
    )
    min_p: float = dataclasses.field(
        default=0.05,
        metadata={
            "help": "The minimum probability for a token to be considered, relative to the probability of the most likely token. Default: 0.05"
        },
    )
    n_predict: int = dataclasses.field(
        default=-1,
        metadata={
            "help": "Set the maximum number of tokens to predict when generating text. Note: May exceed the set limit slightly if the last token is a partial multibyte character. When 0, no tokens will be generated but the prompt is evaluated into the cache. Default: -1, where -1 is infinity."
        },
    )
    n_indent: int = dataclasses.field(
        default=0,
        metadata={
            "help": "Specify the minimum line indentation for the generated text in number of whitespace characters. Useful for code completion tasks. Default: 0"
        },
    )
    n_keep: int = dataclasses.field(
        default=0,
        metadata={
            "help": "Specify the number of tokens from the prompt to retain when the context size is exceeded and tokens need to be discarded. The number excludes the BOS token. By default, this value is set to 0, meaning no tokens are kept. Use -1 to retain all tokens from the prompt."
        },
    )
    stream: bool = dataclasses.field(
        default=False,
        metadata={
            "help": "Allows receiving each predicted token in real-time instead of waiting for the completion to finish (uses a different response format). To enable this, set to true"
        },
    )
    stop: List[str] = dataclasses.field(
        default_factory=list,
        metadata={
            "help": "Specify a JSON array of stopping strings. These words will not be included in the completion, so make sure to add them to the prompt for the next iteration. Default: []"
        },
    )
    typical_p: float = dataclasses.field(
        default=1.0,
        metadata={
            "help": "Enable locally typical sampling with parameter p. Default: 1.0, which is disabled."
        },
    )
    repeat_penalty: float = dataclasses.field(
        default=1.1,
        metadata={
            "help": "Control the repetition of token sequences in the generated text. Default: 1.1"
        },
    )
    repeat_last_n: int = dataclasses.field(
        default=64,
        metadata={
            "help": "Last n tokens to consider for penalizing repetition. Default: 64, where 0 is disabled and -1 is ctx-size."
        },
    )
    penalize_nl: bool = dataclasses.field(
        default=True,
        metadata={
            "help": "Penalize newline tokens when applying the repeat penalty. Default: true"
        },
    )
    presence_penalty: float = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Repeat alpha presence penalty. Default: 0.0, which is disabled."
        },
    )
    frequency_penalty: float = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Repeat alpha frequency penalty. Default: 0.0, which is disabled."
        },
    )
    dry_multiplier: float = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Set the DRY (Don't Repeat Yourself) repetition penalty multiplier. Default: 0.0, which is disabled."
        },
    )
    dry_base: float = dataclasses.field(
        default=1.75,
        metadata={"help": "Set the DRY repetition penalty base value. Default: 1.75"},
    )
    dry_allowed_length: int = dataclasses.field(
        default=2,
        metadata={
            "help": "Tokens that extend repetition beyond this receive exponentially increasing penalty. Default: 2"
        },
    )
    dry_penalty_last_n: int = dataclasses.field(
        default=-1,
        metadata={
            "help": "How many tokens to scan for repetitions. Default: -1, where 0 is disabled and -1 is context size."
        },
    )
    dry_sequence_breakers: List[str] = dataclasses.field(
        default_factory=lambda: ["\n", ":", '"', "*"],
        metadata={
            "help": "Specify an array of sequence breakers for DRY sampling. Default: ['\n', ':', '\"', '*']"
        },
    )
    xtc_probability: float = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Set the chance for token removal via XTC sampler. Default: 0.0, which is disabled."
        },
    )
    xtc_threshold: float = dataclasses.field(
        default=0.1,
        metadata={
            "help": "Set a minimum probability threshold for tokens to be removed via XTC sampler. Default: 0.1 (> 0.5 disables XTC)"
        },
    )
    mirostat: int = dataclasses.field(
        default=0,
        metadata={
            "help": "Enable Mirostat sampling, controlling perplexity during text generation. Default: 0, where 0 is disabled, 1 is Mirostat, and 2 is Mirostat 2.0."
        },
    )
    mirostat_tau: float = dataclasses.field(
        default=5.0,
        metadata={
            "help": "Set the Mirostat target entropy, parameter tau. Default: 5.0"
        },
    )
    mirostat_eta: float = dataclasses.field(
        default=0.1,
        metadata={
            "help": "Set the Mirostat learning rate, parameter eta. Default: 0.1"
        },
    )
    grammar: Optional[str] = dataclasses.field(
        default=None,
        metadata={
            "help": "Set grammar for grammar-based sampling. Default: no grammar"
        },
    )
    json_schema: Optional[Dict[str, Any]] = dataclasses.field(
        default=None,
        metadata={
            "help": "Set a JSON schema for grammar-based sampling. Default: no JSON schema."
        },
    )
    seed: int = dataclasses.field(
        default=-1,
        metadata={
            "help": "Set the random number generator (RNG) seed. Default: -1, which is a random seed."
        },
    )
    ignore_eos: bool = dataclasses.field(
        default=False,
        metadata={
            "help": "Ignore end of stream token and continue generating. Default: false"
        },
    )
    logit_bias: List[
        Union[List[Union[int, str, float, bool]], List[Union[str, float]]]
    ] = dataclasses.field(
        default_factory=list,
        metadata={
            "help": "Modify the likelihood of tokens appearing in the completion. Default: []"
        },
    )
    n_probs: int = dataclasses.field(
        default=0,
        metadata={
            "help": "Return probabilities of top N tokens for each generated token. Default: 0"
        },
    )
    min_keep: int = dataclasses.field(
        default=0,
        metadata={
            "help": "Force samplers to return N possible tokens at minimum. Default: 0"
        },
    )
    t_max_predict_ms: int = dataclasses.field(
        default=0,
        metadata={
            "help": "Time limit in milliseconds for prediction phase. Default: 0, which is disabled."
        },
    )
    image_data: Optional[List[Dict[str, Union[str, int]]]] = dataclasses.field(
        default=None,
        metadata={
            "help": "Array of objects with base64-encoded image data and IDs for multimodal models."
        },
    )
    id_slot: int = dataclasses.field(
        default=-1,
        metadata={
            "help": "Assign completion task to specific slot. -1 for auto-assignment. Default: -1"
        },
    )
    cache_prompt: bool = dataclasses.field(
        default=True,
        metadata={
            "help": "Re-use KV cache from previous request if possible. Default: true"
        },
    )
    samplers: List[str] = dataclasses.field(
        default_factory=lambda: [
            "dry",
            "top_k",
            "typ_p",
            "top_p",
            "min_p",
            "xtc",
            "temperature",
        ],
        metadata={
            "help": 'Order of sampler application. Default: ["dry", "top_k", "typ_p", "top_p", "min_p", "xtc", "temperature"]'
        },
    )
    timings_per_token: bool = dataclasses.field(
        default=False,
        metadata={
            "help": "Include prompt processing and generation speed info in response. Default: false"
        },
    )


@dataclasses.dataclass
class GenerationSettings(BaseParameters):
    """Settings used for text generation"""

    n_predict: int = dataclasses.field(
        metadata={"help": "Maximum number of tokens to predict"}
    )

    seed: int = dataclasses.field(metadata={"help": "Random number generator seed"})

    temperature: float = dataclasses.field(
        metadata={"help": "Randomness of the generated text"}
    )

    dynatemp_range: float = dataclasses.field(
        metadata={"help": "Dynamic temperature range"}
    )

    dynatemp_exponent: float = dataclasses.field(
        metadata={"help": "Dynamic temperature exponent"}
    )

    top_k: int = dataclasses.field(
        metadata={"help": "Limit the next token selection to K most probable tokens"}
    )

    top_p: float = dataclasses.field(
        metadata={"help": "Cumulative probability threshold for token selection"}
    )

    min_p: float = dataclasses.field(
        metadata={"help": "Minimum probability relative to most likely token"}
    )

    xtc_probability: float = dataclasses.field(
        metadata={"help": "Probability for token removal via XTC sampler"}
    )

    xtc_threshold: float = dataclasses.field(
        metadata={"help": "Minimum probability threshold for XTC sampler"}
    )

    typical_p: float = dataclasses.field(
        metadata={"help": "Parameter for locally typical sampling"}
    )

    repeat_last_n: int = dataclasses.field(
        metadata={"help": "Number of tokens to consider for repetition penalty"}
    )

    repeat_penalty: float = dataclasses.field(
        metadata={"help": "Penalty for token repetition"}
    )

    presence_penalty: float = dataclasses.field(
        metadata={"help": "Repeat alpha presence penalty"}
    )

    frequency_penalty: float = dataclasses.field(
        metadata={"help": "Repeat alpha frequency penalty"}
    )

    dry_multiplier: float = dataclasses.field(
        metadata={"help": "DRY repetition penalty multiplier"}
    )

    dry_base: float = dataclasses.field(
        metadata={"help": "DRY repetition penalty base value"}
    )

    dry_allowed_length: int = dataclasses.field(
        metadata={"help": "Length threshold for DRY penalty application"}
    )

    dry_penalty_last_n: int = dataclasses.field(
        metadata={"help": "Number of tokens to scan for DRY repetitions"}
    )

    dry_sequence_breakers: List[str] = dataclasses.field(
        metadata={"help": "Sequence breakers for DRY sampling"}
    )

    mirostat: int = dataclasses.field(
        metadata={"help": "Mirostat sampling mode (0=disabled, 1=v1, 2=v2)"}
    )

    mirostat_tau: float = dataclasses.field(
        metadata={"help": "Mirostat target entropy parameter tau"}
    )

    mirostat_eta: float = dataclasses.field(
        metadata={"help": "Mirostat learning rate parameter eta"}
    )

    stop: List[str] = dataclasses.field(metadata={"help": "List of stopping strings"})

    max_tokens: int = dataclasses.field(
        metadata={"help": "Maximum number of tokens to generate"}
    )

    n_keep: int = dataclasses.field(
        metadata={"help": "Number of tokens to keep from prompt"}
    )

    n_discard: int = dataclasses.field(
        metadata={"help": "Number of tokens to discard from prompt"}
    )

    ignore_eos: bool = dataclasses.field(
        metadata={"help": "Whether to ignore end of stream token"}
    )

    stream: bool = dataclasses.field(
        metadata={"help": "Whether to stream the response"}
    )

    logit_bias: List[Any] = dataclasses.field(
        metadata={"help": "Token biases for logit modification"}
    )

    n_probs: int = dataclasses.field(
        metadata={"help": "Number of probability values to return per token"}
    )

    min_keep: int = dataclasses.field(
        metadata={"help": "Minimum number of tokens to keep in sampling"}
    )

    grammar: str = dataclasses.field(
        metadata={"help": "Grammar for grammar-based sampling"}
    )

    samplers: List[str] = dataclasses.field(
        metadata={"help": "List of samplers to apply in order"}
    )

    speculative_n_max: int = dataclasses.field(
        metadata={"help": "Maximum number of tokens for speculative sampling"}
    )

    speculative_n_min: int = dataclasses.field(
        metadata={"help": "Minimum number of tokens for speculative sampling"}
    )

    speculative_p_min: float = dataclasses.field(
        metadata={"help": "Minimum probability for speculative sampling"}
    )

    timings_per_token: bool = dataclasses.field(
        metadata={"help": "Whether to include per-token timing information"}
    )

    post_sampling_probs: bool = dataclasses.field(
        metadata={"help": "Whether to calculate post-sampling probabilities"}
    )
    lora: List[str] = dataclasses.field(
        default_factory=list, metadata={"help": "List of LoRA samplers to apply in order"}
    )
    grammar_trigger_words: List[str] = dataclasses.field(
        default_factory=list, metadata={"help": "List of trigger words for grammar-based sampling"}
    ) 
    

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> GenerationSettings:
        """Create a GenerationSettings instance from a dictionary

        Args:
            data: Dictionary containing generation settings

        Returns:
            GenerationSettings: An instance of GenerationSettings
        """
        # Handle speculative parameters
        if "speculative.n_max" in data:
            data["speculative_n_max"] = data.pop("speculative.n_max")
        if "speculative.n_min" in data:
            data["speculative_n_min"] = data.pop("speculative.n_min")
        if "speculative.p_min" in data:
            data["speculative_p_min"] = data.pop("speculative.p_min")
        return super().from_dict(data, ignore_extra_fields=True)
        

@dataclasses.dataclass
class CompletionResponse(BaseParameters):
    """Represents a single message in the completion stream response"""

    index: int = dataclasses.field(metadata={"help": "Index"})

    content: str = dataclasses.field(
        metadata={"help": "The generated text content for this message"}
    )

    tokens: List[int] = dataclasses.field(
        metadata={"help": "List of token IDs corresponding to the generated content"}
    )

    stop: bool = dataclasses.field(
        metadata={"help": "Indicates whether this is the last message in the stream"}
    )

    id_slot: int = dataclasses.field(
        metadata={
            "help": "Slot ID assigned for this completion task. -1 means auto-assigned"
        }
    )

    tokens_predicted: int = dataclasses.field(
        metadata={"help": "Number of tokens that have been predicted so far"}
    )

    tokens_evaluated: int = dataclasses.field(
        metadata={"help": "Number of tokens that have been evaluated from the prompt"}
    )

    # Fields that only appear in the final message
    model: Optional[str] = dataclasses.field(
        default=None, metadata={"help": "Name or path of the model used for generation"}
    )

    generation_settings: Optional[GenerationSettings] = dataclasses.field(
        default=None, metadata={"help": "Settings used for this completion generation"}
    )

    prompt: Optional[str] = dataclasses.field(
        default=None,
        metadata={
            "help": "The original input prompt that was used for this completion"
        },
    )

    has_new_line: Optional[bool] = dataclasses.field(
        default=None,
        metadata={
            "help": "Indicates whether the generated content contains a newline character"
        },
    )

    truncated: Optional[bool] = dataclasses.field(
        default=None,
        metadata={
            "help": "Indicates whether the context was truncated during generation"
        },
    )

    stop_type: Optional[str] = dataclasses.field(
        default=None,
        metadata={
            "help": "Type of stop condition that ended the generation. Can be 'none', 'eos', 'limit', or 'word'"
        },
    )

    stopping_word: Optional[str] = dataclasses.field(
        default=None,
        metadata={"help": "The stopping word that caused generation to stop, if any"},
    )

    tokens_cached: Optional[int] = dataclasses.field(
        default=None,
        metadata={
            "help": "Number of tokens that were cached from previous completions"
        },
    )

    timings: Optional[Dict[str, float]] = dataclasses.field(
        default=None,
        metadata={
            "help": "Dictionary containing timing information about prompt processing and token generation"
        },
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CompletionResponse:
        """Create a CompletionResponse instance from a dictionary

        Args:
            data: Dictionary containing response data from the API

        Returns:
            CompletionResponse: An instance of CompletionResponse
        """
        if "generation_settings" in data:
            data["generation_settings"] = GenerationSettings.from_dict(
                data["generation_settings"]
            )
        return super().from_dict(data, ignore_extra_fields=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary

        Returns:
            Dict[str, Any]: Dictionary representation of the response
        """
        return dataclasses.asdict(self)

    @property
    def is_final(self) -> bool:
        """Check if this is the final message in the stream

        Returns:
            bool: True if this is the final message, False otherwise
        """
        return self.model is not None and self.generation_settings is not None


@dataclasses.dataclass
class ChatCompletionRequest(BaseParameters):
    messages: Union[
        str,
        List[Dict[str, str]],
        List[Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, str]]]]]]],
    ]
    model: Optional[str] = dataclasses.field(
        default=None,
        metadata={"help": "Name of the model to use for completion. Default: None"},
    )
    temperature: Optional[float] = dataclasses.field(
        default=0.8,
        metadata={"help": "Adjust the randomness of the generated text. Default: 0.8"},
    )
    top_p: Optional[float] = dataclasses.field(
        default=0.95,
        metadata={
            "help": "Limit the next token selection to a subset of tokens with a cumulative probability above a threshold P. Default: 0.95"
        },
    )
    top_k: Optional[int] = dataclasses.field(
        default=40,
        metadata={
            "help": "Limit the next token selection to the K most probable tokens. Default: 40"
        },
    )
    n: Optional[int] = dataclasses.field(
        default=1, metadata={"help": "Number of completions to generate. Default: 1"}
    )
    max_tokens: Optional[int] = dataclasses.field(
        default=None,
        metadata={"help": "Maximum number of tokens to generate. Default: None"},
    )
    stop: Optional[Union[str, List[str]]] = dataclasses.field(
        default=None,
        metadata={
            "help": "Specify a JSON array of stopping strings. These words will not be included in the completion, so make sure to add them to the prompt for the next iteration. Default: []"
        },
    )
    stream: Optional[bool] = dataclasses.field(
        default=False,
        metadata={
            "help": "Allows receiving each predicted token in real-time instead of waiting for the completion to finish (uses a different response format). To enable this, set to true"
        },
    )
    presence_penalty: Optional[float] = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Repeat alpha presence penalty. Default: 0.0, which is disabled."
        },
    )
    frequency_penalty: Optional[float] = dataclasses.field(
        default=0.0,
        metadata={
            "help": "Repeat alpha frequency penalty. Default: 0.0, which is disabled."
        },
    )
    user: Optional[str] = dataclasses.field(
        default=None, metadata={"help": "User ID for the chat session."}
    )


@dataclasses.dataclass
class ChatMessage(BaseParameters):
    role: str = dataclasses.field(metadata={"help": "Role of the message."})
    content: str = dataclasses.field(metadata={"help": "Content of the message."})
    reasoning_content: Optional[str] = dataclasses.field(
        default=None, metadata={"help": "Reasoning content of reasoning model."}
    )


@dataclasses.dataclass
class ChatCompletionResponseChoice(BaseParameters):
    index: int = dataclasses.field(metadata={"help": "Index of the choice."})
    message: ChatMessage = dataclasses.field(
        metadata={"help": "The generated message."}
    )
    finish_reason: Optional[Literal["stop", "length"]] = dataclasses.field(
        default=None, metadata={"help": "Reason for finishing the completion."}
    )

@dataclasses.dataclass
class DeltaMessage(BaseParameters):
    role: Optional[str] = dataclasses.field(
        default=None, metadata={"help": "Role of the message."}
    )
    content: Optional[str] = dataclasses.field(
        default=None, metadata={"help": "Content of the message."}
    )
    reasoning_content: Optional[str] = dataclasses.field(
        default=None, metadata={"help": "Reasoning content of reasoning model."}
    )


@dataclasses.dataclass
class ChatCompletionResponseStreamChoice:
    index: int = dataclasses.field(metadata={"help": "Index of the choice."})
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]] = None


@dataclasses.dataclass
class ChatCompletionStreamResponse:
    id: str = dataclasses.field(metadata={"help": "ID of the response."})
    object: str = dataclasses.field(metadata={"help": "Type of the response."})
    created: int = dataclasses.field(
        metadata={"help": "Creation timestamp of the response."}
    )
    model: str = dataclasses.field(metadata={"help": "Model used for completion."})
    choices: List[ChatCompletionResponseStreamChoice] = dataclasses.field(
        metadata={"help": "List of completion choices."}
    )
    usage: Optional[Dict[str, Any]] = dataclasses.field(
        default=None, metadata={"help": "Usage information."}
    )
    timings: Optional[Dict[str, float]] = dataclasses.field(
        default=None,
        metadata={
            "help": "Dictionary containing timing information about prompt processing and token generation."
        },
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ChatCompletionStreamResponse:
        """Create a ChatCompletionStreamResponse instance from a dictionary

        Args:
            data: Dictionary containing response data from the API

        Returns:
            ChatCompletionStreamResponse: An instance of ChatCompletionStreamResponse
        """
        choices = [
            ChatCompletionResponseStreamChoice(
                index=choice["index"],
                delta=DeltaMessage(**choice["delta"]),
                finish_reason=choice.get("finish_reason"),
            )
            for choice in data["choices"]
        ]
        return cls(
            id=data["id"],
            object=data.get("object", "chat.completion"),
            created=data["created"],
            model=data["model"],
            choices=choices,
            usage=data.get("usage"),
            timings=data.get("timings"),
        )


@dataclasses.dataclass
class ChatCompletionResponse:
    id: str = dataclasses.field(metadata={"help": "ID of the response."})
    object: str = dataclasses.field(metadata={"help": "Type of the response."})
    created: int = dataclasses.field(
        metadata={"help": "Creation timestamp of the response."}
    )
    model: str = dataclasses.field(metadata={"help": "Model used for completion."})
    choices: List[ChatCompletionResponseChoice] = dataclasses.field(
        metadata={"help": "List of completion choices."}
    )
    usage: Optional[Dict[str, Any]] = dataclasses.field(
        default=None, metadata={"help": "Usage information."}
    )
    timings: Optional[Dict[str, float]] = dataclasses.field(
        default=None,
        metadata={
            "help": "Dictionary containing timing information about prompt processing and token generation."
        },
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ChatCompletionResponse:
        """Create a ChatCompletionResponse instance from a dictionary

        Args:
            data: Dictionary containing response data from the API

        Returns:
            ChatCompletionResponse: An instance of ChatCompletionResponse
        """
        choices = [
            ChatCompletionResponseChoice(
                index=choice["index"],
                message=ChatMessage.from_dict(choice["message"]),
                finish_reason=choice.get("finish_reason"),
            )
            for choice in data["choices"]
        ]
        return cls(
            id=data["id"],
            object=data.get("object", "chat.completion"),
            created=data["created"],
            model=data["model"],
            choices=choices,
            usage=data.get("usage"),
            timings=data.get("timings"),
        )
