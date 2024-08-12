import cv2
import os
import datetime
import re


def set_image_names(folder_path):

    for filename in os.listdir(folder_path):
        print("renaming file: {}".format(filename))
        if filename.endswith('.jpg') or filename.endswith('.png'):

            pattern = re.compile(r'(frame\d+)')
            match = pattern.search(filename)

            if match:
                new_name = match.group(1)
                new_path = os.path.join(folder_path, new_name + ".jpg")
                old_path = os.path.join(folder_path, filename)

                print(old_path)
                print(new_path)

                os.rename(old_path, new_path)   
            else:
                print("Pattern not found in the input string.")

def extract_frame_number(filename):
    return int(filename.lstrip("frame").rstrip(".jpg"))

def create_video(folder_path):

    set_image_names(folder_path)

    images = [img for img in os.listdir(folder_path) if img.endswith(".jpg")]
    images = sorted(images, key=extract_frame_number)

    frame = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, layers = frame.shape

    current_directory = os.getcwd()
    f_path = os.path.join(current_directory, "extensions", "face2video", "finished_videos")
    os.chdir(f_path)

    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    video_name = 'output_video_{}.mp4'.format(current_datetime)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

    for image in images:
        img_path = os.path.join(folder_path, image)
        frame = cv2.imread(img_path)
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()

    return video_name
