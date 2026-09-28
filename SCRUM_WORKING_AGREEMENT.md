# Scrum working agreement

**Product:** WIP workforce intelligence platform  
**Participants:** Dilip — Product Owner and Scrum Master; Codex — development team and technical collaborator  
**Current phase:** Sprint 0 — product discovery and backlog refinement

## Cadence

- **Sprint length:** One week.
- **Sprint Planning:** Up to two hours. Refine the goal and backlog items, agree acceptance criteria, dependencies, and verification, then record the selected work in GitHub.
- **Daily Scrum:** A short daily check-in focused on progress toward the Sprint Goal, next work, and blockers. We will do it interactively when Dilip checks in; Codex cannot initiate a message or GitHub update on its own between conversations.
- **Sprint Review:** Up to one hour, or shorter/longer as the work needs. Demonstrate the increment and get feedback from Dilip acting as Product Owner and, when useful, proxy end user.
- **Retrospective:** Interactive. Discuss what helped, what slowed us down, and one or two concrete changes to try in the next sprint. Record the agreed actions in GitHub.

## GitHub as the work record

- `PRODUCT_BACKLOG.md` is the ordered product backlog and stays a draft until refined with the Product Owner.
- Sprint goals, selected backlog items, decisions, and retrospective actions will be recorded in repository markdown and commits.
- Sprint 1 will not be planned until the application-portal scope and its acceptance criteria are refined together.
- The `source-code/` folder is a frozen snapshot and must not be edited or regenerated unless Dilip explicitly asks for it. Active code work stays in the project files outside that folder.

## Working definition of done

An item is done when the agreed acceptance criteria are met, the change is integrated in the active project files, relevant checks requested for that work pass, and the Product Owner can inspect the result. Known prototype limitations or deferred work are recorded alongside it. A UI-only prototype is not described as production-ready functionality.
