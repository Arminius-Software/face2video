# face2video

This script automates the process of applying face swap to videos using Automatic 1111 with the Reactor extension. The video is split into frames, which are edited using Reactor, and then merged back into a video. Sound is also copied in the process. This script was created because the manual process was rather tedious to do otherwise.

### How to install

You will need working installations of both Automatic 1111 and Reactor for this script to work.
- [Automatic 1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Reactor](https://github.com/Gourieff/sd-webui-reactor)

The Automatic 1111 API needs to be enabled. Add "--api" to the COMMANDLINE_ARGS in the webui-user.bat file in the Automatic 1111 directory.

To install all other dependencies and set up all the needed folders, simply run the install.py script once.

### How to use

1. Put your target video in the input_videos folder and your face images into the input_faces folder (the script has been tested with .mp4, .png, and .jpg files).
2. Go into the main.py file and put the name of your face input file and video input file into the path_input_face and path_input_video variables.
3. Run main.py. (Automatic 1111 has to be running for this step to work)

### Limitations

Since this script uses Reactor, it is limited when applied to faces with lots of movement, especially talking. Face swapping into videos also takes a considerable amount of time, simply because there are a lot of frames even in short clips.
