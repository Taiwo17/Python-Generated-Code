# Keycloak Alternatives: Stack, Security Gate and Recommendation

**Research date:** 28 October 2026 | **Baseline:** Keycloak 26.8.1 | **Audience:** DevOps / engineering review

**Evidence labels used throughout.** *Verified* = read in a vendor release note or advisory this session. *Aggregator* = read on a CVE aggregator (SentinelOne DB, OpenCVE, Kodem, GitLab advisories, newsletters), not on NVD or the vendor page. *Unverified* = not established; do not rely on it. CVSS is given only where a source stated it.

## 1. Executive summary

1. **No candidate clears the security gate more convincingly than Keycloak 26.8.1.** Keycloak had a very heavy 2026 advisory load, but every issue found is tied to a fixed release, and 26.8.1 (13 Oct 2026) is the only line that carries all fixes. Treat Keycloak as the benchmark, not the problem.
2. **Preferred alternative: authentik, conditionally.** Current release 2026.8.5 (21 Oct 2026), a documented security process (advance notice, GHSA plus CVE page, backports to two supported branches), and a simpler runtime (server, worker, PostgreSQL; Redis removed in 2025.10). Condition: the security content of 2026.8.0 to 2026.8.5 could not be retrieved, so confirm it before production.
3. **Second: ZITADEL, conditionally.** Clear fixed-version ranges for each 2026 CVE, single database (PostgreSQL), Go runtime. Conditions: AGPL-3.0 obligations, the official latest release number is unverified (v4.19.4 was seen only in a third-party fork), and one Low SSRF fix was not backported to the v3 line.
4. **Third: Logto, for a narrower use case.** Current release v1.45.0 (13 Oct 2026), prompt fixes (SSRF fixed in 1.43.0, MFA step-up bypass fixed in 1.41.0). It is customer-identity (CIAM) oriented, not a workforce IdP; some features are now licence-gated on self-hosted.
5. **Flagged, do not adopt without vendor confirmation:** **Casdoor** (several critical SAML and token flaws with no fixed version published; vendor reported non-responsive in two advisories) and **SuperTokens Core** (CVE-2026-37171 cross-tenant access, versions 6.0.0 to 11.4.0, no fix identified). **Ory** is good engineering but is a toolkit, not a Keycloak replacement, and its open-source container dependency findings are unresolved in a public issue.
6. **Runtime context.** None of the candidates runs PHP in its production runtime. The PHP "PHP2Shell" critical RCEs (21 Oct 2026) matter only for PHP relying-party apps, SDKs and CMS sites that sit behind the IdP. Node.js, Go, Java and Python all shipped 2026 security releases that the relevant images must include (section 4.2).

## 2. Candidates

| Product | What it is | Full Keycloak replacement? |
| --- | --- | --- |
| Keycloak (baseline) | Java IAM server; OIDC, OAuth 2.0, SAML, LDAP/Kerberos federation, fine-grained admin, UMA, token exchange, SCIM (supported and on by default in 26.8) | n/a |
| authentik | Flow-based IdP with providers for OIDC, SAML, LDAP, RADIUS, SCIM and proxy outposts | Yes for most workforce and self-hosted SSO; WS-Federation is Enterprise-only |
| ZITADEL | Event-sourced multi-tenant IAM (Go), organisations, OIDC, SAML, LDAP as an upstream IdP | Largely yes for SaaS and B2B; LDAP/Kerberos federation depth not verified |
| Logto | CIAM / auth infrastructure for SaaS and AI apps; OIDC, OAuth 2.1, SAML, organisations, RBAC | Partly; narrower, developer-led |
| Casdoor | Go-based IAM/SSO with SAML and OAuth | Feature-wise broad; security gate fails (below) |
| Ory Kratos + Hydra (+ Keto, Oathkeeper, Polis) | Headless identity, OAuth2/OIDC server, permissions, proxy, SAML bridge | No: composable building blocks, no bundled admin product |
| SuperTokens | SDK-driven auth (sessions, passwordless, social) with a Java Core service | No: embedded app-auth, not a central IdP |

Not researched in depth: Authelia, Dex, Gluu, FusionAuth, Zitadel-adjacent managed offerings. They are candidates for a second pass.

## 3. Technology stack

Production runtime is separated from build and optional parts. "Not verified" means no source retrieved.

| Product | Backend (runtime) | Frontend | Database | Cache / queue | Runtime and image |
| --- | --- | --- | --- | --- | --- |
| Keycloak 26.8.1 | Java on Quarkus | Admin/Account consoles (PatternFly-based) | Relational DBs; tested-version table not captured | Embedded clustering (JGroups/Infinispan); Quarkus executor pools | OpenJDK 21 or 25 supported; official image uses OpenJDK 21; Operator for Kubernetes; Apache-2.0 |
| authentik 2026.8.5 | Python 3.14 (Django) core; Go outposts; Rust packages appear in 2026.8 notes | TypeScript web UI (Lit) | PostgreSQL 14 to 18 (aggregator) | PostgreSQL only: cache, queue and websockets moved off Redis in 2025.10 | Server and worker containers; Helm chart and compose.yml; FIPS Python slim-trixie base image appears in 2026.2.4 notes |
| ZITADEL | Go; event-sourced | Separate login UI image (framework not verified) | PostgreSQL only (CockroachDB dropped in v3) | Built-in cache with active invalidation | Single Go binary; needs a 32-char masterkey; AGPL-3.0 |
| Logto 1.45.0 | Node.js / TypeScript (Koa) | Web console (framework not verified) | PostgreSQL 14+ | Redis optional cache (aggregator) | Node.js 22 per template; the README's Node 20.9 minimum is stale because Node 20 reached end of life on 30 Apr 2026 |
| Casdoor | Go | Not verified | Not verified | Not verified | Not verified |
| Ory (Kratos, Hydra) | Go | None bundled | SQL (engines not verified here) | Not verified | Separate services per component; v26.x versioning |
| SuperTokens Core | Java (Java 17 and Java 21 both reported) | None; SDKs (Node, Python, Go) | PostgreSQL 13+ only since 11.0.0 | Not verified | Single Java process on port 3567; must not be internet-exposed |

**Effect of the stacks.** JVM (Keycloak) costs more memory and startup time but gives mature clustering and a very large community. Python + PostgreSQL (authentik) removes Redis, lowers moving parts, but moves cache, queue and pub/sub load onto PostgreSQL, so database sizing and connection limits matter. Go single-binary designs (ZITADEL, Ory) are light and simple to patch by rebuilding with a new toolchain, which matters because Go stdlib fixes arrive in toolchain releases. Node (Logto) inherits Node and npm supply-chain exposure, so pin the runtime and scan npm dependencies.

**Observability.** Not systematically verified for any product. Evidence seen: authentik added queued-task metrics and a structured JSON log path in 2026.2; ZITADEL ships OpenTelemetry libraries (visible in its dependency scan). Verify metrics, tracing and log formats in the PoC.

## 4. Security investigation

### 4.1 Platform CVE register

Affected and fixed versions are quoted from the cited records. "Not captured" means the record was not opened.

**Keycloak (baseline)**

| ID | Issue | Severity | Disclosed / fixed | Affected | Fixed in | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-18963 | Reset-credentials flow bypass: forced password reset without email verification, account takeover | Not captured | NVD 18 Aug 2026; Red Hat 21 Aug | Red Hat build of Keycloak (RHSA-2026:56519, 56520, 56523, 56524) | Upstream fixed version not captured; a downstream fork cherry-picked the fix onto 26.6.4, so 26.6.4 did not contain it | Aggregator + fork notes |
| CVE-2026-94000 | Delegated admin with only manage-users becomes realm-admin via group role mapping | Not captured | 26.8.1 | See notes | 26.8.1 | Keycloak release note (verified) |
| CVE-2026-96445 | Forged header skips OTP on untrusted paths | Medium 6.8 | 26.8.1 | Before 26.8.1 | 26.8.1 | Newsletter table (aggregator) |
| CVE-2026-95503 | Kerberos password auth never verifies the KDC | Medium 6.8 | 26.8.1 | Before 26.8.1 | 26.8.1 | Aggregator |
| CVE-2026-107121 | SMTP StartTLS can fall back to plaintext | Medium 6.5 | 26.8.1 | Before 26.8.1 | 26.8.1 | Aggregator |
| CVE-2026-12388 | IdP mapper admin role escalation | Not captured | 26.8.0 | Before 26.8.0 | 26.8.0 | Release note (verified) |
| CVE-2026-9704 | Token-exchange privilege escalation via silent subject\_token removal | Not captured | 26.6.3 | Before 26.6.3 | 26.6.3 | Release note (verified) |
| CVE-2026-7507 | OIDC session fixation leading to account takeover | Not captured | 26.6.2 | Before 26.6.2 | 26.6.2 | Release note (verified) |
| CVE-2026-4282 | Privilege escalation via forged authorization codes | Not captured | 26.5.7 | Before 26.5.7 | 26.5.7 | Release note (verified) |
| CVE-2026-3872 | Redirect URI validation bypass via ..;/ traversal | Not captured | 26.5.7 | Before 26.5.7 | 26.5.7 | Release note (verified) |

Other patch points: 26.5.3 (Feb 2026), 26.6.1 (CVE-2026-4366 SSRF, CVE-2026-4633 user enumeration), 26.6.2 (many, including CVE-2026-7307 SAML DoS), 26.6.3 (CVE-2026-4874 SSRF, CVE-2026-9792 ROPC bypass). 26.8.1 names 18 Keycloak CVEs and 9 dependency CVEs per a third-party tracker.

**authentik**

| ID | Issue | Severity | Disclosed | Affected | Fixed in | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-61574 | Remote Access endpoints exposed to any authenticated user; stored RAC credentials at risk (GHSA-rv9x-92g6-9cpf) | Not captured | NVD 18 Aug 2026 | Before 2026.2.6 and 2026.5.5 | 2026.2.6, 2026.5.5 (rotate RAC credentials) | Aggregator |
| CVE-2026-57580 | Security advisory published with the 2026.5.5 / 2026.2.6 release | Not captured | Aug 2026 | Not captured | 2026.5.5, 2026.2.6 | Vendor mailing list (verified) |
| CVE-2026-47201 and two GHSA IDs | Security fixes | Not captured | Jun 2026 | Not captured | 2026.2.4 | Release notes (verified) |
| CVE-2026-40165, -40166, -40172, -41569, -41577, -42849 | Six advisories | Not captured | May 2026 | Not captured | 2026.2.3 (and 2025.12.5 for some) | Release notes (verified) |
| CVE-2026-25227, -25748, -25922 | Three advisories | Not captured | Feb 2026 | Not captured | 2026.2.0 | Release notes (verified) |

The 2026.2.7 notes add five more internal security backports (including a libxml2 doctype patch), and 2026.5.6 exists. **Security content of 2026.8.0 to 2026.8.5 was not retrieved: unverified.**

**ZITADEL**

| ID | Issue | Severity | Disclosed | Affected | Fixed in | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-44671 | LDAP filter injection in LDAP IdP login | High 7.5 | 14 May 2026 | 2.71.11 to before 3.4.10; before 4.15.0 | 3.4.10, 4.15.0 | NVD-derived (aggregator) |
| CVE-2026-56664 | Token without iat claim passes freshness check | Medium 4.2 | 10 Jul 2026 | Not captured | 3.4.12, 4.15.2 | Aggregator |
| CVE-2026-55671 | SSRF via DNS rebinding or redirects | Low 2.3 | NVD 10 Jul 2026 | 3.0.0 to 3.4.11; 4.0.0 to 4.15.1 | 4.15.2; **v3 backport judged infeasible** | Aggregator |
| CVE-2026-55672 | Improper authentication (listed High) | High | Jun 2026 | Not captured | Not captured | Aggregator, details unverified |
| CVE-2026-76081 | Deleting several project roles leaves stale grants | Medium 5.5 | 14 Sep 2026 | Grant-based user grants | 4.16.0 (migration step 73) | Aggregator |
| CVE-2026-105206 | user.read checked against caller's org, not target's | Not captured | NVD 4 Oct 2026 | 3.0.0 to 3.4.15; 4.x before 4.17.3 | 4.17.3 (v3 fix version not captured) | Aggregator |

A scan attached to a third-party fork's v4.19.4 build also lists a High Go stdlib finding (CVE-2026-46600, fixed in Go 1.26.6) and Medium gorilla/csrf and x/crypto/ssh items. That is a fork, not the official image. Scan the official image yourself.

**Logto**

| ID | Issue | Severity | Affected | Fixed in | Evidence |
| --- | --- | --- | --- | --- | --- |
| CVE-2026-56739 | SSRF via webhooks and custom OAuth2 connector (GHSA-3556-624q-c5w3) | Not captured | Before 1.43.0 | 1.43.0 | OSV (verified record) |
| CVE-2026-63203 | Account API can leak stored third-party tokens without the identities scope | Not captured | 1.31.0 to 1.42.0 | 1.42.0 | Aggregator |
| CVE-2026-55789 | XML/XPath-style injection (CWE-91) | Not captured | Before 1.41.0 | 1.41.0 | NVD (verified) |
| CVE-2026-55377 | Account Center MFA step-up bypass via WebAuthn registration | Not captured | Before 1.41.0 | 1.41.0 | NVD / OpenCVE |
| CVE-2026-54714 | XSS through unescaped RelayState in SAML auto-submit form | Not captured | Before 1.41.0 | 1.41.0 | OpenCVE |
| CVE-2026-63188 | Path traversal in @logto/tunnel dev tool | Not captured | Before 0.3.9 | 0.3.9 | Not production runtime |

**Casdoor: fails the gate on current evidence**

| ID | Issue | Severity | Disclosed | Affected | Fix |
| --- | --- | --- | --- | --- | --- |
| CVE-2026-9090 | SAML auth bypass: signing certificate taken from the attacker's SAMLResponse | Critical 9.1 | 28 May 2026 | 2.362.0 and earlier | No patched version listed |
| CVE-2026-9092 | Account takeover through unverified email binding | Critical | 28 May 2026 | 2.362.0 and earlier | None identified |
| CVE-2026-9093 | SAML AudienceRestriction not validated | Critical | 28 May 2026 | 2.362.0 and earlier | None identified |
| CVE-2026-9097, -9098 | JWT token exchange ignores revocation; SAML callback accepts unsolicited responses | Critical | May 2026 | Same range | None identified |
| CVE-2026-9094 | Not captured | 9.8 | May 2026 | 2.362.0 and earlier | None identified |
| CVE-2026-9091 | Social-login binding bypasses MFA | Medium 5.3 | 28 May 2026 | Same range | "No solution available yet" |
| CVE-2026-5467 | Open redirect in OAuth authorize | Medium 4.3 | 3 Apr 2026 | Up to 1.1000.0 | "No solution available yet" |
| CVE-2026-84423 | Unauthenticated upload API; vendor deleted the report | Moderate | 1 Sep 2026 | Up to 4.0.0 | None identified |
| CVE-2026-90942 | Built-in certificate material not masked | Critical 9.6 | 14 Sep 2026 | Through 4.4.0 | None identified |

Version strings are inconsistent across sources (2.362.0, a 1.1000.x Go pseudo-version, 4.4.0). Reconcile them against the official release list before any decision.

**Ory**

| ID | Issue | Severity | Disclosed | Fixed in | Evidence |
| --- | --- | --- | --- | --- | --- |
| CVE-2026-33503 | Kratos ListCourierMessages SQL injection via forged pagination tokens (default secret is public) | High 7.2 | 20 Mar 2026 | 26.2.0; set secrets.pagination | Aggregators |
| CVE-2026-33504 | Hydra SQL injection in three Admin list APIs | High 7.2 | Mar 2026 | 26.2.0 | Aggregators |
| CVE-2026-33505, -33506 | Keto (7.2) and Polis (8.8) in the same advisory bundle | See left | Mar 2026 | Bundle advisory v26.2.0; Polis fixed version not captured | Aggregator |

An open Hydra issue (about 8 Oct 2026) lists unresolved container-scan findings, including golang.org/x/crypto before 0.52.0 (CVE-2026-46595, Critical), Go stdlib before 1.26.2, OpenTelemetry SDK and docker/docker (two High with no fix). Applicability to Hydra's actual code paths and the fixed release are **unverified**; one third-party triage found two advisories there to be range-mapping false positives.

**SuperTokens Core**

| ID | Issue | Severity | Disclosed | Affected | Fix |
| --- | --- | --- | --- | --- | --- |
| CVE-2026-37171 | No tenant separation: a user in one tenant can reach another tenant's sessions, data and endpoints | Medium 5.9 | NVD 7 Aug 2026; public disclosure 9 Sep | Core 6.0.0 to 11.4.0 | None identified. Mitigation: keep Core off untrusted networks, set api\_keys |

Multi-tenancy is an enterprise-licensed feature per one summary, which narrows exposure for community-only users (aggregator).

### 4.2 Runtime and dependency vulnerabilities

| Runtime | 2026 events | Fixed versions | Which candidates it touches |
| --- | --- | --- | --- |
| Node.js | 24 Mar: CVE-2026-21637 (incomplete fix) and CVE-2026-21710, both High, plus six more; 18 Jun: 12 fixes (aggregator); 29 Jul: 11 CVEs (3 High). Node 20 reached end of life 30 Apr 2026. October releases not checked | 20.20.2, 22.22.2, 24.14.1, 25.8.2 (Mar); 22.23.0, 24.17.0, 26.3.1 (Jun); 24.18.0 and a patched 26.x (Jul) | Logto runtime; SuperTokens SDKs; OIDC client apps. Keycloak only in build tooling |
| PHP | 21 Oct: CVE-2026-109618 and CVE-2026-109619, unauthenticated RCE, CVSS v4.0 9.2 each; 27 Aug: CVE-2026-17543 (pg\_\* SQL injection, High), CVE-2026-17544 (bccomp write) | 8.5.12, 8.4.27, 8.3.36, 8.2.35; 8.1 and older: no fix | **None** of the products. Applies to PHP client apps and WordPress behind the IdP |
| Java | 20 Oct CPU: 55 Java SE flaws, max CVSS 7.5, 49 remotely exploitable without login; 18 Aug out-of-band: four flaws. Oracle JDK 21 updates now need a paid licence | OpenJDK builds equal to 25.0.5 or 21.0.13 | Keycloak, SuperTokens Core |
| Go | go1.26.6 (13 Aug) fixes net/http, crypto/tls, encoding/asn1, net/url, html/template, x/net idna (CVE-2026-39821, 9.1 per SUSE; CVE-2026-33818, 7.5) | go1.26.6 or later | ZITADEL, Ory, Casdoor, authentik outposts |
| Python | 3.14.8 (30 Sep) expedited security release; 3.14.4 (Apr) fixed CVE-2026-4519, -4786, -6100 | 3.14.8 or later | authentik core |

A fixed runtime in the project's changelog is not proof the shipped image contains it. For each image, check the Go toolchain, JDK or Node version inside it and rescan after pulling.

## 5. Security acceptance gate

| Criterion | Keycloak 26.8.1 | authentik 2026.8.5 | ZITADEL | Logto 1.45.0 | Casdoor | Ory | SuperTokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Critical/High 2026 issues have a fixed release | Yes (26.8 line) | Yes through 2026.2.7 and 2026.5.x; 2026.8.x unverified | Yes (3.4.10+/4.15+ for the High; 4.17.3 latest seen) | Yes | **No** | Yes for SQLi (26.2.0); dependency findings open | **No** (Medium) |
| Supported version | Latest minor only is fully patched | Two newest releases get security cover | Two lines (v3, v4) patched unevenly | Latest only assumed | Unclear | Unclear | Unclear |
| Backports | Partial: 26.6.8 and 26.7.6 not shipped | Yes (2026.2, 2026.5) | Partial (one Low not backported) | Not verified | No evidence | Not verified | No evidence |
| Timely advisories | Release notes yes; GitHub advisory feed lags | Mailing list, GHSA, CVE pages | GHSA + CVE | GHSA + CVE | Weak; vendor reported unresponsive | GHSA + changelog | Weak; disclosure came from a third party |
| Scannable image / SBOM | Yes in principle | Yes | Yes | Yes | Unknown | Findings public | Unknown |
| Unresolved advisories | None known on 26.8.1 | None known; 2026.8 unchecked | None known on 4.17.3+ | None known | **Multiple** | Dependency scan open | **CVE-2026-37171** |
| **Gate result** | Pass | Conditional pass | Conditional pass | Conditional pass | **Fail** | Conditional (toolkit) | **Fail until fixed** |

## 6. Pros and cons

**Keycloak 26.8.1 (baseline).** *Pros:* broadest protocol and federation coverage (OIDC, SAML, LDAP/Kerberos, UMA, SCIM, token exchange); CNCF project; Apache-2.0 with no feature gating; Kubernetes Operator; OpenJDK 21/25 supported. *Cons:* the largest advisory volume in this study (dozens of 2026 CVEs, mostly Medium); only the newest minor receives every fix; heavier JVM footprint; Oracle JDK 21 licence change forces OpenJDK builds. Enterprise support route: Red Hat build (paid).

**authentik.** *Pros:* easy deployment (three services), flexible flow engine, proxy outposts for legacy apps, Kubernetes Helm chart, active release train (2026.8.5 on 21 Oct), two-branch security backports. *Cons:* MIT core plus separate Enterprise licence (WS-Federation, lifecycle management, agent and endpoints are Enterprise); sizeable dependency tree (Python, Go, Rust, TypeScript); PostgreSQL now carries queue and cache load; fewer federation features than Keycloak for Kerberos-heavy estates (not verified); migration from Keycloak is manual (realms to flows/blueprints).

**ZITADEL.** *Pros:* Go single binary, PostgreSQL only, event-sourced audit trail, strong multi-tenancy and organisation model, fixed-version tables in every advisory. *Cons:* **AGPL-3.0** since v3 (network-copyleft: review with legal if you modify and expose it); CockroachDB dropped; v3 and v4 lines differ in fix coverage; release number unverified; observability and LDAP/SAML depth to be tested.

**Logto.** *Pros:* quick fixes for every 2026 issue found, modern developer experience, MPL-2.0, Organizations and SAML apps, many SDKs. *Cons:* CIAM-first, not a workforce directory; v1.45.0 introduced licence-gated self-hosted features (team members, branding removal, custom sign-in UI, more SAML apps, tenant-wide console MFA); a fork's notes claim some are being freed, so recheck; Node and npm supply chain; weaker LDAP/Kerberos federation (not verified).

**Casdoor.** *Pros:* broad feature list, Go. *Cons:* see gate: unpatched critical authentication flaws, reports that the vendor deleted or ignored disclosures, inconsistent versioning. **Do not use** until fixes and a disclosure process are demonstrated.

**Ory.** *Pros:* Go, headless, API-first, OpenID-certified Hydra, excellent for custom login UX; fast SQLi fix. *Cons:* you assemble and operate several services; no bundled admin UI in OSS; SAML needs Polis; public dependency-scan findings; SQLi exposure depended on a default or known pagination secret (always set secrets.pagination).

**SuperTokens.** *Pros:* simple Core, PostgreSQL only, easy SDK integration. *Cons:* not a central IdP; Apache-2.0 core with enterprise-licensed modules (multi-tenancy, MFA, SAML per one summary); open CVE-2026-37171; Core must be isolated from untrusted networks.

## 7. Comparative table

Verification date 28 Oct 2026.

| Product | Latest stable (verified?) | Backend | DB | Deployment | Protocols | Security status | Maintenance | Licence | Best fit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Keycloak | 26.8.1, 13 Oct (verified) | Java/Quarkus | RDBMS | Docker, Operator | OIDC, OAuth2, SAML, LDAP/Kerberos federation, SCIM | Patched on 26.8.1; older minors lag | Monthly-ish; latest minor | Apache-2.0 | Full-featured enterprise IAM |
| authentik | 2026.8.5, 21 Oct (verified) | Python, Go, Rust | PostgreSQL | Compose, Helm | OIDC, SAML, LDAP, RADIUS, SCIM, proxy | Patched through 2026.5.x; 2026.8 unverified | Quarterly plus patches; two branches covered | MIT core + Enterprise licence | Self-hosted workforce SSO |
| ZITADEL | 4.17.3 verified via advisory; 4.19.4 seen in a fork only | Go | PostgreSQL | Binary, Docker, K8s | OIDC, SAML, OAuth2, LDAP IdP | Patched per advisory ranges | Frequent | AGPL-3.0 | Multi-tenant SaaS/B2B |
| Logto | 1.45.0, 13 Oct (verified) | Node/TS | PostgreSQL | Docker, Node | OIDC, OAuth 2.1, SAML | Patched through 1.43.0 | Monthly changelog | MPL-2.0 (+ licence keys for some features) | CIAM for SaaS |
| Casdoor | Unverified | Go | Not verified | Not verified | OAuth, SAML | Critical, unfixed | Unclear | Not verified (confirm) | Avoid for now |
| Ory | 26.2.x (Mar) verified; newer unverified | Go | SQL | Containers | OIDC (Hydra); SAML via Polis | SQLi fixed; deps open | Active | Not verified (confirm) | Custom-built auth |
| SuperTokens | Unverified (11.4.0 affected) | Java | PostgreSQL 13+ | Docker | Session/SDK; SAML via EE | CVE-2026-37171 open | Unclear | Apache-2.0 core + proprietary EE | App-embedded auth |

## 8. Licensing and operating cost

| Product | Licence facts | Gated or paid | Cost drivers |
| --- | --- | --- | --- |
| Keycloak | Apache-2.0 | Nothing gated; Red Hat build is the paid support route | JVM memory (about 500 MB per 100,000 concurrent sessions per one template), database, HA, upgrades each month |
| authentik | MIT core; Enterprise code under a separate licence | WS-Federation, lifecycle management, agent and endpoints, some sync providers, support. Pricing page not retrieved | Server, worker, PostgreSQL (14 to 18) |
| ZITADEL | AGPL-3.0 | Cloud and enterprise support tiers not retrieved | PostgreSQL, masterkey custody |
| Logto | MPL-2.0 | v1.45.0 "Self-Hosted Pro" licence for several features | PostgreSQL, optional Redis |
| Casdoor / Ory | Confirm repository LICENSE files (not verified this session) | Ory commercial network exists | Casdoor not applicable |
| SuperTokens | Apache-2.0 core; proprietary `ee/` modules | Licence key required | PostgreSQL plus one Java process |

Enterprise security SLAs were not verified for any vendor.

## 9. Proof-of-concept plan (authentik, ZITADEL, Logto; Keycloak 26.8.1 as control)

1. **Deploy** each in Docker Compose behind a TLS reverse proxy (Caddy or Traefik, Let's Encrypt), pinned by image digest. Add a Kubernetes pass using the Helm chart or Operator.
2. **Database:** PostgreSQL 16 or 18 with a named volume, `pg_dump` and WAL-based point-in-time backups, restore drill to a clean host, record RTO and RPO.
3. **Secrets:** Docker/Kubernetes secrets or Vault; rotate ZITADEL masterkey handling, authentik secret key, Logto signing keys; confirm none appear in env dumps or logs.
4. **OIDC integration:** a sample app (Node and a PHP app) using authorization code with PKCE; test refresh rotation, logout and token introspection. Add a SAML SP test.
5. **MFA and sessions:** TOTP and WebAuthn enrolment, step-up, session revocation, idle and absolute timeouts, brute-force lockout.
6. **RBAC:** roles and groups mapped to application claims; delegated-admin tests that replay the 2026 escalation classes (group-role mapping, cross-org reads).
7. **Scanning:** Trivy and Grype on images; OWASP Dependency-Check for Java and npm; `govulncheck` for Go binaries; `pip-audit` for Python; OSV-Scanner across lockfiles. Fail the PoC on any unwaived Critical or High.
8. **SBOM:** Syft (CycloneDX or SPDX), plus Cosign signature verification where images are signed.
9. **Upgrade and rollback:** upgrade one minor release, then roll back from backup; run authentik's sequential-upgrade rule and Logto's `alteration deploy` step (which can block rollback once IDs exceed old limits).
10. **Load and footprint:** k6 or Locust for login and token endpoints; record RAM, CPU, p95 latency at 100, 500 and 1,000 logins per minute. Capture Prometheus metrics and log formats.

## 10. Final ranked recommendation

| Rank | Product | Why | Verified patch status | Remaining risks | Test before production |
| --- | --- | --- | --- | --- | --- |
| 1 | **authentik** (conditional) | Simplest runtime among full IdPs, mature flows and outposts, two-branch security backports | Verified through 2026.2.7 and 2026.5.x; 2026.8.x not retrieved | Enterprise-gated features; PostgreSQL load; unreviewed 2026.8 advisories | Read 2026.8 release notes security sections; Trivy on 2026.8.5; HA and backup drills |
| 2 | **ZITADEL** (conditional) | Clean Go and PostgreSQL design; tidy advisories with explicit ranges | Verified to 4.17.3 for the CVEs listed | AGPL-3.0; official latest unverified; v3 backport gaps | Confirm official release and image scan; legal AGPL review; LDAP/SAML tests |
| 3 | **Logto** (CIAM only) | Fast fixes, simple developer experience, current release | Verified to 1.43.0 and 1.45.0 is latest | Not a workforce IdP; licence-gated features; Node supply chain | Scan npm tree; confirm Node 22/24 image; test SAML and MFA |

**Preferred option.** The evidence supports authentik as the preferred Keycloak alternative for self-hosted workforce SSO, subject to the three verification items above. It does not support declaring any alternative safer than Keycloak 26.8.1. If the requirement includes Kerberos or LDAP federation or deep admin permissions, keep Keycloak and upgrade to 26.8.1.

## 11. Missing evidence

- ZITADEL official latest release; Ory current OSS tag; SuperTokens current Core version; Casdoor reconciled version history.
- authentik 2026.8.0 to 2026.8.5 security notes.
- Keycloak CVE-2026-18963 upstream fixed version; most CVSS scores.
- Licences of Casdoor and Ory; vendor SLAs and pricing.
- Node.js October 2026 release; per-image runtime versions.
- Many CVE entries came from aggregators. Confirm each against NVD or the vendor GHSA before filing it in a risk register.

## 12. Sources

Keycloak: keycloak.org release notes 26.5.3, 26.5.7, 26.6.1 to 26.6.3, 26.8.0, 26.8.1, supported-configurations guide; github.com/keycloak/keycloak/releases; buttondown.com/keycloak-advisory-watch; sentinelone.com CVE-2026-18963; github.com/Inform-Software/keycloak/releases. authentik: docs.goauthentik.io/releases/2026.2; github.com/goauthentik/authentik releases 2026.5.3, 2026.8.0, 2026.8.4, 2026.8.5; groups.google.com/g/authentik-security-announcements; sentinelone.com CVE-2026-61574; goauthentik.io/blog/2025-11-13-we-removed-redis. ZITADEL: sentinelone.com CVE-2026-56664, -55671, -76081, -105206; strix.ai CVE-2026-44671; kodemsecurity.com CVE-2026-55671; zitadel.com/docs/product/roadmap and changelog; github.com/HomeLabHD/zitadel/releases (fork). Logto: github.com/logto-io/logto/releases/tag/v1.45.0; osv.dev CVE-2026-56739; nvd.nist.gov CVE-2026-55789 and -55377; opencve.io CVE-2026-54714, -63188; vulners CVE-2026-63203. Casdoor: github.com/advisories GHSA-fwgq-j9r9-qjgr, GHSA-qq8g-36vc-g254, GHSA-3w4h-g9f5-j84p, GHSA-ghh7-j2mm-r3r8; advisories.gitlab.com CVE-2026-9091, -5467; kodemsecurity.com CVE-2026-9090; strix.ai CVE-2026-90942. Ory: changelog.ory.com; opencve.io (Kratos, Hydra); strix.ai CVE-2026-33503; endorlabs.com CVE-2026-33504; github.com/ory/hydra/issues/4133. SuperTokens: openwall.com/lists/oss-security/2026/09/09/4; opencve.io CVE-2026-37171; supertokens.com/docs self-hosting pages. Runtimes: nodejs.org March 2026 release page via github.com/nodejs/nodejs.org; herodevs.com; dev.to Node July 2026; rescana.com and offseq.com PHP2Shell; pasqualepillitteri.it PHP 8.5.12; oracle.com JDK 21.0.12.1 notes; ipa.go.jp Oct 2026 Java alert; pcwelt.de Oct 2026 CPU; linuxsecurity.com and lwn.net go1.26.6; python.org Python 3.14.8.
