import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def transcribe_video(video_path):

    print("OPENAI KEY EXISTS:", bool(os.getenv("OPENAI_API_KEY")))

    try:

        with open(video_path, "rb") as audio_file:

            result = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        print("TRANSCRIPT RESULT:", result.text)

        return result.text

    except Exception as e:

        print("OPENAI ERROR TYPE:", type(e).__name__)
        print("OPENAI ERROR:", repr(e))

        if hasattr(e, "__cause__") and e.__cause__:
            print("CAUSE:", repr(e.__cause__))

        if hasattr(e, "__context__") and e.__context__:
            print("CONTEXT:", repr(e.__context__))

        raise