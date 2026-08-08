import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Support Ticket Management",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# IMPORT PROJECT TOOLS
# =========================================================

from tools.sheet_connector import (
    fetch_new_tickets,
    update_ticket,
    append_processed_ticket,
    delete_ticket_from_pending,
    fetch_processed_tickets
)

from tools.classify_ticket import classify_ticket
from tools.generate_reply import generate_reply
from tools.gmail_sender import send_email_smtp


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ---------------- Main Layout ---------------- */

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }


    /* ---------------- Sidebar ---------------- */

    div[data-testid="stSidebar"] > div:first-child {
        width: 300px;
    }

    div[data-testid="stSidebar"] .stRadio label {
        font-size: 1rem;
    }


    /* ---------------- Main Header ---------------- */

    .dashboard-header {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #2563eb;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }


    /* ---------------- Section Headers ---------------- */

    .section-header {
        font-size: 1.45rem;
        font-weight: 750;
        margin-bottom: 0.8rem;
    }


    /* ---------------- Ticket Card ---------------- */

    .ticket-details {
        background-color: #e0f2fe;
        color: #111827;
        border: 1px solid #d1d5db;
        padding: 1rem 1.1rem;
        border-radius: 10px;
        margin-bottom: 0.7rem;
        min-height: 105px;
    }

    .ticket-header {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.35rem;
    }

    .ticket-category {
        font-size: 0.9rem;
        color: #2563eb;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .ticket-message {
        white-space: pre-wrap;
        color: #374151;
        line-height: 1.45;
    }


    /* ---------------- Pending Ticket Card ---------------- */

    .pending-ticket {
        background-color: #f0f4f8;
        color: #111827;
        border-left: 6px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        line-height: 1.5;
    }


    /* ---------------- Buttons ---------------- */

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 8px;
        font-weight: 600;
    }


    /* ---------------- Alerts ---------------- */

    div[data-testid="stAlert"] {
        border-radius: 8px;
    }


    /* ---------------- Metrics ---------------- */

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 0.8rem;
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("📌 Navigation")

tab_selection = st.sidebar.radio(
    "Go to:",
    [
        "📋 Pending Tickets",
        "📂 Analyzed Tickets",
        "📊 Dashboard"
    ]
)


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    "<div class='dashboard-header'>🤖 AI Support Ticket Management Dashboard</div>",
    unsafe_allow_html=True
)


# =========================================================
# LOAD TICKETS
# =========================================================

try:
    pending_tickets = fetch_new_tickets()
    processed_tickets = fetch_processed_tickets()

except Exception as e:
    st.error(f"❌ Unable to load ticket data: {e}")
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_ticket_label(ticket, idx):
    return f"#{idx} - {ticket.get('Name', 'Unknown')} ({ticket.get('Email', 'No email')})"


def filter_by_date_range(df, date_col, label):

    df = df.dropna(subset=[date_col])

    if df.empty:
        st.info(f"No valid {date_col} data available for {label}.")
        return df

    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()

    if min_date == max_date:
        max_date = min_date + datetime.timedelta(days=1)

    selected_date_range = st.date_input(
        f"📅 Filter {label} by Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date = end_date = selected_date_range

    return df[
        (df[date_col].dt.date >= start_date)
        & (df[date_col].dt.date <= end_date)
    ]


def safe_text(value):
    return html.escape(str(value if value is not None else ""))


# =========================================================
# PENDING TICKETS
# =========================================================

if tab_selection == "📋 Pending Tickets":

    st.subheader("📋 Pending Tickets")

    if not pending_tickets:

        st.success("✅ No pending tickets to process.")

    else:

        # -------------------------------------------------
        # CLASSIFY UNLABELLED TICKETS
        # -------------------------------------------------

        for ticket in pending_tickets:

            if not ticket.get("IssueType_Label"):

                try:

                    with st.spinner(
                        f"Analyzing ticket from {ticket.get('Name', 'customer')}..."
                    ):

                        classification = classify_ticket(
                            ticket.get("Message", "")
                        )

                    issue_type = classification.get(
                        "issue_type",
                        "Other"
                    )

                    sentiment = classification.get(
                        "sentiment",
                        "Neutral"
                    )

                    ticket["IssueType_Label"] = issue_type
                    ticket["Sentiment"] = sentiment

                    update_ticket(
                        ticket.get("RowNumber"),
                        sentiment,
                        issue_type,
                        ticket.get("AutoReply", "")
                    )

                except Exception as e:

                    ticket["IssueType_Label"] = "Other"
                    ticket["Sentiment"] = "Neutral"

                    st.warning(
                        f"⚠️ Could not classify ticket "
                        f"#{ticket.get('RowNumber', '')}: {e}"
                    )

        # -------------------------------------------------
        # SEPARATE ANALYZED / UNANALYZED
        # -------------------------------------------------

        analyzed = [
            ticket
            for ticket in pending_tickets
            if ticket.get("IssueType_Label")
        ]

        unanalyzed = [
            ticket
            for ticket in pending_tickets
            if not ticket.get("IssueType_Label")
        ]

        # -------------------------------------------------
        # TWO COLUMN LAYOUT
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        # =================================================
        # LEFT: NOT YET ANALYZED
        # =================================================

        with col1:

            st.markdown("### ⏳ Pending (Not Yet Analyzed)")

            if not unanalyzed:

                st.success(
                    "No tickets awaiting classification."
                )

            else:

                for i, ticket in enumerate(
                    unanalyzed,
                    start=1
                ):

                    st.markdown(
                        f"""
                        <div class="pending-ticket">
                            <strong>📩 Ticket #{i}</strong><br>
                            <strong>Name:</strong> {safe_text(ticket.get("Name"))}<br>
                            <strong>Email:</strong> {safe_text(ticket.get("Email"))}<br>
                            <strong>Message:</strong><br>
                            {safe_text(ticket.get("Message"))}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # =================================================
        # RIGHT: ANALYZED BUT NOT SENT
        # =================================================

        with col2:

            st.markdown("### ✅ Analyzed (But Not Sent)")

            if not analyzed:

                st.info("No analyzed tickets available.")

            else:

                all_categories = sorted(
                    set(
                        ticket.get(
                            "IssueType_Label",
                            "Other"
                        )
                        for ticket in analyzed
                    )
                )

                selected_categories = st.multiselect(
                    "🎯 Filter by Category",
                    options=all_categories,
                    default=all_categories
                )

                filtered = [
                    ticket
                    for ticket in analyzed
                    if ticket.get("IssueType_Label")
                    in selected_categories
                ]

                if not filtered:

                    st.info(
                        "No tickets match the selected categories."
                    )

                else:

                    selected_to_send = {}

                    # -------------------------------------
                    # TICKET LIST
                    # -------------------------------------

                    for i, ticket in enumerate(
                        filtered,
                        start=1
                    ):

                        cols = st.columns([0.05, 0.95])

                        with cols[0]:

                            selected_to_send[i] = st.checkbox(
                                "",
                                key=f"ticket_select_{ticket.get('RowNumber', i)}"
                            )

                        with cols[1]:

                            st.markdown(
                                f"**📨 Ticket #{i} - "
                                f"{ticket.get('Name', 'Unknown')} "
                                f"({ticket.get('Email', 'No email')})**"
                            )

                            st.markdown(
                                f"**Category:** "
                                f"{ticket.get('IssueType_Label', 'Other')}"
                            )

                            st.write(
                                ticket.get("Message", "")
                            )

                            if st.button(
                                "🗑 Delete",
                                key=f"delete_ticket_{ticket.get('RowNumber', i)}"
                            ):

                                try:

                                    delete_ticket_from_pending(
                                        ticket["RowNumber"]
                                    )

                                    st.success(
                                        "✅ Ticket deleted successfully."
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"❌ Failed to delete ticket: {e}"
                                    )

                    # -------------------------------------
                    # ACTION BUTTONS
                    # -------------------------------------

                    col_btn1, col_btn2, col_btn3 = st.columns(
                        [1.3, 1.3, 1]
                    )

                    # =====================================
                    # SEND SELECTED
                    # =====================================

                    with col_btn1:

                        if st.button(
                            "✉️ Send Replies to Selected",
                            use_container_width=True
                        ):

                            to_process = [
                                ticket
                                for i, ticket in enumerate(
                                    filtered,
                                    start=1
                                )
                                if selected_to_send.get(i)
                            ]

                            if not to_process:

                                st.warning(
                                    "Please select at least one ticket to send replies."
                                )

                            else:

                                success_count = 0

                                try:

                                    with st.spinner(
                                        "Generating and sending replies..."
                                    ):

                                        for ticket in to_process:

                                            if not ticket.get("AutoReply"):

                                                ticket["AutoReply"] = generate_reply(
                                                    ticket.get("Name", ""),
                                                    ticket.get("Message", "")
                                                )

                                            sentiment = ticket.get(
                                                "Sentiment",
                                                "Neutral"
                                            )

                                            issue_type = ticket.get(
                                                "IssueType_Label",
                                                "Other"
                                            )

                                            reply = ticket["AutoReply"]
                                            row_number = ticket.get("RowNumber")

                                            send_email_smtp(
                                                ticket["Email"],
                                                "Automated Reply",
                                                reply
                                            )

                                            update_ticket(
                                                row_number,
                                                sentiment,
                                                issue_type,
                                                reply
                                            )

                                            append_processed_ticket(
                                                ticket,
                                                sentiment,
                                                issue_type,
                                                reply
                                            )

                                            success_count += 1

                                    for ticket in sorted(
                                        to_process,
                                        key=lambda x: x["RowNumber"],
                                        reverse=True
                                    ):

                                        delete_ticket_from_pending(
                                            ticket["RowNumber"]
                                        )

                                    st.success(
                                        f"✅ Sent replies to {success_count} "
                                        f"ticket(s) and updated the records."
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"❌ Failed to process tickets: {e}"
                                    )

                    # =====================================
                    # SEND ALL
                    # =====================================

                    with col_btn2:

                        if st.button(
                            "✉️ Send Replies to All",
                            use_container_width=True
                        ):

                            if not filtered:

                                st.warning(
                                    "No tickets available to send."
                                )

                            else:

                                try:

                                    with st.spinner(
                                        "Generating and sending replies..."
                                    ):

                                        for ticket in filtered:

                                            if not ticket.get("AutoReply"):

                                                ticket["AutoReply"] = generate_reply(
                                                    ticket.get("Name", ""),
                                                    ticket.get("Message", "")
                                                )

                                            sentiment = ticket.get(
                                                "Sentiment",
                                                "Neutral"
                                            )

                                            issue_type = ticket.get(
                                                "IssueType_Label",
                                                "Other"
                                            )

                                            reply = ticket["AutoReply"]

                                            send_email_smtp(
                                                ticket["Email"],
                                                "Automated Reply",
                                                reply
                                            )

                                            update_ticket(
                                                ticket["RowNumber"],
                                                sentiment,
                                                issue_type,
                                                reply
                                            )

                                            append_processed_ticket(
                                                ticket,
                                                sentiment,
                                                issue_type,
                                                reply
                                            )

                                    for ticket in sorted(
                                        filtered,
                                        key=lambda x: x["RowNumber"],
                                        reverse=True
                                    ):

                                        delete_ticket_from_pending(
                                            ticket["RowNumber"]
                                        )

                                    st.success(
                                        f"✅ Sent replies to all {len(filtered)} "
                                        f"analyzed ticket(s)."
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"❌ Failed to send replies: {e}"
                                    )

                    # =====================================
                    # DELETE SELECTED
                    # =====================================

                    with col_btn3:

                        if st.button(
                            "🗑 Delete Selected",
                            use_container_width=True
                        ):

                            to_delete = [
                                ticket
                                for i, ticket in enumerate(
                                    filtered,
                                    start=1
                                )
                                if selected_to_send.get(i)
                            ]

                            if not to_delete:

                                st.warning(
                                    "Please select at least one ticket."
                                )

                            else:

                                try:

                                    for ticket in sorted(
                                        to_delete,
                                        key=lambda x: x["RowNumber"],
                                        reverse=True
                                    ):

                                        delete_ticket_from_pending(
                                            ticket["RowNumber"]
                                        )

                                    st.success(
                                        f"✅ Deleted {len(to_delete)} ticket(s)."
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"❌ Failed to delete tickets: {e}"
                                    )


# =========================================================
# ANALYZED TICKETS
# =========================================================

elif tab_selection == "📂 Analyzed Tickets":

    st.subheader("📂 Analyzed Tickets")


    if not processed_tickets:

        st.info(
            "No tickets have been analyzed yet."
        )

    else:

        df = pd.DataFrame(processed_tickets)


        # -----------------------------------------------
        # TIMESTAMP
        # -----------------------------------------------

        if "Timestamp" in df.columns:

            df["Timestamp"] = pd.to_datetime(
                df["Timestamp"],
                errors="coerce"
            )


        # -----------------------------------------------
        # ISSUE TYPE FILTER
        # -----------------------------------------------

        issue_types = (
            df["IssueType_Label"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_issue_types = st.multiselect(
            "🎯 Filter by Issue Type",
            options=issue_types,
            default=issue_types
        )


        # -----------------------------------------------
        # DATE FILTER
        # -----------------------------------------------

        if (
            "Timestamp" in df.columns
            and not df["Timestamp"].isnull().all()
        ):

            df = filter_by_date_range(
                df,
                "Timestamp",
                "Analyzed Tickets"
            )


        # -----------------------------------------------
        # APPLY FILTER
        # -----------------------------------------------

        df = df[
            df["IssueType_Label"].isin(
                selected_issue_types
            )
        ]


        if df.empty:

            st.info(
                "No tickets match the selected filters."
            )

        else:

            filtered_tickets = df.to_dict(
                "records"
            )

            processed_labels = [
                format_ticket_label(
                    ticket,
                    i
                )
                for i, ticket in enumerate(
                    filtered_tickets,
                    start=1
                )
            ]


            # -------------------------------------------
            # TICKET SELECTOR
            # -------------------------------------------

            selected_processed = st.selectbox(
                "📌 Select an analyzed ticket",
                processed_labels,
                key="processed_select_filtered"
            )


            selected_index = processed_labels.index(
                selected_processed
            )

            ticket = filtered_tickets[selected_index]


            # -------------------------------------------
            # TICKET DETAILS
            # -------------------------------------------

            st.markdown("### 📝 Message")

            st.write(
                ticket.get("Message", "")
            )

            detail_col1, detail_col2 = st.columns(2)

            with detail_col1:

                st.markdown(
                    f"**😊 Sentiment:** `{ticket.get('Sentiment', 'N/A')}`"
                )

            with detail_col2:

                st.markdown(
                    f"**🗂️ Issue Type:** `{ticket.get('IssueType_Label', 'N/A')}`"
                )


            st.markdown("**📬 AI Generated Reply:**")

            st.text_area(
                "Reply",
                ticket.get("AutoReply", ""),
                height=160,
                disabled=True,
                label_visibility="collapsed"
            )


            # -------------------------------------------
            # EXPORT
            # -------------------------------------------

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📁 Export Filtered CSV",
                csv,
                "processed_tickets_filtered.csv",
                "text/csv",
                use_container_width=True
            )


# =========================================================
# DASHBOARD
# =========================================================

elif tab_selection == "📊 Dashboard":

    st.subheader("📊 Analytics Dashboard")


    if not processed_tickets:

        st.info(
            "No processed ticket data available yet."
        )

    else:

        df = pd.DataFrame(
            processed_tickets
        )


        # -----------------------------------------------
        # TIMESTAMP
        # -----------------------------------------------

        if "Timestamp" in df.columns:

            df["Timestamp"] = pd.to_datetime(
                df["Timestamp"],
                errors="coerce"
            )


        # -----------------------------------------------
        # FILTERS
        # -----------------------------------------------

        issue_types = (
            df["IssueType_Label"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_issue_types = st.multiselect(
            "🎯 Filter Dashboard by Issue Type",
            options=issue_types,
            default=issue_types
        )


        if (
            "Timestamp" in df.columns
            and not df["Timestamp"].isnull().all()
        ):

            df = filter_by_date_range(
                df,
                "Timestamp",
                "Dashboard"
            )


        df = df[
            df["IssueType_Label"].isin(
                selected_issue_types
            )
        ]


        if df.empty:

            st.info(
                "No data to display for the selected filters."
            )

        else:

            # -------------------------------------------
            # METRICS
            # -------------------------------------------

            total_tickets = len(df)

            positive_tickets = len(
                df[
                    df["Sentiment"]
                    .astype(str)
                    .str.lower()
                    .eq("positive")
                ]
            )

            negative_tickets = len(
                df[
                    df["Sentiment"]
                    .astype(str)
                    .str.lower()
                    .eq("negative")
                ]
            )

            issue_count = df[
                "IssueType_Label"
            ].nunique()


            metric1, metric2, metric3, metric4 = st.columns(4)


            with metric1:
                st.metric(
                    "🎫 Total Tickets",
                    total_tickets
                )

            with metric2:
                st.metric(
                    "😊 Positive",
                    positive_tickets
                )

            with metric3:
                st.metric(
                    "😞 Negative",
                    negative_tickets
                )

            with metric4:
                st.metric(
                    "🗂️ Issue Types",
                    issue_count
                )


            st.divider()


            # -------------------------------------------
            # CHARTS
            # -------------------------------------------

            chart_col1, chart_col2 = st.columns(2)


            # ===========================================
            # SENTIMENT CHART
            # ===========================================

            with chart_col1:

                st.subheader(
                    "📊 Sentiment Distribution"
                )

                sentiment_counts = (
                    df["Sentiment"]
                    .value_counts(dropna=True)
                )


                if sentiment_counts.empty:

                    st.write(
                        "No sentiment data available."
                    )

                else:

                    fig1, ax1 = plt.subplots(
                        figsize=(6, 4)
                    )

                    ax1.pie(
                        sentiment_counts,
                        labels=sentiment_counts.index,
                        autopct="%1.1f%%",
                        startangle=140
                    )

                    ax1.axis("equal")

                    st.pyplot(
                        fig1,
                        use_container_width=True
                    )

                    plt.close(fig1)


            # ===========================================
            # ISSUE TYPE CHART
            # ===========================================

            with chart_col2:

                st.subheader(
                    "🗂️ Issue Type Distribution"
                )

                issue_counts = (
                    df["IssueType_Label"]
                    .value_counts(dropna=True)
                )


                if issue_counts.empty:

                    st.write(
                        "No issue type data available."
                    )

                else:

                    fig2, ax2 = plt.subplots(
                        figsize=(6, 4)
                    )

                    ax2.bar(
                        issue_counts.index,
                        issue_counts.values
                    )

                    ax2.set_ylabel(
                        "Number of Tickets"
                    )

                    ax2.set_xlabel(
                        "Issue Type"
                    )

                    ax2.tick_params(
                        axis="x",
                        rotation=30
                    )

                    fig2.tight_layout()

                    st.pyplot(
                        fig2,
                        use_container_width=True
                    )

                    plt.close(fig2)