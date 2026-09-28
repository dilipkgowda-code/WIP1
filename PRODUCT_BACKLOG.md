# Product backlog — Sprint 0 draft

**Status:** Initial, unrefined draft for Product Owner review  
**Product:** WIP — workforce intelligence platform  
**Sprint:** 0 (discovery and backlog refinement; Sprint 1 has not been planned)

## Product vision

As an end user, I want one workforce platform that helps my organization hire, train, develop, and retain people, so that we can close skill and behavior gaps and improve workforce outcomes.

The product concept combines recruitment assessment, learning management, and behavioral assessment/coaching. It should connect business goals to required competencies, assessment, learning recommendations, practice, coaching, feedback, behavior change, performance measurement, and continuous improvement.

## Backlog rules for this draft

- Priority is provisional and describes likely value/order for discovery; it is not a Sprint 1 commitment.
- Story points, delivery dates, and technical designs remain unset until refinement.
- “Fintech” is the first sample customer context used in the current screens. Confirm whether it is also the first target pilot segment.
- The current HTML screens are interaction prototypes. They do not establish production security, persistence, or working integrations.
- “AI” items are product hypotheses. Do not present them as committed functionality until their value, data needs, explainability, and human review have been agreed.

## Ordered product backlog

### P0 — Establish a secure customer workspace

**WIP-001 · Customer workspace and domain provisioning**  
As a customer administrator, I want a secure workspace under my organization’s dedicated domain, so that employees recognize and trust the service.

Acceptance criteria:
- An authorized operator can create, configure, suspend, and restore a customer workspace.
- The customer’s approved domain is verified before it is activated.
- A user in one customer workspace cannot access another customer’s records.
- Domain, workspace owner, lifecycle state, and provisioning events are recorded.
- The deployment and support cost of per-customer domains is measurable.

**WIP-002 · Sign-in, identity, and access roles**  
As a customer user, I want to sign in securely and see only the tools allowed for my role.

Acceptance criteria:
- Supported roles and permissions are documented for customer admin, hirer, candidate/learner, trainer, assessor, and platform operator.
- A customer admin can invite, disable, and reactivate users and assign permitted roles.
- Sign-in, sign-out, session expiry, and account recovery have agreed behavior.
- Privileged changes are auditable; authorization is enforced by the backend, not only by the interface.
- Authentication configuration can support the agreed customer identity provider requirements.

### P0 — Configure and run hiring

**WIP-003 · Manage departments and hiring roles**  
As a hirer or admin, I want to create, edit, enable, and disable roles, so that open positions reflect current hiring needs.

Acceptance criteria:
- A role records department, title, experience level, key skills, and expertise.
- Authorized admins can create and edit roles and enable or disable them.
- Disabled roles are retained for history and are not offered as open roles.
- Hirers can search and filter roles by department, status, and relevant role details.
- Changes are saved persistently and the role list reflects them after reload.

**WIP-004 · Candidate application and hiring workflow**  
As a candidate, I want to view an enabled role and submit an application, so that I can be considered for a suitable position.

Acceptance criteria:
- Candidates can view role details and submit the agreed profile/application fields.
- The workflow confirms receipt and shows the candidate’s current application stage.
- Hirers can find applications for their authorized roles and update the stage.
- Candidates cannot view other candidates’ private information.
- Required data, retention rules, and candidate consent wording are agreed before implementation.

**WIP-005 · Recruitment assessment**  
As a hiring team member, I want role-relevant assessments and review evidence, so that decisions use consistent, job-related criteria.

Acceptance criteria:
- An authorized user can associate an assessment with a role and define its competency criteria.
- Candidates receive clear instructions and can complete an assigned assessment.
- Reviewers can see the submitted evidence and record a structured evaluation.
- Assessment criteria and reviewer actions are traceable.
- Any automated scoring or ranking is explainable, reviewable by a person, and separately approved before use.

### P0 — Onboard and build role skills

**WIP-006 · Candidate/learner learning dashboard**  
As a learner, I want to see assigned, in-progress, and completed learning with clear progress, so that I know what to do next.

Acceptance criteria:
- The dashboard shows assigned items, completed items, and progress.
- Learners can open an assigned module and record completion.
- Progress remains available across sessions and devices.
- The learner can navigate onboarding, job learning, the library, and questions.

**WIP-007 · Onboarding pathway**  
As a new joiner, I want a guided onboarding path, so that I can learn how the organization works and connect with people across teams.

Acceptance criteria:
- The pathway can include onboarding, cultural orientation, buddy allotment, and inter-department orientation.
- An authorized trainer/admin can assign and update onboarding items.
- The learner can see the owner, due date (if configured), status, and next action for each item.
- Completion and changes are recorded for the learner and authorized administrators.

**WIP-008 · Trainer-managed job learning**  
As a trainer, I want to publish role-specific learning modules, so that employees receive relevant training for their department and role.

Acceptance criteria:
- An authorized trainer can create, edit, assign, and retire a module.
- A module has a title, description, audience, content, and completion rule.
- Learners see only modules assigned to them or made available to their audience.
- Changes to assignments and completion are recorded.

**WIP-009 · Learning library and moderated contributions**  
As a learner, I want to find useful video and PDF resources and suggest new material, so that learning can continue beyond assigned modules.

Acceptance criteria:
- Learners can browse and filter approved resources by topic and format.
- A learner can submit supported content with title and topic metadata.
- A designated reviewer can approve or reject a submission and record the decision.
- Only approved submissions are available in the shared library.
- File type, size, access, malware scanning, and retention rules are agreed for production uploads.

**WIP-010 · Learning questions and support**  
As a learner, I want to ask a question about learning or onboarding and receive a response, so that I can resolve blockers.

Acceptance criteria:
- A learner can submit a question with a topic and see its response status.
- An authorized trainer or support user can respond and close the question.
- The learner can see the response; access to other learners’ questions follows agreed policy.
- Notifications and service expectations are defined during refinement.

### P0 — Develop people and measure value

**WIP-011 · Competency and skill-gap view**  
As a manager or HR partner, I want to compare required competencies with available evidence, so that I can identify development needs.

Acceptance criteria:
- Competency frameworks can be associated with roles or teams.
- The system distinguishes assessed evidence from inferred or self-reported information.
- A user with permission can see skill gaps and the evidence behind them.
- A gap can lead to a recommended learning or coaching action, with human confirmation.

**WIP-012 · Coaching and behavioral development**  
As an employee, I want structured feedback, practice, and coaching actions, so that I can build effective workplace behaviors over time.

Acceptance criteria:
- An authorized coach can create a development plan with goals, practice actions, and follow-up dates.
- The employee can review feedback and record progress.
- Access to sensitive feedback is limited to agreed participants and can be audited.
- Coaching uses the agreed Plutchik-inspired visual palette: admiration and trust; learning uses trust and anticipation.
- The product avoids presenting behavioral results as clinical diagnoses.

**WIP-013 · Workforce outcomes and learning impact**  
As an HR leader, I want to compare workforce development activity with business outcomes, so that I can decide what to improve.

Acceptance criteria:
- Authorized users can view agreed measures for learning, assessment, and workforce outcomes.
- Metric definitions, data sources, reporting periods, and access rules are documented.
- Where data is unavailable, the dashboard identifies the gap rather than implying a causal result.
- Exports and aggregate reporting follow tenant permissions and privacy rules.

### P1 — Expand workforce planning

**WIP-014 · Career pathways and internal opportunities**  
As an employee, I want to understand possible next roles and the skills needed, so that I can plan my development.

Acceptance criteria:
- Authorized admins can define role pathways and required competencies.
- Employees can view pathways available to them and compare their current evidence with requirements.
- The system does not promise promotion or make employment decisions automatically.

**WIP-015 · Retention and engagement insights**  
As an HR leader, I want privacy-aware engagement and retention signals, so that I can identify where support may be needed.

Acceptance criteria:
- The organization approves which data may be used and the minimum group sizes for reporting.
- Reports show aggregated trends with definitions and limitations.
- Individual-level signals are not exposed without explicit policy, permissions, and review.
- Predictive attrition functionality remains out of scope until validated with representative data and approved safeguards.

### P1 — Connect customer systems

**WIP-016 · Customer HR and talent system integration**  
As a customer administrator, I want approved workforce data to flow from my existing systems, so that users do not have to maintain duplicate records.

Acceptance criteria:
- The first integration is selected from validated pilot-customer needs.
- Data fields, direction, frequency, failure handling, and ownership are documented.
- Admins can monitor integration status and resolve or escalate errors.
- Integration access is tenant-scoped, least-privileged, and auditable.

### P2 — Explore AI-supported work

**WIP-017 · AI-assisted recommendations and screening (discovery first)**  
As an HR professional, I want relevant skill and learning recommendations, so that I can focus attention on useful next steps.

Acceptance criteria:
- Discovery identifies the user problem, success measure, data source, and fallback before implementation.
- Recommendations show the evidence and allow a person to accept, change, or dismiss them.
- The system does not automatically reject or make employment decisions.
- Privacy, bias, explainability, and applicable legal requirements are reviewed before any pilot.

## Sprint 0 refinement topics

Resolve these with the Product Owner before selecting Sprint 1 work:

1. **First release audience:** Is fintech the first pilot customer, or only the example used for the prototype?
2. **First end-to-end outcome:** Should the first usable release prove hiring assessment, new-hire onboarding, or one journey connecting hiring to learning?
3. **Customer tenancy:** Does “dedicated secure domain” mean a customer-specific subdomain, customer-owned domain, isolated deployment, or a combination? Which are included in the premium tier?
4. **First user roles:** Which roles must work in the first release, and who may see candidate results, learning records, and coaching feedback?
5. **Assessment scope:** Which candidate and employee competencies or behavioral assessments are required first, and who authors/validates them?
6. **Learning content:** Who supplies initial content, what file formats and sizes are needed, and who can approve material?
7. **System integrations:** What HRMS/ATS/LMS is used by the intended pilot customer, if known?
8. **Measures of success:** What observable result would make the pilot valuable to the customer?
9. **Hosting and service expectations:** What data residency, availability, recovery, support, and security requirements must be met for the pilot?
10. **AI boundary:** Which AI ideas should remain discovery-only until customer evidence and safeguards are available?

## Ready for Sprint 1 checklist (proposed)

A backlog item can be considered for Sprint 1 after the Product Owner and development team agree on its user outcome, acceptance criteria, dependencies, data/privacy implications, and how it will be verified. The Sprint Goal, selected items, and estimates will be recorded only after refinement.

## Source context

- `LEAPOne Workforce Intelligence System.pptx`: Hire, Train, Develop, Retain; recruitment assessment, learning management, and behavioral development; continuous improvement and business impact.
- `Workforce intelligence platform.docx`: connect business goals to competencies, assessment, learning recommendation, practice, coaching, feedback, behavior change, performance measurement, and business impact.
- Prior product discussions: fintech sample customer, role administration, candidate/assessor learning spaces, onboarding, buddy and inter-department orientation, voluntary learning, approved video/PDF library, progress, questions, dedicated customer domain, and the Plutchik-inspired theme choices.
