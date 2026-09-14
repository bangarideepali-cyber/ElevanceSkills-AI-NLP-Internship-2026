import streamlit as st
import json
import os
import re
import math
from collections import Counter

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="ArXiv Research Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# FILE PATHS
# =====================================================

DATA_FILE = "arxiv-metadata-oai-snapshot.json"

MODEL_FOLDER = "models"

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "search_model.json"
)

# =====================================================
# STOP WORDS
# =====================================================

STOP_WORDS = {
    "the", "and", "for", "are", "was", "were",
    "with", "from", "this", "that", "have",
    "has", "been", "into", "their", "there",
    "about", "which", "using", "used", "such",
    "than", "then", "they", "them", "what",
    "where", "when", "how", "why", "does",
    "can", "could", "would", "should", "will",
    "our", "your", "you", "its", "also",
    "between", "through", "these", "those",
    "research", "paper"
}

# =====================================================
# TEXT TOKENIZER
# =====================================================

def tokenize(text):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    words = [
        word
        for word in words
        if len(word) >= 3
        and word not in STOP_WORDS
    ]

    return words


# =====================================================
# LOAD ARXIV DATA
# =====================================================

@st.cache_data
def load_data():

    papers = []

    if not os.path.exists(DATA_FILE):

        return papers

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                if not line.strip():
                    continue

                try:

                    paper = json.loads(line)

                    papers.append({
                        "id": paper.get(
                            "id",
                            ""
                        ),

                        "title": paper.get(
                            "title",
                            ""
                        ),

                        "abstract": paper.get(
                            "abstract",
                            ""
                        ),

                        "authors": paper.get(
                            "authors",
                            ""
                        ),

                        "categories": paper.get(
                            "categories",
                            ""
                        )
                    })

                    # Load first 10,000 papers
                    if len(papers) >= 10000:
                        break

                except json.JSONDecodeError:

                    continue

    except Exception as e:

        st.error(
            f"Error loading dataset: {e}"
        )

    return papers


papers = load_data()


# =====================================================
# CHECK DATA
# =====================================================

if not papers:

    st.error(
        "❌ No ArXiv papers were loaded."
    )

    st.write(
        "Make sure this file is inside the project folder:"
    )

    st.code(
        "arxiv-metadata-oai-snapshot.json"
    )

    st.stop()


st.success(
    f"✅ {len(papers)} research papers loaded successfully!"
)


# =====================================================
# BUILD SEARCH MODEL
# =====================================================

@st.cache_data
def build_search_model(papers):

    document_frequency = Counter()

    document_tokens = []

    for paper in papers:

        text = (
            paper["title"]
            + " "
            + paper["abstract"]
            + " "
            + paper["categories"]
        )

        tokens = tokenize(text)

        document_tokens.append(
            tokens
        )

        unique_words = set(tokens)

        for word in unique_words:

            document_frequency[word] += 1


    total_documents = len(papers)

    idf = {}

    for word, frequency in document_frequency.items():

        idf[word] = math.log(
            (total_documents + 1)
            / (frequency + 1)
        ) + 1

    return document_tokens, idf


document_tokens, idf = build_search_model(
    papers
)


# =====================================================
# SAVE MODEL INFORMATION
# =====================================================

def save_model():

    try:

        # Check that models is really a folder
        if not os.path.isdir(MODEL_FOLDER):

            return

        model_information = {

            "model_type":
                "Custom TF-IDF Search",

            "documents":
                len(papers),

            "vocabulary_size":
                len(idf),

            "description":
                "Local ArXiv research paper search model"
        }

        with open(
            MODEL_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                model_information,
                file,
                indent=4
            )

    except Exception:

        pass


save_model()


# =====================================================
# SEARCH PAPERS
# =====================================================

def search_papers(question):

    query_words = tokenize(
        question
    )

    if not query_words:

        return []

    results = []

    query_counter = Counter(
        query_words
    )

    for index, paper in enumerate(
        papers
    ):

        title = paper[
            "title"
        ].lower()

        abstract = paper[
            "abstract"
        ].lower()

        categories = paper[
            "categories"
        ].lower()

        tokens = document_tokens[
            index
        ]

        token_counter = Counter(
            tokens
        )

        score = 0

        # ---------------------------------------------
        # WORD MATCHING
        # ---------------------------------------------

        for word in query_counter:

            if word not in token_counter:

                continue

            frequency = token_counter[
                word
            ]

            tf = frequency / max(
                len(tokens),
                1
            )

            word_idf = idf.get(
                word,
                1
            )

            score += (
                tf * word_idf * 10
            )

            # Title bonus
            if word in title:

                score += 10

            # Category bonus
            if word in categories:

                score += 4

            # Abstract bonus
            if word in abstract:

                score += 2


        # ---------------------------------------------
        # PHRASE MATCH
        # ---------------------------------------------

        question_text = question.lower()

        if question_text in title:

            score += 20

        if question_text in abstract:

            score += 8


        if score > 0:

            results.append(
                (
                    score,
                    paper
                )
            )


    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return results[:5]


# =====================================================
# GENERATE SHORT ANSWER
# =====================================================

def generate_answer(
    question,
    results
):

    if not results:

        return (
            "I could not find a relevant research "
            "paper for your question."
        )

    best_paper = results[0][1]

    title = best_paper[
        "title"
    ]

    abstract = best_paper[
        "abstract"
    ]

    sentences = re.split(
        r"(?<=[.!?])\s+",
        abstract.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 20
    ]

    if len(sentences) >= 2:

        answer = " ".join(
            sentences[:2]
        )

    elif sentences:

        answer = sentences[0]

    else:

        answer = abstract[:500]


    return (
        f"Based on the most relevant paper "
        f"**{title}**:\n\n"
        f"{answer}"
    )


# =====================================================
# MAIN TITLE
# =====================================================

st.title(
    "🤖 ArXiv Research Chatbot"
)

st.write(
    "Ask a research question and find "
    "relevant research papers from ArXiv."
)


# =====================================================
# QUESTION INPUT
# =====================================================

question = st.text_input(
    "💬 Ask your research question",
    placeholder=
    "Example: How is machine learning used in healthcare?"
)


# =====================================================
# SEARCH
# =====================================================

if question:

    with st.spinner(
        "🔎 Searching research papers..."
    ):

        results = search_papers(
            question
        )


    # =================================================
    # CHATBOT ANSWER
    # =================================================

    st.subheader(
        "🤖 Chatbot Answer"
    )

    answer = generate_answer(
        question,
        results
    )

    st.info(
        answer
    )


    # =================================================
    # RESEARCH PAPERS
    # =================================================

    if results:

        st.subheader(
            "📚 Relevant Research Papers"
        )

        for rank, (
            score,
            paper
        ) in enumerate(
            results,
            start=1
        ):

            with st.expander(
                f"#{rank} 📄 {paper['title']}"
            ):

                st.write(
                    f"⭐ **Relevance Score:** "
                    f"{round(score, 3)}"
                )


                # -------------------------------------
                # SUMMARY
                # -------------------------------------

                st.write(
                    "### 📝 Short Summary"
                )

                abstract = paper[
                    "abstract"
                ]

                sentences = re.split(
                    r"(?<=[.!?])\s+",
                    abstract.strip()
                )

                summary = " ".join(
                    sentences[:3]
                )

                st.write(
                    summary
                )


                # -------------------------------------
                # AUTHORS
                # -------------------------------------

                st.write(
                    "### 👨‍🔬 Authors"
                )

                st.write(
                    paper["authors"]
                )


                # -------------------------------------
                # CATEGORIES
                # -------------------------------------

                st.write(
                    "### 🏷️ Categories"
                )

                st.write(
                    paper["categories"]
                )


                # -------------------------------------
                # FULL ABSTRACT
                # -------------------------------------

                st.write(
                    "### 📖 Full Abstract"
                )

                st.write(
                    paper["abstract"]
                )


                # -------------------------------------
                # ARXIV ID
                # -------------------------------------

                st.write(
                    "### 🔗 ArXiv ID"
                )

                st.code(
                    paper["id"]
                )


    else:

        st.warning(
            "❌ No relevant papers found."
        )

        st.write(
            "Try keywords such as:"
        )

        st.write(
            "machine learning"
        )

        st.write(
            "artificial intelligence"
        )

        st.write(
            "deep learning"
        )

        st.write(
            "computer vision"
        )


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title(
    "ℹ️ About Chatbot"
)

st.sidebar.write(
    """
This is an ArXiv Research Chatbot.

Features:

🤖 Chatbot-style answer

🔎 Research paper search

📊 TF-IDF based retrieval

⭐ Relevance scoring

📝 Automatic summaries

📚 ArXiv metadata

💻 Streamlit interface
"""
)

st.sidebar.markdown("---")

st.sidebar.write(
    "📁 Model: Custom TF-IDF Search"
)

st.sidebar.write(
    "📚 Dataset: ArXiv Research Papers"
)

st.sidebar.write(
    "💻 Framework: Streamlit"
)