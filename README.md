# 🤖 ResolveX

### AI-Powered Customer Support Ticket Automation System

ResolveX is an AI-powered customer support ticket management system that automates the support workflow from **ticket submission and AI classification to response generation, email delivery, and ticket tracking**.

It uses **Groq LLMs** for ticket analysis and response generation, **Google Sheets** for ticket storage, and **Gmail SMTP** for automated customer communication.

---

## 🚀 Features

- 🎫 Customer support ticket submission
- 🤖 AI-based sentiment and issue classification
- ✍️ Personalized AI-generated replies
- 📧 Automated email responses through Gmail SMTP
- 📋 Pending and processed ticket management
- 🎯 Category-based ticket filtering
- ☑️ Individual and bulk ticket selection
- 🗑️ Individual and bulk ticket deletion
- 📊 Support ticket dashboard and analytics
- 📁 CSV export of processed tickets
- ☁️ Google Sheets-based cloud storage

---

## 🔄 Workflow

```text
Customer
   ↓
Submit Ticket
   ↓
PendingTickets (Google Sheets)
   ↓
AI Classification
   ├── Sentiment
   └── Issue Type
   ↓
AI Reply Generation
   ↓
Support Agent Review
   ↓
Gmail SMTP → Customer
   ↓
ProcessedTickets (Google Sheets)
```

---

## 🧠 AI Capabilities

ResolveX uses the **Groq API** with the `llama-3.3-70b-versatile` model.

### 🎯 Ticket Classification

Tickets are classified by:

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

The system generates a professional and personalized response based on the customer's name and issue description.

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| AI / LLM | Groq API, Llama 3.3 70B |
| Data Storage | Google Sheets |
| Sheets API | gspread |
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

| File | Purpose |
|------|---------|
| `main.py` | Streamlit support dashboard and ticket management |
| `register_ticket.py` | Customer ticket submission interface |
| `classify_ticket.py` | AI sentiment and issue classification |
| `generate_reply.py` | AI response generation |
| `gmail_sender.py` | Gmail SMTP email delivery |
| `sheet_connector.py` | Google Sheets operations |

---

## ☁️ Google Sheets Storage

ResolveX uses Google Sheets as a lightweight cloud data store.

```text
SupportTickets
│
├── PendingTickets
└── ProcessedTickets
```

**PendingTickets** stores incoming tickets awaiting processing.

**ProcessedTickets** stores processed tickets along with their classification, sentiment, and generated response.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/OnkarShesh/ResolveX.git
cd ResolveX
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
EMAIL_ADDRESS=your_gmail_address
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Place the Google service-account credentials in:

```text
google_cred.json
```

The service account must have access to the **SupportTickets** Google Spreadsheet.

> ⚠️ Never commit `.env` or `google_cred.json` to GitHub.

---

## ▶️ Running the Application

ResolveX has two Streamlit applications.

### 🎫 1. Customer Ticket Submission

Run:

```bash
streamlit run register_ticket.py
```

Customers can submit:

- Full Name
- Email Address
- Issue Type
- Issue Description

Submitted tickets are automatically stored in:

```text
Google Sheets → PendingTickets
```

### 🤖 2. AI Ticket Manager

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run main.py
```

The support dashboard allows agents to:

- View and analyze tickets
- Review sentiment and issue categories
- Generate AI replies
- Send replies through Gmail
- Select and process multiple tickets
- Delete tickets
- View processed tickets
- Export ticket data as CSV

---

## 📸 Screenshots

### 🎫 Customer Ticket Submission

_Add screenshot here_

### 📋 Pending & Analyzed Tickets

_Add screenshot here_

### 🤖 AI Ticket Analysis

_Add screenshot here_

### 📊 Processed Tickets & Analytics

_Add screenshot here_

---

## 🔒 Security

Sensitive credentials are kept outside the GitHub repository.

```text
.env
google_cred.json
venv/
.venv/
__pycache__/
*.pyc
```

API keys, email credentials, and Google service-account credentials should **never** be committed to GitHub.

If credentials are accidentally exposed, revoke and replace them immediately.

---

## 🔮 Future Improvements

- 🔐 Role-based support-agent authentication
- 🚨 Automatic ticket priority detection
- 📊 Advanced support analytics
- 💬 Conversation history and follow-ups
- 🗄️ PostgreSQL database integration
- 🐳 Docker and cloud deployment

---

## 👨‍💻 Author

**Onkar Shesh**

B.Tech — Computer Science and Business Systems

[GitHub](https://github.com/OnkarShesh)

---

## ⭐ Project

ResolveX demonstrates an end-to-end AI-powered customer support workflow combining **LLM automation, cloud data storage, email communication, and an interactive support dashboard**.

If you find the project useful, consider giving the repository a ⭐.