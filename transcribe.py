import whisper
import os


# Tell Python where FFmpeg is
os.environ["PATH"] += os.pathsep + r"C:\Users\spala\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin"


model = whisper.load_model("base")


def transcribe_video(video_path):

    result = model.transcribe(
        video_path
    )

    return result["text"]