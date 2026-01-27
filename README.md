# IAM Lifecycle Automation (Joiner–Mover–Leaver)

This repo demonstrates a realistic IAM lifecycle workflow where an HR feed drives:
- Joiner: provision user + assign role-based access
- Mover: remove old access + grant new access (no privilege accumulation)
- Leaver: disable account + revoke sessions/tokens + remove access

## Repo layout
- hr-data/employees.csv: HR source-of-truth simulation
- policies/role_mapping.json: department/location → groups mapping
- scripts/
  - onboard_user.py
  - update_user.py
  - offboard_user.py
- logs/sample_audit.log: audit trail output

## Run
python3 scripts/onboard_user.py
python3 scripts/update_user.py
python3 scripts/offboard_user.py

## Security controls demonstrated
- Least privilege via role/group mapping
- Automated deprovisioning on termination
- Access recalculation on role change (no access accumulation)
- Audit logging for every lifecycle action
- MFA enforcement and access review are simulated (easy to wire to Okta/Entra APIs)
