import whisper


print("Loading Whisper model...")

model = whisper.load_model("base")

print("Whisper model loaded")


def transcribe_video(video_path):

    print("Transcribing:", video_path)

    result = model.transcribe(
        video_path
    )

    transcript = result["text"]

    print(
        "Transcript:",
        transcript
    )

    return transcript