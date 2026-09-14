import streamlit as st
from medical_chatbot import MedicalChatbot


# -----------------------------------------
# Page Configuration
# -----------------------------------------

st.set_page_config(
    page_title="Medical Q&A Chatbot",
    page_icon="🩺",
    layout="centered"
)


# -----------------------------------------
# Title
# -----------------------------------------

st.title("🩺 Medical Q&A Chatbot")

st.write(
    "Ask a medical question and get the most "
    "relevant answer."
)


# -----------------------------------------
# Disclaimer
# -----------------------------------------

st.warning(
    "⚠️ This chatbot is for educational purposes only. "
    "It does not replace professional medical advice."
)


# -----------------------------------------
# Dataset Path
# -----------------------------------------

DATASET_PATH = "medquad.csv"


# -----------------------------------------
# Load Chatbot
# -----------------------------------------

@st.cache_resource
def load_chatbot():

    return MedicalChatbot(
        DATASET_PATH
    )


try:

    chatbot = load_chatbot()

except Exception as e:

    st.error(
        "Unable to load the medical dataset."
    )

    st.code(str(e))

    st.stop()


# -----------------------------------------
# Dataset Information
# -----------------------------------------

st.success(
    f"Medical dataset loaded: "
    f"{len(chatbot.data)} questions"
)


# -----------------------------------------
# Question Input
# -----------------------------------------

question = st.text_input(
    "Enter your medical question:",
    placeholder="Example: What are the symptoms of fever?"
)


# -----------------------------------------
# Ask Button
# -----------------------------------------

if st.button("🔍 Get Answer"):

    if not question.strip():

        st.warning(
            "Please enter a medical question."
        )

    else:

        # Find answer
        (
            answer,
            score,
            matched_question,
            source
        ) = chatbot.find_answer(
            question
        )


        # ---------------------------------
        # Answer
        # ---------------------------------

        st.subheader("💬 Answer")

        st.write(answer)


        # ---------------------------------
        # Source
        # ---------------------------------

        st.write(
            f"**Source:** {source}"
        )


        # ---------------------------------
        # Relevance Score
        # ---------------------------------

        st.write(
            f"**Relevance Score:** "
            f"{score:.2f}"
        )


        # ---------------------------------
        # Matched Question
        # ---------------------------------

        if matched_question:

            with st.expander(
                "View matched question"
            ):

                st.write(
                    matched_question
                )


        # ---------------------------------
        # Entity Recognition
        # ---------------------------------

        st.subheader(
            "🔎 Medical Entities"
        )

        entities = chatbot.extract_entities(
            question
        )

        found = False


        # Diseases
        if entities["Diseases"]:

            st.write(
                "**Diseases:** "
                + ", ".join(
                    entities["Diseases"]
                )
            )

            found = True


        # Symptoms
        if entities["Symptoms"]:

            st.write(
                "**Symptoms:** "
                + ", ".join(
                    entities["Symptoms"]
                )
            )

            found = True


        # Treatments
        if entities["Treatments"]:

            st.write(
                "**Treatments:** "
                + ", ".join(
                    entities["Treatments"]
                )
            )

            found = True


        if not found:

            st.write(
                "No basic medical entities detected."
            )


# -----------------------------------------
# Footer
# -----------------------------------------

st.markdown("---")

st.caption(
    "Dataset: MedQuAD"
)

st.caption(
    "Retrieval Mechanism: Text Similarity"
)

st.caption(
    "Medical Entity Recognition: "
    "Keyword-based"
)

st.caption(
    "User Interface: Streamlit"
)