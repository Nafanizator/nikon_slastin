#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        
        # Создаём publisher
        self.publisher = self.create_publisher(String, 'my_chat_topic', 10)
        
        # Таймер на 1 секунду
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.get_logger().info("Узел talker запущен!")

    def timer_callback(self):
        msg = String()
        msg.data = f"Привет! Сейчас {self.get_clock().now().to_msg().sec}"
        
        self.publisher.publish(msg)
        self.get_logger().info(f"Отправлено: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
