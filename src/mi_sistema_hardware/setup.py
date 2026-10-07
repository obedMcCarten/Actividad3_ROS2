import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mi_sistema_hardware'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Línea clave para que ROS 2 instale los archivos .launch.py:
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vboxuser',
    maintainer_email='vboxuser@todo.todo',
    description='Paquete de integracion de hardware para Actividad 3',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Registramos los 3 ejecutables:
            'hardware_emulator = mi_sistema_hardware.emulator_node:main',
            'monitor_node = mi_sistema_hardware.monitor_node:main',
            'operator_node = mi_sistema_hardware.operator_node:main',
        ],
    },
)

