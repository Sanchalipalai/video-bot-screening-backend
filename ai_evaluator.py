import re

print("🔥 LOADED NEW RULE BASED AI EVALUATOR FILE 🔥")
def evaluate_candidate(transcript, question=None):

    print("===== RULE BASED EVALUATOR =====")
    print("TRANSCRIPT:", transcript)
    print("QUESTION:", question)


    transcript = (transcript or "").lower()
    question = (question or "").lower()


    # -----------------------------
    # Communication Score
    # -----------------------------

    words = transcript.split()
    word_count = len(words)

    communication = 50

    if word_count > 40:
        communication += 10

    if word_count > 80:
        communication += 10

    if word_count > 120:
        communication += 10


    sentences = re.split(r"[.!?]", transcript)

    if len([s for s in sentences if s.strip()]) >= 3:
        communication += 10


    fillers = [
        "um",
        "uh",
        "like",
        "you know",
        "basically",
        "actually"
    ]

    for filler in fillers:
        communication -= transcript.count(filler) * 2


    communication = max(0, min(100, communication))


    # -----------------------------
    # Technical Score
    # -----------------------------

    technical_keywords = [
        "python",
        "java",
        "javascript",
        "react",
        "node",
        "fastapi",
        "api",
        "sql",
        "database",
        "docker",
        "aws",
        "git",
        "github",
        "machine learning",
        "ai"
    ]


    technical = 40


    for keyword in technical_keywords:
        if keyword in transcript:
            technical += 5


    technical = min(100, technical)



    # -----------------------------
    # Confidence Score
    # -----------------------------

    confidence = 60


    strong_words = [
        "built",
        "created",
        "developed",
        "implemented",
        "designed",
        "experience",
        "managed"
    ]


    weak_words = [
        "maybe",
        "probably",
        "not sure",
        "guess"
    ]


    for word in strong_words:
        if word in transcript:
            confidence += 5


    for word in weak_words:
        if word in transcript:
            confidence -= 8


    confidence = max(0, min(100, confidence))



    # -----------------------------
    # Relevance Score
    # -----------------------------

    question_words = [
        word for word in question.split()
        if len(word) > 3
    ]


    matches = 0

    for word in question_words:
        if word in transcript:
            matches += 1


    if question_words:
        relevance = int(
            matches / len(question_words) * 100
        )
    else:
        relevance = 70


    relevance = max(40, min(100, relevance))



    # -----------------------------
    # Final Score
    # -----------------------------

    overall = int(
        communication * 0.30 +
        technical * 0.35 +
        confidence * 0.15 +
        relevance * 0.20
    )



    # -----------------------------
    # Feedback
    # -----------------------------

    feedback = []


    if communication >= 70:
        feedback.append(
            "Communication is clear."
        )
    else:
        feedback.append(
            "Candidate should explain ideas more clearly."
        )


    if technical >= 70:
        feedback.append(
            "Good technical knowledge demonstrated."
        )
    else:
        feedback.append(
            "More technical details are needed."
        )


    if confidence >= 70:
        feedback.append(
            "Candidate appears confident."
        )


    if relevance >= 70:
        feedback.append(
            "Answer is relevant to the question."
        )
    else:
        feedback.append(
            "Answer could be more focused."
        )


    result = {
        "overall_score": overall,
        "communication_score": communication,
        "technical_score": technical,
        "confidence_score": confidence,
        "relevance_score": relevance,
        "feedback": " ".join(feedback)
    }


    print("RULE RESULT:", result)


    return result