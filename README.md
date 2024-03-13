# face2video

This script automates the process of applying face swap to videos using Automatic 1111 with the Reactor extension. The video is split into frames, which are edited using Reactor, and then merged back into a video. Sound is also copied in the process. This script was created because the manual process was rather tedious to do otherwise.

You can also use ForgeUI instead of Automatic 1111.

### How to install

You will need working installations of both Automatic 1111 and Reactor for this script to work.
- [Automatic 1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Reactor](https://github.com/Gourieff/sd-webui-reactor)

The Automatic 1111 API needs to be enabled. Add "--api" to the COMMANDLINE_ARGS in the webui-user.bat file in the Automatic 1111 directory.

To install all other dependencies and set up all the needed folders, simply run the install.py script once.

### How to use

1. Put your target video in the input_videos folder and your face image into the input_faces folder (the script has been tested with .mp4, .png, and .jpg files).
2. Run the main.py file to start the gui.  
3. Click on "Choose Face" and then on "Choose Video" and select the files you want to use from the input folders.
4. Click on "Split Video Into Frames". 
5. Click on "Swap Face". (Automatic 1111 has to be running for this step to work)
6. Click on "Merge Frames Into Video".
7. Your finished video file will be in the finished_videos folder.

### Limitations

Since this script uses Reactor, it is limited when applied to faces with lots of movement, especially talking. Face swapping into videos also takes a considerable amount of time, simply because there are a lot of frames even in short clips.
