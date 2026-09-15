import sys
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# PROJECT CONFIGURATION
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "autonomus_job.sqlite3"
)


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

from src.database.db import get_recommendations


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Job Application Agent",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🤖 AI Job Application Agent")

st.write(
    "AI-powered job matching with "
    "human-in-the-loop application preparation."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Job Search")

role = st.sidebar.text_input(
    "Target Role",
    value="Python",
)

location = st.sidebar.text_input(
    "Location",
    value="Hyderabad",
)

st.sidebar.info(
    "The agent prepares recommendations "
    "but does not automatically submit applications."
)


# ---------------------------------------------------------
# LOAD RECOMMENDATIONS
# ---------------------------------------------------------

recommendations = get_recommendations(
    DATABASE_PATH
)


# ---------------------------------------------------------
# DASHBOARD SUMMARY
# ---------------------------------------------------------

st.subheader("Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Recommendations",
        len(recommendations),
    )

with col2:
    pending_count = sum(
        1
        for item in recommendations
        if item["status"] == "PENDING_APPROVAL"
    )

    st.metric(
        "Pending Approval",
        pending_count,
    )

with col3:
    approved_count = sum(
        1
        for item in recommendations
        if item["status"] == "APPROVED"
    )

    st.metric(
        "Approved",
        approved_count,
    )


st.divider()


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

st.subheader("Job Recommendations")


if not recommendations:

    st.info(
        "No recommendations found. "
        "Run the AI job agent first."
    )

else:

    for recommendation in recommendations:

        with st.container(border=True):

            st.markdown(
                f"### Job ID: "
                f"{recommendation['job_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Selected Resume:**"
                )

                st.write(
                    recommendation[
                        "resume_name"
                    ]
                )

            with col2:

                score_percentage = (
                    recommendation["score"]
                    * 100
                )

                st.metric(
                    "Match Score",
                    f"{score_percentage:.2f}%",
                )

            status = recommendation[
                "status"
            ]

            if status == "PENDING_APPROVAL":

                st.warning(
                    f"Status: {status}"
                )

            elif status == "APPROVED":

                st.success(
                    f"Status: {status}"
                )

            elif status == "REJECTED":

                st.error(
                    f"Status: {status}"
                )

            else:

                st.info(
                    f"Status: {status}"
                )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Autonomous AI Job Application Agent "
    "• Human approval required"
)