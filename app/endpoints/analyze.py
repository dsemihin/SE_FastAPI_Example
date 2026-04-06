import logging
from fastapi import APIRouter, File, UploadFile
from app.models.schemas import FaceAnalysisResponse
from app.services.deepface_service import DeepFaceService

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analyze", tags=["Face Analysis"])

@router.post("/", response_model=FaceAnalysisResponse)
async def analyze_face(file: UploadFile = File(...)):
    """
    Анализ лица на загруженном изображении
    """
    logger.info(f"Получен запрос на анализ файла: {file.filename}")
    logger.info(f"Тип файла: {file.content_type}")
    
    # Проверяем тип файла
    if not file.content_type.startswith("image/"):
        logger.warning(f"Неверный тип файла: {file.content_type}")
        return FaceAnalysisResponse(
            success=False,
            error="Файл должен быть изображением"
        )
    
    try:
        # Читаем байты
        image_bytes = await file.read()
        logger.info(f"Прочитано {len(image_bytes)} байт")
        
        # Анализируем
        logger.info("Запуск анализа через DeepFace")
        result = await DeepFaceService.analyze_face(image_bytes)
        
        if "error" in result:
            logger.error(f"Ошибка анализа: {result['error']}")
            return FaceAnalysisResponse(
                success=False,
                error=result["error"]
            )
        
        logger.info(f"Анализ успешно завершен. Эмоция: {result['emotion']}, Возраст: {result['age']}, Пол: {result['gender']}")
        return FaceAnalysisResponse(
            success=True,
            data={
                "emotion": result["emotion"],
                "emotion_scores": result["emotion_scores"],
                "age": result["age"],
                "gender": result["gender"],
                "gender_confidence": result["gender_confidence"]
            }
        )
        
    except Exception as e:
        logger.exception("Непредвиденная ошибка при анализе изображения")
        return FaceAnalysisResponse(
            success=False,
            error=f"Внутренняя ошибка сервера: {str(e)}"
        )
