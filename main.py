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
        self.processing_unit = "CPU"
        self.input_type = "Single Image"
        self.main_path = os.path.dirname(os.path.abspath(__file__))

    def append_output(self, text):

        text = f"{text} \n"
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, text)
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)

    def open_file_dialog_face(self):
        
        if self.input_type == "Single Image":
            path = "input_faces/"
        else:
            path = "input_faces_models"
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        initial_directory = os.path.join(current_directory, path)
        
        directory_path = filedialog.askopenfile(initialdir=initial_directory)
        if directory_path:
            file_name = os.path.basename(directory_path.name)
            self.append_output(f"Selected {file_name}")
            self.input_face = directory_path.name

    def open_file_dialog_video(self):

        path = "input_videos/"
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        initial_directory = os.path.join(current_directory, path)
        
        directory_path = filedialog.askopenfile(initialdir=initial_directory)
        if directory_path:
            file_name = os.path.basename(directory_path.name)
            self.append_output(f"Selected {file_name}")
            self.input_video = directory_path.name

    def change_processing_unit(self):

        if self.processing_unit == "GPU (CUDA)":
            self.processing_unit = "CPU"
        else:
            self.processing_unit = "GPU (CUDA)"

        self.append_output("Automatic1111 needs to be restarted after changing the \nprocessing unit for changes to apply!")

    def change_input_type(self):

        if self.input_type == "Single Image":
            self.input_type = "Face Model"
        else:
            self.input_type = "Single Image"

    def split_video(self):

        if self.input_video == "":
            self.append_output("No video selected")
        else:
            self.append_output("Splitting video into frames...")
            get_frames_from_video.get_frames(os.path.join(self.main_path, self.input_video), self.main_path)
            self.append_output("Finished splitting video into frames")
            self.append_output("Ready to swap face")

    def start_split_video_thread(self):

        thread = threading.Thread(target=self.split_video)
        thread.start()

    def swap_face(self):

        if self.input_video == "" or self.input_face == "":
            self.append_output("Select a face and a video")
        else:
            files = os.listdir(self.main_path + "/extracted_frames/")

            if self.input_type == "Single Image":
                source_choice = 0
                input_model = ""
            else:
                source_choice = 1
                input_model = self.input_face
                self.input_face = ""

            for index, file in enumerate(files):
                file_path = os.path.join(self.main_path, "extracted_frames", file)
                automatic1111_api.api_change_face(file, self.input_face, input_model, file_path, self.processing_unit, source_choice)
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
        file_name_video = turn_frames_into_video.create_video(os.path.join(self.main_path, "finished_frames"))
        self.append_output("Adding sound...")
        copy_sound_from_video.add_sound(self.input_video,file_name_video)
        self.append_output("Finished creating video!")

        self.delete_old_frames()

    def start_merge_video_thread(self):
        thread = threading.Thread(target=self.merge_video)
        thread.start()       


root = tk.Tk()
root.title("Face2Video")
root.geometry("800x800") 

dark_background_color = "#333333" 
text_color = "white"  
root.configure(bg=dark_background_color)

file_button_width = 20
file_button_height = 2

button_width = 30
button_height = 2

new_video = Face2Video()

header_label = tk.Label(root, text="Face2Video - Easy Faceswapping", font=("Helvetica", 20, "bold"), fg=text_color, bg=dark_background_color)
header_label.pack(pady=20)

processing_unit_button = tk.Button(root, text=f"Selected: {new_video.processing_unit}", command=lambda: update_button_processing_unit(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
processing_unit_button.pack(pady=5)

input_type_button = tk.Button(root, text=f"Selected: {new_video.input_type}", command=lambda: update_button_input_type(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
input_type_button.pack(pady=5)

select_face_button = tk.Button(root, text="Choose Face", command=lambda: new_video.open_file_dialog_face(), font=("Helvetica", 14), width=file_button_width, height=file_button_height, bg=dark_background_color, fg=text_color)
select_face_button.pack(pady=5)

select_video_button = tk.Button(root, text="Choose Video", command=lambda: new_video.open_file_dialog_video(), font=("Helvetica", 14), width=file_button_width, height=file_button_height, bg=dark_background_color, fg=text_color)
select_video_button.pack(pady=5)

split_button = tk.Button(root, text="Split Video Into Frames", command=lambda: new_video.start_split_video_thread(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
split_button.pack(pady=5)

swap_button = tk.Button(root, text="Swap Face", command=lambda: new_video.start_swap_face_thread(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
swap_button.pack(pady=5)

merge_button = tk.Button(root, text="Merge Frames Into Video", command=lambda: new_video.start_merge_video_thread(), font=("Helvetica", 14), width=button_width, height=button_height, bg=dark_background_color, fg=text_color)
merge_button.pack(pady=5)

output_text = tk.Text(root, height=10, width=50, font=("Helvetica", 12), bg=dark_background_color, fg=text_color, state=tk.DISABLED)
output_text.pack(pady=10)

def update_button_processing_unit():

    new_video.change_processing_unit()
    processing_unit_button.config(text=f"Selected: {new_video.processing_unit}")

def update_button_input_type():

    new_video.change_input_type()
    input_type_button.config(text=f"Selected: {new_video.input_type}")

if __name__ == "__main__":
    root.mainloop()
