from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class RecognitionHistoryResponse(BaseModel):
    id: int
    filename: str
    timestamp: datetime
    dominant_emotion: Optional[str] = None
    confidence: Optional[float] = None
    result_json: Dict[str, Any]
    
    class Config:
        from_attributes = True


class HistoryListResponse(BaseModel):
    total: int
    items: list[RecognitionHistoryResponse]
