from auth_routes import auth_router
from order_routes import order_router
from fastapi import FastAPI
import logging
import time

app = FastAPI()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware para medir tempo de resposta


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Path: {request.url.path} | Method: {request.method} | Duration: {process_time * 1000:.2f}ms")
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(auth_router)
app.include_router(order_router)
