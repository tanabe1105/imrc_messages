import rclpy
from rclpy.node import Node
import math

# 椎名のカスタムメッセージ！
from imrc_messages.msg import LedControl
from imrc_messages.msg import LedData

COLOR_VALUES = [
    {"color": "RED", "value_r": 255, "value_g": 0, "value_b": 0},
    {"color": "GREEN", "value_r": 0, "value_g": 255, "value_b": 0},
    {"color": "BLUE", "value_r": 0, "value_g": 0, "value_b": 255},
    {"color": "WHITE", "value_r": 255, "value_g": 255, "value_b": 255},
]

class LedController(Node):
    def __init__(self):
        super().__init__('led_controller')
        self.pub = self.create_publisher(LedData, 'led_data', 10)
        self.sub = self.create_subscription(LedControl, 'led_cmd', self.led_cmd_callback, 10)

    def led_cmd_callback(self, msg):
        brightness = 0.0
        if(msg.led_brightness < 0.0):
            brightness = 0.0
        elif(msg.led_brightness > 1.0):
            brightness = 1.0
        else:
            brightness = msg.led_brightness

        ledData = LedData()
        ledData.led_index = msg.led_index
        ledData.led_color_red, ledData.led_color_green, ledData.led_color_blue = self.get_color_data(msg.led_color)

        ledData.led_color_red *= brightness
        ledData.led_color_green *= brightness
        ledData.led_color_blue *= brightness

        ledData.led_mode = msg.led_mode
        ledData.blink_duration = msg.blink_duration

        self.pub.publish(ledData)

    def get_color_data(self, color):
        for color_data in COLOR_VALUES:
            if(color == color_data["color"]):
                return color_data["value_r"], color_data["value_g"], color_data["value_b"]

def main():
    rclpy.init()
    ledController = LedController()
    rclpy.spin(ledController)
    rclpy.shutdown()

