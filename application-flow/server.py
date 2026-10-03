"""Local demo API for the WIP application flow.

Run from the repository root with: python application-flow/server.py
Data is held in memory and cleared on restart.
"""
from __future__ import annotations

import base64
import binascii
import json
import os
import re
import smtplib
import threading
from email.message import EmailMessage
import uuid
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
LOCK = threading.Lock()
APPLICATIONS: list[dict] = []
RESUMES: dict[str, dict] = {}
MAX_RESUME_BYTES = 5 * 1024 * 1024
PIPELINE_STAGES = ("Submitted", "Screening", "Assessment", "Interview", "Offer", "Hired", "Rejected", "Withdrawn")


class BooleanSearch:
    """Small recursive-descent parser with NOT > AND > OR precedence."""

    def __init__(self, expression: str):
        if len(expression) > 500:
            raise ValueError("Search query must be 500 characters or fewer")
        self.tokens = re.findall(r'"(?:[^"\\]|\\.)*"|\(|\)|\bAND\b|\bOR\b|\bNOT\b|[^\s()]+', expression, re.I)
        self.position = 0

    def peek(self):
        return self.tokens[self.position].upper() if self.position < len(self.tokens) else None

    def take(self):
        token = self.tokens[self.position]
        self.position += 1
        return token

    def parse(self):
        if not self.tokens:
            return None
        result = self.parse_or()
        if self.position != len(self.tokens):
            raise ValueError("Unexpected token in Boolean search")
        return result

    def parse_or(self):
        node = self.parse_and()
        while self.peek() == "OR":
            self.take()
            node = ("OR", node, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_unary()
        while self.peek() == "AND":
            self.take()
            node = ("AND", node, self.parse_unary())
        return node

    def parse_unary(self):
        if self.peek() == "NOT":
            self.take()
            return ("NOT", self.parse_unary())
        if self.peek() == "(":
            self.take()
            node = self.parse_or()
            if self.peek() != ")":
                raise ValueError("Missing closing parenthesis in Boolean search")
            self.take()
            return node
        token = self.peek()
        if token is None or token in ("AND", "OR", ")"):
            raise ValueError("Expected a search term in Boolean search")
        raw = self.take()
        return ("TERM", raw[1:-1] if raw.startswith('"') and raw.endswith('"') else raw)

    @staticmethod
    def matches(node, text: str) -> bool:
        if node is None:
            return True
        operator = node[0]
        if operator == "TERM":
            return node[1].casefold() in text.casefold()
        if operator == "NOT":
            return not BooleanSearch.matches(node[1], text)
        if operator == "AND":
            return BooleanSearch.matches(node[1], text) and BooleanSearch.matches(node[2], text)
        return BooleanSearch.matches(node[1], text) or BooleanSearch.matches(node[2], text)


def applicant_search_text(record: dict) -> str:
    return " ".join(str(value) for value in (
        record.get("candidateName", ""), record.get("candidateEmail", ""),
        record.get("jobTitle", ""), record.get("jobId", ""), record.get("skills", ""),
        record.get("expertise", ""), record.get("qualifications", ""),
        record.get("experience", ""), record.get("eligibility", ""),
    ))


def send_confirmation(record: dict) -> dict:
    """Send a candidate receipt email when SMTP environment settings are configured."""
    host = os.getenv("SMTP_HOST")
    sender = os.getenv("SMTP_FROM")
    if not host or not sender:
        return {"status": "not_configured", "sentAt": None}
    message = EmailMessage()
    message["Subject"] = f"Application received: {record['jobTitle']}"
    message["From"] = sender
    message["To"] = record["candidateEmail"]
    message.set_content(
        f"Hello {record['candidateName']},\\n\\n"
        f"We have received your application for {record['jobTitle']} "
        f"(reference {record['id']}). The hiring team will review it and update you.\\n\\n"
        "Regards,\\nTalent Acquisition"
    )
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    timeout = 15
    try:
        if os.getenv("SMTP_USE_SSL", "false").lower() == "true":
            with smtplib.SMTP_SSL(host, port, timeout=timeout) as client:
                if username:
                    client.login(username, password or "")
                client.send_message(message)
        else:
            with smtplib.SMTP(host, port, timeout=timeout) as client:
                client.starttls()
                if username:
                    client.login(username, password or "")
                client.send_message(message)
        return {"status": "sent", "sentAt": now_iso()}
    except Exception as exc:
        print(f"Confirmation email delivery failed: {type(exc).__name__}")
        return {"status": "failed", "sentAt": None, "detail": "Email provider delivery failed"}


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
            # Demo-only identity filter. Production requires authenticated roles.
            email = self.headers.get("X-Demo-Email", "").strip().lower()
            params = parse_qs(parsed.query)
            query = params.get("q", [""])[0].strip()
            stage = params.get("stage", [""])[0].strip()
            job_id = params.get("jobId", [""])[0].strip()
            try:
                expression = BooleanSearch(query).parse()
            except ValueError as exc:
                return self._json(400, {"error": str(exc)})
            with LOCK:
                records = [dict(item) for item in APPLICATIONS]
            if email:
                records = [item for item in records if item["candidateEmail"].lower() == email]
            if stage:
                records = [item for item in records if item.get("stage") == stage]
            if job_id:
                records = [item for item in records if item.get("jobId") == job_id]
            if expression:
                records = [item for item in records if BooleanSearch.matches(expression, applicant_search_text(item))]
            return self._json(200, {"applications": records, "count": len(records), "stages": PIPELINE_STAGES})
        if parsed.path == "/api/ats/stages":
            return self._json(200, {"stages": PIPELINE_STAGES})
        if parsed.path == "/api/ats/jobs":
            with LOCK:
                records = [dict(item) for item in APPLICATIONS]
            jobs = {}
            for item in records:
                job = jobs.setdefault(item["jobId"], {
                    "jobId": item["jobId"], "jobTitle": item["jobTitle"],
                    "total": 0, "stageCounts": {}, "applications": [],
                })
                job["total"] += 1
                job["stageCounts"][item["stage"]] = job["stageCounts"].get(item["stage"], 0) + 1
                job["applications"].append(item)
            return self._json(200, {"jobs": list(jobs.values())})
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
                "stage": "Submitted",
                "createdAt": now_iso(),
                "updatedAt": now_iso(),
                "interview": None,
                "result": "",
                "activity": [{"type": "submitted", "at": now_iso(),
                              "message": "Application received"}],
            }
            APPLICATIONS.append(record)
        email_delivery = send_confirmation(record)
        with LOCK:
            record["confirmationEmail"] = email_delivery
            record["activity"].append({
                "type": "confirmation_email", "at": now_iso(),
                "message": f"Candidate confirmation email {email_delivery['status']}",
            })
        return self._json(201, {"application": record, "confirmationEmail": email_delivery})

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
                new_stage = str(data["stage"]).strip()
                if new_stage not in PIPELINE_STAGES:
                    return self._json(400, {"error": "Invalid ATS stage", "allowedStages": PIPELINE_STAGES})
                record["stage"] = new_stage
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
