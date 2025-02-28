from typing import List, Optional

from pydantic import BaseModel


class JsonEntriesSpec(BaseModel):
    schema_name: str
    subset: Optional[List[str]] = None


class TextsSpec(BaseModel):
    dataset: str
    filenames: Optional[List[str]] = None


class RequestSettings(BaseModel):
    batch_size: int
    block_ms: int
    min_idle_time_ms: int
    max_times_delivered: int
    use_cache: int


class ExtractionRequest(BaseModel):
    model: str
    json_entries: JsonEntriesSpec
    texts: TextsSpec
    settings: RequestSettings


