#!/usr/bin/env python3
"""Публикатор чётных чисел с отслеживанием переполнения"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')
        
        # Создаём publisher для чётных чисел
        self.publisher = self.create_publisher(Int32, '/even_numbers', 10)
        
        # Создаём publisher для переполнения
        self.overflow_publisher = self.create_publisher(Int32, '/overflow', 10)
        
        # Таймер на 0.1 секунды (10 Гц)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Начальное значение
        self.counter = 0
        
        self.get_logger().info("Узел even_pub запущен! Публикуем чётные числа 0,2,4...98")

    def timer_callback(self):
        msg = Int32()
        msg.data = self.counter
        self.publisher.publish(msg)
        self.get_logger().info(f"Публикую: {self.counter}")
        
        # Проверяем переполнение
        if self.counter >= 100:
            overflow_msg = Int32()
            overflow_msg.data = self.counter
            self.overflow_publisher.publish(overflow_msg)
            self.get_logger().warn(f"!!! ПЕРЕПОЛНЕНИЕ !!! Значение: {self.counter}")
            self.counter = 0
        else:
            # Увеличиваем на 2
            self.counter += 2

def main(args=None):
    rclpy.init(args=args)
    node = EvenNumberPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
