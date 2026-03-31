#!/usr/bin/env python3
"""Узел-слушатель сообщений о переполнении с поддержкой параметров"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class OverflowListener(Node):
    def __init__(self):
        super().__init__('overflow_listener')
        
        # Объявляем параметры
        self.declare_parameter('overflow_topic', '/overflow')
        self.declare_parameter('enable_logging', True)
        
        # Читаем параметры
        self.topic = self.get_parameter('overflow_topic').value
        self.enable_logging = self.get_parameter('enable_logging').value
        
        # Подписываемся на топик
        self.subscription = self.create_subscription(
            Int32,
            self.topic,
            self.callback,
            10
        )
        
        self.get_logger().info(f"Узел overflow_listener запущен!")
        self.get_logger().info(f"  Слушаю топик: {self.topic}")

    def callback(self, msg):
        self.get_logger().warn(f"!!! ПЕРЕПОЛНЕНИЕ !!! Получено значение: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = OverflowListener()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

