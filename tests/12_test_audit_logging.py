import os
import json
from utils.audit import audit_event

def test_audit_event_logging():
    audit_event(
        action="create_user",
        actor="admin@kasama.local",
        target="user:richard@kasama.local",
        metadata={"role": "sysoper", "status": "active"}
    )

    log_file = "var_logs/AuditTrail.log"
    assert os.path.exists(log_file)

    with open(log_file, "r") as f:
        logs = f.readlines()

    assert any("create_user" in log for log in logs)
    assert any("admin@kasama.local" in log for log in logs)
    