import get_frames_from_video
import turn_frames_into_video
import copy_sound_from_video
import automatic1111_api

import tkinter as tk
from tkinter import filedialog

import threading
import os


class Face2Video():

    def __init__(self):
        self.input_face = ""
        self.input_video = ""

    def append_output(self, text):
        text = f"{text} \n"
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, text)
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)

    def open_file_dialog(self, path, is_face):
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        initial_directory = os.path.join(current_directory, path)
        
        directory_path = filedialog.askopenfile(initialdir=initial_directory)
        if directory_path:
            file_name = os.path.basename(directory_path.name)
            self.append_output(f"Selected {file_name}")
            if is_face:
                self.input_face = directory_path.name
            else:
                self.input_video = directory_path.name

    def split_video(self):

        if self.input_video == "":
            self.append_output("No video selected")
        else:
            self.append_output("Splitting video into frames...")
            get_frames_from_video.get_frames(self.input_video)
            self.append_output("Finished splitting video into frames")
            self.append_output("Ready to swap face")

    def start_split_video_thread(self):
        thread = threading.Thread(target=self.split_video)
        thread.start()

    def swap_face(self):
        if self.input_video == "" or self.input_face == "":
            self.append_output("Select a face and a video")
        else:
            files = os.listdir("extracted_frames/")
            for index, file in enumerate(files):
                file_path = os.path.join("extracted_frames/", file)
                automatic1111_api.api_change_face(file, self.input_face, file_path)
                self.append_output(f"Finished image {index + 1} of {len(files)}")
            self.append_output("Finished swapping faces")
            self.append_output("Ready to merge frames")

    def start_swap_face_thread(self):
        thread = threading.Thread(target=self.swap_face)
        thread.start()

    def delete_old_frames(self):

        paths = ["extracted_frames/", "finished_frames/"]

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

    def merge_video(self):

        self.append_output("Creating video...")
        file_name_video = turn_frames_into_video.create_video("finished_frames/")
        self.append_output("Adding sound...")
        copy_sound_from_video.add_sound(self.input_video,file_name_video)
        self.append_output("Finished creating video!")

        self.delete_old_frames()

    def start_merge_video_thread(self):
        thread = threading.Thread(target=self.merge_video)
        thread.start()       


root = tk.Tk()
root.title("Face2Video")
root.geometry("800x600") 

dark_background_color = "#333333" 
text_color = "white"  
root.configure(bg=dark_background_color)

file_button_width = 20
file_button_height = 2

button_width = 30
button_height = 2

new_video = Face2Video()

header_label = tk.Label(root, text="Face2Video - Easy Faceswapping", font=("Helvetica", 20, "bold"), fg=text_color, bg=dark_background_color)
header_label.pack(pady=15)

select_face_button = tk.Button(root, text="Choose Face", command=lambda: new_video.open_file_dialog("input_faces/", True), font=("Helvetica", 12), width=file_button_width, height=file_button_height, bg=dark_background_color, fg=text_color)
select_face_button.pack(pady=5)

select_video_button = tk.Button(root, text="Choose Video", command=lambda: new_video.open_file_dialog("input_videos/", False), font=("Helvetica", 12), width=file_button_width, height=file_button_height, bg=dark_background_color, fg=text_color)
select_video_button.pack(pady=5)

split_button = tk.Button(root, text="Split Video Into Frames", command=lambda: new_video.start_split_video_thread(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
split_button.pack(pady=5)

swap_button = tk.Button(root, text="Swap Face", command=lambda: new_video.start_swap_face_thread(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
swap_button.pack(pady=5)

merge_button = tk.Button(root, text="Merge Frames Into Video", command=lambda: new_video.start_merge_video_thread(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
merge_button.pack(pady=5)

output_text = tk.Text(root, height=10, width=50, font=("Helvetica", 12), bg=dark_background_color, fg=text_color, state=tk.DISABLED)
output_text.pack(pady=10)


if __name__ == "__main__":
    root.mainloop()
