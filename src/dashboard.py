import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from earth_engine_tools import initialize_earth_engine
from orthophoto_vision import analyse_latest_finland_orthophoto
from vision import run_site_analysis


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )

client = OpenAI(api_key=api_key)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Wood-Site AI Agent",
    page_icon="🌲",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "site_result" not in st.session_state:
    st.session_state.site_result = None

if "historical_result" not in st.session_state:
    st.session_state.historical_result = None

if "analysed_latitude" not in st.session_state:
    st.session_state.analysed_latitude = None

if "analysed_longitude" not in st.session_state:
    st.session_state.analysed_longitude = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# ---------------------------------------------------------
# Follow-up question function
# ---------------------------------------------------------

def answer_site_question(
    question: str,
    analysis: str,
    metadata: dict,
    latitude: float,
    longitude: float,
    chat_messages: list,
    historical_comparison: str | None = None,
) -> str:
    """
    Answer follow-up questions using the existing
    site assessment and, if available, the historical
    comparison.

    The orthophoto is not downloaded again.
    """

    previous_conversation = []

    for message in chat_messages:
        previous_conversation.append(
            f"{message['role'].upper()}: "
            f"{message['content']}"
        )

    conversation_text = "\n".join(
        previous_conversation
    )

    if historical_comparison:
        historical_context = (
            "\nHistorical monitoring result:\n"
            "--------------------------------\n"
            f"{historical_comparison}\n"
            "--------------------------------\n"
        )
    else:
        historical_context = (
            "\nHistorical monitoring result:\n"
            "No historical comparison has been run yet.\n"
        )

    prompt = (
        "You are the Wood-Site AI Agent.\n\n"

        "The location below has already been analysed "
        "using high-resolution orthophoto imagery.\n\n"

        f"Latitude: {latitude}\n"
        f"Longitude: {longitude}\n"
        f"Imagery source: {metadata['source']}\n"
        f"Orthophoto year: "
        f"{metadata['orthophoto_year']}\n\n"

        "Existing high-resolution site assessment:\n"
        "--------------------------------\n"
        f"{analysis}\n"
        "--------------------------------\n"

        f"{historical_context}\n"

        "Previous follow-up conversation:\n"
        f"{conversation_text if conversation_text else 'None'}\n\n"

        f"User's new question:\n{question}\n\n"

        "Answer using only the evidence available above.\n\n"

        "If historical monitoring has been run, you may "
        "answer questions about visible changes over time "
        "using that historical comparison.\n\n"

        "If historical monitoring has not been run and the "
        "user asks about change over time, explain that a "
        "temporal comparison is required.\n\n"

        "Do not claim that you are viewing or analysing "
        "the imagery again during this follow-up response.\n\n"

        "Do not invent visual features or changes that are "
        "not supported by the available assessments.\n\n"

        "Do not infer exact timber volume, production, "
        "sales, revenue, company performance, market demand, "
        "or purchasing intention.\n\n"

        "Clearly distinguish observations from uncertainty. "
        "Keep the answer concise and evidence-based."
    )

    response = client.responses.create(
        model="gpt-5",
        input=prompt,
    )

    return response.output_text


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🌲 Wood-Site AI Agent")

st.write(
    "AI-assisted identification and monitoring of "
    "wood-storage and wood-processing sites using "
    "geospatial imagery."
)

st.divider()


# ---------------------------------------------------------
# Coordinate input
# ---------------------------------------------------------

st.subheader("Analyse a location")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Latitude",
        value=60.868673,
        format="%.7f",
    )

with col2:
    longitude = st.number_input(
        "Longitude",
        value=26.7346685,
        format="%.7f",
    )


# ---------------------------------------------------------
# Map
# ---------------------------------------------------------

st.subheader("Selected location")

map_data = {
    "lat": [latitude],
    "lon": [longitude],
}

st.map(map_data)


# ---------------------------------------------------------
# High-resolution analysis button
# ---------------------------------------------------------

if st.button(
    "Analyse Location",
    type="primary",
    use_container_width=True,
):

    try:

        with st.spinner(
            "Searching Earth Engine and analysing "
            "the location..."
        ):

            initialize_earth_engine()

            result = (
                analyse_latest_finland_orthophoto(
                    latitude=latitude,
                    longitude=longitude,
                )
            )

        st.session_state.site_result = result
        st.session_state.analysed_latitude = latitude
        st.session_state.analysed_longitude = longitude

        # New location = reset historical/chat context
        st.session_state.historical_result = None
        st.session_state.chat_messages = []

        st.success(
            "Analysis completed successfully."
        )

    except Exception as error:

        st.error(
            "The location could not be analysed."
        )

        st.exception(error)


# ---------------------------------------------------------
# Display stored analysis
# ---------------------------------------------------------

if st.session_state.site_result is not None:

    result = st.session_state.site_result

    metadata = result["metadata"]
    analysis = result["analysis"]

    analysed_latitude = (
        st.session_state.analysed_latitude
    )

    analysed_longitude = (
        st.session_state.analysed_longitude
    )

    st.divider()

    # -----------------------------------------------------
    # Imagery information
    # -----------------------------------------------------

    st.subheader("Imagery information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.metric(
            "Orthophoto year",
            metadata["orthophoto_year"],
        )

    with info_col2:
        st.metric(
            "Imagery source",
            "Finland NLS",
        )

    st.write(
        f"**Earth Engine image:** "
        f"`{metadata['image_id']}`"
    )

    st.write(
        "**Image handling:** Retrieved directly from "
        "Earth Engine and analysed in memory. "
        "No permanent local image was created."
    )

    st.divider()

    # -----------------------------------------------------
    # AI site assessment
    # -----------------------------------------------------

    st.subheader("AI Site Assessment")

    st.markdown(
        analysis
    )

    st.caption(
        "The assessment is based on visible evidence "
        "in geospatial imagery. It does not directly "
        "establish production volume, sales, market "
        "demand, purchasing intent, or company performance."
    )

    st.divider()

    # -----------------------------------------------------
    # Historical monitoring
    # -----------------------------------------------------

    st.subheader("Historical Monitoring")

    st.write(
        "Pilot historical monitoring is currently available "
        "for FIN001 using the prepared 2021, 2022 and 2025 "
        "reference images."
    )

    fin001_latitude = 60.868673
    fin001_longitude = 26.7346685

    is_fin001 = (
        abs(analysed_latitude - fin001_latitude) < 0.0001
        and
        abs(analysed_longitude - fin001_longitude) < 0.0001
    )

    if is_fin001:

        if st.button(
            "Compare Historical Changes",
            use_container_width=True,
        ):

            try:

                with st.spinner(
                    "Analysing historical imagery "
                    "and comparing changes..."
                ):

                    historical_result = (
                        run_site_analysis("FIN001")
                    )

                st.session_state.historical_result = (
                    historical_result
                )

                # Clear old chat because new evidence
                # has now been added to the session.
                st.session_state.chat_messages = []

                st.success(
                    "Historical comparison completed."
                )

            except Exception as error:

                st.error(
                    "Historical comparison failed."
                )

                st.exception(error)

    else:

        st.info(
            "Historical monitoring is currently implemented "
            "as a pilot for FIN001. Automated historical "
            "monitoring for arbitrary coordinates is a "
            "planned extension."
        )


    # -----------------------------------------------------
    # Display historical comparison
    # -----------------------------------------------------

    if st.session_state.historical_result is not None:

        historical_result = (
            st.session_state.historical_result
        )

        historical_comparison = (
            historical_result[
                "historical_comparison"
            ]
        )

        st.subheader(
            "Visible Changes Over Time"
        )

        st.markdown(
            historical_comparison
        )

        st.caption(
            "Historical comparison is based on the "
            "available pilot imagery for FIN001. "
            "Observed changes should be interpreted as "
            "visible site-level indicators rather than "
            "direct measurements of production or demand."
        )

    st.divider()

    # -----------------------------------------------------
    # Follow-up chat
    # -----------------------------------------------------

    st.subheader("Ask about this site")

    st.write(
        "Ask follow-up questions about the site, "
        "infrastructure, visible activity, or historical "
        "changes. Existing analyses are reused without "
        "retrieving the orthophoto again."
    )

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

    user_question = st.chat_input(
        "Ask something about this site..."
    )

    if user_question:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": user_question,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        historical_comparison = None

        if (
            st.session_state.historical_result
            is not None
        ):
            historical_comparison = (
                st.session_state.historical_result[
                    "historical_comparison"
                ]
            )

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "Thinking..."
                ):

                    answer = answer_site_question(
                        question=user_question,
                        analysis=analysis,
                        metadata=metadata,
                        latitude=analysed_latitude,
                        longitude=analysed_longitude,
                        chat_messages=(
                            st.session_state.chat_messages[:-1]
                        ),
                        historical_comparison=(
                            historical_comparison
                        ),
                    )

                st.markdown(answer)

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as error:

            st.error(
                "The follow-up question could not "
                "be answered."
            )

            st.exception(error)