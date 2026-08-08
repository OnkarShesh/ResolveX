import streamlit as st
from datetime import datetime
from tools.sheet_connector import get_pending_sheet
import re


# ------------------- PAGE CONFIG -------------------

st.set_page_config(
    page_title="Submit a Support Ticket",
    page_icon="📩",
    layout="centered",
    initial_sidebar_state="auto"
)


# ------------------- CUSTOM CSS -------------------

st.markdown("""
<style>

    /* Main page */
    .block-container {
        max-width: 1000px;
        padding-top: 1.3rem;
        padding-bottom: 1.2rem;
    }

    /* Main title */
    h1 {
        font-size: 2.45rem !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
        margin-top: 0 !important;
        margin-bottom: 0.25rem !important;
    }

    /* Subtitle */
    .subtitle {
        font-size: 1rem;
        color: #b8b8b8;
        line-height: 1.4;
        margin-bottom: 1rem;
    }

    /* Form card */
    div[data-testid="stForm"] {
        padding: 1.25rem 1.4rem 1.1rem 1.4rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background-color: rgba(255, 255, 255, 0.035);
    }

    /* Form heading */
    div[data-testid="stForm"] h3 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
        margin-bottom: 0.7rem !important;
        line-height: 1.2 !important;
    }

    /* Labels */
    div[data-testid="stWidgetLabel"] p {
        font-size: 0.94rem !important;
        font-weight: 600 !important;
        line-height: 1.25 !important;
    }

    /* Text inputs */
    div[data-baseweb="input"] {
        border-radius: 8px;
    }

    div[data-baseweb="input"] input {
        min-height: 40px;
    }

    /* Select box */
    div[data-baseweb="select"] {
        border-radius: 8px;
    }

    /* Text area */
    div[data-baseweb="textarea"] {
        border-radius: 8px;
    }

    div[data-baseweb="textarea"] textarea {
        min-height: 125px;
        line-height: 1.45;
    }

    /* Reduce vertical spacing inside form */
    div[data-testid="stForm"] div[data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

    /* Hide Streamlit keyboard hint */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Submit button */
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 44px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 8px;
        margin-top: 0.7rem;
    }

</style>
""", unsafe_allow_html=True)


# ------------------- PAGE TITLE -------------------

st.title("📩 Submit a Support Ticket")

st.markdown(
    """
    <div class="subtitle">
        Please fill out the form below, and our support team will get back to you soon.
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------- DATABASE FUNCTION -------------------

def append_ticket_to_pending(name, email, issue_type, message):

    sheet = get_pending_sheet()

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet.append_row([
            timestamp,
            name,
            email,
            issue_type,
            message,
            "",
            "",
            ""
        ])

        return True

    except Exception as e:
        st.error(f"Failed to submit ticket: {e}")
        return False


# ------------------- EMAIL VALIDATION -------------------

def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


# ------------------- SUPPORT TICKET FORM -------------------

with st.form("ticket_form"):

    st.subheader("📄 Ticket Information")

    # Name + Email
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Full Name",
            placeholder="e.g., Onkar Shesh"
        )

    with col2:
        email = st.text_input(
            "Email Address",
            placeholder="e.g., onkar@example.com"
        )

    # Issue Type
    issue_type = st.selectbox(
        "Select Issue Type",
        [
            "Billing",
            "Technical",
            "Login Issue",
            "Other"
        ]
    )

    # Message
    message = st.text_area(
        "Describe your issue in detail",
        height=125,
        placeholder="Describe your issue in detail..."
    )

    # Submit
    submitted = st.form_submit_button(
        "📨 Submit Ticket"
    )


# ------------------- FORM SUBMISSION -------------------

if submitted:

    name = name.strip()
    email = email.strip()
    message = message.strip()

    # Required field validation
    if not name or not email or not message:

        st.error("⚠️ Please fill in all required fields.")

    # Email validation
    elif not is_valid_email(email):

        st.error("⚠️ Please enter a valid email address.")

    else:

        success = append_ticket_to_pending(
            name,
            email,
            issue_type,
            message
        )

        if success:
            st.success(
                "✅ Your support ticket has been submitted successfully!"
            )