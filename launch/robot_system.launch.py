#!/usr/bin/env python3
"""Базовый launch-файл для запуска системы"""
from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    return LaunchDescription([
        # Узел-публикатор чётных чисел
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            parameters=[
                {'publish_frequency': 8.0},      # 8 Гц
                {'overflow_threshold': 80},      # порог 80
                {'topic_name': '/even_numbers'}, # имя топика
                {'enable_logging': True},        # логи включены
            ],
        ),
        # Узел-слушатель переполнения
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='overflow_listener',
            name='overflow_listener',
            output='screen',
        ),
    ])
