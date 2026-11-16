# Epic — E0 · Discovery and project baseline

## Business objective

**AS** the team responsible for the chatbot
**I NEED** a verified baseline of the existing applications, data, agreement and local development environment
**SO THAT** implementation planning starts from the discovery already performed and does not duplicate completed preparatory work

## Context and rationale

The `Discovery Sprint` in Milano contains three preparatory tasks covering repository context, project-scope documentation and local kick-off setup. The discovery report v1.0 consolidates the resulting analysis and remains explicit about product decisions and Firebase or Google Cloud evidence that are still pending.

## Expected value and success measures

- The two mobile repositories and their relevant technical context are analysed and documented.
- The signed scope, exclusions, delivery plan, proposed architecture, risks and open questions are consolidated in the discovery report.
- The local discovery environment and client workspace structure are prepared for review of both applications.
- Milano workflow state is preserved: all three replicated tasks remain `in_review`.

## Scope

Included:
- Repository access and technical analysis of the iOS and Android applications.
- Analysis of Firebase integration, authentication and the current Firestore data model from the application code.
- Documentation of the signed project scope, exclusions, plan and conditions.
- Preliminary architecture, risks and open discovery questions.
- Local kick-off setup and application build preparation.

Excluded:
- Product implementation.
- Remediation of legacy systems outside the chatbot scope.
- Closure of decisions that require client approval or Firebase and Google Cloud console evidence.
- Visual design and mobile navigation.

## Included tasks

- [F43425 — Repository context](TASK-01-repository-context.md).
- [F43428 — Document project scope](TASK-02-document-project-scope.md).
- [F4342C — Initial setup and local kick-off](TASK-03-local-kickoff-setup.md).

## Risks and dependencies

- Late or incomplete Firebase and Google Cloud access — high impact.
- An unvalidated query catalogue or unresolved product decisions — high impact.
- No separate development environment — high impact.
- Milano contains no detailed acceptance evidence for the local builds — medium impact.

## Milestone

- Discovery scope reviewed — 10 November 2026.

## Open decisions after discovery

- A separate Firebase development project is preferred but remains unconfirmed; this blocks assumptions in E1, E2, E3 and E6.
- The binding catalogue of 15–25 representative questions and actions still requires validation; it remains a dependency of E1, E2, E3 and E6.
- Availability, usage limits, languages, health-record fields, retention, provider selection and deployment interaction style remain open decisions recorded by the discovery report.

## Links

- [Technical roadmap](../../ROADMAP.md).
- Local operational context.
- Discovery report v1.0.
