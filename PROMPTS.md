# TrustVault – AI Prompts Documentation

## Day 1: Security Threats & Documentation

**Date:** 2026-10-21

**Prompt 1:**

"Identify the major security threats in my TrustVault secure document-sharing application and suggest ways to prevent them."

**Response Summary:**

AI identified potential security threats such as unauthorized access, weak password security, insecure file uploads, SQL injection, and brute-force attacks. It suggested authentication, access control, input validation, and rate limiting as possible security measures.

**What I Implemented:**
- Created `THREATS.md` to document security risks.
- Identified potential threats to confidential documents.
- Documented possible mitigation measures.

**What Was Wrong:**

Identifying threats and documenting possible solutions does not automatically protect the application. The security measures must be implemented and tested.

**Learning:**

Threat modeling helps identify security risks and plan suitable protections for an application.

**Related Commit:** [View project files](https://github.com/23jr1a0409/trustvault09/commit/147432f)

---

## Day 2: Authentication and Access Control

**Date:** 2026-10-22

**Prompt 1:**

"How should I implement authentication and role-based access control in my Flask secure document-sharing application?"

**Response Summary:**

AI explained that authentication verifies a user's identity, while authorization determines which resources and actions the user is allowed to access.

**What I Implemented:**
- Implemented user registration and login using Flask.
- Used password hashing for password storage.
- Protected the dashboard using Flask-Login's `@login_required`.
- Identified document-level permissions as a separate requirement.

**What Was Wrong:**

A basic homepage or login form alone cannot enforce document-level permissions. Each protected resource needs appropriate authorization checks.

**Learning:**

Authentication and authorization are different security controls. The login and dashboard functionality was implemented, but document-level permissions still need to be implemented and tested.

**Related Commit:** [View authentication commit](https://github.com/23jr1a0409/trustvault09/commit/c5c34b5)

---

## Day 3: Secure File Uploads

**Date:** 2026-10-23

**Prompt 1:**

"How can I securely handle document uploads in a Flask document-sharing application?"

**Response Summary:**

AI suggested validating uploaded files, restricting permitted file types and sizes, generating safe filenames, and preventing unauthorized access to stored documents.

**What I Implemented:**
- Identified file-upload validation as a security requirement.
- Documented risks related to unsafe filenames and untrusted file types.
- Listed upload validation and access-control checks needed before implementation.

**What Was Wrong:**

Accepting uploaded files without proper validation and access restrictions can introduce security risks. The suggestions alone do not implement secure file uploads.

**Learning:**

File uploads require validation, safe storage, and access restrictions. TrustVault's file-upload functionality has not yet been implemented.

**Related Commit:** [View prompt documentation commit](https://github.com/23jr1a0409/trustvault09/commit/2df22d7)

---

## Day 4: Rate Limiting and Security Hardening

**Date:** 2026-10-23

**Prompt 1:**

"How can I use Flask-Limiter to reduce brute-force attempts against login and registration endpoints?"

**Response Summary:**

AI suggested configuring request limits for authentication endpoints and selecting an appropriate storage backend.

**What I Implemented:**
- Identified the need for rate limits on login and registration routes.
- Documented endpoint-specific limits as a security requirement.
- Identified the need to test whether excessive requests receive an HTTP 429 response.

**What Was Wrong:**

Installing a rate-limiting package or documenting a configuration does not protect routes unless the limiter is correctly configured and applied.

**Learning:**

Rate limiting must be implemented and tested on the actual endpoints before claiming brute-force protection. Rate limiting is not currently confirmed as implemented in TrustVault.

**Related Commit:** [View prompt documentation commit](https://github.com/23jr1a0409/trustvault09/commit/2df22d7)

---

## Day 5: Audit Trail and Permission Changes

**Date:** 2026-10-23

**Prompt 1:**

"How should I design an audit trail to record document access and permission changes in TrustVault?"

**Response Summary:**

AI explained that an audit trail should record relevant events, the acting user, the affected document, the action performed, and a timestamp. Access to audit records should also be restricted.

**What I Implemented:**
- Identified document access and permission changes as events that should be tracked.
- Documented the need to restrict audit-log access to authorized users.
- Listed audit-event recording and access-control checks required before implementation.

**What Was Wrong:**

General application logs may not contain enough information to investigate document access or permission changes. An audit trail needs specific events and relevant details.

**Learning:**

Audit logs should record important security events and be protected against unauthorized access or modification. The audit-trail functionality has not yet been implemented in TrustVault.

**Related Commit:** [View prompt documentation commit](https://github.com/23jr1a0409/trustvault09/commit/2df22d7)

---

## Project Links

- **GitHub Repository:** https://github.com/23jr1a0409/trustvault09
- **Live Application:** https://trustvault09.onrender.com

