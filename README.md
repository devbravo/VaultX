# VaultX Technologies

## Overview
VaultX Technologies is at the forefront of developing AI-powered solutions to uphold data privacy and regulatory compliance, including GDPR and similar frameworks. Our innovative platform combines rule-based techniques (such as regular expressions) with advanced machine learning models (NER) to accurately detect and identify Personally Identifiable Information (PII) in chats, documents, and other data streams. PII is then encrypted and securely managed in real-time, ensuring robust protection while seamlessly integrating into business operations across diverse industries.

## Features

### Core Features:
1. **PII Detection**:
   - Real-time identification of PII in text inputs such as chatbot messages, web forms, email communication, file-uploads and shared documents.
   - Supports regex-based detection and advanced NLP models.

2. **PII Encryption**:
   - AES-256 encryption to secure sensitive information before storage.
   - Unique encryption keys for each user or session for enhanced security.

3. **Secure Storage**:
   - Encrypted databases (PostgreSQL or MongoDB) for PII.

4. **PII Decryption**:
   - Secure session tokens for retrieving and decrypting PII.
   - Automatic session expiration to prevent unauthorized reuse.

5. **Key Rotation**:
   - Regular key rotation and secure key management.

---

## Use Cases
1. **Customer Support Tickets**
  - Detect and encrypt PII in customer service interactions, such as emails or support tickets, ensuring sensitive information like account numbers, addresses, or payment details are securely managed while maintaining compliance with data privacy regulations.
2. **Financial Transactions and Reports**
  - Identify and secure PII in financial documents, such as invoices, transaction logs, or tax reports, to protect sensitive client and account information during processing, sharing, or storage.
3. **Healthcare Records and Forms**
  - Extract and anonymize PII in medical records, insurance claims, or patient forms to safeguard sensitive health data, enabling healthcare providers to comply with regulations like HIPAA while sharing data for analysis or collaboration.

---

## Technical Stack
- **Programming Languages**: Python.
- **Frameworks**: FastAPI.
- **Libraries**: Spacy, Langgraph.
- **Database**:
  - Locat storage (JSON) (encrypted).
- **Encryption**: AES-256 with secure key management.
- **Deployment**:
  - Docker for containerization.

---

## Functional Requirements
1. **PII Detection**:
   - Tokenize user inputs for PII isolation.
   - Detect sensitive information like emails, phone numbers, and names.

2. **PII Encryption**:
   - Implement AES-256 encryption.
   - Use secure key rotation policies based on time and key usage.

3. **Secure Data Storage**:
   - Segregate PII from general user data.

4. **Decryption Protocols**:
   - Use secure session tokens for linking PII.
   - Ensure decrypted data is never persisted in plain text.

---

## Non-Functional Requirements
- **Security**:
  - HTTPS for all endpoints.
  - Regular vulnerability scans and penetration testing.
- **Performance**:
  - Real-time processing with minimal latency.
- **Compliance**:
  - Adhere to GDPR, CCPA, and HIPAA guidelines.
- **Availability**:
  - High availability (99.9% uptime) with failover mechanisms.

---

## Installation

### Prerequisites
1. Python 3.10+
2. Docker and Docker Compose

### Setup Instructions 
#### With Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/vaultx-technologies/vaultx.git
   cd vaultx
   ```

2. Run Docker (optional):
   ```bash
   docker-compose up --build
   ```

#### Without Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/vaultx-technologies/vaultx.git
   cd vaultx
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     LANGSMITH_API_KEY=your_langsmith_api_key
     ```

5. Run the application:
   ```bash
   uvicorn src.app.main:app --reload
   ```

6. Run langraph server:
   ```bash
   pip install --upgrade "langgraph-cli[inmem]"
   ```

---

## Roadmap
1. **MVP**:
   - Core PII detection, encryption, and storage.
   - FastAPI-based backend.

2. **Phase 2**:
   - Multi-language PII detection.
   - Integration with chat platforms (e.g., Slack, Microsoft Teams).

3. **Future Enhancements**:
  1. **Advanced PII Anonymization Options**: 
    - Feature: Add support for automated PII anonymization in text (e.g., replacing names or addresses with pseudonyms).
    - Use Case: Allows businesses to work with anonymized datasets for analytics while ensuring compliance.
  2. **Multi-Language PII Detection**
    - Feature: Expand PII detection capabilities to include multi-language support using pre-trained multilingual NER models like SpaCy’s or Hugging Face’s models.
    - Use Case: Enables global businesses to comply with regional regulations (e.g., GDPR, CCPA) in non-English markets.
  3. **Integration with Cloud Platforms**
	  - Feature: Build integrations for cloud services like AWS, Azure, and GCP to detect and encrypt PII in their storage solutions (e.g., S3 buckets, Google Cloud Storage).
	  - Use Case: Automates compliance for companies storing PII in the cloud

---

## Contact
- **Team Name**: VaultX Technologies
- **Email**: diegofranco711@gmail.com

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


