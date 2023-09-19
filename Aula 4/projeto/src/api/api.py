from fastapi import FastAPI, Request
from src.api import routes
from src.utils import logger, db_manager
import datetime


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

    # Log and store details about the request and response
    logger.log_message(
        f"{request.method} {request.url} - {response.status_code} (Latency: {latency_miliseconds:.0f} seconds)"
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
