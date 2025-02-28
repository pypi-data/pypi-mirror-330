from typing import Literal, Optional, Dict, Any, List

from pydantic import BaseModel, NonNegativeInt


class WorkUnitStatusCounts(BaseModel):
    total: NonNegativeInt
    cached: NonNegativeInt
    pending: NonNegativeInt
    unprocessed: NonNegativeInt
    processed: NonNegativeInt


class RequestShortStatus(BaseModel):
    request_id: str
    status: Literal["unknown", "submitted", "running", "completed", "cancelled", "timeout"]
    work_unit_status_counts: Optional[WorkUnitStatusCounts] = None


class ValueResult(BaseModel):
    ok: bool
    value: Optional[Any] = None
    raw: Optional[str] = None


class FilenameResult(BaseModel):
    filename: str
    kv: Dict[str, ValueResult]


class RequestDetailedStatus(BaseModel):
    request_id: str
    status: Literal["unknown", "submitted", "running", "completed", "cancelled", "timeout"]
    work_unit_status_counts: Optional[WorkUnitStatusCounts] = None
    processed: Dict[str, FilenameResult]

    def get_successful_rows(self) -> List[Dict]:
        rows = []
        for filename, filename_result in self.processed.items():
            dct = {
                "filename": filename
            }
            if any(not v.ok for v in filename_result.kv.values()):
                continue
            for k, v in filename_result.kv.items():
                dct[k] = v.value
            rows.append(dct)
        return rows
