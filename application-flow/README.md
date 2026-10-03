# Application flow local demo

## Run the server

From the repository root, configure an SMTP account using environment variables and start the server:

```powershell
$env:SMTP_HOST = "smtp.example.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your-smtp-user"
$env:SMTP_PASSWORD = "your-smtp-password"
$env:SMTP_FROM = "recruitment@example.com"
python application-flow/server.py
```

The server uses STARTTLS on the configured port. Set `SMTP_USE_SSL=true` only when the provider requires implicit TLS. Keep credentials in environment variables or a secret manager; never commit them. If `SMTP_HOST` or `SMTP_FROM` is missing, applications still submit but the response reports `confirmationEmail.status = not_configured`. If SMTP delivery fails, the application remains recorded and the response reports `failed`; configure monitoring and a persistent retry queue before production.

Open the form at [http://127.0.0.1:8000/application-flow/candidate-application.html](http://127.0.0.1:8000/application-flow/candidate-application.html).

## Backend routes

- `GET /api/health` — server health.
- `GET /api/ats/stages` — supported ATS stages: Submitted, Screening, Assessment, Interview, Offer, Hired, Rejected, Withdrawn.
- `GET /api/ats/jobs` — applications grouped by job, including stage counts and candidate records.
- `GET /api/applications?q=python%20AND%20(fintech%20OR%20payments)&stage=Screening&jobId=FIN-ROLE-001` — Boolean search and filters across candidate name, email, job, skills, expertise, qualifications, experience, and eligibility. Operators are case-insensitive; precedence is NOT, AND, OR. Quote phrases and use parentheses.
- `POST /api/applications` — submit application, attach resume, and send a confirmation email when SMTP is configured.
- `PATCH /api/applications/{id}` — update ATS stage, interview details, or result. Stage values are validated against the supported workflow.
- `GET /api/resumes/{id}` — download a resume in this demo.

## Prototype limitations

Applications and resumes are held in memory and disappear when the server stops. The demo has no authentication or access control for candidate records or resume downloads, no malware scanning, no persistent database, and no durable email queue. Do not use real candidate data or expose this server to the internet. Production needs authentication and role authorization, tenant isolation, encrypted storage, malware scanning, retention/deletion controls, audit logging, rate limiting, an email provider with delivery monitoring and retries, and legal review of applicant notices and declarations.
