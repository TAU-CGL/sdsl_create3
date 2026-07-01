# sdsl-create3
iRobot Create3 ROS node for companion Raspberry Pi for the SDSL (Sparse Distance Sampling Localization) project.

This package depends also on the iRobot Create3 examples: [https://github.com/iRobotEducation/create3_examples](https://github.com/iRobotEducation/create3_examples)

## Introduction

The SDSL method was originally presented on ICRA 2023, with subsequent papers also in 2025 & 2026.  
We solve the kidnapped robot problem. That is, we assume the map of the environment is known; we strive to find the robot's location using merely k (~16) distance measurements and the robot's odometry.  
Localization should be robust even in the face of unforeseen obstacles or changes in the environment, so long that the majority of the k distance samples correspond to features in the prior map of the environment.

This repository should contain everything to recreate the physical demonstration of the SDSL approach on an iRobot Create 3.

In this project, we support three modes for the robot:
* Mapping - This mode should be used ideally only once, to capture a (rough) map of the environment.
* Localization - Start the localization of the robot. Publishes a pose with covariance, either by the SDSL method or other baselines we compare to in our papers. 
* Navigation - The robot can navigate to any other pose in the envrionment upon demand. Whenever the pose is uncertain, the robot first moves and gathers further measurements autonomously until it converges to a certain pose.

### Related Repositories

The current repository ([sdsl_create3](https://github.com/TAU-CGL/sdsl_create3)) contains only a useful launchfile, specifically for the iRobot Create 3 robot, and a dockerfile that sets up the demo.

The [sdsl](https://github.com/TAU-CGL/sdsl) library is a C++ header-only implementation of the method, with Python bindings. It can be used in wider contexts (for different kinds of robots), and is detached from the ROS ecosystem.

The [sdsl_ros2](https://github.com/TAU-CGL/sdsl_ros2) repository is the ROS2 wrapper of the SDSL technique and should be general for any planar robot, regradless of its type, so long it publishes and reads the correct topics.

As mentioned above, the dockerfile automatically fetches both of these repositories automatically.

Finally, there is the [sdsl_create3_sim](https://github.com/TAU-CGL/sdsl_create3_sim), which is a simulated version of the iRobot Create 3. The interface and everything described in this README file should hold exactly the same also for the simulation.

## Hardware

<!-- TODO: Add an image of the hardware -->

The required hardware for out demonstration is as follows:

* iRobot Create 3
* SLAMTEC RPLIDAR C1
* A 3D printed mount for the LiDAR (`misc/RPLIDAR_C1_mount_v2.stl`) <!-- TODO: Upload the STL file -->
* 4x M2 screws (to attach the LiDAR to the mount)
* 4x M3 screws (to attach the mount to the robot's base)
* Raspberry Pi 5
    * In the past, we have used RPi4 which was significantly slower, but could run natively the correct version of Ubuntu
    * We have used the RPi5 model with 4GB of RAM and a 32GB microSD card
* USB C cable (to power RPi5 from the robot)
* Some computer/laptop with Ubuntu 22.04 LTS + ROS2 humble (can be a VM. In out demo we used a VM on an M1 macBook).

Note that the robot, the Raspberry Pi and the computer/VM should all be under the same WLAN, and use `fastrtps` as middleware.

## Firmware

In this demonstration we have used the following firmware versions:

* ROS2 - Humble
* iRobot Create 3 - H.2.6 (must be humble!)
* Raspberry Pi 5 - Ubuntu 24.04 LTS
    * Note that one should use Ubuntu 22.04 for ROS2 humble, hence we use docker

We called our robot (i.e., RPi5's hostname) `sdslbot`. You may use any other name if you'd like.

## Running Docker

After `git clone` for the current repository, enter the `docker` directory.   
Make sure to add executable (`chmod +x`) to the script files `build.sh` and `run.sh`.  
Use `build.sh` once to build the docker container. The `run.sh` opens an interactive session, from which you can run one of three scripts:
* `~/run_mapping.sh` - Starts the demo in Mapping mode
* `~/run_localization.sh` - Starts the demo in Localization mode
* `~/run_navigation.sh` - Starts the demo in Navigation mode

See above for the description of each mode. The three scripts are created in the `Dockerfile`, and they merely call a specific ROS launchfile.

## Mapping Mode

<!-- TODO: Talk about mapping RVIZ -->
**Make sure that the LIDAR is mounted correctly (the robot's and LIDAR's centers should coincide. Also notice the orientation.**
When running the `run_mapping.sh` script on the RPi5, we start the LIDAR node and SLAM. It may take a minute until the mapping starts.  
Move the robot around the environment to gather information and build the map. You can use `teleop_twist_keyboard` from either the SSH session with the RPi or directly from the computer, or you can use a gamepad (e.g., XBOX Controller or DualShock 4).

When you are done mapping, run the script `scripts/save_map.sh`, which saves the map into the `~/maps` directory. The map's name will unique and will include the date and time of creation for easy archiving. Make sure to upload the map to the `~/maps` also in the Raspberry Pi.

You **must** rename the map files to `my_map.pgm` and `my_map.yaml` as the dockerfile copies them to the container. These represent the "known" map that is then used for localizaiton.

One easy way for copying files from remote computer to RPi is via SSH:

'''
scp ~/maps/my_map.yaml user@sdslbot:~/maps/my_map.yaml
scp ~/maps/my_map.pgm user@sdslbot:~/maps/my_map.pgm
'''

You of course may change `user@sdslbot` to your own hostname.
