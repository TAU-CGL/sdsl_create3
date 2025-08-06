import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import LePotatoPi.GPIO.GPIO as GPIO

BUZZER_PIN = 13
JOYPAD_BUTTON_INDEX = 12

class HornNode(Node):
    def __init__(self):
        super().__init__('horn_node')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )
        self.get_logger().info('Horn node has been started.')

    def joy_callback(self, msg: Joy):
        if len(msg.buttons) > JOYPAD_BUTTON_INDEX and msg.buttons[JOYPAD_BUTTON_INDEX] == 1:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            self.get_logger().debug("R3 pressed → buzzer ON")
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            self.get_logger().debug("R3 released → buzzer OFF")
    
    def destroy_node(self):
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup()
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