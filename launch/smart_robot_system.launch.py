#!/usr/bin/env python3
"""Умный launch-файл с поддержкой режимов fast/slow"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    # Объявляем аргумент для выбора режима
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='slow',
        description='Режим работы: fast (20Гц, порог 50) или slow (5Гц, порог 150)'
    )
    
    # Получаем значение режима
    mode = LaunchConfiguration('mode')
    
    # Вместо LaunchConfiguration мы не можем использовать Python-логику напрямую,
    # поэтому используем специальный подход - будем определять параметры через IncludeLaunchDescription
    # или создадим несколько вариантов узлов
    
    return LaunchDescription([
        mode_arg,
        
        # Узел-публикатор для режима fast
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            condition=lambda context: LaunchConfiguration('mode').perform(context) == 'fast',
            parameters=[
                {'publish_frequency': 20.0},
                {'overflow_threshold': 50},
                {'topic_name': '/even_numbers_fast'}
            ],
        ),
        
        # Узел-публикатор для режима slow
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            condition=lambda context: LaunchConfiguration('mode').perform(context) == 'slow',
            parameters=[
                {'publish_frequency': 5.0},
                {'overflow_threshold': 150},
                {'topic_name': '/even_numbers_slow'}
            ],
        ),
        
        # Слушатель переполнения (работает в обоих режимах)
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='overflow_listener',
            name='overflow_listener',
            output='screen',
        ),
    ])
