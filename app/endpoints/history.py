"""
Модуль с эндпоинтами для работы с историей распознаваний.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/", response_model=schemas.HistoryListResponse)
async def get_history(
    skip: int = 0,
    limit: int = 50,
    emotion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Получить историю распознаваний.
    
    - **skip**: сколько записей пропустить (пагинация)
    - **limit**: сколько записей показать (макс. 50)
    - **emotion**: фильтр по эмоции (например, "happy", "sad")
    """
    records = crud.get_history(db, skip=skip, limit=limit, emotion_filter=emotion)
    total = crud.get_total_count(db, emotion_filter=emotion)
    
    items = []
    for record in records:
        result_json = json.loads(record.result_json)
        items.append(schemas.RecognitionHistoryResponse(
            id=record.id,
            filename=record.filename,
            timestamp=record.timestamp,
            dominant_emotion=record.dominant_emotion,
            confidence=record.confidence,
            result_json=result_json
        ))
    
    return schemas.HistoryListResponse(total=total, items=items)


@router.get("/{record_id}", response_model=schemas.RecognitionHistoryResponse)
async def get_history_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить конкретную запись истории по ID.
    """
    record = crud.get_history_record(db, record_id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found"
        )
    
    result_json = json.loads(record.result_json)
    
    return schemas.RecognitionHistoryResponse(
        id=record.id,
        filename=record.filename,
        timestamp=record.timestamp,
        dominant_emotion=record.dominant_emotion,
        confidence=record.confidence,
        result_json=result_json
    )


@router.delete("/{record_id}")
async def delete_history_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить запись из истории по ID.
    """
    success = crud.delete_history_record(db, record_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found"
        )
    
    return {"message": f"Record {record_id} deleted successfully"}


@router.post("/clear")
async def clear_history(
    db: Session = Depends(get_db)
):
    """
    Очистить всю историю распознаваний.
    """
    deleted_count = crud.clear_all_history(db)
    
    return {
        "message": "History cleared successfully",
        "deleted_count": deleted_count
    }