from typing import Dict, List, Optional, Union, Literal
from typing_extensions import TypedDict, NotRequired  # Required by pydantic under Python < 3.12


class RedisConfigDict(TypedDict):
    """TypedDict representing the RedisConfig structure."""

    host: str
    port: int
    db: int


class DiskCacheConfigDict(TypedDict):
    """TypedDict representing the DiskCacheConfig structure."""

    cache_dir: str


class RateLimitConfigDict(TypedDict):
    """TypedDict representing the RateLimitConfig structure."""

    enabled: bool
    backend: Literal["memory", "redis", "diskcache"]
    redis: Optional[RedisConfigDict]
    diskcache: Optional[DiskCacheConfigDict]
    default_rpm: int
    default_tpm: int


class ServerDict(TypedDict):
    """TypedDict representing the Server structure."""

    host: str
    port: int
    url: Optional[str]


class EndpointOptionDict(TypedDict):
    """TypedDict representing the model endpoint option structure."""

    endpoint_id: str
    model_id: str
    rpm: NotRequired[int]
    tpm: NotRequired[int]
    concurrent_requests: NotRequired[int]


class ModelConfigDict(TypedDict):
    """TypedDict representing the model configuration structure."""

    id: str
    endpoints: List[Union[str, EndpointOptionDict]]
    function_call_available: bool
    response_format_available: bool
    native_multimodal: bool
    context_length: int
    max_output_tokens: Optional[int]


class BackendSettingsDict(TypedDict):
    """TypedDict representing the BackendSettings structure."""

    models: Dict[str, ModelConfigDict]


class EndpointSettingDict(TypedDict):
    """TypedDict representing the EndpointSetting structure."""

    id: str
    api_base: Optional[str]
    api_key: str
    region: Optional[str]
    api_schema_type: Optional[str]
    credentials: Optional[dict]
    is_azure: Optional[bool]
    is_vertex: Optional[bool]
    is_bedrock: Optional[bool]
    rpm: Optional[int]
    tpm: Optional[int]
    concurrent_requests: Optional[int]
    proxy: Optional[str]


class SettingsDict(TypedDict):
    """TypedDict representing the expected structure of the settings dictionary."""

    endpoints: List[EndpointSettingDict]
    token_server: Optional[ServerDict]
    rate_limit: Optional[RateLimitConfigDict]
    # 各模型后端配置
    anthropic: BackendSettingsDict
    deepseek: BackendSettingsDict
    gemini: BackendSettingsDict
    groq: BackendSettingsDict
    local: BackendSettingsDict
    minimax: BackendSettingsDict
    mistral: BackendSettingsDict
    moonshot: BackendSettingsDict
    openai: BackendSettingsDict
    qwen: BackendSettingsDict
    yi: BackendSettingsDict
    zhipuai: BackendSettingsDict
    baichuan: BackendSettingsDict
    stepfun: BackendSettingsDict
    xai: BackendSettingsDict
