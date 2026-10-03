# Application flow local demo

Start the Python API and static file server from the repository root:

```powershell
python application-flow/server.py
```

Open the candidate form at [http://127.0.0.1:8000/application-flow/candidate-application.html](http://127.0.0.1:8000/application-flow/candidate-application.html).

The API includes `GET /api/health`, `GET /api/applications`, `POST /api/applications`, `PATCH /api/applications/{id}`, and `GET /api/resumes/{id}`. The application form collects candidate contact details, qualifications, skills, experience, job-related eligibility and declarations, plus a resume upload. PDF, DOC, and DOCX files up to 5 MB are accepted.

This is a local prototype. Application records and resume files are held in memory and disappear when the server stops. The demo has no authentication or access control for candidate records or resume downloads, no malware scanning, and no persistent database. Do not use real candidate data or expose it to the internet. Production needs authentication and authorization, tenant isolation, durable encrypted storage, malware scanning, retention controls, audit logging, and legal review of applicant notices and declarations.
