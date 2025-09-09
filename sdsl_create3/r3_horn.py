import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from gpiozero import DigitalOutputDevice

BUZZER_PIN = 13
JOYPAD_BUTTON_INDEX = 12

class HornNode(Node):
    def __init__(self):
        super().__init__('horn_node')

        self.buzzer = DigitalOutputDevice(BUZZER_PIN)

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )
        self.get_logger().info('Horn node has been started.')

    def joy_callback(self, msg: Joy):
        if len(msg.buttons) > JOYPAD_BUTTON_INDEX and msg.buttons[JOYPAD_BUTTON_INDEX] == 1:
            self.buzzer.on()
            self.get_logger().debug("R3 pressed → buzzer ON")
        else:
            self.buzzer.off()
            self.get_logger().debug("R3 released → buzzer OFF")
    
    def destroy_node(self):
        self.buzzer.value = 0
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HornNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
