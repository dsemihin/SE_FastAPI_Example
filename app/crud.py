from sqlalchemy.orm import Session
from sqlalchemy import desc
import json
from datetime import datetime
from app.database import RecognitionHistory


def create_recognition_record(db: Session, filename: str, result: dict, 
                               dominant_emotion: str = None, confidence: float = None):
    result_json_str = json.dumps(result, ensure_ascii=False)
    db_record = RecognitionHistory(
        filename=filename,
        result_json=result_json_str,
        dominant_emotion=dominant_emotion,
        confidence=confidence,
        timestamp=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_history(db: Session, skip: int = 0, limit: int = 50, emotion_filter: str = None):
    query = db.query(RecognitionHistory)
    if emotion_filter:
        query = query.filter(RecognitionHistory.dominant_emotion == emotion_filter)
    return query.order_by(desc(RecognitionHistory.timestamp)).offset(skip).limit(limit).all()


def get_total_count(db: Session, emotion_filter: str = None):
    query = db.query(RecognitionHistory)
    if emotion_filter:
        query = query.filter(RecognitionHistory.dominant_emotion == emotion_filter)
    return query.count()


def get_history_record(db: Session, record_id: int):
    return db.query(RecognitionHistory).filter(RecognitionHistory.id == record_id).first()


def delete_history_record(db: Session, record_id: int):
    record = get_history_record(db, record_id)
    if record:
        db.delete(record)
        db.commit()
        return True
    return False


def clear_all_history(db: Session):
    count = db.query(RecognitionHistory).count()
    db.query(RecognitionHistory).delete()
    db.commit()
    return count
