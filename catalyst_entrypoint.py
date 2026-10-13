"""Catalyst AppSail entry point for the application-flow demo.

Catalyst supplies X_ZOHO_CATALYST_LISTEN_PORT at runtime. This wrapper
keeps the existing local demo server available while binding AppSail to the
container interface and runtime-assigned port.
"""
from __future__ import annotations

import os
from http.server import ThreadingHTTPServer
from pathlib import Path
from runpy import run_path

ROOT = Path(__file__).resolve().parent
application = run_path(str(ROOT / "application-flow" / "server.py"), run_name="wip_application_flow")
Handler = application["Handler"]

host = "0.0.0.0"
port = int(os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT", "8000"))
server = ThreadingHTTPServer((host, port), Handler)
print(f"Application flow AppSail server listening on {host}:{port}")
try:
    server.serve_forever()
finally:
    server.server_close()
