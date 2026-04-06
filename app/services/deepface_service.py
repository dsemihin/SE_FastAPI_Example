import logging
from deepface import DeepFace
import cv2
import numpy as np
from typing import Dict, Any

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

class DeepFaceService:
    
    @staticmethod
    async def analyze_face(image_bytes: bytes) -> Dict[str, Any]:
        """
        Анализирует лицо на изображении и возвращает эмоции, возраст, пол
        """
        try:
            logger.info("Начало анализа изображения")
            
            # Конвертируем байты в изображение OpenCV
            logger.debug("Конвертация байтов в изображение OpenCV")
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                logger.error("Не удалось декодировать изображение")
                return {"error": "Не удалось декодировать изображение"}
            
            logger.info("Изображение успешно декодировано")
            
            # Анализ через DeepFace
            logger.info("Запуск DeepFace.analyze()")
            result = DeepFace.analyze(
                img_path=img,
                actions=['emotion', 'age', 'gender'],
                enforce_detection=False,
                silent=True
            )
            logger.info("DeepFace.analyze() завершил работу")
            
            # DeepFace возвращает список, берем первый элемент
            analysis = result[0] if isinstance(result, list) else result
            
            logger.debug(f"Результат анализа: эмоция={analysis.get('dominant_emotion')}, возраст={analysis.get('age')}")
            
            return {
                "success": True,
                "emotion": analysis.get("dominant_emotion", "unknown"),
                "emotion_scores": analysis.get("emotion", {}),
                "age": analysis.get("age", 0),
                "gender": analysis.get("dominant_gender", "unknown"),
                "gender_confidence": analysis.get("gender", {}).get(analysis.get("dominant_gender", ""), 0) if analysis.get("gender") else 0
            }
            
        except Exception as e:
            logger.exception(f"Ошибка при работе DeepFace: {str(e)}")
            return {"error": str(e)}
