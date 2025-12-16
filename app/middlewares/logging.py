
import logging
from fastapi import FastAPI, Request

def setup_logging(app: FastAPI):
    logger = logging.getLogger('babafly')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    @app.middleware('http')
    async def log_requests(request: Request, call_next):
        logger.info(f'{request.method} {request.url.path}')
        response = await call_next(request)
        logger.info(f'{request.method} {request.url.path} -> {response.status_code}')
        return response
