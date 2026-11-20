import sys
import os

# Add project root to Python path
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px

from backend.database import history_collection


# Page Configuration
st.set_page_config(
    page_title="LearnMitra-AI Analytics",
    page_icon="📚",
    layout="wide"
)


# Dashboard Heading
st.title("📚 LearnMitra-AI")
st.subheader("Learning Analytics Dashboard")

st.write(
    "Monitor translations, explanations, quizzes "
    "and chatbot learning activities."
)


# Fetch MongoDB Data
@st.cache_data(ttl=10)
def load_history():

    records = list(
        history_collection.find(
            {},
            {"_id": 0}
        ).sort("created_at", -1)
    )

    return records


try:
    records = load_history()

    if records:

        df = pd.DataFrame(records)

        # Activity Summary
        total_activities = len(df)

        translations = len(
            df[df["activity_type"] == "translation"]
        )

        explanations = len(
            df[df["activity_type"] == "explanation"]
        )

        quizzes = len(
            df[df["activity_type"] == "quiz"]
        )

        chats = len(
            df[df["activity_type"] == "chat"]
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Activities", total_activities)
        col2.metric("Translations", translations)
        col3.metric("Explanations", explanations)

        col4, col5 = st.columns(2)

        col4.metric("Quizzes", quizzes)
        col5.metric("Chat Conversations", chats)

        st.divider()

        # Activity Distribution
        st.subheader("📊 Activity Distribution")

        activity_counts = (
            df["activity_type"]
            .value_counts()
            .reset_index()
        )

        activity_counts.columns = [
            "Activity",
            "Count"
        ]

        fig = px.pie(
            activity_counts,
            names="Activity",
            values="Count",
            title="Learning Activities"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Recent Activities
        st.subheader("🕒 Recent Learning Activities")

        display_df = df.copy()

        display_df["created_at"] = pd.to_datetime(
            display_df["created_at"],
            errors="coerce"
        )

        display_df["created_at"] = (
            display_df["created_at"].dt.strftime(
                "%d-%m-%Y %H:%M"
            )
        )

        display_columns = [
            column for column in [
                "activity_type",
                "input",
                "language",
                "target_language",
                "created_at"
            ]
            if column in display_df.columns
        ]

        st.dataframe(
            display_df[display_columns],
            use_container_width=True
        )

        # Activity Filter
        st.subheader("🔍 Filter Activities")

        activity_options = [
            "All",
            "translation",
            "explanation",
            "quiz",
            "chat"
        ]

        selected_activity = st.selectbox(
            "Select Activity Type",
            activity_options
        )

        if selected_activity == "All":
            filtered_df = display_df
        else:
            filtered_df = display_df[
                display_df["activity_type"] == selected_activity
            ]

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True
        )

    else:
        st.info("No learning activities found yet.")

except Exception as error:

    st.error("Unable to load learning analytics.")

    st.write(str(error))


# Footer
st.divider()

st.caption("LearnMitra-AI | Learning Analytics Dashboard")
