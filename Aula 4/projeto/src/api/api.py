from fastapi import FastAPI, Request
from src.api import routes
from src.utils import db_manager
import datetime
import logging
import os

LOGGING_PATH = os.path.join("logs", "app.log")
logging.basicConfig(
    filename=LOGGING_PATH,  # specify the file name and path
    level=logging.DEBUG,  # set the logging level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # specify the format
    datefmt="%Y-%m-%d %H:%M:%S",
)  # format for the date in the log messages


app = FastAPI()

# Inicializando o DBManager e configurando as tabelas
db = db_manager.DBManager()
db.setup_tables()


@app.middleware("http")
async def log_and_store_requests(request: Request, call_next):
    start_time = datetime.datetime.now()

    response = await call_next(request)

    end_time = datetime.datetime.now()
    latency = end_time - start_time
    latency_miliseconds = latency.total_seconds() / 1000

    logging.info(
        f"Request: {request.method} {request.url} - Response: {response.status_code} - Latency: {latency_miliseconds} ms"
    )

    # Usando o DBManager para inserir métricas no banco de dados
    db.insert_operational_metric(
        start_time,
        request.method,
        str(request.url),
        response.status_code,
        latency_miliseconds,
    )

    return response


app.include_router(routes.router)
