import subprocess
from enum import StrEnum


class YtDlpWrapper:

    DEFAULT_FOLDER = "downloads"

    class RequestType(StrEnum):
        best_audio = "best_audio" 
        davinci_compatible = "davinci_compatible"
        best_video_and_audio = "best_video_and_audio"

    commands: dict[RequestType, str] = {
        RequestType.best_audio: 'yt-dlp -o "{directory}/%(title)s by %(uploader)s.%(ext)s" -f ba -x --audio-format mp3 --audio-quality 320k {URL}',
        RequestType.davinci_compatible: 'yt-dlp -o "{directory}/HVENC264 - %(title)s by %(uploader)s.%(ext)s" -S vcodec:h264,res,acodec:aac "{URL}"',
        RequestType.best_video_and_audio: 'yt-dlp -o "{directory}/%(title)s.%(ext)s" -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" {URL}',
    }

    @staticmethod
    def call(request: RequestType, url: str, directory = DEFAULT_FOLDER):
        command = YtDlpWrapper.commands[request].format(directory = directory, URL = url);
        print("Running command %s" % command)
        subprocess.run(command, shell=True, capture_output=True)
