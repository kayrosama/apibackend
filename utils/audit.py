import json
import os
from datetime import datetime, UTC
import logging
from logging.handlers import RotatingFileHandler

class JsonAuditFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

def get_audit_logger(name: str) -> logging.Logger:
    os.makedirs("var_logs", exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RotatingFileHandler("var_logs/AuditTrail.log", maxBytes=5_000_000, backupCount=5)
        handler.setFormatter(JsonAuditFormatter())
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger

audit_logger = get_audit_logger("audit")

def audit_event(action: str, actor: str, target: str = None, metadata: dict = None):
    event = {
        "action": action,
        "actor": actor,
        "target": target,
        "metadata": metadata or {}
    }
    audit_logger.info(json.dumps(event))
    