ts = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
import csv, json, os, datetime

BASE = os.path.dirname(os.path.dirname(__file__))
EMP_CSV = os.path.join(BASE, "hr-data", "employees.csv")
ROLE_MAP = os.path.join(BASE, "policies", "role_mapping.json")
AUDIT_LOG = os.path.join(BASE, "logs", "sample_audit.log")

def log(msg: str):
    ts = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} {msg}\n")

def clean(v): return (v or "").strip()

def desired_groups(emp, mapping):
    groups = set(mapping.get("default_groups", []))
    dept = clean(emp.get("department"))
    loc  = clean(emp.get("location"))
    groups.update(mapping.get("department_to_groups", {}).get(dept, []))
    groups.update(mapping.get("location_to_groups", {}).get(loc, []))
    return sorted(groups)

def onboard(emp, mapping):
    email = clean(emp.get("email"))
    if not email:
        return
    groups = desired_groups(emp, mapping)
    print(f"[JOINER] Create user: {email}")
    print(f"[JOINER] Assign groups: {groups}")
    print("[JOINER] Enforce MFA: enabled (simulated)")
    log(f"JOINER user={email} groups={groups} mfa=enabled source=hr")

if __name__ == "__main__":
    with open(ROLE_MAP, encoding="utf-8") as f:
        mapping = json.load(f)
    with open(EMP_CSV, encoding="utf-8") as f:
        for emp in csv.DictReader(f):
            if clean(emp.get("status")).upper() == "ACTIVE":
                onboard(emp, mapping)
