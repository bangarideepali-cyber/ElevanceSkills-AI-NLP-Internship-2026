from langdetect import detect

# ==========================================
# CONVERSATION MEMORY
# ==========================================

conversation_history = []


# ==========================================
# LANGUAGE DETECTION
# ==========================================

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"


# ==========================================
# INTENT DETECTION
# ==========================================

def detect_intent(text):

    text_lower = text.lower()

    # Greeting
    if (
        "hello" in text_lower
        or "hi" in text_lower
        or "hey" in text_lower
        or "नमस्ते" in text
        or "नमस्कार" in text
    ):
        return "greeting"

    # Python learning
    if (
        "python" in text_lower
        and (
            "learn" in text_lower
            or "सीख" in text
            or "शिक" in text
        )
    ):
        return "python_learning"

    # Python question
    if "python" in text_lower:
        return "python_question"

    # Name question
    if (
        "what is my name" in text_lower
        or "what's my name" in text_lower
        or "मेरा नाम क्या है" in text
        or "माझे नाव काय आहे" in text
        or "আমার নাম কি" in text
        or "আমার নাম কী" in text
    ):
        return "name_question"

    # Goodbye
    if (
        "bye" in text_lower
        or "goodbye" in text_lower
        or "अलविदा" in text
        or "बाय" in text
        or "निघतो" in text
    ):
        return "goodbye"

    return "general"


# ==========================================
# FIND SAVED NAME
# ==========================================

def find_saved_name():

    for message in reversed(conversation_history):

        old_message = message["user"]
        old_text = old_message.lower()

        # English
        if "my name is" in old_text:

            name = old_text.split("my name is", 1)[1].strip()

            if name:
                return name.title()

        # Hindi
        if (
            "मेरा नाम" in old_message
            and "क्या" not in old_message
        ):

            name = old_message.split("मेरा नाम", 1)[1]

            name = name.replace("है", "").strip()

            if name:
                return name

        # Marathi
        if (
            "माझे नाव" in old_message
            and "काय" not in old_message
        ):

            name = old_message.split("माझे नाव", 1)[1]

            name = name.replace("आहे", "").strip()

            if name:
                return name

        # Bengali
        if (
            "আমার নাম" in old_message
            and "কি" not in old_message
            and "কী" not in old_message
        ):

            name = old_message.split("আমার নাম", 1)[1]

            name = (
                name
                .replace("হয়", "")
                .replace("হয়", "")
                .strip()
            )

            if name:
                return name

    return None


# ==========================================
# MAIN CHATBOT FUNCTION
# ==========================================

def get_response(user_message):

    # Detect language
    language = detect_language(user_message)

    # Detect intent
    intent = detect_intent(user_message)

    # Save conversation
    conversation_history.append({
        "user": user_message,
        "language": language,
        "intent": intent
    })

    text = user_message.lower().strip()


    # ======================================
    # NAME - ENGLISH
    # ======================================

    if "my name is" in text:

        name = text.split("my name is", 1)[1].strip()

        response = (
            f"Nice to meet you, {name.title()}! "
            "I will remember your name."
        )


    # ======================================
    # NAME - HINDI
    # ======================================

    elif (
        "मेरा नाम" in user_message
        and "क्या" not in user_message
    ):

        name = user_message.split("मेरा नाम", 1)[1]

        name = name.replace("है", "").strip()

        response = (
            f"ठीक है, {name}! "
            "मुझे आपका नाम याद रहेगा।"
        )


    # ======================================
    # NAME - MARATHI
    # ======================================

    elif (
        "माझे नाव" in user_message
        and "काय" not in user_message
    ):

        name = user_message.split("माझे नाव", 1)[1]

        name = name.replace("आहे", "").strip()

        response = (
            f"ठीक आहे, {name}! "
            "मला तुमचे नाव लक्षात राहील."
        )


    # ======================================
    # NAME - BENGALI
    # ======================================

    elif (
        "আমার নাম" in user_message
        and "কি" not in user_message
        and "কী" not in user_message
    ):

        name = user_message.split("আমার নাম", 1)[1]

        name = (
            name
            .replace("হয়", "")
            .replace("হয়", "")
            .strip()
        )

        response = (
            f"ঠিক আছে, {name}! "
            "আমি আপনার নাম মনে রাখব।"
        )


    # ======================================
    # ASK NAME
    # ======================================

    elif intent == "name_question":

        name = find_saved_name()

        if name:

            if language == "hi":

                response = f"आपका नाम {name} है।"

            elif language == "mr":

                response = f"तुमचे नाव {name} आहे."

            elif language == "bn":

                response = f"আপনার নাম {name}।"

            else:

                response = f"Your name is {name}."

        else:

            response = (
                "You have not told me your name yet."
            )


    # ======================================
    # GREETING
    # ======================================

    elif intent == "greeting":

        if language == "hi":

            response = "नमस्ते! मैं आपकी मदद करने के लिए यहाँ हूँ।"

        elif language == "mr":

            response = "नमस्कार! मी तुम्हाला मदत करण्यासाठी येथे आहे."

        elif language == "bn":

            response = "নমস্কার! আমি আপনাকে সাহায্য করতে এখানে আছি।"

        else:

            response = "Hello! How can I help you?"


    # ======================================
    # PYTHON LEARNING
    # ======================================

    elif intent == "python_learning":

        if language == "mr":

            response = (
                "हो! मी तुम्हाला Python शिकायला मदत करू शकते. "
                "आपण Python basics पासून सुरुवात करूया."
            )

        elif language == "hi":

            response = (
                "हाँ! मैं आपको Python सीखने में मदद कर सकती हूँ। "
                "हम Python basics से शुरुआत कर सकते हैं।"
            )

        else:

            response = (
                "Yes! I can help you learn Python. "
                "We can start with Python basics."
            )


    # ======================================
    # PYTHON QUESTION
    # ======================================

    elif intent == "python_question":

        if language == "mr":

            response = (
                "Python ही एक popular programming language आहे. "
                "ती Data Science, AI आणि Web Development मध्ये वापरली जाते."
            )

        elif language == "hi":

            response = (
                "Python एक popular programming language है। "
                "इसका उपयोग Data Science, AI और Web Development में किया जाता है।"
            )

        else:

            response = (
                "Python is a popular programming language. "
                "It is widely used in Data Science, AI and Web Development."
            )


    # ======================================
    # GOODBYE
    # ======================================

    elif intent == "goodbye":

        if language == "hi":

            response = "अलविदा! फिर मिलते हैं।"

        elif language == "mr":

            response = "निरोप! पुन्हा भेटूया."

        elif language == "bn":

            response = "বিদায়! আবার দেখা হবে।"

        else:

            response = "Goodbye! See you again."


    # ======================================
    # GENERAL HINDI
    # ======================================

    elif language == "hi":

        response = (
            "मैं आपका प्रश्न समझ गई। "
            "मैं आपकी मदद करने के लिए यहाँ हूँ।"
        )


    # ======================================
    # GENERAL MARATHI
    # ======================================

    elif language == "mr":

        response = (
            "मला तुमचा प्रश्न समजला. "
            "मी तुम्हाला मदत करण्यासाठी येथे आहे."
        )


    # ======================================
    # GENERAL BENGALI
    # ======================================

    elif language == "bn":

        response = (
            "আমি আপনার প্রশ্ন বুঝতে পেরেছি। "
            "আমি আপনাকে সাহায্য করতে এখানে আছি।"
        )


    # ======================================
    # GENERAL ENGLISH
    # ======================================

    else:

        response = (
            "I understand your question. "
            "I am here to help you."
        )


    return response