#!/usr/bin/env python3
"""Узел-слушатель сообщений о переполнении"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class OverflowListener(Node):
    def __init__(self):
        super().__init__('overflow_listener')
        
        # Подписываемся на топик /overflow
        self.subscription = self.create_subscription(
            Int32,
            '/overflow',
            self.callback,
            10
        )
        
        self.get_logger().info("Узел overflow_listener запущен! Слушаю топик /overflow")

    def callback(self, msg):
        # Выводим предупреждение при получении сообщения
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
