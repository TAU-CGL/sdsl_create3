"""
ROS Node for SDS (Sparse Distance Sampling) publisher.
This reduces significantly (usually about ~2%) the amount of data of a LiDAR laser scan.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class SDSPublisher(Node):
    def __init__(self):
        super().__init__("sds_publisher")

        self.declare_parameter("k", 16)
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            "/scan",
            self.scan_callback,
            10
        )
        self.sds_publisher = self.create_publisher(LaserScan, "/sds", 10)

    def scan_callback(self, msg):
        k = self.get_parameter("k").get_parameter_value().integer_value
        # assert len(msg.ranges) % k == 0

        sparse_msg = LaserScan()

        sparse_msg.header = msg.header
        sparse_msg.angle_min = msg.angle_min
        sparse_msg.angle_max = msg.angle_max
        sparse_msg.angle_increment = (msg.angle_max - msg.angle_min) / k
        sparse_msg.time_increment = 0.0
        sparse_msg.scan_time = 0.0
        sparse_msg.range_min = msg.range_min
        sparse_msg.range_max = msg.range_max
        sparse_msg.ranges = msg.ranges[::len(msg.ranges) // k]
        sparse_msg.intensities = msg.intensities[::len(msg.intensities) // k]

        self.sds_publisher.publish(sparse_msg)


def main(args=None):
    rclpy.init(args = args)
    sds_publisher = SDSPublisher()
    try:
        rclpy.spin(sds_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        sds_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()