sudo docker run -it \
	--network host \
	--privileged \
	--device=/dev/input/event6 \
	--device=/dev/ttyUSB0:/dev/ttyUSB0 \
	--group-add dialout \
	ros-humble-create3 bash
