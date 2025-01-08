# ROS Project: Streaming video from a connected camera
### About
Stream video from Publisher to Subscribers using OpenCV and Flask. And it can be viewed using Qt app "video_stream/app.py" or any web browser at the specified IP Address, Or You can use the IP Address as an REST API for streaming, BUT USE "img" HTML TAGNAME not "video" AND THE IP ADDRESS AS "src" ATTRIBUTE.
## Requirements
- ROS 2 (Preferred "Jazzy" Distro)
- Flask
- Connected Camera
- OpenCV ("cv2" module)
## Setup
1. Copy "Makefile.build" to ros projects directory
2. Rename it to "Makefile"
3. Copy this script to your shell config file e.g.".bashrc" or ".zshrc"
  Bash:
```bash
source ~/{ros_projects}/install/setup.bash
source {ros_location}/{ros_distro}/setup.bash
```
  Zsh:
```zsh
source ~/{ros_projects}/install/setup.zsh
source {ros_location}/{ros_distro}/setup.zsh
```
4. Replace each placeholder with it's correct location
5. Restart your shell
## Build the project
Preferred to have multiple terminal session opened
1. Export an environment variable "ROS_PACKAGE" to the name of the project.
  Ex:
  ```bash
export ROS_PACKAGE="video_stream"
  ```
2. Run "make" in projects directory.
3. Switch to another terminal session and goto project's directory
4. To execute Publisher script run "make pub"
5. To execute Subscriber script run "make sub"
