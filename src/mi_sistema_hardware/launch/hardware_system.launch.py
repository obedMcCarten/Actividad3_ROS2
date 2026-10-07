from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Nodo Emulador de Hardware
        Node(
            package='mi_sistema_hardware',
            executable='hardware_emulator',
            name='hardware_emulator',
            output='screen'
        ),
        # 2. Nodo Monitor con parámetro sobrescrito a 75
        Node(
            package='mi_sistema_hardware',
            executable='monitor_node',
            name='monitor_node',
            output='screen',
            parameters=[
                {'umbral_temperatura': 75}
            ]
        ),
        # 3. Nodo Operador
        Node(
            package='mi_sistema_hardware',
            executable='operator_node',
            name='operator_node',
            output='screen'
        )
    ])
