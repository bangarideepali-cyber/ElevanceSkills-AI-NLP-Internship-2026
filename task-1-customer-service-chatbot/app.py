import streamlit as st
import csv
import os
import time

CSV_FILE = "dataset/customer_service.csv"

st.title("🤖 Customer Service Chatbot")
st.write("Ask your question below:")

# Read CSV without pandas
def load_data():
    questions = []
    answers = []

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            questions.append(row["question"])
            answers.append(row["answer"])

    return questions, answers


# Simple matching
def find_answer(user_question, questions, answers):

    user_words = set(user_question.lower().split())

    best_answer = None
    best_score = 0

    for i, question in enumerate(questions):

        question_words = set(question.lower().split())

        common_words = user_words.intersection(question_words)

        score = len(common_words)

        if score > best_score:
            best_score = score
            best_answer = answers[i]

    if best_score > 0:
        return best_answer

    return "Sorry, I don't know the answer."


# Load knowledge base
questions, answers = load_data()

user_question = st.text_input("Enter your question:")

if user_question:

    answer = find_answer(
        user_question,
        questions,
        answers
    )

    st.success(answer)


st.write("---")
st.write("📚 Knowledge Base automatically reads new information from the CSV file.")
