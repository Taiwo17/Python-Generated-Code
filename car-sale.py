from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path



out = Path(__file__).resolve().parent
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.7)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.8)
sec.right_margin = Inches(0.8)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(9.5)
for s in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
    styles[s].font.name = "Aptos Display"
styles["Title"].font.size = Pt(28)
styles["Title"].font.bold = True
styles["Heading 1"].font.size = Pt(17)
styles["Heading 2"].font.size = Pt(12.5)
styles["Heading 3"].font.size = Pt(10.5)

def shade(cell, fill="EAF0F6"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def add_bullet(text, level=0):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p

def add_num(text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p

def add_table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Light Shading Accent 1"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        shade(c, "D9E7F5")
        for r in c.paragraphs[0].runs:
            r.bold = True
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            for p in cells[i].paragraphs:
                p.paragraph_format.space_after = Pt(1)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t

# Cover
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\n")
title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.add_run("AutoLead CRM")
subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = subtitle.add_run("Product Requirements Document (PRD)")
r.bold = True
r.font.size = Pt(16)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Commercial SaaS for independent car dealers and dealerships\n")
p.add_run("Initial market: Lagos, Nigeria | Version 1.0 | 20 October 2026")
doc.add_paragraph("\n")
call = doc.add_paragraph()
call.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = call.add_run("Product promise: Never lose track of a potential car buyer again.")
rr.italic = True
rr.font.size = Pt(12)
doc.add_page_break()

doc.add_heading("Document Control", level=1)
add_table(["Field", "Details"], [
    ("Product", "AutoLead CRM"),
    ("Document", "Product Requirements Document"),
    ("Version / status", "1.0 — Initial commercial product specification; validate assumptions with pilot customers"),
    ("Product owner", "Founder / Product Owner"),
    ("Primary market", "Lagos, Nigeria, with potential expansion to other Nigerian and African markets"),
    ("Primary users", "Independent car dealers, dealership owners/managers, salespeople"),
    ("Business model", "Subscription SaaS, priced in Nigerian naira (NGN)"),
    ("Deployment approach", "Web application, initially deployable on a VPS using Coolify; AWS is optional, not a launch requirement"),
])
doc.add_heading("1. Executive Summary", level=1)
doc.add_paragraph(
    "AutoLead CRM is a mobile-friendly customer and sales management platform for independent used-car dealers "
    "and small-to-medium dealerships. It helps dealers capture enquiries, remember follow-ups, manage vehicle stock, "
    "track sales opportunities and understand team activity in one place."
)
doc.add_paragraph(
    "The initial commercial focus is not to build a general-purpose dealership ERP or a vehicle marketplace. "
    "It is to solve the narrow, high-value problem of enquiries being scattered across WhatsApp, calls, social media, "
    "contacts and notebooks—and interested buyers not receiving consistent follow-up."
)
doc.add_paragraph(
    "The MVP will combine lead management, follow-up tasks, WhatsApp click-to-chat, vehicle inventory, a simple sales "
    "pipeline, basic reporting and secure multi-tenant accounts. Early success will be measured by repeat usage, "
    "completed follow-ups, customer retention and willingness to pay, not by the number of features shipped."
)

doc.add_heading("2. Problem Statement", level=1)
doc.add_paragraph(
    "Dealers frequently handle many enquiries across different channels while simultaneously showing vehicles, "
    "negotiating prices and managing stock. Customer details and conversation history can become fragmented. "
    "Follow-ups may be forgotten, team leads may not know which salesperson owns a prospect, and managers may lack "
    "a clear view of the pipeline. AutoLead CRM should reduce this operational friction without requiring dealers "
    "to abandon WhatsApp."
)
doc.add_heading("2.1 Assumptions to validate", level=2)
for x in [
    "Missed or delayed follow-up is a sufficiently painful and frequent problem for the target segment.",
    "Dealers will consistently enter or import leads if the workflow is quick and mobile-friendly.",
    "Dealers are willing to pay a recurring subscription for better follow-up, organization and visibility.",
    "A simple WhatsApp-assisted workflow is useful before full WhatsApp Business Platform integration.",
    "Independent dealers are an effective initial segment; small dealerships may require team features earlier.",
]:
    add_bullet(x)

doc.add_heading("3. Product Vision and Positioning", level=1)
doc.add_paragraph("Vision: Help car dealers turn more enquiries into organized sales opportunities.")
doc.add_paragraph("Positioning: A simple sales follow-up and inventory CRM designed around the way car dealers work.")
doc.add_heading("3.1 Core value proposition", level=2)
for x in [
    "Keep every prospective buyer and their vehicle interest in one searchable record.",
    "Know who needs to be contacted today and which follow-ups are overdue.",
    "Continue using WhatsApp while keeping sales activity and next actions organized in AutoLead CRM.",
    "Track the journey from enquiry to inspection, negotiation and a recorded outcome.",
    "Give dealership owners visibility into team activity and pipeline performance as they grow.",
]:
    add_bullet(x)

doc.add_heading("4. Goals, Non-Goals and Success Metrics", level=1)
doc.add_heading("4.1 MVP goals", level=2)
for x in [
    "Let a dealer create or capture a lead quickly and find it again.",
    "Make the next follow-up action and due date visible.",
    "Enable WhatsApp-assisted contact without falsely claiming a message was sent or delivered.",
    "Track a dealer's vehicle inventory and link prospects to vehicles.",
    "Support multiple users within a dealership with organization-level data isolation.",
    "Enable a founder to onboard pilot customers, understand usage and charge for subscriptions.",
]:
    add_bullet(x)
doc.add_heading("4.2 Non-goals for MVP", level=2)
for x in [
    "Public vehicle marketplace or classified-ad platform.",
    "Native iOS or Android apps; the MVP is a responsive web application.",
    "Full WhatsApp inbox synchronization, automated outbound campaigns or delivery webhooks.",
    "AI lead scoring, AI sales agents or automated vehicle valuation.",
    "Vehicle financing, payment processing between buyers and sellers, accounting or escrow.",
    "Complex multi-branch enterprise workflows and custom reporting.",
    "Microservices architecture or a cloud design chosen mainly to demonstrate DevOps skills.",
]:
    add_bullet(x)
doc.add_heading("4.3 Initial success metrics", level=2)
add_table(["Metric", "Definition / initial target", "Why it matters"], [
    ("Dealer activation", "A new dealer records at least 5 leads and 3 vehicles within 7 days of onboarding (hypothesis)", "Indicates initial setup and value discovery"),
    ("Lead capture speed", "Median time to add a lead under 30 seconds for a simple record (target)", "Reduces friction"),
    ("Follow-up completion", "Share of due follow-up tasks marked completed; establish baseline during pilot", "Measures use of the core workflow"),
    ("Weekly active dealerships", "Organizations with meaningful activity in a 7-day period", "Measures repeat usage"),
    ("Pilot conversion", "Aim for 3–5 pilot users and at least 2–3 paying customers; validate rather than assume", "Tests willingness to pay"),
    ("Retention", "Track active and paying organizations at 30, 60 and 90 days", "Tests sustained value"),
    ("Business outcomes", "Track inspections, negotiations and recorded wins; do not claim uplift without baseline comparison", "Connects usage to dealer value"),
])

doc.add_heading("5. Target Users and Personas", level=1)
doc.add_heading("5.1 Primary: Independent dealer / owner-operator", level=2)
doc.add_paragraph("Owns or manages a small inventory and handles most sales personally. Needs a quick, low-friction way to remember buyers, manage stock and follow up from a phone.")
doc.add_paragraph("Primary jobs: capture enquiries; remember buyer preferences; arrange inspections; know vehicle availability; avoid forgetting serious prospects.")
doc.add_heading("5.2 Secondary: Dealership owner or sales manager", level=2)
doc.add_paragraph("Oversees several salespeople and wants visibility into assigned leads, follow-up discipline, pipeline stages and sales outcomes.")
doc.add_heading("5.3 Secondary: Salesperson", level=2)
doc.add_paragraph("Needs to see assigned leads, record conversations and next actions, and keep vehicle and customer details accessible.")
doc.add_heading("5.4 Initial segment strategy", level=2)
doc.add_paragraph(
    "Interview both independent dealers and established dealerships, but optimize the first release for the simplest workflow "
    "that produces paid adoption. Independent dealers are the proposed starting segment because the buyer and decision-maker "
    "are often the same person. Validate this assumption through interviews."
)

doc.add_heading("6. Product Scope and Prioritization", level=1)
add_table(["Priority", "Capability", "Release"], [
    ("P0 — Must have", "Authentication, organization setup and tenant isolation", "MVP"),
    ("P0 — Must have", "Lead capture, search, filters, detail and activity history", "MVP"),
    ("P0 — Must have", "Follow-up task creation, due lists and completion outcomes", "MVP"),
    ("P0 — Must have", "WhatsApp click-to-chat with editable message templates", "MVP"),
    ("P0 — Must have", "Vehicle inventory and availability status", "MVP"),
    ("P0 — Must have", "Sales pipeline and won/lost outcome", "MVP"),
    ("P0 — Must have", "Basic dashboard and responsive mobile UX", "MVP"),
    ("P0 — Must have", "Admin/support access controls, backups and audit-relevant events", "MVP"),
    ("P1 — Should have", "CSV import/export for leads and vehicles", "After core validation / early MVP if practical"),
    ("P1 — Should have", "Listing copy generator for WhatsApp/social sharing", "Post-MVP"),
    ("P1 — Should have", "Salesperson assignment, team reports and role permissions", "Early team plan"),
    ("P1 — Should have", "Subscription checkout and billing-state automation", "Before self-serve scale; manual invoicing can support first pilots"),
    ("P2 — Later", "Official WhatsApp Business Platform integration", "After demand and cost validation"),
    ("P2 — Later", "Advanced analytics, multi-branch support, automated campaigns", "Based on paying-customer evidence"),
])

doc.add_heading("7. Functional Requirements", level=1)
doc.add_heading("7.1 Authentication and organization setup", level=2)
for x in [
    "Users can register, sign in and sign out securely.",
    "A new customer can create an organization/dealership and configure its display name, contact details, currency and local time zone.",
    "The first user becomes organization owner; the owner can invite additional users when team functionality is enabled.",
    "Users can reset forgotten passwords through a verified recovery process.",
    "All organization-owned records must be scoped to the authenticated organization and checked on the server.",
    "Suspended or expired subscriptions may be restricted according to a clearly defined policy; data must not be silently deleted because a payment fails.",
]:
    add_bullet(x)
doc.add_heading("7.2 Lead management", level=2)
doc.add_paragraph("A lead represents a person or organization that may buy a vehicle. Required fields should be minimal to support fast capture.")
add_table(["Field", "Requirement"], [
    ("Full name or display name", "Required"),
    ("Phone number", "Required; store normalized form where feasible and display user-friendly format"),
    ("Email", "Optional"),
    ("Lead source", "Optional enum: WhatsApp, phone call, Instagram, Facebook, website, referral, walk-in, other"),
    ("Vehicle interest", "Optional link to one or more inventory vehicles; allow free-text interest if stock item is not yet created"),
    ("Preferred make/model", "Optional"),
    ("Budget and currency", "Optional; use a numeric amount and currency code"),
    ("Purchase timeline", "Optional: urgent, within 30 days, later, unknown"),
    ("Assigned user", "Optional for solo plan; required or configurable for team plan"),
    ("Pipeline stage", "Required, default New enquiry"),
    ("Next follow-up", "Optional date/time; prominently prompt for a next action"),
    ("Notes", "Optional; avoid storing unnecessary sensitive information"),
    ("Created/updated timestamps", "System-generated"),
])
doc.add_heading("Lead list and detail requirements", level=3)
for x in [
    "List leads with name, phone, vehicle interest, stage, owner and next follow-up date.",
    "Search by name or phone; filter by stage, source, assignee and follow-up status.",
    "Open a lead detail page showing contact details, linked vehicles, notes, activity history and upcoming tasks.",
    "Allow authorized users to edit a lead, update its stage, add notes and archive or mark it inactive.",
    "Warn about likely duplicate phone numbers within the same organization; do not merge records without user confirmation.",
    "Record meaningful changes and activities with timestamps and actor where feasible.",
]:
    add_bullet(x)

doc.add_heading("7.3 Sales pipeline", level=2)
add_table(["Stage", "Meaning / transition guidance"], [
    ("New enquiry", "A new prospective buyer has been recorded."),
    ("Contacted", "Dealer has attempted or made contact; outcome should be recorded where possible."),
    ("Qualified", "Dealer believes the buyer has a plausible need, budget and timeline."),
    ("Inspection scheduled", "An inspection or viewing has a planned date/time."),
    ("Inspection completed", "Viewing occurred; dealer records the result and next action."),
    ("Negotiation", "Price, terms or purchase decision are being discussed."),
    ("Won", "A sale is recorded and linked to the relevant vehicle where applicable."),
    ("Lost", "Opportunity is closed without a sale; capture a loss reason when known."),
])
doc.add_paragraph("Users can move a lead between stages. A transition to Won should prompt for sale details where available. A transition to Lost should prompt for a reason such as price, vehicle unavailable, chose another seller, no response, postponed or other. Pipeline stages are organization-scoped and must not be interpreted as guaranteed sales forecasts.")

doc.add_heading("7.4 Follow-up tasks and reminders", level=2)
for x in [
    "Create a task linked to a lead, with title/type, due date/time, assignee, priority, status and optional notes.",
    "Task types may include call, WhatsApp message, inspection, send vehicle details and other.",
    "Task status: pending, completed, cancelled. Store completion time, completing user and outcome.",
    "Provide views for overdue, due today, upcoming and completed tasks.",
    "Show the next follow-up clearly on the dashboard and lead detail.",
    "Allow rescheduling and completing a task with an outcome note.",
    "MVP reminder delivery: in-app task lists and dashboard indicators; email reminders may be enabled if configured. Do not promise push notifications until implemented.",
    "Use a configured organization time zone for display and scheduling; persist timestamps in UTC.",
    "Avoid duplicate reminders and make reminder scheduling idempotent.",
]:
    add_bullet(x)

doc.add_heading("7.5 WhatsApp-assisted communication", level=2)
for x in [
    "Provide a WhatsApp action on a lead that opens a chat with the correct phone number using a valid click-to-chat URL.",
    "Offer editable message templates such as initial response, inspection confirmation, follow-up after viewing and availability update.",
    "Allow users to review and edit the message before switching to WhatsApp.",
    "Record an activity such as 'WhatsApp chat opened' only if the product can reliably detect the click; do not label it as sent or delivered.",
    "Users can manually record the communication outcome after returning to the CRM.",
    "Do not scrape, automate or synchronize private WhatsApp conversations in the MVP.",
    "Any future official WhatsApp integration must account for consent, opt-in, template approval, applicable platform policies, pricing, webhook security and delivery states.",
]:
    add_bullet(x)

doc.add_heading("7.6 Vehicle inventory", level=2)
add_table(["Field", "Requirement"], [
    ("Make, model and year", "Required for a normal vehicle record"),
    ("Trim/variant", "Optional"),
    ("Asking price and currency", "Required; validate non-negative value"),
    ("Condition", "Used, new, or other agreed controlled value"),
    ("Mileage", "Optional numeric value with unit"),
    ("Transmission and fuel type", "Optional controlled values"),
    ("Description", "Optional"),
    ("Photos", "Multiple images; validate type/size and use durable object storage in production"),
    ("Stock/reference number", "Optional; unique within organization if provided"),
    ("Availability", "Available, Reserved, Sold, Unavailable"),
    ("Date added and timestamps", "System-generated"),
])
for x in [
    "Create, edit, view, search and filter inventory.",
    "Display vehicle availability clearly; sold or unavailable vehicles should not be presented as available.",
    "Link one lead to multiple vehicles and one vehicle to multiple interested leads.",
    "When a vehicle is marked Sold, prompt for confirmation and sale details; do not automatically close every linked lead.",
    "Retain historical sale price separately from current asking price.",
    "Ensure photo storage persists across application container restarts and redeployments.",
]:
    add_bullet(x)

doc.add_heading("7.7 Sales recording", level=2)
for x in [
    "Record a completed sale against a lead and vehicle when applicable.",
    "Capture sale date, actual sale price, currency, responsible salesperson and optional notes.",
    "Do not overwrite the vehicle's original asking price with the final sale price.",
    "Prevent accidental duplicate sale records or provide a clear correction workflow.",
    "Allow authorized users to view a list of recorded sales and simple totals for a selected period.",
]:
    add_bullet(x)

doc.add_heading("7.8 Dashboard and reporting", level=2)
for x in [
    "Display new leads for the selected period, open leads by stage, overdue follow-ups, tasks due today, scheduled inspections, active negotiations, available vehicles and recorded sales.",
    "Provide date filters where relevant.",
    "Allow filtering by salesperson for authorized managers in team plans.",
    "Define every metric consistently and document the calculation; do not mix asking prices with realized sales revenue.",
    "Use organization-scoped queries and apply the same authorization checks as other endpoints.",
]:
    add_bullet(x)

doc.add_heading("7.9 Listing content generation (post-MVP)", level=2)
doc.add_paragraph(
    "Generate a draft listing from saved vehicle details for WhatsApp or social channels. The dealer must review and approve "
    "the content before copying or sharing it. The feature must not invent vehicle specifications, condition claims or pricing."
)

doc.add_heading("8. Key User Journeys", level=1)
doc.add_heading("Journey A: Capture a new buyer", level=2)
for x in [
    "Dealer opens the lead form on a mobile device.",
    "Dealer enters name, phone, source and vehicle interest.",
    "System validates the minimum fields and saves the lead.",
    "Lead appears in the New enquiry stage and the dealer can set the next follow-up.",
    "The dashboard and lead list update to reflect the new record.",
]:
    add_num(x)
doc.add_heading("Journey B: Follow up through WhatsApp", level=2)
for x in [
    "Dealer opens the Due today list and selects a lead.",
    "Dealer opens the linked lead and selects a WhatsApp template.",
    "System creates a prefilled click-to-chat action; dealer reviews and edits the message in WhatsApp.",
    "Dealer returns to AutoLead CRM and records the outcome, next action and follow-up date.",
    "Task is marked completed only when the dealer confirms completion, not merely when WhatsApp opens.",
]:
    add_num(x)
doc.add_heading("Journey C: Track an inspection and close a sale", level=2)
for x in [
    "Dealer moves a qualified lead to Inspection scheduled and creates a task with date/time.",
    "After the inspection, dealer records the outcome and moves the lead to Inspection completed or Negotiation.",
    "When a sale is completed, dealer marks the lead Won and records the final sale details.",
    "Vehicle availability is updated to Sold with confirmation; sale reporting reflects the actual sale price.",
]:
    add_num(x)
doc.add_heading("Journey D: Onboard a dealership team", level=2)
for x in [
    "Owner creates an organization and invites team members.",
    "Owner assigns leads to salespeople and defines available roles.",
    "Salespeople see only records permitted by the organization's access policy.",
    "Manager reviews team activity and pipeline reports.",
]:
    add_num(x)

doc.add_heading("9. Data Model (Logical)", level=1)
add_table(["Entity", "Purpose / key relationships"], [
    ("Organization", "Tenant/dealership; plan, billing status, settings and time zone."),
    ("User", "Identity, authentication metadata, organization membership and role."),
    ("Lead", "Prospective buyer; organization, contact details, stage, source, assignee and timestamps."),
    ("Vehicle", "Inventory item; organization, specs, price, availability and stock reference."),
    ("LeadVehicle", "Many-to-many relationship between leads and vehicles."),
    ("FollowUpTask", "Task linked to lead and organization; due date, assignee, status and outcome."),
    ("Activity", "Timeline events such as lead created, stage changed, note added, task completed or WhatsApp action opened."),
    ("Sale", "Recorded transaction; lead, vehicle, sale date, actual sale price and salesperson."),
    ("VehiclePhoto", "Photo metadata and durable object-storage key linked to a vehicle."),
    ("Subscription / BillingRecord", "Plan, billing period, provider reference, status and audit-friendly payment events."),
    ("AuditLog", "Security-sensitive actions and relevant administrative changes."),
])
doc.add_paragraph(
    "Every tenant-owned entity must carry or resolve to an organization_id. Enforce tenant boundaries in the API and, "
    "where practical, reinforce them with database constraints or PostgreSQL row-level security. Use foreign keys, "
    "appropriate indexes and transactions for related operations."
)

doc.add_heading("10. Proposed API Surface", level=1)
doc.add_paragraph("Use versioned REST endpoints, for example /api/v1. Exact routes can be refined during implementation.")
add_table(["Area", "Example endpoints"], [
    ("Authentication", "POST /auth/register, POST /auth/login, POST /auth/logout, POST /auth/forgot-password"),
    ("Organizations / users", "GET /organization, PATCH /organization, GET /users, POST /users/invitations"),
    ("Leads", "GET /leads, POST /leads, GET /leads/{id}, PATCH /leads/{id}, POST /leads/{id}/activities"),
    ("Follow-ups", "GET /follow-ups?status=due, POST /follow-ups, PATCH /follow-ups/{id}, POST /follow-ups/{id}/complete"),
    ("Vehicles", "GET /vehicles, POST /vehicles, GET /vehicles/{id}, PATCH /vehicles/{id}, POST /vehicles/{id}/photos"),
    ("Sales", "GET /sales, POST /sales, GET /sales/{id}, PATCH /sales/{id}"),
    ("Dashboard", "GET /dashboard/summary, GET /dashboard/pipeline, GET /dashboard/activity"),
    ("Billing", "GET /billing/subscription, POST /billing/checkout or provider-specific routes when enabled"),
])
doc.add_paragraph("All endpoints must validate inputs, authenticate the user, authorize the requested action, scope data to the tenant, return predictable errors and avoid exposing secrets or unnecessary personal data.")

doc.add_heading("11. UX and Design Requirements", level=1)
for x in [
    "Mobile-first responsive layout; core lead and follow-up workflows must work on common smartphone screen sizes.",
    "Fast lead capture with minimal required fields and clear validation.",
    "Navigation centered on Dashboard, Leads, Follow-ups, Vehicles and Sales.",
    "Use plain language familiar to dealers; avoid unnecessary CRM jargon.",
    "Show clear empty states with an obvious next action.",
    "Show confirmation for destructive actions and provide recovery where practical.",
    "Provide accessible contrast, keyboard navigation for key flows, visible focus states and useful form labels.",
    "Use loading, success and error states that make network failures understandable.",
    "Support NGN currency formatting and configurable local time zone; do not assume every user will always use the same currency or locale.",
]:
    add_bullet(x)

doc.add_heading("12. Subscription and Commercial Requirements", level=1)
doc.add_paragraph("Proposed test pricing (not market-validated):")
add_table(["Plan", "Illustrative price", "Intended user", "Possible entitlements"], [
    ("Starter", "₦9,900/month", "Independent dealer", "Core leads, follow-ups, inventory, WhatsApp click-to-chat, basic dashboard"),
    ("Growth", "₦24,900/month", "Busy dealer / small team", "Starter plus multiple users, lead assignment and team reports"),
    ("Dealership", "From ₦49,900/month", "Larger team", "Growth plus enhanced permissions, reporting and agreed support"),
])
for x in [
    "Validate willingness to pay with actual dealer interviews and paid pilots before treating prices as final.",
    "For the first pilot, manual invoicing or payment confirmation may be acceptable if access and expiry are handled safely.",
    "Before self-service scale, integrate a suitable payment provider and verify payment status using server-side webhooks.",
    "Never trust a client-side success redirect as proof of payment.",
    "Define grace periods, failed-payment behaviour, cancellation, refunds and data export before enabling automated subscription enforcement.",
    "Display plan limits and renewal terms clearly; do not delete customer data automatically on subscription expiry.",
]:
    add_bullet(x)

doc.add_heading("13. Technical Architecture and Deployment", level=1)
doc.add_heading("13.1 Recommended initial stack", level=2)
add_table(["Layer", "Recommendation", "Notes"], [
    ("Frontend", "Next.js + TypeScript", "Responsive web application"),
    ("Backend", "Node.js API (Express or NestJS)", "Choose one; modular monolith preferred"),
    ("Database", "PostgreSQL", "Managed or self-hosted with reliable backups"),
    ("ORM / migrations", "Prisma", "Reviewed migrations and rollback/forward-fix plan"),
    ("Packaging", "Docker / Docker Compose", "Reproducible development and deployment"),
    ("Hosting", "VPS with Coolify", "Suitable for first launch if operated securely"),
    ("CI/CD", "GitHub Actions", "Tests, linting, type checking, image build and deployment"),
    ("Images", "Persistent object storage or S3-compatible storage", "Avoid container-local ephemeral storage for production photos"),
    ("Email", "Transactional email provider if required", "For password recovery and optional reminders"),
    ("Monitoring", "Uptime checks, application error tracking and server/database metrics", "Alert on failures, disk pressure and backup issues"),
])
doc.add_heading("13.2 Architecture principles", level=2)
for x in [
    "Start with a modular monolith; avoid microservices until there is a demonstrated need.",
    "Keep secrets in deployment environment/secret management, never in source control or frontend bundles.",
    "Use HTTPS, secure session/cookie settings, rate limiting and safe authentication practices.",
    "Use least-privilege database and infrastructure credentials.",
    "Use automated database backups, off-host copies and periodically tested restore procedures.",
    "Run schema migrations as an explicit deployment step and preserve backward compatibility where needed.",
    "Use health checks, structured logs, error reporting and an operational runbook.",
    "Keep staging and production separated where practical; never use real customer data in development without a lawful and secured process.",
    "Set a hosting budget alert and monitor actual resource usage before scaling.",
]:
    add_bullet(x)
doc.add_heading("13.3 Availability and performance targets", level=2)
doc.add_paragraph(
    "Initial targets to validate: p95 under 500 ms for common API requests under an agreed pilot load, excluding external "
    "services and large image transfers. A 99.5% monthly availability objective may be used as an aspirational early target, "
    "but it is not a guarantee. Set realistic commitments based on actual hosting, monitoring and recovery capabilities."
)

doc.add_heading("14. Security, Privacy and Compliance", level=1)
for x in [
    "Enforce tenant isolation on every read and write, including search, exports, background jobs, dashboard queries and file access.",
    "Use secure password hashing or a reputable identity provider; implement safe password reset and session invalidation.",
    "Validate and normalize user input; protect against injection, cross-site scripting, CSRF where applicable and insecure direct object references.",
    "Limit access by role and organization; audit privileged actions.",
    "Encrypt traffic in transit; use encrypted storage and backups where supported.",
    "Collect only personal information needed for the service; define retention, correction, export and deletion workflows.",
    "Publish clear privacy information and terms before onboarding commercial customers.",
    "Assess obligations under the Nigeria Data Protection Act and applicable NDPC guidance; seek qualified advice where needed.",
    "Establish an incident response process, backup restore process and method to notify affected parties or authorities where legally required.",
    "Do not use customer contact lists for marketing unrelated to the service without an appropriate lawful basis and permissions.",
    "Restrict support access to customer data and document any exceptional access.",
]:
    add_bullet(x)

doc.add_heading("15. Reliability and Operational Requirements", level=1)
for x in [
    "Monitor service availability and critical application errors.",
    "Back up the database automatically and store copies outside the primary application host.",
    "Test restoration before onboarding paying customers and repeat on a defined schedule.",
    "Document deployment, rollback/forward-fix, database migration and incident procedures.",
    "Use persistent object storage for uploaded photos and validate upload limits.",
    "Make background jobs and reminder delivery retry-safe and idempotent.",
    "Provide a way for customers to report problems and for the founder to review support requests.",
    "Plan for service maintenance and communicate material outages to customers.",
]:
    add_bullet(x)

doc.add_heading("16. Acceptance Criteria", level=1)
criteria = [
    ("Lead creation", "A signed-in user can create a lead with required fields; it appears in the correct organization’s list and can be searched."),
    ("Tenant isolation", "A user from Organization A cannot access Organization B records by changing IDs, filters, URLs, exports or API parameters."),
    ("Follow-up workflow", "A user can create, reschedule and complete a follow-up; due/overdue views reflect the correct organization time zone."),
    ("WhatsApp action", "The action opens a chat to the correct number with editable text; CRM does not claim delivery from the click alone."),
    ("Inventory", "An authorized user can create and update a vehicle; availability is visible and photo references persist after redeployment."),
    ("Pipeline", "A lead can move through stages; Won/Lost outcomes and loss reasons are stored accurately."),
    ("Sale recording", "A completed sale stores actual sale price separately from vehicle asking price and updates relevant reports."),
    ("Dashboard", "Counts match underlying records for a documented date range and respect organization permissions."),
    ("Responsive UX", "Core workflows work at mobile and desktop viewport sizes."),
    ("Recovery", "A database backup can be restored in a test environment using documented instructions."),
    ("Deployment", "A tested release can be deployed with health checks and a documented recovery/rollback approach."),
]
add_table(["Area", "Acceptance test"], criteria)

doc.add_heading("17. Testing Strategy", level=1)
for x in [
    "Unit tests for validation, stage transitions, pricing calculations and metric definitions.",
    "Integration tests for database operations, authorization and tenant isolation.",
    "End-to-end tests for lead capture, follow-up completion, inventory updates and sale recording.",
    "Security tests for cross-tenant access, authorization bypasses, input validation and upload controls.",
    "Mobile usability tests with representative dealers using their own devices.",
    "Backup restoration and deployment smoke tests.",
    "Pilot acceptance testing with real workflows and feedback before general availability.",
]:
    add_bullet(x)

doc.add_heading("18. Risks and Mitigations", level=1)
add_table(["Risk", "Impact", "Mitigation"], [
    ("Dealers do not consistently enter leads", "Low usage and churn", "Minimize fields, support import, make mobile workflows fast and observe real usage"),
    ("Dealers will not pay proposed prices", "Weak revenue model", "Test paid pilots before expanding scope; adjust segment, value proposition or packaging"),
    ("Competitors offer similar inventory/WhatsApp features", "Hard to differentiate", "Focus on follow-up execution and measurable workflow outcomes; verify competitor gaps in interviews"),
    ("Data leak across dealerships", "Severe trust and legal impact", "Tenant isolation tests, server-side authorization, least privilege and audit logs"),
    ("Lost data or photos", "Customer harm and churn", "Off-host backups, durable object storage and restore drills"),
    ("WhatsApp platform rules or pricing change", "Integration costs or disruption", "Keep click-to-chat as initial fallback; evaluate official API costs and policies before integration"),
    ("Payment failures and subscription disputes", "Revenue loss and support burden", "Clear terms, provider webhooks, reconciliation and defined grace-period behaviour"),
    ("Scope creep", "Delayed launch", "Prioritize P0 requirements and gate additions on customer evidence"),
    ("Founder support workload grows", "Poor scalability", "Self-service onboarding, help content, templates and clear support boundaries"),
])

doc.add_heading("19. Customer Discovery and Go-to-Market Plan", level=1)
doc.add_heading("19.1 Discovery plan", level=2)
for x in [
    "Interview 10–15 independent dealers and dealership managers in Lagos.",
    "Ask them to describe their most recent enquiry and follow-up process instead of pitching first.",
    "Document current tools, lost-lead examples, team structure, inventory size, buying authority and current spending.",
    "Show a prototype and ask them to walk through a realistic lead.",
    "Recruit 3–5 pilot dealerships and agree on a pilot duration, usage expectations and price after the pilot.",
    "Request explicit permission before using customer names, logos, testimonials or performance figures publicly.",
]:
    add_bullet(x)
doc.add_heading("19.2 Initial sales channels", level=2)
for x in [
    "Founder-led direct outreach to dealers found through public listings and referrals.",
    "In-person demonstrations where practical.",
    "Dealer referrals after users experience value.",
    "Short demo videos showing the lead-to-follow-up workflow.",
    "Relevant dealer groups and communities, following their rules and avoiding spam.",
]:
    add_bullet(x)
doc.add_heading("19.3 Suggested 90-day roadmap", level=2)
add_table(["Period", "Focus", "Exit evidence"], [
    ("Weeks 1–2", "Interviews and competitor/workflow research", "Repeated problem pattern and shortlist of pilot prospects"),
    ("Weeks 3–4", "Prototype and pricing tests", "Users can complete key flow; initial willingness-to-pay evidence"),
    ("Weeks 5–7", "Build P0 MVP", "Core workflow passes tests and security review"),
    ("Weeks 8–9", "Pilot onboarding", "Real leads and follow-ups used in the product"),
    ("Weeks 10–11", "Fix friction and test paid plans", "First paying customers and observed repeat usage"),
    ("Week 12", "Review metrics and decide next iteration", "Evidence-based decision to improve, reposition or expand"),
])

doc.add_heading("20. Open Questions / Decisions to Confirm", level=1)
for x in [
    "Which segment shows the strongest urgency and willingness to pay: independent dealers or multi-salesperson dealerships?",
    "What is the minimum useful vehicle and lead limit for each plan?",
    "Will email reminders be part of MVP, or will dashboard/in-app reminders be sufficient for pilots?",
    "Should team invitations and role-based access be in the first paid release or only the Growth plan?",
    "Which Nigerian payment provider best fits the initial subscription model and settlement needs?",
    "What privacy, retention and customer support terms are appropriate for the service?",
    "What onboarding and import assistance do early customers need?",
    "Which product name and domain are available and legally appropriate? AutoLead CRM is a working name until checked.",
]:
    add_bullet(x)

doc.add_heading("21. MVP Definition of Done", level=1)
for x in [
    "P0 features are implemented and acceptance-tested.",
    "Tenant isolation and role checks have been tested beyond the happy path.",
    "Production environment has HTTPS, secure secrets, monitoring and off-host backups.",
    "A database restore has been successfully tested.",
    "The product works on a mobile browser with real dealer workflows.",
    "At least three pilot dealers have completed onboarding or the founder has documented why the pilot target was not met.",
    "A support contact and basic onboarding guide are available.",
    "Pricing and pilot terms are clear, and no unsupported claims are made about automated messaging or sales uplift.",
]:
    add_bullet(x)

doc.add_heading("Appendix A — Suggested Navigation", level=1)
add_table(["Navigation item", "Primary content"], [
    ("Dashboard", "Today's follow-ups, overdue tasks, lead stages, inspections, negotiations, inventory summary and sales"),
    ("Leads", "Searchable lead list, filters, create lead and lead details"),
    ("Follow-ups", "Overdue, due today, upcoming and completed task views"),
    ("Vehicles", "Inventory list, filters, create/edit vehicle and photos"),
    ("Sales", "Recorded sales, sale detail and date-filtered totals"),
    ("Team", "Users, invitations and assignments; available according to plan"),
    ("Settings", "Organization details, time zone, templates, subscription and account security"),
])

doc.add_heading("Appendix B — Core Product Principles", level=1)
for x in [
    "Sell a business outcome, not a feature checklist.",
    "Make the next best action obvious.",
    "Work with dealers’ existing WhatsApp habits rather than forcing a new communication channel.",
    "Do not claim that a message was sent, a lead was converted or revenue increased without evidence.",
    "Protect one dealership’s information from every other dealership.",
    "Prefer validated customer needs over founder assumptions.",
    "Keep the first release operationally simple, secure and recoverable.",
]:
    add_bullet(x)

# Footer
for section in doc.sections:
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("AutoLead CRM PRD • Version 1.0 • Commercial MVP").font.size = Pt(8)

docx_path = Path(__file__).parent / "AutoLead_CRM_PRD.docx"
# doc.save(docx_path)

print(f"Document saved successfully to: {docx_path.resolve()}")

# Also provide a markdown companion version by extracting the authored content in a concise structured form.
md = r"""# AutoLead CRM — Product Requirements Document (PRD)

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
"""
# Save the Markdown document
md_path = out / "AutoLead_CRM_PRD.md"
md_path.write_text(md, encoding="utf-8")
print(f"Markdown document saved successfully to: {md_path}")

print("\nAll documents have been generated successfully!")

print(f"Created: {docx_path} ({docx_path.stat().st_size:,} bytes)")
print(f"Created: {md_path} ({md_path.stat().st_size:,} bytes)")
