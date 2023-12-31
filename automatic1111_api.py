import requests
import base64
import os


# see http://127.0.0.1:7860/docs#/
# add --api in webui-user

url = "http://127.0.0.1:7860"

def api_change_face(file, face_image, input_image):

  # Open the image file in binary mode
  with open(input_image, "rb") as image_file:
      image_binary = image_file.read()

  base64_image = base64.b64encode(image_binary).decode('utf-8')

  with open(face_image, "rb") as image_file:
      image_binary_face = image_file.read()
  base64_image_face = base64.b64encode(image_binary_face).decode('utf-8')

  current_directory = os.getcwd()
  path = os.path.join(current_directory, "finished_frames/")
  result_path = os.path.join(path, file)

  payload = {
    "source_image": base64_image_face,
    "target_image": base64_image,
    "source_faces_index": [
      0
    ],
    "face_index": [
      0
    ],
    "upscaler": "None",
    "scale": 1,
    "upscale_visibility": 1,
    "face_restorer": "None",
    "restorer_visibility": 1,
    "codeformer_weight": 0.5,
    "restore_first": 1,
    "model": "inswapper_128.onnx",
    "gender_source": 0,
    "gender_target": 0,
    "save_to_file": 1,
    "result_file_path": result_path
  }

  response = requests.post(url=f'{url}/reactor/image', json=payload)

  #r = response.json()
  #print("Response Code:", response.status_code)
