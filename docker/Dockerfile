FROM ros:humble-ros-core

RUN apt-get update && apt-get install -y \
	git \
	nano \
	evtest \
	ros-humble-irobot-create-msgs \
	ros-humble-teleop-twist-joy \
	ros-humble-teleop-twist-keyboard \
	build-essential python3-colcon-common-extensions python3-rosdep ros-humble-rmw-fastrtps-cpp \
	\
	&& rm -rf /var/lib/apt/lists/* \
	&& echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> ~/.bashrc \
	&& echo "ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps5'" >> ~/run_teleop_joy.sh \
	&& echo "ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/sdslbot/cmd_vel" >> ~/run_teleop_keyboard.sh \
	\
	&& mkdir -p ~/ros_ws/src \
	&& cd ~/ros_ws/src \
	&& git clone https://github.com/iRobotEducation/create3_examples.git --branch humble \
	&& cd .. \
	&& rosdep init \
	&& rosdep update \
	&& rosdep install --from-path src --ignore-src -yi \
	&& colcon build