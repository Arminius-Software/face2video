from moviepy.editor import VideoFileClip
import datetime
import os


def add_sound(video_sound_path, video_no_sound_path):
    
    video_with_sound = VideoFileClip(video_sound_path)
    video_without_sound = VideoFileClip(video_no_sound_path)

    video_without_sound = video_without_sound.set_audio(video_with_sound.audio)

    fps = video_with_sound.fps or 30
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = "finished_videos/final_{}.mp4".format(current_datetime)

    video_without_sound.write_videofile(output_path, codec='libx264', fps=fps)

    os.remove(video_no_sound_path)
