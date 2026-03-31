#!/usr/bin/env python3
"""Узел-публикатор чётных чисел с детектором переполнения"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')
        
        # Публикатор в основной топик
        self.publisher = self.create_publisher(Int32, '/even_numbers', 10)
        
        # Публикатор в топик переполнения
        self.overflow_publisher = self.create_publisher(Int32, '/overflow', 10)
        
        # Таймер на 10 Гц
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        # Счётчик
        self.counter = 0
        
        self.get_logger().info("Узел even_pub запущен! Публикую чётные числа")

    def timer_callback(self):
        # Создаём основное сообщение
        msg = Int32()
        msg.data = self.counter
        self.publisher.publish(msg)
        self.get_logger().info(f"Публикую: {self.counter}")
        
        # Проверяем на переполнение
        if self.counter >= 100:
            # Публикуем сообщение о переполнении
            overflow_msg = Int32()
            overflow_msg.data = self.counter
            self.overflow_publisher.publish(overflow_msg)
            self.get_logger().warn(f"!!! ПЕРЕПОЛНЕНИЕ !!! Значение: {self.counter}")
            
            # Сбрасываем счётчик
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
