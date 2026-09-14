import streamlit as st

st.set_page_config(
    page_title="Customer Sentiment Chatbot",
    page_icon="🤖"
)

st.title("🤖 Customer Sentiment Chatbot")
st.write("I can understand customer emotions and respond accordingly.")


positive_words = [
    "good", "great", "excellent", "amazing", "happy",
    "love", "helpful", "perfect", "thank", "thanks",
    "satisfied", "awesome", "best"
]

negative_words = [
    "bad", "worst", "terrible", "hate", "angry",
    "disappointed", "poor", "problem", "issue",
    "wrong", "horrible", "unhappy", "frustrated"
]


def detect_sentiment(message):

    message = message.lower()

    positive_score = 0
    negative_score = 0

    for word in positive_words:
        if word in message:
            positive_score += 1

    for word in negative_words:
        if word in message:
            negative_score += 1

    if positive_score > negative_score:
        return "Positive"

    elif negative_score > positive_score:
        return "Negative"

    else:
        return "Neutral"


def chatbot_response(sentiment):

    if sentiment == "Positive":
        return "😊 Thank you for your positive feedback! We're happy to know that you had a good experience."

    elif sentiment == "Negative":
        return "😔 I'm sorry that you had a bad experience. I understand your frustration and will try to help you resolve the issue."

    else:
        return "🙂 Thank you for contacting us. I'll be happy to help you with your request."


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


user_message = st.text_input("💬 Enter your message:")


if st.button("Send"):

    if user_message.strip():

        sentiment = detect_sentiment(user_message)

        response = chatbot_response(sentiment)

        st.session_state.chat_history.append(
            (user_message, sentiment, response)
        )


st.subheader("💬 Conversation")


for message, sentiment, response in st.session_state.chat_history:

    st.write("👤 **Customer:**", message)

    if sentiment == "Positive":
        st.success("😊 Sentiment: Positive")

    elif sentiment == "Negative":
        st.error("😔 Sentiment: Negative")

    else:
        st.info("😐 Sentiment: Neutral")

    st.write("🤖 **Chatbot:**", response)

    st.divider()