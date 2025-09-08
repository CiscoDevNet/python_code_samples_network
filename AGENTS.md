## Dev environment tips

- **Python version**: Use Python 3.9+.
- **Virtual env (recommended)**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install -U pip
  ```
- **Each sample is standalone**: cd into a sample directory, read its `README.md`, install that folder’s `requirements.txt` if present, then run the script.
- **Install dependencies (pattern)**:
  ```bash
  cd /python_code_samples_network/<sample-folder>
  [ -f requirements.txt ] && python -m pip install -r requirements.txt
  ```
- **Common packages**: Some samples use `requests`, `ncclient`, `pysnmp`, or `netmiko`. If a folder has no `requirements.txt`, install what the `README.md` mentions, e.g.:
  ```bash
  python -m pip install requests ncclient netmiko pysnmp
  ```
- **Secrets and device access**: Most scripts expect you to edit device/controller IP, username, and password inside the script (or helper files like `device_info.py`). Ensure network reachability and open ports (SSH/NETCONF/RESTCONF/HTTPS).

### Quick run examples

- **Netmiko interface example**
  ```bash
  cd /python_code_samples_network/netmiko-interface-example
  python -m pip install -r requirements.txt
  # Set device details in device_info.py
  python netmiko-get-interface.py
  python netmiko-create-interface.py
  python netmiko-delete-interface.py
  ```

- **RESTCONF – update IP address**
  ```bash
  cd /python_code_samples_network/restconf_update_ipaddress
  python -m pip install -r requirements.txt
  python updateip.py
  ```

- **NETCONF – get/edit config**
  ```bash
  cd /python_code_samples_network/NC-get-config
  python -m pip install ncclient
  python NC-get-config.py
  ```

## Testing instructions

- **There is no unified test suite** in this repository. Most folders contain minimal examples meant to run directly against real devices/controllers.
- **Smoke test** a change by running the sample(s) you touched:
  ```bash
  cd /python_code_samples_network/<sample-folder>
  [ -f requirements.txt ] && python -m pip install -r requirements.txt
  python <script>.py
  ```
- **Static checks (optional)**: If you add new Python code, you can run lightweight checks:
  ```bash
  python -m pip install ruff mypy
  ruff check .
  mypy --ignore-missing-imports .
  ```

- **Test the code with the Cisco DevNet sandbox**
  Visit https://devnetsandbox.cisco.com/DevNet to book a related sandbox
  
- **Latest Cisco API documentation**:
  https://developer.cisco.com/docs/


## PR instructions

- **Title format**: `[sample-folder] <Short description>` (e.g., `[RESTCONF] fix hostname PUT example`).
- **Scope**: Keep changes limited to one sample folder when possible. If you cross-cut multiple folders, explain why in the PR description.
- **Before committing**:
  - Run the modified script(s) to ensure they work end-to-end.
  - If you added deps, include or update that folder’s `requirements.txt`.
  - Update `README.md` within the affected folder.
  - Run optional linters:
    ```bash
    ruff check .
    ```
- **Security**: Do not commit real credentials or tokens. Use placeholders and document required env vars or files.

## Contribution conventions

- **Coding style**: Prefer clear, readable Python with descriptive variable names and early returns. Avoid catching exceptions without handling.
- **Inputs**: Use constants or a small config block at the top of the script for device IP/credentials. Consider reading from environment variables if it improves UX.
- **Outputs**: Print concise results or JSON. Avoid noisy logs; add `-v/--verbose` only if needed.
- **Dependencies**: Pin major versions when practical; keep per-folder `requirements.txt` minimal.
- **Backward compatibility**: Do not change existing sample behavior unless clearly improving or fixing a bug; document changes.


