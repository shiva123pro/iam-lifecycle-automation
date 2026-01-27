import json, os, datetime

BASE = os.path.dirname(os.path.dirname(__file__))
ROLE_MAP = os.path.join(BASE, "policies", "role_mapping.json")
AUDIT_LOG = os.path.join(BASE, "logs", "sample_audit.log")

def log(msg: str):
    ts = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} {msg}\n")

def compute_groups(dept, loc, mapping):
    dept = (dept or "").strip()
    loc  = (loc or "").strip()
    groups = set(mapping.get("default_groups", []))
    groups.update(mapping.get("department_to_groups", {}).get(dept, []))
    groups.update(mapping.get("location_to_groups", {}).get(loc, []))
    return sorted(groups)

def mover(email, old_dept, old_loc, new_dept, new_loc, mapping):
    old_groups = compute_groups(old_dept, old_loc, mapping)
    new_groups = compute_groups(new_dept, new_loc, mapping)
    removed = sorted(set(old_groups) - set(new_groups))
    added   = sorted(set(new_groups) - set(old_groups))

    print(f"[MOVER] User: {email}")
    print(f"[MOVER] Remove groups: {removed}")
    print(f"[MOVER] Add groups: {added}")
    print("[MOVER] Trigger access review: yes (simulated)")
    log(f"MOVER user={email} removed={removed} added={added} access_review=triggered source=hr")

if __name__ == "__main__":
    with open(ROLE_MAP, encoding="utf-8") as f:
        mapping = json.load(f)
    mover("john.doe@demo.com", "IT", "US", "Finance", "US", mapping)
