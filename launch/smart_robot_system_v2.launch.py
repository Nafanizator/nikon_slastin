#!/usr/bin/env python3
"""Умный launch-файл с поддержкой режимов fast/slow"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def get_mode_config(mode):
    """Возвращает конфигурацию для выбранного режима"""
    configs = {
        'fast': {
            'freq': 20.0,
            'threshold': 50,
            'topic': '/even_numbers_fast',
            'description': 'Быстрый режим (отладка)'
        },
        'slow': {
            'freq': 5.0,
            'threshold': 150,
            'topic': '/even_numbers_slow',
            'description': 'Медленный режим (нормальная работа)'
        }
    }
    return configs.get(mode, configs['slow'])

def launch_setup(context):
    """Основная функция запуска"""
    mode = LaunchConfiguration('mode').perform(context)
    config = get_mode_config(mode)
    
    print(f"\n=== {config['description']} ===")
    print(f"  Частота: {config['freq']} Гц")
    print(f"  Порог: {config['threshold']}")
    print(f"  Топик: {config['topic']}\n")
    
    return [
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='even_number_publisher',
            name='even_pub',
            output='screen',
            parameters=[
                {'publish_frequency': config['freq']},
                {'overflow_threshold': config['threshold']},
                {'topic_name': config['topic']}
            ],
        ),
        Node(
            package='super_NikonSlastin_study_pkg',
            executable='overflow_listener',
            name='overflow_listener',
            output='screen',
        ),
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'mode',
            default_value='slow',
            description='Режим работы: fast (20Гц, порог 50) или slow (5Гц, порог 150)'
        ),
        OpaqueFunction(function=launch_setup)
    ])
