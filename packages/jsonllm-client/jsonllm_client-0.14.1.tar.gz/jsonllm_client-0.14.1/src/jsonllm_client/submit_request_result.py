from typing import Optional

from pydantic import BaseModel


class SubmitRequestResult(BaseModel):
    ok: bool
    request_id: Optional[str] = None
    error_message: Optional[str] = None
