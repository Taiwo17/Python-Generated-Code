# AutoLead CRM — Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** 20 October 2026  
**Market:** Lagos, Nigeria  
**Status:** Initial commercial specification; validate assumptions with pilot customers

> **Product promise:** Never lose track of a potential car buyer again.

## 1. Executive summary
AutoLead CRM is a mobile-friendly SaaS platform for independent used-car dealers and small-to-medium dealerships. It helps dealers capture enquiries, remember follow-ups, manage vehicle stock, track sales opportunities and understand team activity in one place.

The MVP focuses on the pain of enquiries being scattered across WhatsApp, calls, social media, contacts and notebooks—and interested buyers not receiving consistent follow-up. It is not initially a public marketplace or a full dealership ERP.

## 2. Problem and assumptions
Dealers handle enquiries across multiple channels while showing vehicles, negotiating and managing stock. Fragmented customer details and inconsistent follow-up can cause missed opportunities and poor visibility.

Assumptions to validate:
- Missed or delayed follow-up is a frequent, costly problem.
- Dealers will enter/import leads if the workflow is quick and mobile-friendly.
- Dealers will pay recurring fees for organization, follow-up and visibility.
- WhatsApp click-to-chat is useful before full platform integration.
- Independent dealers are a practical initial segment; team dealerships may require team features sooner.

## 3. Vision and positioning
**Vision:** Help car dealers turn more enquiries into organized sales opportunities.  
**Positioning:** A simple sales follow-up and inventory CRM designed around the way car dealers work.

Core value:
- Keep prospective buyers and vehicle interests searchable.
- Show who needs to be contacted today and which follow-ups are overdue.
- Continue using WhatsApp while organizing sales activity in the CRM.
- Track the journey from enquiry to inspection, negotiation and outcome.
- Provide team visibility as dealerships grow.

## 4. Goals and non-goals
### MVP goals
- Fast lead capture and search.
- Follow-up tasks with due dates and outcomes.
- WhatsApp click-to-chat with editable templates.
- Vehicle inventory and availability tracking.
- Sales pipeline and basic reporting.
- Secure multi-tenant accounts.
- Onboarding and subscription support for pilot customers.

### Out of scope initially
- Public vehicle marketplace.
- Native iOS/Android apps.
- Full WhatsApp inbox synchronization or automated campaigns.
- AI lead scoring or sales agents.
- Financing, payments between buyer and seller, accounting or escrow.
- Complex multi-branch workflows and microservices.

## 5. Target users
1. **Independent dealer/owner-operator:** needs a fast way to remember buyers, manage stock and follow up from a phone.
2. **Dealership owner/sales manager:** needs lead assignment, salesperson accountability and pipeline visibility.
3. **Salesperson:** needs assigned leads, communication history and clear next actions.

Interview both individual dealers and teams, but prioritize the segment that demonstrates the strongest pain and willingness to pay.

## 6. MVP priorities
### P0 — MVP
- Authentication, organization setup and tenant isolation.
- Lead capture, search, filters, detail and activity history.
- Follow-up task creation, due lists and completion outcomes.
- WhatsApp click-to-chat and editable message templates.
- Vehicle inventory and availability.
- Sales pipeline and won/lost outcomes.
- Basic dashboard and mobile-first UI.
- Backups, monitoring and support/admin access controls.

### P1 — Early follow-up
- CSV import/export.
- Listing copy generator.
- Team assignment and enhanced reporting.
- Automated subscription billing.

### P2 — Later
- Official WhatsApp Business Platform integration.
- Advanced analytics, multi-branch support and automated campaigns.

## 7. Functional requirements
### 7.1 Authentication and organizations
- Secure registration, login, logout and password recovery.
- Organization/dealership profile, currency and time zone.
- Owner can invite users when team features are enabled.
- Every tenant-owned record must be authorized and scoped server-side.
- Failed payment or expiry must not silently delete data.

### 7.2 Lead management
Required: display name, phone, pipeline stage and timestamps. Optional: email, source, vehicle interest, preferred make/model, budget/currency, timeline, assignee, follow-up and notes.

Lead list/detail must support search by name/phone; filters by stage, source, assignee and follow-up status; edit, archive, stage updates and activity history. Warn about duplicate phone numbers without automatically merging.

### 7.3 Pipeline
Stages: **New enquiry → Contacted → Qualified → Inspection scheduled → Inspection completed → Negotiation → Won/Lost**.

Won prompts for sale details where available. Lost prompts for a reason such as price, unavailable vehicle, chose another seller, no response, postponed or other. Pipeline stage is not a guaranteed forecast.

### 7.4 Follow-ups
- Tasks include type, due date/time, assignee, priority, status and notes.
- Types: call, WhatsApp message, inspection, send vehicle details, other.
- Status: pending, completed, cancelled.
- Views: overdue, due today, upcoming, completed.
- Store completion time, actor and outcome.
- MVP reminders can use dashboard/in-app indicators; email reminders only if configured.
- Store timestamps in UTC and display in the organization time zone.
- Reminder jobs must be retry-safe and idempotent.

### 7.5 WhatsApp
- Open the correct WhatsApp chat using a valid click-to-chat URL.
- Provide editable templates for initial response, inspection confirmation, post-viewing follow-up and availability updates.
- Record “chat opened” only as an interaction; do not claim a message was sent/delivered merely because WhatsApp opened.
- Dealer manually records outcome and next action.
- No scraping or full inbox synchronization in MVP.
- Future official integration must account for consent, opt-in, template approval, platform policy, pricing and webhook security.

### 7.6 Inventory
Vehicle fields: make, model, year, trim, asking price/currency, condition, mileage, transmission, fuel type, description, photos, stock reference, availability and timestamps.

Availability: Available, Reserved, Sold, Unavailable. Link many leads to many vehicles. Sold vehicles must not appear as available. Keep historical sale price separate from asking price. Use durable object storage for production photos.

### 7.7 Sales
Record sale date, actual sale price/currency, lead, vehicle, salesperson and notes. Prevent accidental duplicate records. Do not overwrite asking price with sale price.

### 7.8 Dashboard
Show new leads, open leads by stage, overdue/due-today tasks, inspections, negotiations, available inventory and recorded sales. Define calculations consistently, apply date filters and enforce permissions.

### 7.9 Listing generator (post-MVP)
Draft listing text from saved vehicle data for social/WhatsApp sharing. Dealer reviews before sharing. Never invent specifications or claims.

## 8. Key user journeys
1. **Capture lead:** enter minimal details, save, set next follow-up and see the lead in the pipeline.
2. **Follow up:** open due task, review/edit WhatsApp message, contact buyer, return to CRM and record outcome; task completes only after user confirms.
3. **Close sale:** move lead through inspection and negotiation, record final sale details and mark vehicle sold after confirmation.
4. **Team onboarding:** owner invites users, assigns leads and reviews permitted activity reports.

## 9. Logical data model
- **Organization:** tenant, plan, billing status, settings and time zone.
- **User:** identity, organization membership and role.
- **Lead:** contact, stage, source, assignee and timestamps.
- **Vehicle:** specs, price, availability and stock reference.
- **LeadVehicle:** many-to-many lead/vehicle link.
- **FollowUpTask:** due date, assignee, status and outcome.
- **Activity:** timeline events and actor.
- **Sale:** lead, vehicle, sale date, actual sale price and salesperson.
- **VehiclePhoto:** durable object-storage key and metadata.
- **Subscription/BillingRecord:** plan, period, provider reference and status.
- **AuditLog:** security-sensitive and administrative actions.

All tenant-owned data must be scoped to an organization. Use foreign keys, indexes, transactions and, where practical, PostgreSQL row-level security.

## 10. Proposed API
Use versioned REST endpoints under `/api/v1`:
- Auth: `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/forgot-password`
- Organization/users: `/organization`, `/users`, `/users/invitations`
- Leads: `/leads`, `/leads/{id}`, `/leads/{id}/activities`
- Follow-ups: `/follow-ups`, `/follow-ups/{id}`, `/follow-ups/{id}/complete`
- Vehicles: `/vehicles`, `/vehicles/{id}`, `/vehicles/{id}/photos`
- Sales: `/sales`, `/sales/{id}`
- Dashboard: `/dashboard/summary`, `/dashboard/pipeline`, `/dashboard/activity`
- Billing: `/billing/subscription` and provider-specific routes when enabled

Every endpoint must authenticate, authorize, validate, scope data to tenant and return predictable errors.

## 11. UX requirements
- Mobile-first responsive design.
- Minimal required fields for lead capture.
- Navigation: Dashboard, Leads, Follow-ups, Vehicles, Sales, Team (as available), Settings.
- Plain language, clear empty/loading/error states and confirmation for destructive actions.
- Accessible contrast, labels, keyboard navigation and visible focus.
- NGN formatting and configurable time zone/currency.

## 12. Pricing hypotheses
Prices are initial tests, not validated market rates.

| Plan | Proposed price | Target |
|---|---:|---|
| Starter | ₦9,900/month | Independent dealer |
| Growth | ₦24,900/month | Busy dealer/small team |
| Dealership | From ₦49,900/month | Larger team |

Validate willingness to pay through interviews and paid pilots. Manual billing may support early pilots; before self-service scale, use a payment provider and server-side verified webhooks. Define failed payment, grace period, cancellation, refund and data export policies. Never trust a client-side redirect as payment proof.

## 13. Technical architecture
- Frontend: Next.js + TypeScript.
- Backend: Node.js API using Express or NestJS.
- Database: PostgreSQL; Prisma migrations.
- Packaging: Docker/Compose.
- Hosting: VPS managed through Coolify initially; AWS optional.
- CI/CD: GitHub Actions.
- Photos: persistent object storage or S3-compatible storage.
- Operations: HTTPS, secure secrets, monitoring, structured logs, backups and restore drills.

Prefer a modular monolith. Do not store production photos or customer data on ephemeral container filesystems. Use least privilege, rate limiting, health checks, staged deployment where practical and documented migration/recovery procedures.

Initial performance target: p95 under 500 ms for common API requests under an agreed pilot load. A 99.5% availability objective is aspirational and must not be promised without operational evidence.

## 14. Security and privacy
- Enforce tenant isolation on reads/writes, searches, exports, background jobs, dashboards and file access.
- Secure authentication, sessions, password recovery and authorization.
- Validate inputs and defend against injection, XSS, CSRF where applicable and insecure direct object references.
- Encrypt traffic; protect backups and secrets.
- Minimize personal data; define retention, export, correction and deletion workflows.
- Publish privacy information and terms.
- Assess requirements under the Nigeria Data Protection Act and applicable NDPC guidance; obtain qualified advice as needed.
- Establish incident response and restrict/audit support access.

## 15. Reliability and operations
- Automated off-host database backups and tested restore procedure.
- Persistent object storage for photos.
- Monitoring for availability, errors, disk pressure and database issues.
- Deployment and incident runbooks.
- Safe migrations, health checks and recovery/rollback approach.
- Retry-safe background jobs.
- Support channel and basic onboarding guide.

## 16. Acceptance criteria
- Lead can be created, searched and accessed only within its organization.
- Cross-tenant access tests fail securely across IDs, filters, exports and APIs.
- Follow-up due/overdue views respect organization time zone.
- WhatsApp opens the correct number; no false sent/delivered status.
- Vehicle photos persist through redeployment; availability is accurate.
- Won/Lost outcomes and loss reasons are saved.
- Sale price is distinct from asking price.
- Dashboard totals match source records and respect permissions.
- Core workflows work on mobile and desktop.
- Backup restore succeeds in a test environment.
- Release can be deployed with health checks and documented recovery.

## 17. Testing
- Unit tests for validation, transitions and metrics.
- Integration tests for data access and tenant boundaries.
- End-to-end tests for lead, follow-up, inventory and sale workflows.
- Security tests for authorization and upload handling.
- Mobile usability tests with target dealers.
- Backup restore and deployment smoke tests.
- Pilot acceptance testing before general availability.

## 18. Risks and mitigations
- **Low data entry:** minimize fields, import data, observe usage.
- **Low willingness to pay:** test paid pilots before expanding scope.
- **Competition:** differentiate on follow-up execution and validate competitors’ gaps.
- **Tenant data leak:** authorization tests, least privilege and audit logs.
- **Data loss:** off-host backups, durable photo storage and restore drills.
- **WhatsApp changes/costs:** keep click-to-chat fallback; validate official API economics.
- **Payment disputes:** verified webhooks, clear terms and reconciliation.
- **Scope creep:** gate features on customer evidence.

## 19. Customer validation and go-to-market
1. Interview 10–15 independent dealers and dealership managers in Lagos.
2. Ask them to walk through recent enquiries and follow-up rather than asking only if they like the idea.
3. Document tools, lost-lead examples, team structure, inventory and current spend.
4. Demonstrate a prototype with a realistic workflow.
5. Recruit 3–5 pilot dealerships and agree on duration, usage expectations and post-pilot pricing.
6. Get permission before publishing testimonials, names, logos or performance results.

Initial channels: founder-led direct outreach, in-person demos, referrals, short demo videos and relevant dealer communities. Avoid spam.

### Suggested 90-day roadmap
| Period | Focus | Exit evidence |
|---|---|---|
| Weeks 1–2 | Interviews and research | Repeated problem pattern and pilot prospects |
| Weeks 3–4 | Prototype and pricing tests | Workflow understood and willingness-to-pay evidence |
| Weeks 5–7 | Build P0 MVP | Core workflows and security tests pass |
| Weeks 8–9 | Pilot onboarding | Real leads and follow-ups are used |
| Weeks 10–11 | Improve and charge | First paying customers and repeat usage |
| Week 12 | Review and decide | Evidence-based next iteration |

## 20. Open decisions
- Which segment shows strongest urgency and willingness to pay?
- What lead/vehicle limits should each plan have?
- Are email reminders needed in MVP?
- Are team invitations/roles needed for the first paid release?
- Which payment provider fits the business?
- What privacy, retention and support terms apply?
- What onboarding/import assistance is needed?
- Confirm name and domain availability before public launch.

## 21. MVP definition of done
- P0 requirements implemented and acceptance-tested.
- Tenant isolation tested beyond happy paths.
- HTTPS, secrets, monitoring and off-host backups configured.
- Database restore successfully tested.
- Core mobile workflows work with real dealer scenarios.
- Pilot onboarding completed or unmet targets documented.
- Support contact and onboarding guide available.
- Pricing/terms clear and no unsupported claims about message delivery or sales uplift.

## Appendix A — Suggested navigation
Dashboard; Leads; Follow-ups; Vehicles; Sales; Team (plan-dependent); Settings.

## Appendix B — Product principles
- Sell business outcomes, not a feature checklist.
- Make the next action obvious.
- Work with WhatsApp habits rather than forcing a new channel.
- Never claim message delivery or sales uplift without evidence.
- Keep tenant data isolated.
- Prefer validated needs over assumptions.
- Keep the first release simple, secure and recoverable.
