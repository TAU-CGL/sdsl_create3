from better_launch import BetterLaunch, launch_this

@launch_this
def create3_launch():
    bl = BetterLaunch()

    # bl.include("create3_lidar_slam", "sensors_launch.py")
    # bl.include("create3_lidar_slam", "slam_toolbox_launch.py")