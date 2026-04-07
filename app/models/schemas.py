from pydantic import BaseModel
from typing import Optional, Dict, Any

class FaceAnalysisResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
