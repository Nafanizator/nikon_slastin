#!/usr/bin/env python3
"""Узел-публикатор чётных чисел с поддержкой параметров"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub')
        
        # Объявляем параметры с значениями по умолчанию
        self.declare_parameter('publish_frequency', 10.0)   # частота в Гц
        self.declare_parameter('overflow_threshold', 100)   # порог переполнения
        self.declare_parameter('topic_name', '/even_numbers') # имя топика
        
        # Читаем параметры
        self.freq = self.get_parameter('publish_frequency').value
        self.threshold = self.get_parameter('overflow_threshold').value
        self.topic = self.get_parameter('topic_name').value
        
        # Создаём публикаторы
        self.publisher = self.create_publisher(Int32, self.topic, 10)
        self.overflow_publisher = self.create_publisher(Int32, '/overflow', 10)
        
        # Создаём таймер с рассчитанным периодом
        period = 1.0 / self.freq
        self.timer = self.create_timer(period, self.timer_callback)
        
        # Счётчик
        self.counter = 0
        
        self.get_logger().info(f"Узел even_pub запущен с параметрами:")
        self.get_logger().info(f"  - частота: {self.freq} Гц")
        self.get_logger().info(f"  - порог: {self.threshold}")
        self.get_logger().info(f"  - топик: {self.topic}")

    def timer_callback(self):
        # Создаём основное сообщение
        msg = Int32()
        msg.data = self.counter
        self.publisher.publish(msg)
        self.get_logger().info(f"Публикую в {self.topic}: {self.counter}")
        
        # Проверяем на переполнение
        if self.counter >= self.threshold:
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
