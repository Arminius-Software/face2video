import get_frames_from_video
import turn_frames_into_video
import copy_sound_from_video
import automatic1111_api
import os


# put path to face image / input video here before running script
# tested only with .mp4

path_input_video = "input_videos/video.mp4"
path_input_face = "input_faces/face.jpg"

frames_input = "extracted_frames/"
frames_output = "finished_frames/"

def create_frames(path_input_video):

    get_frames_from_video.get_frames(path_input_video)

def change_face(path_input_face, frames_input):

    files = os.listdir(frames_input)
            
    for file in files:
        file_path = os.path.join(frames_input, file)
        automatic1111_api.api_change_face(file, path_input_face, file_path)

def create_final_video(frames_input, frames_output):

    file_name_video = turn_frames_into_video.create_video(frames_output)

    print(path_input_video)
    print(file_name_video)

    copy_sound_from_video.add_sound(path_input_video, file_name_video)

    # delete frames when video is finished

    paths = [frames_input, frames_output]

    for path in paths:
        if os.path.exists(path):
            files = os.listdir(path)
            
            for file in files:
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    print(f"Skipped {file_path} as it's not a file.")
        else:
            print(f"The folder path '{path}' does not exist.")


def main():
    create_frames(path_input_video)
    change_face(path_input_face, frames_input)
    create_final_video(frames_input, frames_output)


if __name__ == "__main__":
    main()