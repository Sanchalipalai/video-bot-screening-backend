import os
import json
from openai import OpenAI


print("XAI KEY EXISTS:", bool(os.getenv("XAI_API_KEY")))


client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)


def analyze_transcript(question, transcript):

    try:
        response = client.chat.completions.create(
            model="grok-3-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI interview evaluator.

Evaluate the candidate answer based on:
- Communication clarity
- Relevance to question
- Technical understanding
- Confidence
- Completeness

Return ONLY valid JSON.

Format:
{
    "overall_score": number between 0 and 100,
    "feedback": "short detailed feedback"
}
"""
                },
                {
                    "role": "user",
                    "content": f"""
Interview Question:
{question}

Candidate Answer:
{transcript}
"""
                }
            ],
            temperature=0.3
        )


        result_text = response.choices[0].message.content

        print("GROK RAW RESULT:", result_text)


        # Remove markdown formatting if Grok adds it
        result_text = result_text.replace("```json", "")
        result_text = result_text.replace("```", "")
        result_text = result_text.strip()


        result = json.loads(result_text)

        return result


    except Exception as e:
        print("GROK ERROR:", e)

        return {
            "overall_score": 0,
            "feedback": "AI evaluation failed"
        }