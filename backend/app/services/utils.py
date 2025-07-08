import logging
import time

logger = logging.getLogger(__name__)


def medir_tempo(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        resultado = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} executada em {end - start:.3f} segundos")
        return resultado

    return wrapper


def medir_tempo_async(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        resultado = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executada em {end - start:.3f} segundos")
        return resultado

    return wrapper
