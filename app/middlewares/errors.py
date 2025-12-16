
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import logging

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.exception('Unhandled exception')
        return JSONResponse({'detail': 'Internal Server Error'}, status_code=500)
