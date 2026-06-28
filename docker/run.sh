sudo docker run -it \
	--network host \
	--privileged \
	--device=/dev/input/event6 \
	ros-humble-create3 bash
