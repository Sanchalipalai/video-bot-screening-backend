import re



def analyze_transcript(question, transcript):


    text = transcript.lower()


    score = 0


    # -------------------------
    # 1. Communication score
    # -------------------------

    words = len(
        transcript.split()
    )


    if words >= 100:
        communication = 90

    elif words >= 60:
        communication = 80

    elif words >= 30:
        communication = 70

    else:
        communication = 50



    # -------------------------
    # 2. Technical knowledge
    # -------------------------

    technical_keywords = [

        "python",
        "java",
        "javascript",
        "react",
        "api",
        "database",
        "sql",
        "cloud",
        "aws",
        "docker",
        "machine learning",
        "ai",
        "backend",
        "frontend",
        "fastapi"

    ]


    found = 0


    for word in technical_keywords:

        if word in text:
            found += 1



    technical = min(
        50 + (found * 10),
        100
    )



    # -------------------------
    # 3. Confidence
    # -------------------------

    confidence_words = [

        "worked",
        "built",
        "developed",
        "implemented",
        "created",
        "experience"

    ]


    confidence_hits = 0


    for word in confidence_words:

        if word in text:
            confidence_hits += 1



    confidence = min(
        50 + confidence_hits * 10,
        100
    )



    # -------------------------
    # Final score
    # -------------------------

    overall = round(

        (
            communication
            +
            technical
            +
            confidence

        ) / 3,

        2

    )



    feedback = ""


    if overall >= 80:

        feedback = (
            "Strong answer. "
            "Candidate demonstrated good communication "
            "and technical understanding."
        )


    elif overall >= 60:

        feedback = (
            "Average answer. "
            "Candidate should provide more technical "
            "details and examples."
        )


    else:

        feedback = (
            "Weak answer. "
            "Candidate needs clearer explanation "
            "and more relevant experience."
        )



    return {


        "communication_score": communication,


        "technical_score": technical,


        "confidence_score": confidence,


        "overall_score": overall,


        "feedback": feedback

    }