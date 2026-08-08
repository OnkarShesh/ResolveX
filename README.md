# 🤖 ResolveX

### AI-Powered Customer Support Ticket Automation System

ResolveX is an AI-powered customer support ticket management system that automates the support workflow from **ticket submission and AI classification to response generation, email delivery, and ticket tracking**.

The system uses **Groq LLMs** for ticket analysis and response generation, **Google Sheets** for ticket storage, and **Gmail SMTP** for automated customer communication.

---

## 🚀 Features

- 🎫 Customer support ticket submission
- 🤖 AI-based sentiment and issue classification
- ✍️ AI-generated customer replies
- 📧 Automated email responses through Gmail SMTP
- 📋 Pending and processed ticket management
- 🎯 Ticket filtering by issue category
- ☑️ Individual and bulk ticket selection
- 🗑️ Individual and bulk ticket deletion
- 📊 Support ticket dashboard and analytics
- 📁 CSV export of processed tickets
- ☁️ Google Sheets-based ticket storage

---

## 🔄 Workflow

```text
Customer
   ↓
Submit Support Ticket
   ↓
Google Sheets → PendingTickets
   ↓
AI Classification
   ├── Sentiment
   └── Issue Type
   ↓
AI Reply Generation
   ↓
Support Agent Review
   ↓
Gmail SMTP
   ↓
Customer receives reply
   ↓
Google Sheets → ProcessedTickets
```

---

## 🧠 AI Capabilities

ResolveX uses the **Groq API** with the `llama-3.3-70b-versatile` model for ticket analysis and response generation.

### 🎯 Ticket Classification

Each support ticket is analyzed and classified based on:

**Sentiment**
- Positive
- Negative
- Neutral

**Issue Type**
- Billing
- Technical
- Login
- General
- Other

### ✍️ AI Reply Generation

The system generates a professional and personalized response using the customer's name and issue description.

Example:

```text
Hello Onkar,

We understand the issue you are experiencing and appreciate
you reaching out to our support team. Our team is reviewing
your request and will assist you with the issue shortly.

Best regards,
Customer Support Team
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| AI / LLM | Groq API, Llama 3.3 70B |
| Data Storage | Google Sheets |
| Google Sheets API | gspread |
| Email | Gmail SMTP |
| Data Processing | Pandas, Matplotlib |
| Configuration | python-dotenv |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```text
ResolveX/
│
├── main.py
├── register_ticket.py
├── requirements.txt
├── .gitignore
│
└── tools/
    ├── classify_ticket.py
    ├── generate_reply.py
    ├── gmail_sender.py
    └── sheet_connector.py
```

### 📄 File Overview

| File | Purpose |
|------|---------|
| `main.py` | Main Streamlit dashboard and ticket management |
| `register_ticket.py` | Customer ticket submission interface |
| `classify_ticket.py` | AI-based sentiment and issue classification |
| `generate_reply.py` | AI-generated customer response |
| `gmail_sender.py` | Gmail SMTP email delivery |
| `sheet_connector.py` | Google Sheets data operations |
| `requirements.txt` | Project dependencies |
| `.gitignore` | Prevents sensitive and unnecessary files from being committed |

---

## ☁️ Google Sheets Storage

ResolveX uses **Google Sheets as a lightweight cloud-based data store**.

The `SupportTickets` spreadsheet contains two worksheets:

```text
SupportTickets
│
├── PendingTickets
│
└── ProcessedTickets
```

### 📋 PendingTickets

Stores customer tickets waiting to be analyzed and processed.

### ✅ ProcessedTickets

Stores processed tickets along with their classification, sentiment, and generated response for historical tracking.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/OnkarShesh/ResolveX.git
cd ResolveX
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

### Windows PowerShell

```powershell
.\venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
EMAIL_ADDRESS=your_gmail_address
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Also place your Google service-account credentials in:

```text
google_cred.json
```

The Google service account must have access to the **SupportTickets** Google Spreadsheet.

> ⚠️ Never commit `.env` or `google_cred.json` to GitHub.

---

# ▶️ Running ResolveX

ResolveX has **two Streamlit applications** that can be run separately.

## 1. 🎫 Customer Ticket Submission

Start the customer-facing ticket submission interface:

```bash
streamlit run register_ticket.py
```

This opens the customer ticket submission page.

Customers can enter:

- Full Name
- Email Address
- Issue Type
- Issue Description

After submission, the ticket is automatically stored in:

```text
Google Sheets → PendingTickets
```

---

## 2. 🤖 AI Ticket Manager

Open another terminal, activate the same virtual environment, and run:

```bash
streamlit run main.py
```

The AI Ticket Manager allows the support team to:

- 📋 View pending tickets
- 🤖 Analyze tickets using AI
- 😊 View ticket sentiment
- 🎯 View issue categories
- ✍️ Generate AI replies
- 📧 Send replies through Gmail SMTP
- ☑️ Select multiple tickets
- 📤 Send replies to selected tickets
- 🗑️ Delete individual tickets
- 🗑️ Delete selected tickets
- 📊 View processed tickets
- 📁 Export processed ticket data as CSV

---

# 🔁 Complete Execution Flow

```text
                 ┌──────────────────────┐
                 │       Customer       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Submit Support Ticket│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    PendingTickets    │
                 │    Google Sheets     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   AI Classification  │
                 │                      │
                 │ • Sentiment          │
                 │ • Issue Type         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  AI Reply Generation │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Support Agent Review│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Gmail SMTP      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Customer receives    │
                 │       reply          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   ProcessedTickets   │
                 │    Google Sheets     │
                 └──────────────────────┘
```

---

# 📸 Screenshots

### 🎫 Customer Ticket Submission

_Add screenshot here_

### 📋 Pending Tickets

_Add screenshot here_

### 🤖 AI Ticket Analysis

_Add screenshot here_

### 📊 Processed Tickets & Analytics

_Add screenshot here_

---

# 🔒 Security

ResolveX keeps sensitive credentials outside the GitHub repository.

The following files should remain local:

```text
.env
google_cred.json
venv/
.venv/
__pycache__/
*.pyc
```

API keys, email credentials, and Google service-account credentials should **never** be committed to GitHub.

If credentials are accidentally exposed, they should be revoked and replaced immediately.

---

# 🔮 Future Improvements

- 🔐 Role-based support-agent authentication
- 🚨 Automatic ticket priority detection
- 📊 Advanced support analytics
- 💬 Conversation history
- 🔁 Automated customer follow-ups
- 🗄️ PostgreSQL database integration
- 🐳 Docker deployment
- ☁️ Cloud deployment
- 🔔 Real-time notifications
- 📈 Advanced ticket performance metrics

---

# 👨‍💻 Author

**Onkar Shesh**

B.Tech — Computer Science and Business Systems

[GitHub](https://github.com/OnkarShesh)

---

## ⭐ Project

ResolveX demonstrates an end-to-end AI-powered customer support workflow combining **LLM-based automation, cloud data storage, email communication, and an interactive support dashboard**.

If you find the project useful, consider giving the repository a ⭐ on GitHub.