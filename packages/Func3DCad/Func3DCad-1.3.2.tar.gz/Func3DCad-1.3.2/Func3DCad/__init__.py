"""
Func3DCad - пакет для работы с 3D-моделированием.
"""

from .core import Model3D, Transform
from .utils import calculate_volume, calculate_surface_area
from .file_io import export_model, import_model
from .render import render_model

__all__ = [
    "Model3D", "Transform",
    "calculate_volume", "calculate_surface_area",
    "export_model", "import_model",
    "render_model"
]

__version__ = "1.3.2"


# --------------------------------------------------------AUTONOMUS-----------------------------------------------------------------------

# from robocad.studica import RobotVmxTitan
# import time

# robot = RobotVmxTitan(False)


# def StopMotors():
#     (
#         robot.motor_speed_0,
#         robot.motor_speed_1,
#         robot.motor_speed_2,
#         robot.motor_speed_3,
#     ) = (0, 0, 0, 0)
#     time.sleep(0.1)
#     return


# def Rotate(degrees, speed):
#     robot.reset_yaw()
#     if degrees > 0:
#         for index, mult in enumerate([1, -0.5, 0.25, -0.125]):
#             robot.motor_speed_0 = speed * mult
#             robot.motor_speed_1 = speed * mult
#             time.sleep(0.1)
#             while True:
#                 if ((index % 2 == 0) and (robot.yaw > degrees)) or (
#                     (index % 2 == 1) and (robot.yaw < degrees)
#                 ):
#                     break
#             time.sleep(0.1)
#             StopMotors()
#     else:
#         for index, mult in enumerate([-1, 0.5, -0.25, 0.125]):
#             robot.motor_speed_0 = speed * mult
#             robot.motor_speed_1 = speed * mult
#             time.sleep(0.1)
#             while True:
#                 if ((index % 2 == 0) and (robot.yaw < degrees)) or (
#                     (index % 2 == 1) and (robot.yaw > degrees)
#                 ):
#                     break
#             time.sleep(0.1)
#             StopMotors()
#     return


# def Distance(units, speed):
#     start_enc_0 = robot.motor_enc_0
#     robot.motor_speed_0 = speed * 1
#     robot.motor_speed_1 = speed * -1
#     time.sleep(0.1)
#     while True:
#         if start_enc_0 + units > robot.motor_enc_0:
#             break
#     time.sleep(0.1)
#     StopMotors()
#     return

# # Ждет нажатия на кнопку старт
# while not robot.vmx_flex[1]:
#     time.sleep(0.1)

# time.sleep(1)
# Distance(2000, 100) # Проехать 2000
# time.sleep(1)
# Rotate(-90)  # Повернуть налево
# time.sleep(1)
# StopMotors()
# time.sleep(1)
# robot.stop()