from moviepy.editor import VideoFileClip, AudioFileClip
from glob import glob
import ntpath
import os

def convert_video_to_audio_moviepy(video_fn, target_fp, output_ext="wav"):
    clip = VideoFileClip(video_fn)
    clip.audio.write_audiofile(f"{target_fp}/{ntpath.basename(video_fn)[:-4]}.{output_ext}")

def change_audio_format(audio_fn, target_fp, output_ext="wav"):
    clip = AudioFileClip(audio_fn)
    clip.write_audiofile(f"{target_fp}/{ntpath.basename(audio_fn)[:-4]}.{output_ext}")

if __name__ == "__main__":
    source_fp = 'videos/*.mp4'
    target_fp = 'audio'
    files = glob(source_fp)
    os.makedirs(target_fp, exist_ok=True)
    for file in files:
        convert_video_to_audio_moviepy(file, target_fp)
        # change_audio_format(file, target_fp)