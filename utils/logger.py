import logging
import os
import json
from datetime import datetime, UTC
from logging.handlers import RotatingFileHandler

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "logger": record.name,
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage()
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def get_logger(name: str) -> logging.Logger:
    os.makedirs("var_logs", exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        handler = RotatingFileHandler("var_logs/SystemOut.log", maxBytes=5_000_000, backupCount=5)
        handler.setFormatter(JsonFormatter())
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JsonFormatter())
        logger.setLevel(getattr(logging, log_level, logging.INFO))
        logger.addHandler(handler)
        logger.addHandler(console_handler)
    return logger
    