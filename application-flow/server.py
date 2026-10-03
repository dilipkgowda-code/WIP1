"""Local demo API for the WIP application flow.

Run from the repository root with: python application-flow/server.py
Data is held in memory and cleared on restart.
"""
from __future__ import annotations

import base64
import binascii
import json
import re
import threading
import uuid
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
LOCK = threading.Lock()
APPLICATIONS: list[dict] = []
RESUMES: dict[str, dict] = {}
MAX_RESUME_BYTES = 5 * 1024 * 1024


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        # A 5 MiB resume expands to under 7 MiB in base64.
        if length > 8_000_000:
            raise ValueError("Request body is too large")
        value = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(value, dict):
            raise ValueError("Expected a JSON object")
        return value

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self._json(200, {"ok": True, "service": "application-flow-demo"})
        if parsed.path == "/api/applications":
            # Demo-only filter; production must derive identity from authenticated sessions.
            email = self.headers.get("X-Demo-Email", "").strip().lower()
            with LOCK:
                records = [dict(item) for item in APPLICATIONS]
            if email:
                records = [item for item in records if item["candidateEmail"].lower() == email]
            return self._json(200, {"applications": records})
        match = re.fullmatch(r"/api/resumes/([a-f0-9-]+)", parsed.path)
        if match:
            with LOCK:
                resume = RESUMES.get(match.group(1))
            if not resume:
                return self._json(404, {"error": "Resume not found"})
            self.send_response(200)
            self.send_header("Content-Type", resume["contentType"])
            self.send_header("Content-Disposition", f'attachment; filename="{resume["filename"]}"')
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(resume["content"])))
            self.end_headers()
            self.wfile.write(resume["content"])
            return
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/applications":
            return self._json(404, {"error": "Not found"})
        try:
            data = self._body()
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"error": str(exc)})
        required = ("jobId", "jobTitle", "candidateName", "candidateEmail")
        if any(not str(data.get(key, "")).strip() for key in required):
            return self._json(400, {"error": "Job and candidate details are required"})
        email = str(data["candidateEmail"]).strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            return self._json(400, {"error": "Enter a valid email address"})
        resume_data = data.get("resume")
        if not isinstance(resume_data, dict) or not resume_data.get("filename") or not resume_data.get("base64"):
            return self._json(400, {"error": "Please attach your resume"})
        filename = re.sub(r"[^A-Za-z0-9._ -]", "_", Path(str(resume_data["filename"])).name)[:180]
        extension = Path(filename).suffix.lower()
        types = {
            ".pdf": "application/pdf",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        if extension not in types:
            return self._json(400, {"error": "Resume must be a PDF, DOC, or DOCX file"})
        try:
            resume_bytes = base64.b64decode(str(resume_data["base64"]), validate=True)
        except (binascii.Error, ValueError):
            return self._json(400, {"error": "Resume upload is not valid base64 data"})
        if not resume_bytes or len(resume_bytes) > MAX_RESUME_BYTES:
            return self._json(400, {"error": "Resume must be between 1 byte and 5 MB"})
        if extension == ".pdf" and not resume_bytes.startswith(b"%PDF-"):
            return self._json(400, {"error": "The selected file does not appear to be a PDF"})
        if extension == ".docx" and not resume_bytes.startswith(b"PK"):
            return self._json(400, {"error": "The selected file does not appear to be a DOCX document"})

        with LOCK:
            duplicate = next((item for item in APPLICATIONS
                              if item["jobId"] == str(data["jobId"])
                              and item["candidateEmail"].lower() == email), None)
            if duplicate:
                return self._json(409, {"error": "You have already applied for this role"})
            resume_id = str(uuid.uuid4())
            RESUMES[resume_id] = {
                "filename": filename,
                "contentType": types[extension],
                "content": resume_bytes,
            }
            record = {
                "id": str(uuid.uuid4()),
                "jobId": str(data["jobId"]),
                "jobTitle": str(data["jobTitle"]).strip(),
                "candidateName": str(data["candidateName"]).strip(),
                "candidateEmail": email,
                "phone": str(data.get("phone", "")).strip(),
                "skills": data.get("skills", []),
                "expertise": str(data.get("expertise", "")).strip(),
                "qualifications": data.get("qualifications", []),
                "experience": data.get("experience", []),
                "eligibility": data.get("eligibility", {}),
                "declarations": data.get("declarations", {}),
                "resumeName": filename,
                "resumeId": resume_id,
                "stage": "Applied",
                "createdAt": now_iso(),
                "updatedAt": now_iso(),
                "interview": None,
                "result": "",
                "activity": [{"type": "submitted", "at": now_iso(),
                              "message": "Application received"}],
            }
            APPLICATIONS.append(record)
        return self._json(201, {"application": record})

    def do_PATCH(self):
        match = re.fullmatch(r"/api/applications/([a-f0-9-]+)", urlparse(self.path).path)
        if not match:
            return self._json(404, {"error": "Not found"})
        try:
            data = self._body()
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"error": str(exc)})
        with LOCK:
            record = next((item for item in APPLICATIONS if item["id"] == match.group(1)), None)
            if not record:
                return self._json(404, {"error": "Application not found"})
            messages = []
            if "stage" in data:
                record["stage"] = str(data["stage"]).strip()
                messages.append(f"Application stage updated to {record['stage']}")
            if "interview" in data:
                record["interview"] = data["interview"]
                messages.append("Interview details updated")
            if "result" in data:
                record["result"] = str(data["result"]).strip()
                messages.append(f"Application result updated: {record['result']}")
            if not messages:
                return self._json(400, {"error": "No supported application changes supplied"})
            record["updatedAt"] = now_iso()
            record["activity"].extend(
                {"type": "update", "at": record["updatedAt"], "message": message}
                for message in messages
            )
            updated = dict(record)
        return self._json(200, {"application": updated})

    def log_message(self, format, *args):
        print("%s - %s" % (self.log_date_time_string(), format % args))


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    server = ThreadingHTTPServer(address, Handler)
    print(f"Application flow demo: http://{address[0]}:{address[1]}/application-flow/candidate-application.html")
    print("Demo data is in memory and resets when the server stops. Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping application flow demo server.")
    finally:
        server.server_close()
