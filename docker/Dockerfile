FROM ros:humble-ros-core

SHELL ["/bin/bash", "-c"]

# Install basic ROS dependencies
RUN apt-get update && apt-get install -y \
	git nano evtest build-essential python3-colcon-common-extensions python3-rosdep ros-humble-rmw-fastrtps-cpp

# Setup basic ROS envs and scripts
RUN echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> ~/.bashrc \
        && echo "ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps5'" >> ~/run_teleop_joy.sh \
	&& echo "ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/sdslbot/cmd_vel" >> ~/run_teleop_keyboard.sh \
	&& mkdir -p ~/ros_ws/src

# Install ROS packages
RUN apt-get install -y \
	ros-humble-irobot-create-msgs \
	ros-humble-teleop-twist-joy \
	ros-humble-teleop-twist-keyboard \
	ros-humble-rplidar-ros

# Clone the repositories into the workspace
RUN cd ~/ros_ws/src \
	&& git clone https://github.com/iRobotEducation/create3_examples.git --branch humble \
	&& git clone https://github.com/TAU-CGL/sdsl_create3.git \
	&& git clone https://github.com/TAU-CGL/sdsl_ros2.git && cd sdsl_ros2 && git submodule update --init --recursive && cd .. \
	&& cd ..

# Install SDSL dependencies
RUN cd ~ \
	&& git clone https://github.com/CGAL/cgal.git \
	&& cd cgal \
	&& cmake -B build && cd build \
	&& make && make install \
	&& apt-get install libglm-dev

# Init and build dependencies 
RUN cd ~/ros_ws \
	&& rosdep init \
	&& rosdep update \
	&& rosdep install --from-path src --ignore-src -yi

# Build the workspace
RUN cd ~/ros_ws \
	&& source /opt/ros/humble/setup.bash \
	&& colcon build

# Clean the apt lists
RUN rm -rf /var/lib/apt/lists/*
