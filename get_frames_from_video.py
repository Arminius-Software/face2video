import cv2


def get_frames(path):

  vidcap = cv2.VideoCapture(path)

  success,image = vidcap.read()
  count = 0
  success = True

  while success:

    try:
      success,image = vidcap.read()
      count += 1 
      print('Read a new frame: ', success)

      cv2.imwrite("extracted_frames/frame%d.jpg" % count, image)
    except Exception:

      print("finished extracting frames from video")