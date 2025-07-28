import psutil
import uvicorn
from asgi import application

if __name__ == "__main__":
    uvicorn.run(
        "asgi:application",
        log_level=application.config.server.LOGLEVEL,
        port=application.config.server.PORT,
        host=application.config.server.HOST,
        workers=psutil.cpu_count(logical=True) + 1,
    )
