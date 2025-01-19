# User Stories for VaultX Technologies

## Feature Group: PII Detection and Encryption

### 1. Real-Time PII Detection
- **As a** customer service agent,
- **I want** sensitive information (e.g., names, SSNs, credit card numbers) detected in real-time chat messages,
- **So that** I can ensure compliance with data privacy regulations.
- **Acceptance Criteria:**
  - Regex-based and AI-based (NER) PII detection runs on all incoming messages.
  - Detected PII is masked in the agent's interface.
  - Logs store encrypted versions of detected PII.

---

### 2. PII Encryption for Storage
- **As a** data security officer,
- **I want** all PII data encrypted before storage in our database,
- **So that** it remains secure and inaccessible to unauthorized users.
- **Acceptance Criteria:**
  - Data stored in the database is encrypted using AES-256 encryption.
  - Key rotation occurs every 30 days or after 1,000 uses.
  - Decryption can only be performed by authenticated API requests.

---

### 3. Support for File Uploads
- **As a** compliance officer,
- **I want** the system to detect PII in uploaded files (PDFs, Word documents),
- **So that** sensitive information in customer-submitted files is also protected.
- **Acceptance Criteria:**
  - Supported file formats include `.pdf`, `.docx`, and `.txt`.
  - Detected PII is encrypted and replaced with placeholders in downloaded redacted files.

---

## Feature Group: Dashboard Management

### 4. Real-Time Monitoring
- **As a** security manager,
- **I want** a real-time dashboard showing PII detection and encryption activities,
- **So that** I can monitor compliance efforts.
- **Acceptance Criteria:**
  - Dashboard updates every 5 seconds with PII detection events.
  - Includes data type breakdowns (e.g., emails, phone numbers, SSNs).
  - Displays encryption key usage statistics.

---

### 5. User Consent Management
- **As a** product owner,
- **I want** users to provide consent before their PII is processed,
- **So that** we comply with GDPR and similar regulations.
- **Acceptance Criteria:**
  - Consent dialog box appears before form submissions.
  - Audit logs track consent with timestamps and user IDs.

---

## Feature Group: Alerts and Notifications

### 6. Breach Notifications
- **As a** compliance officer,
- **I want** the system to notify me immediately when unauthorized PII access is detected,
- **So that** I can respond quickly to potential data breaches.
- **Acceptance Criteria:**
  - Email and SMS alerts are triggered on unauthorized access attempts.
  - Logs include details about the attempted access (IP address, time, etc.).

---

### Prioritization and Technical Notes
1. High Priority:
   - Real-Time PII Detection
   - PII Encryption for Storage
2. Medium Priority:
   - File Upload Support
   - Dashboard Management
3. Low Priority:
   - User Consent Management
   - Alerts and Notifications

---