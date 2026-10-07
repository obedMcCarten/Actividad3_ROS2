#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

# Importamos el mensaje del tópico y el servicio
from robx7_interfaces.msg import HardwareStatus
from std_srvs.srv import Trigger


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        # 1. Declarar y leer el parámetro estático (por defecto 50)
        self.declare_parameter('umbral_temperatura', 50)
        self.umbral_temperatura = self.get_parameter('umbral_temperatura').get_parameter_value().integer_value
        self.get_logger().info(f'Monitor iniciado con umbral_temperatura = {self.umbral_temperatura}°C')

        # Variables para almacenar el último estado recibido
        self.ultima_temperatura = 0
        self.motores_listos = False
        self.ultimo_debug = 'Sin datos recibidos'

        # 2. Suscriptor al tópico /hardware_status
        self.subscription = self.create_subscription(
            HardwareStatus,
            '/hardware_status',
            self.hardware_status_callback,
            10
        )

        # 3. Servidor de Servicio /check_system
        self.srv = self.create_service(
            Trigger,
            '/check_system',
            self.check_system_callback
        )

    def hardware_status_callback(self, msg):
        # Actualizamos la memoria del monitor
        self.ultima_temperatura = msg.temperatura
        self.motores_listos = msg.motores_listos
        self.ultimo_debug = msg.debug_msg

        # Evaluar si supera el umbral configurado
        if self.ultima_temperatura > self.umbral_temperatura:
            self.get_logger().warn(
                f'ALERTA: Temperatura ({self.ultima_temperatura}°C) excede el umbral ({self.umbral_temperatura}°C)!'
            )

    def check_system_callback(self, request, response):
        # Evaluar si el sistema es seguro para operar
        es_seguro = (self.ultima_temperatura <= self.umbral_temperatura) and self.motores_listos

        if es_seguro:
            response.success = True
            response.message = f'Autorización concedida. Temp: {self.ultima_temperatura}°C, Motores listos.'
        else:
            response.success = False
            response.message = f'Bloqueo de seguridad: Temp={self.ultima_temperatura}°C (Umbral={self.umbral_temperatura}), Motores={self.motores_listos}'

        return response


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
