import pypandoc

markdown = r"""# Keycloak Alternatives: Technology Stack, Pros and Cons, and Security Assessment

**Research date:** 28 October 2026  
**Audience:** DevOps, infrastructure, and security engineering review

> **Important research limitation:** This report records the release and advisory evidence identified during the research, but it does not establish that every CVE in every transitive dependency has been exhaustively checked through 28 October 2026. Product release versions and runtime versions must be verified against the exact production image before approval. A newer release is not, by itself, proof that a vulnerability is fixed.

## 1. Executive summary

This is a security-led technology evaluation, not simply a comparison of authentication products. The key question is which product meets the identity requirements, remains supported, and has demonstrably addressed applicable vulnerabilities.

### Initial shortlist

1. **authentik** — a broad self-hosted identity platform with flexible authentication flows and an administrator-friendly interface. Investigate its PostgreSQL, Redis, worker, and server architecture, and verify the licence terms for advanced features.
2. **ZITADEL** — a modern, API-driven identity platform with OIDC/OAuth, multi-tenancy, and automated deployment options. Verify enterprise-feature boundaries and exact database/migration requirements.
3. **Logto** — a developer-focused authentication and identity platform with SDKs and modern application-login workflows. Confirm enterprise federation requirements and self-hosted feature entitlements.

These are candidates for evaluation, not security-approved winners. Keycloak remains the baseline because it offers a broad IAM feature set, established federation capabilities, and a mature Java-based ecosystem.

## 2. Research methodology and evidence standard

- **Verified:** A current official release or vendor advisory explicitly supports the claim.
- **Documented:** Official documentation describes the feature or architecture, but production behaviour still needs testing.
- **Unverified:** The affected/fixed version range or security status has not been established from the available evidence.
- **Not applicable:** The issue concerns a component not present in the selected deployment.

### Production security acceptance gate

A candidate should pass all of the following before production approval:

1. The deployed release is supported and pinned to a specific version or image digest.
2. All applicable critical and high-severity advisories have been addressed in the exact release or a documented backport.
3. Runtime and dependency versions are verified, not inferred from marketing material.
4. Container images and operating-system packages are scanned.
5. Authentication, authorization, session handling, and federation flows pass security tests.
6. Database recovery, upgrades, and rollback procedures are demonstrated.

A clean vulnerability scan is not proof that an identity provider is secure. Scanners may not detect authentication bypasses, faulty authorization rules, or logical flaws in SAML and OAuth/OIDC implementations.

## 3. Candidate products and scope

| Product | What it provides | Replacement scope |
|---|---|---|
| Keycloak | Identity provider, SSO, user federation, client management, authorization, and identity brokering | Baseline |
| authentik | Self-hosted identity provider, application access, authentication flows, directory integrations | Broad replacement candidate |
| ZITADEL | Cloud-native identity platform with organizations, projects, applications, and identity APIs | Broad replacement candidate |
| Logto | Developer-focused authentication and identity platform | Strong for application IAM; verify enterprise federation needs |
| Casdoor | Identity and access management with OAuth/OIDC and other integrations | Broad candidate; verify exact feature parity |
| Ory Kratos + Hydra | Identity management and OAuth2/OIDC authorization server, often combined with other Ory services | Composable solution rather than one-to-one replacement |
| SuperTokens | Application authentication, sessions, MFA, and social login | Primarily application authentication; narrower IAM scope |
| FusionAuth | Application identity, SSO, federation, and enterprise-oriented IAM capabilities | Worth evaluating where commercial support matters |

FusionAuth is included as an additional commercial alternative. These products serve different use cases; not all are direct replacements for Keycloak.

## 4. Technology-stack comparison

The following describes the main architectural characteristics. Exact dependency versions, minimum hardware requirements, supported database versions, and base-image contents must be verified against the selected release before deployment.

| Product | Backend and runtime | Frontend | Database and supporting services | Container and deployment model |
|---|---|---|---|---|
| **Keycloak** | Java; Quarkus-based runtime | TypeScript/JavaScript-based administration and account interfaces | PostgreSQL, with other databases supported depending on release; internal caching | Official container image; Kubernetes, Helm/operator and standard container deployments |
| **authentik** | Python/Django-based server, with Go-based components for some outposts and services | TypeScript-based web interface | PostgreSQL; Redis has historically been part of the deployment architecture, so verify the current release's requirements | Official containers; Docker Compose and Kubernetes deployments |
| **ZITADEL** | Go | TypeScript-based Console and login interfaces | PostgreSQL | Official containers; Kubernetes and Helm deployment options |
| **Logto** | Node.js/TypeScript | React/TypeScript-based interfaces | PostgreSQL | Official Docker image and Compose deployment; Kubernetes/cloud deployment options require release-specific verification |
| **Casdoor** | Go; Beego framework | React/JavaScript-based administration interface | Supports several SQL database options; verify supported engines and versions in the chosen release | Official Docker image and Kubernetes deployment options |
| **Ory Kratos + Hydra** | Go | Login and registration interfaces are typically supplied or customised separately | SQL database support depends on component and release; PostgreSQL and MySQL are commonly used | Separate services deployed with containers, Kubernetes, or managed Ory offering |
| **SuperTokens** | Core authentication service implemented in Java; application SDKs vary by language | JavaScript/TypeScript UI and SDK ecosystem | PostgreSQL or MySQL support depends on core version; verify supported versions and scaling requirements | Core service plus application integration; Docker and Kubernetes deployment options |
| **FusionAuth** | Java-based server | Web-based administration and login interfaces | Database and bundled-service requirements must be checked against selected edition and deployment guide | Official container and cloud deployment options |

### How the stack affects operations

**Java-based platforms — Keycloak and SuperTokens core**
- Mature runtime ecosystem, extensive libraries, and established monitoring options.
- JVM memory sizing, garbage collection, startup behaviour, and database connection pools require attention.
- Security depends on the bundled Java version, framework dependencies, and container image—not just the product release.

**Go-based platforms — ZITADEL, Casdoor, and Ory**
- A compiled service can simplify runtime packaging and deployment.
- Smaller runtime images are possible, but not guaranteed; image size is not a security or performance benchmark.
- Go standard-library and module vulnerabilities still require tracking and patching.

**Python-based platform — authentik**
- Python and Django provide a mature web framework, extensibility, and a familiar development ecosystem.
- Python packages, Django, system libraries, and background-worker components contribute to the patching surface.
- Do not assume a Python-based product must be slower or less secure than a Go-based product; measure the actual workload.

**Node.js/TypeScript platform — Logto**
- TypeScript across backend and frontend can simplify developer onboarding and application integration.
- The Node.js runtime, npm dependency tree, and production container must be kept current.
- Node.js security releases can affect a product even when the product's own source code has not changed.

These are architectural trade-offs, not benchmark findings. Actual throughput, memory consumption, and latency depend on configuration, database behaviour, authentication methods, session storage, and concurrent load.

## 5. Security assessment: October 2026 findings

### 5.1 Current release evidence

**Verification date:** 28 October 2026. The release versions below were identified in official release pages during research. Verify the current release pages again before deployment.

| Product | Latest stable release observed | Evidence and security significance |
|---|---|---|
| Keycloak | `26.8.1` | Reported released 13 October. Earlier `26.7.5` explicitly fixes several security issues, including CVE-2026-16103 and CVE-2026-18203 through CVE-2026-18208. Confirm which fixes are included in `26.8.1`. |
| authentik | `2026.8.5` | Reported released 21 October. Recent advisories include high-severity SAML, MFA, and privilege-escalation issues. Verify advisory-specific fixed versions. |
| ZITADEL | `4.20.0` | Reported released 22 October. Release notes document Go 1.26.10 and `golang.org/x/net` v0.60.0. Earlier `4.19.2` fixed two high-severity identity issues and one low-severity issue. |
| Logto | `1.45.0` | Reported released 13 October. Release history includes security hardening for SSRF and OAuth-related functionality. Verify the complete current advisory list and deployed dependency versions. |
| Casdoor | `4.11.0` | Reported released 26 September. Release notes list fixes for OAuth, MFA, SSRF, cross-organization permissions, and other security-sensitive functionality. A complete CVE-to-fix mapping was not established here. |
| Ory Kratos | `26.2.0` | The official release page lists this version, but the retrieved release date is March 2026. A more recent stable release was not verified in the available evidence; confirm before selecting a version. |
| SuperTokens Core | `12.4.1` | Reported released 23 October. Release history includes work on security-release publishing and image promotion by digest. This is not proof that every applicable vulnerability has been fixed. |

**Release policy:** Never choose a product merely because its release is recent. Select a supported version with explicit fixes, then verify the exact image digest, runtime version, and dependency inventory.

### 5.2 Security incidents affecting identity platforms

Severity labels below reflect cited advisories where available. Exact CVSS scores and fixed-version ranges must be taken from individual advisory records.

| Product / advisory | Issue and severity | Patch verification required |
|---|---|---|
| authentik — `GHSA-qgqp-xh8r-v73r` | High: MFA bypass involving recipient override in the email authenticator; published 9 September 2026 | Confirm advisory fixed release and test email-based MFA, recipient binding, and recovery flows. |
| authentik — `GHSA-35v6-hv2g-6992` | High: account takeover involving SAML NameID comment truncation; published 15 July 2026 | Verify fixed version and test federated account matching and NameID validation. |
| authentik — `GHSA-rv9x-92g6-9cpf` | High: RAC endpoints and stored credentials exposed to authenticated users, with potential cross-application boundary violations; published 15 July 2026 | Verify fixed version and test application isolation and credential access. |
| authentik — `GHSA-h6c5-mpvq-j4jc` | High: privilege escalation through delegated group and user management; published 9 September 2026 | Test least-privilege administration and delegated role boundaries. |
| authentik — `GHSA-cxwx-9x59-28qm` | High: denial of service through malformed SAML messages; published 9 September 2026 | Verify patch and test malformed SAML input handling. |
| authentik — `GHSA-xp7f-xjjx-gwm8` | Critical: SourceStage bypass via an empty POST; published 28 May 2026 | Verify fixed release and test authentication-flow enforcement. |
| ZITADEL — `GHSA-x4c7-fpcx-w9q6` | High: SAML identity-provider confusion potentially leading to account takeover | Release notes explicitly identify the fix in `4.19.2`; confirm deployed release contains it. |
| ZITADEL — `GHSA-jh92-5mrj-p2w2` | High: account takeover through an unsigned Login V2 session cookie | Release notes explicitly identify the fix in `4.19.2`. Configure a strong `ZITADEL_SESSION_COOKIE_SECRET` as directed. |
| ZITADEL — `GHSA-w4gv-rcwj-w6r5` | Low: end-user impersonators could impersonate administrators | Release notes identify a fix in `4.19.2`; confirm deployed version and authorization behaviour. |
| Ory Kratos — `GHSA-hgx2-28f8-6g2r` | High: SQL injection via forged pagination tokens; published 20 March 2026 | Confirm advisory fixed version and test pagination-token validation. Exact fixed version was not established in the retrieved evidence. |

These findings do not prove the projects remain vulnerable in their latest releases. They demonstrate why fixed version ranges must be checked individually.

For authentik, the advisory history includes several high- and critical-severity findings during 2026. Its `2026.8.5` release is recent, but the release snippet alone does not prove all listed vulnerabilities are fixed in that version. Treat the mapping as unverified until official release notes for each advisory confirm it.

### 5.3 Runtime vulnerabilities: Node.js and PHP

A product can patch its own application code while remaining exposed through its runtime or bundled libraries. Runtime incidents are relevant even when the IAM product itself is not written in the affected language.

#### Node.js: CVE-2026-111497

**Issue:** Brotli decoder out-of-bounds write.  
**CVSS v3.1:** 9.8, critical.  
**Disclosure:** October 2026 security release.

The vulnerability affects the Brotli decoder bundled with Node.js. An application that decompresses attacker-controlled Brotli input through `node:zlib` can potentially suffer memory corruption, information disclosure, denial of service, or remote code execution.

The official Node.js security release identifies these fixed versions:

| Release line | Fixed version |
|---|---:|
| Node.js 22 | `22.23.4` |
| Node.js 24 | `24.22.1` |
| Node.js 26 | `26.12.1` |

Versions before the listed patch releases in those lines are affected.

**Impact:** Logto's Node.js runtime must be checked against these fixed versions. Logto version `1.45.0` alone does not establish which Node.js binary its production container uses. Inspect the actual image and SBOM, then verify the runtime patch level.

**Acceptance condition:** No affected Node.js runtime remains in the production image, including inherited or sidecar images where applicable.

#### PHP: CVE-2026-109618 and CVE-2026-109619

The official PHP news archive records a security release on 21 October 2026 for PHP 8.5.12, 8.4.27, 8.3.36, and 8.2.35. The PHP team described both vulnerabilities as critical and capable of unauthenticated remote code execution, and stated that no complete mitigation was available other than upgrading.

| PHP release line | Security release to verify |
|---|---:|
| PHP 8.5 | `8.5.12` |
| PHP 8.4 | `8.4.27` |
| PHP 8.3 | `8.3.36` |
| PHP 8.2 | `8.2.35` |

The retrieved announcement establishes affected release lines and recommended fixed releases, but individual advisory details, component-level affected ranges, and CVSS scores should be retrieved before assigning a more precise technical classification.

On 26 October, PHP also published updated Windows builds containing Brotli 1.2.1 to address `CVE-2026-111497`, reachable through cURL when automatic response decompression is enabled.

**Impact:** PHP is not identified as a core production runtime for the shortlisted products. These PHP CVEs should not be attributed directly to Keycloak, authentik, ZITADEL, or Logto without evidence that an affected PHP component is deployed. They remain relevant if the overall environment includes PHP applications, gateways, custom integrations, or auxiliary services.

### 5.4 Java, Go, Python, and dependency assessment

A complete, verified list of applicable 2026 CVEs for every dependency in every product was not established by the retrieved evidence. The following checks are mandatory.

| Component | Evidence and required action |
|---|---|
| Java / Quarkus | For Keycloak, inspect the exact Java runtime in the image, bundled libraries, and official Keycloak security advisories. A Keycloak release number alone does not prove all Java CVEs are remediated. |
| Go | ZITADEL `4.20.0` explicitly records a build with Go `1.26.10` and `golang.org/x/net` `v0.60.0`. Compare both against relevant Go security advisories. |
| Python / Django | authentik's release history records a Django update to `5.2.17` in a `2026.2.7` maintenance release. This is evidence of dependency maintenance, not full security clearance for `2026.8.5`. |
| Node.js / npm | For Logto, verify Node.js version, lockfile dependencies, and production-only package inventory. Apply the October Node.js security release if the deployed runtime is affected. |
| Go modules / SQL drivers | For Ory and Casdoor, scan compiled module metadata and source manifests; compare findings against official Go advisories and product release notes. |
| Operating-system packages | Inspect the final image for vulnerable OpenSSL, libc, compression libraries, CA certificates, and other OS packages. Upgrade the image even if the application dependency scan is clean. |

### 5.5 CVE register: established evidence and open items

| Vulnerability | Affected component | Fixed version / evidence | Status for this study |
|---|---|---|---|
| CVE-2026-111497 | Node.js Brotli decoder | Node.js `22.23.4`, `24.22.1`, `26.12.1`; PHP Windows rebuilds also include Brotli 1.2.1 | Fixed versions documented; deployed image must be checked. |
| CVE-2026-109618 | PHP | PHP `8.5.12`, `8.4.27`, `8.3.36`, `8.2.35` | Official PHP release identifies fixed releases; detailed advisory mapping still required. |
| CVE-2026-109619 | PHP | PHP `8.5.12`, `8.4.27`, `8.3.36`, `8.2.35` | Official PHP release identifies fixed releases; detailed advisory mapping still required. |
| CVE-2026-16103 | Keycloak | Listed as a fix in Keycloak `26.7.5` | Confirm inclusion and applicability in `26.8.1`. |
| CVE-2026-18203 through CVE-2026-18208 | Keycloak | Listed in the `26.7.5` security fixes | Confirm each advisory against `26.8.1`; do not infer from version number alone. |
| `GHSA-qgqp-xh8r-v73r` | authentik | High-severity MFA bypass | Exact fixed version not verified here. |
| `GHSA-35v6-hv2g-6992` | authentik | High-severity SAML account takeover | Exact fixed version not verified here. |
| `GHSA-x4c7-fpcx-w9q6` | ZITADEL | High-severity SAML IdP confusion | Fix explicitly recorded in `4.19.2`; verify selected deployment. |
| `GHSA-jh92-5mrj-p2w2` | ZITADEL | High-severity unsigned session cookie | Fix explicitly recorded in `4.19.2`; configure session secret correctly. |
| `GHSA-hgx2-28f8-6g2r` | Ory Kratos | High-severity SQL injection through pagination tokens | Exact fixed version not verified here. |

The table intentionally does not invent CVSS scores where they were not established. A completed report should link each CVE to its individual NVD record or vendor advisory, record publication and modification dates, and identify precise affected and fixed version ranges.

## 6. Feature and protocol comparison

| Product | OIDC / OAuth 2.0 | SAML 2.0 | LDAP / directory integration | MFA / passkeys | Overall fit |
|---|---|---|---|---|---|
| Keycloak | Yes | Yes | Yes; federation and directory integration | Yes | Broad enterprise IAM |
| authentik | Yes | Yes | LDAP provider and source integrations | Yes | Broad IAM and application access |
| ZITADEL | Yes | Verify exact feature set | Verify required LDAP federation or bridging pattern | Yes; feature and policy dependent | Modern identity infrastructure |
| Logto | Yes | Verify exact feature set and edition | Verify exact directory and federation requirements | Yes; feature and edition dependent | Developer-focused IAM |
| Casdoor | Yes | Supported; verify required SAML roles and flows | Directory integration available; verify configuration | Supported options depend on release | Broad IAM candidate |
| Ory Kratos + Hydra | Yes, through Hydra and related components | Verify separate SAML integration requirements | Verify separate integration requirements | Component and configuration dependent | Composable identity platform |
| SuperTokens | OAuth-related flows and application authentication; verify issuer requirements | Verify external SAML integration needs | Not a full directory-federation replacement by itself | Yes | Application authentication |
| FusionAuth | Yes | Supported capabilities depend on edition and configuration | Verify required LDAP integration | Yes | Application and enterprise identity |

LDAP support is not the same as acting as an LDAP server, federating against Active Directory, or providing complete directory synchronization. Similarly, supporting SAML as a service provider does not necessarily mean a product can act as a SAML identity provider.

If the requirement includes corporate SSO, AD/LDAP federation, SAML applications, and OAuth/OIDC for internal services, authentik and Keycloak deserve particular attention. If the main requirement is modern application login and token issuance, Logto, ZITADEL, and SuperTokens may be more appropriate.

## 7. Advantages and disadvantages

### 7.1 authentik

**Advantages**
- Broad self-hosted IAM capabilities and configurable authentication flows.
- Useful for protecting internal applications and integrating identity with existing infrastructure.
- Docker and Kubernetes deployment options.
- Python/Django ecosystem is familiar to many web engineers.
- LDAP, SAML, and OIDC capabilities make it worth evaluating as a general-purpose replacement.

**Disadvantages**
- More deployment components to maintain than a single application container may suggest.
- Worker, database, and other service requirements must be planned and monitored.
- Recent high-severity advisories mean patch verification and authentication regression testing are especially important.
- Enterprise features and support arrangements must be reviewed against the applicable licence.

**Assessment:** A strong first proof of concept for a self-hosted replacement. Do not approve it until the 2026 advisory-to-fixed-version mapping is complete.

### 7.2 ZITADEL

**Advantages**
- Go-based service and modern identity APIs.
- PostgreSQL-backed architecture.
- Multi-organization and application identity model.
- Recent release notes provide concrete security-fix and runtime-version evidence.
- Suitable for teams that prefer API-driven identity management.

**Disadvantages**
- Organization/project model differs from Keycloak's realm-oriented model.
- Migration may require redesigning authorization, tenant boundaries, and application configuration.
- Recent SAML and session-cookie findings require explicit regression tests.
- Some enterprise capabilities and support options may require a paid plan.

**Assessment:** A compelling candidate for a modern identity platform, especially where API-driven operations and multi-tenancy matter.

### 7.3 Logto

**Advantages**
- Developer-focused authentication workflows and SDKs.
- TypeScript/Node.js ecosystem.
- PostgreSQL-backed architecture.
- Suitable for modern web and mobile applications.
- Recent releases demonstrate ongoing development of security controls and migration features.

**Disadvantages**
- Not necessarily a complete replacement for every Keycloak federation and administration use case.
- Node.js runtime patching is an operational requirement, not optional.
- Self-hosted premium features and licensing need careful evaluation.
- Enterprise SAML, directory, and authorization requirements must be checked against the chosen edition.

**Assessment:** Strong for application-centric IAM. Less compelling as a direct replacement if the principal objective is comprehensive enterprise identity federation.

### 7.4 Casdoor

**Advantages**
- Go-based backend and multiple database options.
- Broad authentication-provider integration model.
- Container deployment and customization opportunities.
- A candidate for organizations seeking an extensible, self-hosted IAM platform.

**Disadvantages**
- Supported database and federation matrix needs release-specific confirmation.
- Security hardening commits are valuable but do not substitute for a complete advisory register.
- The team must establish a clear process for reviewing upstream fixes and updating images.
- Feature parity and migration tooling may require additional engineering.

**Assessment:** Worth testing, but do not rank it above candidates with stronger verified evidence until its security and compatibility checks are complete.

### 7.5 Ory Kratos and Hydra

**Advantages**
- Separates identity management from OAuth2/OIDC authorization.
- Go-based services and composable architecture.
- Useful for teams wanting control over login interfaces and application-specific identity flows.
- Can support a well-defined service-oriented architecture.

**Disadvantages**
- Kratos and Hydra do not provide the same all-in-one administrator experience as Keycloak.
- Additional components may be needed for authorization, federation, directory integration, and user interfaces.
- Operational complexity increases as more components are introduced.
- The March 2026 Kratos advisory concerning SQL injection must be checked against the exact deployed version.

**Assessment:** Best for engineering teams that want composability and can own the integration work. Not the simplest drop-in replacement.

### 7.6 SuperTokens

**Advantages**
- Focused application-authentication workflows.
- Sessions, MFA, social login, and application SDK integrations.
- Practical for developers integrating authentication into an existing product.
- Multiple application-language SDKs.

**Disadvantages**
- Not equivalent to Keycloak's full enterprise federation and identity administration feature set.
- LDAP, SAML federation, and centralized enterprise IAM requirements may need other products or integrations.
- Application integration patterns differ from using a standalone enterprise identity provider.

**Assessment:** Strong for application authentication, but not a default choice for replacing enterprise IAM.

### 7.7 Keycloak baseline

**Advantages**
- Broad IAM functionality, including SSO, OIDC/OAuth, SAML, directory integration, and identity brokering.
- Mature extension ecosystem and extensive deployment documentation.
- Established container and Kubernetes deployment approaches.
- Release process explicitly distinguishes patch releases and security fixes.

**Disadvantages**
- Java runtime and JVM tuning add operational considerations.
- Database and cache configuration must be managed carefully at scale.
- Custom extensions can complicate upgrades.
- Recent security fixes still need to be reviewed and applied promptly.

**Assessment:** Do not replace Keycloak just because a competitor uses Go or Node.js. A replacement must deliver a meaningful improvement in security, operating cost, maintainability, or required functionality.

## 8. Licensing, support, and operating cost

This is a licensing review framework, not a legal opinion. Verify the exact repository licence, edition, and current commercial terms before purchasing or deploying.

| Product | Licensing / commercial considerations | Main operational costs |
|---|---|---|
| Keycloak | Apache License 2.0 | Runtime, database, caching, backups, monitoring, upgrades, staffing |
| authentik | Open-source core with enterprise/commercial offerings; check exact current licence and feature matrix | Server, database, workers, integrations, storage, support |
| ZITADEL | Apache-licensed core with commercial offerings; verify feature and support boundaries | PostgreSQL, application service, replicas, backups, monitoring |
| Logto | Open-source core with paid self-hosted and managed options; verify current licence and premium entitlements | PostgreSQL, Node.js service, upgrades, support, optional paid features |
| Casdoor | Apache-licensed project; verify precise repository and dependency licences | Application, database, integrations, maintenance |
| Ory | Open-source components plus commercial Ory Network offerings; verify component and support terms | Multiple services, databases, integration engineering, or managed-service fees |
| SuperTokens | Open-source core and commercial offerings; verify current enterprise entitlements | Core service, database, SDK maintenance, support |
| FusionAuth | Commercial product with free and paid tiers; verify edition restrictions and support plans | Licence, server/database infrastructure, optional support |

### Total cost of ownership categories

Do not compare products by container size alone. Estimate:

- Compute and memory for the identity service and any workers.
- Managed or self-hosted PostgreSQL and storage.
- High availability, replicas, load balancing, and disaster recovery.
- Email/SMS delivery, MFA, external identity providers, and network traffic.
- Centralized logs, metrics, traces, alerting, and security scanning.
- Engineer time for upgrades, patch verification, and incident response.
- Enterprise licensing and support SLAs, if required.

For a small proof of concept, one application instance and one development database may be sufficient. That is not a production sizing recommendation. Production capacity must be determined through load tests, availability requirements, and recovery objectives.

## 9. Practical proof-of-concept deployment and testing plan

Run the same test suite against Keycloak and the three shortlisted alternatives: authentik, ZITADEL, and Logto. This keeps the comparison fair and produces evidence that can be reviewed.

### Phase 1: Deploy and baseline

Use Docker Compose for the initial comparison.

- Pin each application image to a verified release and digest.
- Use PostgreSQL where supported by the product's official deployment guidance.
- Persist database data in a named volume or managed database.
- Keep databases and internal service ports off the public network.
- Configure HTTPS through a reverse proxy or test ingress.
- Store credentials in a secrets manager or protected deployment secret mechanism.
- Do not use development-mode defaults for a production-like deployment.

Collect container startup time, idle CPU and memory, database connections, and health-check results. Record host specifications and all configuration settings.

### Phase 2: Authentication and authorization

Integrate each candidate with the same sample web application using OIDC.

Test:
1. Authorization Code flow with PKCE.
2. Login, logout, refresh-token rotation, and session expiry.
3. MFA enrollment, recovery, and enforcement.
4. Invalid, expired, and wrong-audience tokens.
5. Role-based access control and tenant isolation.
6. User provisioning, account deactivation, and access revocation.
7. SAML federation if part of the actual requirement.
8. LDAP or Active Directory integration if required.
9. Rate limiting, brute-force protections, and account-recovery flows.

Record pass/fail results, required custom code, and product-specific workarounds.

### Phase 3: Supply-chain and vulnerability scanning

Use these tools where appropriate:

- **Trivy:** scan images, filesystem dependencies, misconfigurations, and secrets; generate SBOMs where appropriate.
- **Grype:** run an independent vulnerability scan against the same images and compare findings.
- **OWASP Dependency-Check:** useful for known vulnerabilities in supported dependency ecosystems; complement it with image and runtime scanning.

Example commands:

```bash
# Scan a pinned product image
trivy image --scanners vuln,misconfig,secret \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  registry.example.com/iam-product@sha256:YOUR_VERIFIED_DIGEST

# Generate an SBOM
trivy image --format cyclonedx \
  --output sbom.cdx.json \
  registry.example.com/iam-product@sha256:YOUR_VERIFIED_DIGEST

# Run an independent vulnerability scan
grype registry.example.com/iam-product@sha256:YOUR_VERIFIED_DIGEST
```

Replace the placeholder image with the exact official image reference and digest. Do not copy the example registry or digest into a real deployment.

Use language-specific dependency analysis as well:

- **Java:** Maven/Gradle dependency analysis and OWASP Dependency-Check.
- **Node.js:** `npm audit` against the appropriate lockfile and production dependency set.
- **Python:** `pip-audit` or an equivalent package scanner.
- **Go:** `govulncheck` and module dependency analysis.
- **OS packages:** Trivy or Grype against the final image.

A scanner may not detect every vulnerability in statically compiled binaries. Cross-check vendor advisories and image build metadata.

### Phase 4: Operational resilience

- Perform a database backup and restore into a clean environment.
- Test an upgrade from the selected previous supported release.
- Verify users, clients, sessions, keys, and configuration survive the upgrade as expected.
- Test rollback using a documented recovery procedure; do not assume an older application can use a database after an irreversible schema migration.
- Test graceful restart and service recovery.
- Simulate database unavailability and inspect error handling.
- Test performance under realistic concurrent login and token-refresh traffic.
- Document resource usage, latency, errors, and database connections.

### Phase 5: Production readiness checklist

- [ ] **Supported release:** Exact application version and support status confirmed.
- [ ] **Advisories reviewed:** Applicable critical/high issues mapped to fixed versions or approved backports.
- [ ] **Image and SBOM:** Production image digest, runtime, dependencies, and OS packages verified.
- [ ] **Authentication tests:** OIDC, MFA, sessions, authorization, and required federation tests pass.
- [ ] **Secrets and TLS:** No default secrets; HTTPS, key rotation, and secure cookie settings verified.
- [ ] **Recovery and upgrade:** Backup restoration, upgrade, and rollback procedures demonstrated.
- [ ] **Load and observability:** Performance baseline, logs, metrics, health checks, and alerts documented.

Completing the checklist is a tracking aid, not automatic security approval.

## 10. Final ranked recommendation

This is a **research-priority ranking**, not a claim that all three candidates have passed the security gate.

### 1. authentik — first broad IAM proof of concept

**Why:** Self-hosted identity capabilities, flexible authentication flows, directory integration, and broad application-access functionality.

**Main risk:** Several 2026 high- and critical-severity advisories need exact fixed-version verification. Do not approve `2026.8.5` until this is complete.

### 2. ZITADEL — modern identity-platform candidate

**Why:** Multi-tenancy, API-driven management, Go-based architecture, and useful release-note evidence for recent security fixes.

**Main risk:** Confirm that the deployed version includes the documented fixes and that Login V2 has a strong, correctly configured session-cookie secret.

### 3. Logto — application-centric candidate

**Why:** Application authentication, developer SDKs, and modern OIDC-based integration.

**Main risk:** Verify the actual Node.js runtime against the October 2026 security releases, then confirm whether the product covers all required enterprise federation features.

### Should Keycloak be replaced?

Not yet on the evidence collected.

If the requirement is a broad, self-hosted enterprise IAM platform, Keycloak should remain in the proof of concept as the baseline. Its recent security fixes also need verification: the presence of a newer release is not sufficient proof that all relevant advisories are resolved.

If the requirement is narrower—application login, OIDC, MFA, and developer SDKs—Logto or SuperTokens may offer a better fit. If composability and custom identity workflows are priorities, Ory deserves a separate evaluation. Casdoor should remain on the candidate list until its release, security, and compatibility evidence has been examined in comparable depth.

**Security acceptance conclusion:** None of the alternatives can be declared fully security-approved from this research alone. This does not mean that they are insecure; it means the available evidence is insufficient to certify that every applicable critical- and high-severity issue has been fixed in the exact production artifact.

## 11. Outstanding research items

Before presenting this as a final engineering recommendation, close these gaps:

1. Retrieve individual vendor advisory records for every listed product and map each applicable vulnerability to affected and fixed versions.
2. Confirm current supported release branches and support policies for all candidates.
3. Inspect official Dockerfiles, image manifests, and SBOMs to establish exact production runtime versions and base images.
4. Verify complete OIDC, OAuth 2.0, SAML, LDAP, MFA, and authorization feature matrices against the actual requirements.
5. Confirm current licences, self-hosted enterprise restrictions, support SLAs, and managed-service pricing.
6. Run the same deployment, security, performance, backup, and upgrade tests against each finalist.
7. Record every unverified issue explicitly rather than treating a missing advisory as evidence that no vulnerability exists.

## 12. Primary source directory

Use these official records to complete the remaining checks:

- [Keycloak releases](https://github.com/keycloak/keycloak/releases)
- [authentik releases](https://github.com/goauthentik/authentik/releases)
- [authentik security advisories](https://github.com/goauthentik/authentik/security/advisories)
- [ZITADEL releases](https://github.com/zitadel/zitadel/releases)
- [Logto releases](https://github.com/logto-io/logto/releases)
- [Casdoor releases](https://github.com/casdoor/casdoor/releases)
- [Ory Kratos releases](https://github.com/ory/kratos/releases)
- [Ory Kratos security advisories](https://github.com/ory/kratos/security/advisories)
- [SuperTokens Core releases](https://github.com/supertokens/supertokens-core/releases)
- [Node.js October 2026 security releases](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
- [PHP 2026 security and release archive](https://www.php.net/archive/2026.php)
- [NVD vulnerability database](https://nvd.nist.gov/vuln/search)

## Conclusion

Start with authentik and ZITADEL for broad IAM, and Logto for application-centric authentication. Run the same proof of concept against Keycloak. Promote only the candidate that passes the security acceptance gate and demonstrates a meaningful operational or functional advantage.
"""

output_path = "C:/Users/USER/Desktop/school_project/cv_code/keycloak_alternatives_research.md"
pypandoc.convert_text(
    markdown,
    "md",
    format="md",
    outputfile=output_path,
    extra_args=["--standalone"]
)

import os
assert os.path.exists(output_path) and os.path.getsize(output_path) > 10000
print(f"Created: {output_path}\nSize: {os.path.getsize(output_path):,} bytes")
