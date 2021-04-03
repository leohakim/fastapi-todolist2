import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from apps.todo.routers import router as todo_router
from config import settings
from databases import Database
import logging

logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():

    # MongoDB Connection
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_NAME]

    # PgSQL Connection
    database = Database(settings.DATABASE_URL, min_size=2, max_size=10)
    try:
        await database.connect()
        app.state.pgsql_db = database
        logger.info("PostgreSQL Connected")
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


@app.on_event("shutdown")
async def shutdown_db_client():

    # MongoDB Disconnection
    app.mongodb_client.close()

    # PgSQL Disconnection
    try:
        await app.state.pgsql_db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")


app.include_router(todo_router, tags=["tasks"], prefix="/task")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
