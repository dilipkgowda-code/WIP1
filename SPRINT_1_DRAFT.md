# Sprint 1 — application portal draft

**Status:** Draft for backlog refinement; not a Sprint commitment  
**Sprint length:** One week (per the Scrum working agreement)  
**Product Owner:** Dilip  
**Sprint Goal:** TBD after refinement

## User story

As a hirer, I want to publish jobs to a candidate-facing application portal, find applicants using Boolean skill searches, track applications, schedule interviews, record results, and automatically notify candidates about important updates, so that my team can manage hiring transparently from one workspace.

## Acceptance criteria to refine

1. **Post a job:** An authorized hirer can create, edit, publish, and close a job with the agreed role details, department, experience level, skills, expertise, and application fields.
2. **Candidate application:** A candidate can open the published job page, submit the required application information, and receive confirmation. The candidate can access only their own application information.
3. **Boolean skill search:** An authorized hirer can search applicant skills using the agreed Boolean syntax (proposed: `AND`, `OR`, `NOT`, parentheses, and quoted phrases). Results show the criteria that matched and only include applicants the hirer is authorized to view.
4. **Application tracking:** The hirer can view the applicants for a job and move each application through an agreed workflow. The candidate receives an automatic update when a configured stage change occurs.
5. **Interview scheduling:** The hirer can set, change, or cancel an interview with date, time zone, format/location or meeting link, and interview participants. The candidate receives the corresponding message.
6. **Interview results:** An authorized interviewer can record structured feedback and an outcome. Access to interviewer notes follows an agreed permission rule. The candidate receives an outcome message only for outcomes approved for communication.
7. **Automatic messages:** Messages use approved templates and a channel agreed with the customer. The system records delivery status or failure and lets an authorized user retry or otherwise follow up.
8. **Data protection:** Candidate notice/consent, access permissions, retention/deletion, and handling of CVs or other attachments are agreed before collecting real candidate data.

## Proposed story slices for refinement

This is one broad outcome and may be too large for a one-week sprint. Refine it into demonstrable vertical slices before Sprint Planning:

- Hirer publishes an enabled job and receives a shareable application page.
- Candidate applies; the hirer sees the application and the candidate receives confirmation.
- Hirer tracks an application and searches skills using the selected Boolean behavior.
- Hirer schedules an interview, records feedback/result, and the candidate receives configured updates.

The Product Owner and development team should select a coherent slice that can be completed, demonstrated, and verified in the week. No estimates or Sprint 1 commitment have been made.

## Open refinement decisions

- Which fields are required on the job and candidate application form? Are CV/file uploads needed in the first slice?
- What Boolean syntax and skill normalization are expected? Are searches exact matches, synonyms, or both?
- What are the application stages, and which stage changes should message candidates?
- Should the first candidate messages be in-portal, email, SMS, or a combination? What consent is required?
- Who can see interviewer notes and candidate outcomes? Which outcomes can be sent automatically?
- Is the portal only WIP-hosted for the first slice, with external job-board integrations deferred?
- Which tenant and persistence/security assumptions must be implemented before real candidate data is used?

## Definition of done for this draft

This document is ready for Sprint Planning only after the Product Owner confirms the user value, the smallest scope, acceptance criteria, and data/message policies, and the development team agrees on dependencies and verification. Until then, it remains a planning draft.
