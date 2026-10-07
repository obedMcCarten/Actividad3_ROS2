#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class OperatorNode(Node):
    def __init__(self):
        super().__init__('operator_node')

        # 1. Creamos el cliente para el servicio /check_system[cite: 1]
        self.client = self.create_client(Trigger, '/check_system')

        # Esperar a que el servidor esté disponible
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio /check_system del Monitor...')

        # 2. Timer para hacer peticiones periódicas cada 3 segundos[cite: 1]
        self.timer = self.create_timer(3.0, self.send_request)
        self.get_logger().info('Nodo Operador listo. Iniciando consultas periódicas...')

    def send_request(self):
        req = Trigger.Request()
        future = self.client.call_async(req)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f'[OPERADOR] Respuesta: {response.message}')
            else:
                self.get_logger().error(f'[OPERADOR] Respuesta: {response.message}')
        except Exception as e:
            self.get_logger().error(f'Fallo en la llamada al servicio: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = OperatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
