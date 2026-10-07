#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import random

# Importamos la interfaz que vimos en tu terminal
from robx7_interfaces.msg import HardwareStatus


class HardwareEmulatorNode(Node):
    def __init__(self):
        super().__init__('hardware_emulator')

        # 1. Creamos el Publisher en el tópico /hardware_status
        self.publisher_ = self.create_publisher(HardwareStatus, '/hardware_status', 10)

        # 2. Creamos un temporizador para publicar cada 1.0 segundo (1 Hz)
        self.timer = self.create_timer(1.0, self.publish_hardware_status)

        self.get_logger().info('Nodo Emulador de Hardware iniciado...')

    def publish_hardware_status(self):
        msg = HardwareStatus()

        # Simulamos variaciones de temperatura (entre 35°C y 85°C)
        msg.temperatura = random.randint(35, 85)

        # Si la temperatura es menor o igual a 70, motores listos; si no, fallan
        if msg.temperatura <= 70:
            msg.motores_listos = True
            msg.debug_msg = 'Operacion normal'
        elif msg.temperatura <= 80:
            msg.motores_listos = True
            msg.debug_msg = 'Calentando'
        else:
            msg.motores_listos = False
            msg.debug_msg = 'Fallo de sensor / Sobrecalentamiento'

        # Publicamos el mensaje
        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publicando -> Temp: {msg.temperatura}°C | Motores: {msg.motores_listos} | Estado: {msg.debug_msg}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = HardwareEmulatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
