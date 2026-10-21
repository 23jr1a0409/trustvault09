# TrustVault – Security Threats Documentation

## Day 1: Threat Modeling & Security Hardening

**Prompt 1:**
"Identify the major security threats in my TrustVault secure document-sharing application and explain how to prevent them."

**Response Summary:** AI identified potential threats such as unauthorized access, weak password security, insecure file uploads, SQL injection, and brute-force attacks. It suggested authentication, access control, input validation, and rate limiting as possible mitigations.

**What I implemented:**
- Created `THREATS.md` to document security risks.
- Identified unauthorized document access as a potential threat.
- Listed password security and file-upload risks.
- Documented possible security measures to protect confidential documents.

**Learning:** Threat modeling helps identify security weaknesses and plan appropriate protections before deploying an application.

---

## Day 2: Brute-Force Attack Protection

**Prompt 1:**
"Explain how rate limiting in Flask can help protect TrustVault against brute-force login attacks."

**Response Summary:** AI explained how Flask-Limiter restricts repeated requests and can return HTTP 429 (Too Many Requests) when a configured request limit is exceeded.

**What I implemented:**
- Identified repeated login attempts as a security threat.
- Documented rate limiting as a possible mitigation.
- Identified login and registration endpoints as areas requiring protection.

**Learning:** Rate limiting helps reduce automated password guessing and should be combined with secure password hashing and authentication controls.

---

## Day 3: Unauthorized Document Access

**Prompt 1:**
"Explain the risks of unauthorized document access in TrustVault and how role-based access control can help prevent them."

**Response Summary:** AI explained that confidential documents may be exposed if the application does not verify user permissions. It recommended server-side authorization checks before allowing document access, downloads, or modifications.

**What I implemented:**
- Documented unauthorized access as a potential threat.
- Identified role-based access control as a mitigation.
- Listed document operations that require permission checks.

**Learning:** Every document request must be checked by the server. Hiding a document link alone does not prevent unauthorized access.

---

## Day 4: Secure File Uploads

**Prompt 1:**
"Identify file-upload security risks in TrustVault and recommend ways to prevent malicious or unauthorized files from being uploaded."

**Response Summary:** AI recommended validating file types and sizes, generating safe filenames, storing files outside publicly accessible directories, and restricting access to uploaded documents.

**What I implemented:**
- Identified insecure file uploads as a potential threat.
- Documented file validation and safe storage as mitigations.
- Identified the need for access checks before downloading files.

**Learning:** File validation and private storage help reduce the risk of malicious uploads and accidental exposure of confidential documents.

---

## Conclusion

TrustVault's threat model identifies security risks involving user accounts, confidential documents, file uploads, and repeated login attempts. The listed mitigations should be implemented and tested before the application is considered secure.