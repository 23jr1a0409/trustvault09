# TrustVault – AI Prompts Documentation

## Day 1: Security Threats & Documentation

**Prompt 1:**
"Identify the major security threats in my TrustVault secure document-sharing application and suggest ways to prevent them."

**Response Summary:** AI identified potential threats such as unauthorized access, weak password security, insecure file uploads, SQL injection, and brute-force attacks. It suggested authentication, access control, input validation, and rate limiting as possible security measures.

**What I implemented:**
- Created `THREATS.md` to document security risks.
- Identified potential threats to confidential documents.
- Documented possible mitigation measures.

**Learning:** Threat modeling helps identify security risks and plan suitable protections for a secure document-sharing application.
---

## Day 2: Authentication and Access Control

**Date:** 2026-10-22

**Prompt 1:**
"How should I implement authentication and role-based access control in my Flask secure document-sharing application?"

**Response Summary:** AI explained that authentication verifies a user's identity, while authorization determines which documents and actions the user is allowed to access.

**What I implemented:**
- Reviewed the authentication and authorization requirements for TrustVault.
- Identified the need to restrict confidential documents to authorized users.
- Documented the security measures that must be tested before deployment.

**What was wrong:** A basic Flask homepage alone does not provide authentication or enforce document permissions.

**Learning:** Authentication and authorization are different security controls. Both must be implemented and tested before protecting real documents.

---

## Day 3: Secure File Uploads

**Date:** 2026-10-23

**Prompt 1:**
"How can I securely handle document uploads in a Flask document-sharing application?"

**Response Summary:** AI suggested validating uploaded files, restricting permitted file types and sizes, generating safe filenames, and preventing unauthorized access to stored documents.

**What I implemented:**
- Identified file-upload validation as a security requirement.
- Documented risks related to unsafe filenames and untrusted file types.
- Listed upload validation and access-control checks needed before deployment.

**What was wrong:** Accepting files without validation can expose an application to malicious or unexpected uploads.

**Learning:** File uploads require validation and safe storage. These protections must be implemented and tested before claiming uploads are secure.

---

## Day 4: Rate Limiting and Security Hardening

**Date:** 2026-10-23

**Prompt 1:**
"How can I use Flask-Limiter to reduce brute-force attempts against login and registration endpoints?"

**Response Summary:** AI suggested configuring request limits for authentication endpoints and selecting an appropriate storage backend.

**What I implemented:**
- Reviewed the need for rate limits on login and registration routes.
- Identified endpoint-specific limits as a security requirement.
- Documented the need to test rate-limit responses.

**What was wrong:** Merely installing a rate-limiting package does not protect routes unless the limiter is configured and applied correctly.

**Learning:** Rate limiting should be tested on the actual endpoints. A 429 response should be verified before claiming the protection works.

---

## Day 5: Audit Trail and Permission Changes

**Date:** 2026-10-23

**Prompt 1:**
"How should I design an audit trail to record document access and permission changes in TrustVault?"

**Response Summary:** AI explained that an audit trail should record relevant events, the acting user, the affected document, the action, and a timestamp. Access to audit records should also be restricted.

**What I implemented:**
- Identified document access and permission changes as audit events to track.
- Documented the need to restrict audit-log access to authorized roles.
- Listed audit-event recording and access-control checks required before deployment.

**What was wrong:** A log that records only general messages may not provide enough information to investigate unauthorized access or permission changes.

**Learning:** Audit logs should be useful for investigations, protected against unauthorized modification, and tested to ensure important events are recorded.