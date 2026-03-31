#!/usr/bin/env python3
"""Launch-файл для запуска системы публикации чётных чисел"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Объявляем аргументы launch-файла
    freq_arg = DeclareLaunchArgument(
        'publish_frequency',
        default_value='8.0',
        description='Частота публикации чётных чисел (Гц)'
    )
    
    threshold_arg = DeclareLaunchArgument(
        'overflow_threshold',
        default_value='80',
        description='Порог, после которого происходит переполнение'
    )
    
    topic_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='/even_numbers',
        description='Имя топика для публикации чётных чисел'
    )
    
    # Получаем значения аргументов
    frequency = LaunchConfiguration('publish_frequency')
    threshold = LaunchConfiguration('overflow_threshold')
    topic = LaunchConfiguration('topic_name')
    
    return LaunchDescription([
        freq_arg,
        threshold_arg,
        topic_arg,
        
        # Узел-публикатор
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            parameters=[
                {'publish_frequency': frequency},
                {'overflow_threshold': threshold},
                {'topic_name': topic}
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
