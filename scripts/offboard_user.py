import os, datetime

BASE = os.path.dirname(os.path.dirname(__file__))
AUDIT_LOG = os.path.join(BASE, "logs", "sample_audit.log")

def log(msg: str):
    ts = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} {msg}\n")

def offboard(email: str):
    email = (email or "").strip()
    if not email:
        return
    print(f"[LEAVER] Disable account: {email}")
    print(f"[LEAVER] Revoke sessions/tokens: {email}")
    print(f"[LEAVER] Remove group memberships: {email}")
    log(f"LEAVER user={email} action=disabled sessions=revoked groups=removed source=hr")

if __name__ == "__main__":
    offboard("ravi.sharma@demo.com")
