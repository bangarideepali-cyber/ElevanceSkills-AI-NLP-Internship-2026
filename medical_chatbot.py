import csv
import re
import math


class MedicalChatbot:

    def __init__(self, csv_path):

        self.data = []

        # Load MedQuAD CSV
        with open(
            csv_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                question = ""
                answer = ""

                # Find Question and Answer columns
                for key, value in row.items():

                    if key and "question" in key.lower():
                        question = value or ""

                    if key and "answer" in key.lower():
                        answer = value or ""

                if question.strip() and answer.strip():

                    self.data.append({
                        "question": question.strip(),
                        "answer": answer.strip()
                    })

        # Built-in fallback medical knowledge
        # Used when the CSV does not contain a matching question.
        self.fallback_data = [

            {
                "keywords": [
                    "fever",
                    "temperature",
                    "high temperature"
                ],
                "answer":
                "Fever is a temporary increase in body temperature, "
                "often caused by an infection. Common symptoms may "
                "include sweating, chills, headache and weakness. "
                "Drink adequate fluids and rest. If the fever is severe, "
                "persistent, or accompanied by serious symptoms, consult "
                "a healthcare professional."
            },

            {
                "keywords": [
                    "diabetes",
                    "blood sugar"
                ],
                "answer":
                "Diabetes is a condition in which blood glucose levels "
                "are higher than normal. Common symptoms can include "
                "increased thirst, frequent urination, fatigue and "
                "unexplained weight changes. Management may involve "
                "healthy eating, physical activity, monitoring blood "
                "glucose and medicines prescribed by a healthcare professional."
            },

            {
                "keywords": [
                    "asthma",
                    "breathing problem"
                ],
                "answer":
                "Asthma is a condition that affects the airways and "
                "can cause symptoms such as wheezing, coughing, chest "
                "tightness and shortness of breath. Treatment depends "
                "on the individual and may include inhaled medicines "
                "prescribed by a healthcare professional."
            },

            {
                "keywords": [
                    "headache",
                    "head pain"
                ],
                "answer":
                "Headache can have many possible causes, including "
                "stress, dehydration, lack of sleep, illness or migraine. "
                "Rest, adequate hydration and identifying possible triggers "
                "may help. Frequent, severe or unusual headaches should be "
                "discussed with a healthcare professional."
            },

            {
                "keywords": [
                    "cough"
                ],
                "answer":
                "Cough is a common symptom that can occur with infections, "
                "allergies, asthma and other conditions. Staying hydrated "
                "and resting may help. A persistent, severe or breathing-"
                "related cough should be evaluated by a healthcare professional."
            },

            {
                "keywords": [
                    "cancer"
                ],
                "answer":
                "Cancer is a group of diseases in which abnormal cells "
                "grow uncontrollably. Symptoms and treatment vary greatly "
                "depending on the type of cancer. Diagnosis and treatment "
                "should be managed by qualified healthcare professionals."
            },

            {
                "keywords": [
                    "hypertension",
                    "high blood pressure"
                ],
                "answer":
                "Hypertension means persistently high blood pressure. "
                "It may not cause noticeable symptoms, which is why regular "
                "blood pressure checks are important. Management can include "
                "lifestyle changes and medicines prescribed by a healthcare professional."
            },

            {
                "keywords": [
                    "migraine"
                ],
                "answer":
                "Migraine is a neurological condition that can cause "
                "moderate to severe headache, sometimes with nausea and "
                "sensitivity to light or sound. Treatment varies between "
                "individuals and should be discussed with a healthcare professional."
            },

            {
                "keywords": [
                    "anemia"
                ],
                "answer":
                "Anemia occurs when the blood does not have enough healthy "
                "red blood cells or hemoglobin. Symptoms may include fatigue, "
                "weakness, dizziness and shortness of breath. The cause should "
                "be identified by a healthcare professional before treatment."
            },

            {
                "keywords": [
                    "pneumonia"
                ],
                "answer":
                "Pneumonia is an infection that causes inflammation in the "
                "air sacs of the lungs. Symptoms can include cough, fever, "
                "chest pain and difficulty breathing. Treatment depends on "
                "the cause and severity and should be determined by a healthcare professional."
            }
        ]

    # -----------------------------------------
    # Tokenization
    # -----------------------------------------

    def tokenize(self, text):

        text = text.lower()

        words = re.findall(
            r"\b[a-z]+\b",
            text
        )

        stop_words = {
            "the",
            "is",
            "are",
            "a",
            "an",
            "what",
            "what's",
            "of",
            "in",
            "to",
            "for",
            "and",
            "or",
            "how",
            "can",
            "does",
            "do",
            "i",
            "my",
            "me",
            "with",
            "on",
            "be",
            "it",
            "about",
            "tell",
            "please"
        }

        return [
            word
            for word in words
            if word not in stop_words
        ]

    # -----------------------------------------
    # Similarity calculation
    # -----------------------------------------

    def similarity(self, question1, question2):

        words1 = set(
            self.tokenize(question1)
        )

        words2 = set(
            self.tokenize(question2)
        )

        if not words1 or not words2:
            return 0

        common_words = words1.intersection(words2)

        score = (
            len(common_words)
            / math.sqrt(
                len(words1) * len(words2)
            )
        )

        return score

    # -----------------------------------------
    # Find answer from MedQuAD
    # -----------------------------------------

    def find_answer(self, user_question):

        best_score = 0
        best_question = ""
        best_answer = ""

        # Search MedQuAD dataset
        for item in self.data:

            score = self.similarity(
                user_question,
                item["question"]
            )

            if score > best_score:

                best_score = score

                best_question = item[
                    "question"
                ]

                best_answer = item[
                    "answer"
                ]

        # If MedQuAD has a good match
        if best_score >= 0.15:

            return (
                best_answer,
                best_score,
                best_question,
                "MedQuAD Dataset"
            )

        # -------------------------------------
        # Fallback knowledge
        # -------------------------------------

        user_text = user_question.lower()

        best_fallback = None
        fallback_score = 0

        for item in self.fallback_data:

            matched = 0

            for keyword in item["keywords"]:

                if keyword in user_text:
                    matched += 1

            if matched > fallback_score:

                fallback_score = matched
                best_fallback = item

        if best_fallback:

            return (
                best_fallback["answer"],
                0.20,
                "General medical information",
                "Medical Knowledge Fallback"
            )

        return (
            "Sorry, I could not find a relevant answer. "
            "Please try asking your question using a disease, "
            "symptom or treatment name.",
            0,
            "",
            "No Match"
        )

    # -----------------------------------------
    # Medical Entity Recognition
    # -----------------------------------------

    def extract_entities(self, text):

        text = text.lower()

        diseases = [
            "diabetes",
            "cancer",
            "asthma",
            "covid",
            "pneumonia",
            "arthritis",
            "migraine",
            "depression",
            "hypertension",
            "heart disease",
            "flu",
            "obesity",
            "anemia",
            "malaria",
            "tuberculosis",
            "stroke"
        ]

        symptoms = [
            "fever",
            "cough",
            "headache",
            "fatigue",
            "pain",
            "nausea",
            "vomiting",
            "dizziness",
            "shortness of breath",
            "rash",
            "swelling",
            "diarrhea",
            "weakness",
            "chest pain",
            "stomach pain"
        ]

        treatments = [
            "medicine",
            "medication",
            "treatment",
            "therapy",
            "vaccine",
            "surgery",
            "antibiotic",
            "insulin",
            "chemotherapy",
            "radiation",
            "injection",
            "inhaler"
        ]

        found_diseases = [
            word
            for word in diseases
            if word in text
        ]

        found_symptoms = [
            word
            for word in symptoms
            if word in text
        ]

        found_treatments = [
            word
            for word in treatments
            if word in text
        ]

        return {
            "Diseases": found_diseases,
            "Symptoms": found_symptoms,
            "Treatments": found_treatments
        }