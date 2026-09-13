import streamlit as st
import urllib.request
import urllib.error
import json
import base64


# =========================================
# PAGE SETTINGS
# =========================================

st.set_page_config(
    page_title="Multi-Modal AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Multi-Modal AI Assistant")
st.write("Text + Image AI Assistant")


# =========================================
# GEMINI API KEY
# =========================================

api_key = st.text_input(
    "Enter Gemini API Key:",
    type="password"
)


# =========================================
# CONVERSATION HISTORY
# =========================================

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================
# GEMINI MODEL
# =========================================

def find_model(api_key):

    # Gemini 2.5 is unavailable for new users.
    # Gemini 3.6 Flash is used here.
    return "gemini-3.6-flash"


# =========================================
# ASK GEMINI
# =========================================

def ask_gemini(
    api_key,
    model_name,
    question,
    image_file
):

    # -----------------------------------------
    # PREVIOUS CONVERSATION
    # -----------------------------------------

    previous_conversation = ""

    for item in st.session_state.history:

        previous_conversation += (
            "\nUser: "
            + item["question"]
            + "\nAssistant: "
            + item["answer"]
        )


    # -----------------------------------------
    # PROMPT
    # -----------------------------------------

    prompt = f"""
You are a Multi-Modal AI Assistant.

You can understand both text and images.

Previous conversation:
{previous_conversation}

Current user question:
{question}

Instructions:

1. Understand the user's question carefully.
2. Analyze the uploaded image if one is provided.
3. Use previous conversation context when relevant.
4. If the question is ambiguous, ask for clarification.
5. Give evidence-based answers.
6. Do not invent information.
7. Clearly distinguish observations from assumptions.
8. Validate your answer before responding.
9. Give a clear and useful final response.
"""


    # -----------------------------------------
    # TEXT PART
    # -----------------------------------------

    parts = [
        {
            "text": prompt
        }
    ]


    # =========================================
    # IMAGE PROCESSING
    # =========================================

    if image_file is not None:

        image_bytes = image_file.getvalue()

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        parts.append(
            {
                "inline_data": {
                    "mime_type": image_file.type,
                    "data": image_base64
                }
            }
        )


    # =========================================
    # REQUEST DATA
    # =========================================

    data = {
        "contents": [
            {
                "parts": parts
            }
        ]
    }


    # =========================================
    # GEMINI API URL
    # =========================================

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        + model_name
        + ":generateContent"
    )


    # =========================================
    # CREATE REQUEST
    # =========================================

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )


    # =========================================
    # SEND REQUEST
    # =========================================

    with urllib.request.urlopen(request) as response:

        result = json.loads(
            response.read().decode("utf-8")
        )


    # =========================================
    # GET RESPONSE
    # =========================================

    candidates = result.get(
        "candidates",
        []
    )

    if not candidates:

        return "No reliable response was generated."


    response_content = candidates[0].get(
        "content",
        {}
    )

    response_parts = response_content.get(
        "parts",
        []
    )


    answer = ""

    for part in response_parts:

        if "text" in part:

            answer += part["text"]


    # =========================================
    # RESPONSE VALIDATION
    # =========================================

    answer = answer.strip()

    if len(answer) < 5:

        return "Response validation failed."


    return answer


# =========================================
# QUESTION INPUT
# =========================================

question = st.text_input(
    "Ask your question:"
)


# =========================================
# IMAGE UPLOAD
# =========================================

uploaded_image = st.file_uploader(
    "Upload an image:",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]
)


# =========================================
# DISPLAY UPLOADED IMAGE
# =========================================

if uploaded_image is not None:

    st.success(
        "✅ Image uploaded successfully!"
    )

    st.write(
        "Image name:",
        uploaded_image.name
    )

    st.write(
        "Image type:",
        uploaded_image.type
    )

    # Convert image into Base64
    image_base64 = base64.b64encode(
        uploaded_image.getvalue()
    ).decode("utf-8")

    # Display actual image without st.image()
    st.html(
        f"""
        <div style="margin-top:15px;">

            <p>
                <b>📷 Uploaded Image:</b>
            </p>

            <img
                src="data:{uploaded_image.type};base64,{image_base64}"
                style="
                    max-width:500px;
                    width:100%;
                    height:auto;
                    border-radius:10px;
                "
            >

        </div>
        """
    )

    st.success(
        "🖼️ Image is ready for AI analysis."
    )


# =========================================
# ASK ASSISTANT BUTTON
# =========================================

if st.button("Ask Assistant"):

    # -----------------------------------------
    # CHECK API KEY
    # -----------------------------------------

    if not api_key:

        st.warning(
            "Please enter your Gemini API key."
        )


    # -----------------------------------------
    # CHECK QUESTION
    # -----------------------------------------

    elif not question:

        st.warning(
            "Please enter your question."
        )


    # -----------------------------------------
    # PROCESS REQUEST
    # -----------------------------------------

    else:

        try:

            with st.spinner(
                "Analyzing your question and image..."
            ):

                # Find Gemini model
                model = find_model(
                    api_key
                )

                st.info(
                    "Using model: "
                    + model
                )


                # Send request to Gemini
                answer = ask_gemini(

                    api_key,

                    model,

                    question,

                    uploaded_image

                )


                # -----------------------------------------
                # DISPLAY RESPONSE
                # -----------------------------------------

                st.subheader(
                    "🤖 Assistant Response"
                )

                st.write(
                    answer
                )


                # -----------------------------------------
                # SAVE CONVERSATION
                # -----------------------------------------

                st.session_state.history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )


        # =========================================
        # GEMINI API ERROR
        # =========================================

        except urllib.error.HTTPError as e:

            error_message = e.read().decode(
                "utf-8",
                errors="ignore"
            )

            st.error(
                "Gemini API Error"
            )

            st.write(
                "HTTP Error:",
                e.code
            )

            st.write(
                error_message
            )


        # =========================================
        # OTHER ERROR
        # =========================================

        except Exception as e:

            st.error(
                "Something went wrong."
            )

            st.write(
                str(e)
            )


# =========================================
# CONVERSATION HISTORY
# =========================================

if st.session_state.history:

    st.subheader(
        "💬 Conversation History"
    )

    for item in st.session_state.history:

        st.write(
            "**You:**",
            item["question"]
        )

        st.write(
            "**Assistant:**",
            item["answer"]
        )

        st.write("---")
