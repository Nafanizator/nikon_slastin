#!/usr/bin/env python3
"""Умный launch-файл с выбором режима работы (fast/slow)"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
def generate_launch_description():
    # Объявляем аргумент для выбора режима
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='slow',
        description='Режим работы: fast (быстрый) или slow (медленный)'
    )
    # Получаем значение аргумента
    mode = LaunchConfiguration('mode')
    # Используем PythonExpression для динамического вычисления параметров
    frequency = PythonExpression([
        "20.0 if '", mode, "' == 'fast' else 5.0"
    ])
    threshold = PythonExpression([
        "50 if '", mode, "' == 'fast' else 150"
    ])
    topic = PythonExpression([
        "'/even_numbers_fast' if '", mode, "' == 'fast' else '/even_numbers_slow'"
    ])
    return LaunchDescription([
        mode_arg,
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            parameters=[
                {'publish_frequency': frequency},
                {'overflow_threshold': threshold},
                {'topic_name': topic},
                {'enable_logging': True},
            ],
        ),
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='overflow_listener',
            name='overflow_listener',
            output='screen',
        ),
    ])
