import os
import subprocess


def create_folders(folder_names):

    current_directory = os.path.dirname(__file__)
    
    for folder_name in folder_names:
        folder_path = os.path.join(current_directory, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created successfully in {current_directory}.")
        else:
            print(f"Folder '{folder_name}' already exists in {current_directory}.")

def install_libraries(lib_versions):
    for lib, version in lib_versions.items():
        try:
            subprocess.check_call(["pip", "install", f"{lib}=={version}"])
            print(f"Successfully installed {lib} version {version}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {lib} version {version}.")


def main():

    folder_names = ["input_faces", "input_faces_models", "input_videos", "extracted_frames", "finished_frames", "finished_videos"]
    create_folders(folder_names)

    libraries_and_versions = {"moviepy": "1.0.3", "requests": "2.31.0", "opencv-python": "4.8.0.76", "opencv-contrib-python" : "4.8.1.78"}
    install_libraries(libraries_and_versions)

if __name__ == "__main__":
    main()
