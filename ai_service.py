from ai_evaluator import evaluate_candidate


def analyze_transcript(question, transcript):

    try:
        print("===== LOCAL AI EVALUATOR =====")

        result = evaluate_candidate(
            transcript,
            question
        )

        print(
            "LOCAL AI RESULT:",
            result
        )

        return result


    except Exception as e:

        print(
            "LOCAL EVALUATOR ERROR:",
            e
        )

        return {
            "overall_score": 0,
            "feedback": "Evaluation failed"
        }