import os
import json

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def fallback_analysis(question, transcript):

    text = transcript.lower()

    words = len(transcript.split())

    if words >= 100:
        communication = 90
    elif words >= 60:
        communication = 80
    elif words >= 30:
        communication = 70
    else:
        communication = 50

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

    found = sum(1 for keyword in technical_keywords if keyword in text)

    technical = min(50 + found * 10, 100)

    confidence_words = [
        "worked",
        "built",
        "developed",
        "implemented",
        "created",
        "experience"
    ]

    confidence_hits = sum(1 for word in confidence_words if word in text)

    confidence = min(50 + confidence_hits * 10, 100)

    overall = round(
        (communication + technical + confidence) / 3,
        2
    )

    if overall >= 80:
        feedback = "Strong answer. Candidate demonstrated good communication and technical understanding."
        recommendation = "Hire"

    elif overall >= 60:
        feedback = "Average answer. Candidate should provide more technical details and examples."
        recommendation = "Maybe"

    else:
        feedback = "Weak answer. Candidate needs clearer explanation and more relevant experience."
        recommendation = "No Hire"

    return {

        "communication_score": communication,

        "technical_score": technical,

        "confidence_score": confidence,

        "overall_score": overall,

        "recommendation": recommendation,

        "strengths": [],

        "improvements": [],

        "feedback": feedback

    }


def analyze_transcript(question, transcript):

    if transcript.strip() == "":
        return fallback_analysis(question, transcript)

    prompt = f"""
You are an experienced technical recruiter.

Evaluate the candidate's interview answer.

Question:
{question}

Transcript:
{transcript}

Return ONLY valid JSON.

{{
    "communication_score": 0-100,
    "technical_score": 0-100,
    "confidence_score": 0-100,
    "overall_score": 0-100,
    "recommendation": "Hire" or "Maybe" or "No Hire",
    "strengths": [
        "...",
        "..."
    ],
    "improvements": [
        "...",
        "..."
    ],
    "feedback": "Short recruiter feedback"
}}
"""

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": "You are a senior technical recruiter."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2

        )

        result = response.choices[0].message.content

        print("AI RESPONSE:")
        print(result)

        return json.loads(result)

    except Exception as e:

        print("OPENAI ERROR:", e)

        return fallback_analysis(question, transcript)