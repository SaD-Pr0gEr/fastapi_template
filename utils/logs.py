import json
import logging
import sys
import time
from logging import LogRecord

from core.context import request_id_ctx, user_id_ctx


class RequestIdentifyContextFilter(logging.Filter):
    def filter(self, record: LogRecord):
        record.request_id = request_id_ctx.get()
        record.user_id = user_id_ctx.get()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: LogRecord):
        log_record = {
            "local_time": time.strftime(
                "%Y-%m-%dT%H:%M:%S", time.localtime(record.created)
            ),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "request_id": getattr(record, "request_id", "-"),
            "user_id": getattr(record, "user_id", None) or "Anonym",
            "timestamp": record.created,
            "module": record.module,
            "filename": record.filename,
            "line": record.lineno,
        }
        return json.dumps(log_record)


def setup_logging(level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIdentifyContextFilter())
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
