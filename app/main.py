from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config
from app.endpoints import analyze
from app.endpoints import history
from app.database import engine, Base
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title=Config.APP_NAME, debug=Config.DEBUG)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# CORS для Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(analyze.router)
app.include_router(history.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {Config.APP_NAME}", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
