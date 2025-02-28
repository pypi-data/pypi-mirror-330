class Model3D:
    """Базовый класс 3D-модели."""
    def __init__(self, vertices=None, faces=None):
        self.vertices = vertices or []
        self.faces = faces or []

    def add_vertex(self, vertex):
        """Добавляет вершину."""
        self.vertices.append(vertex)

    def add_face(self, face):
        """Добавляет грань."""
        self.faces.append(face)


class Transform:
    """Класс для трансформаций 3D-модели."""
    @staticmethod
    def scale(model, factor):
        """Масштабирование модели."""
        model.vertices = [(x * factor, y * factor, z * factor) for x, y, z in model.vertices]

    @staticmethod
    def translate(model, dx, dy, dz):
        """Перемещение модели."""
        model.vertices = [(x + dx, y + dy, z + dz) for x, y, z in model.vertices]

# ----------------------------------------------------------WASD--------------------------------------------------------------------

# import pygame, sys, time
# from robocad.studica import RobotVmxTitan

# robot = RobotVmxTitan(False)
# pygame.init()
# screen = pygame.display.set_mode((400, 300))
# pygame.display.set_caption("Press W, A, S, D (Press Q to exit)")

# time.sleep(1)

# def move(key):
#     speeds = {"W": (30, -30), "A": (-30, -30), "D": (30, 30), "S": (-30, 30)}
#     robot.motor_speed_0, robot.motor_speed_1 = speeds.get(key, (0, 0))
#     time.sleep(0.1)

# def stop():
#     robot.motor_speed_0 = robot.motor_speed_1 = 0
#     time.sleep(0.1)


# # Ждет нажатия на кнопку старт
# while not robot.vmx_flex[1]:
#     time.sleep(0.1)

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_q:
#                 print("Exiting...")
#                 running = False
#             elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
#                 move(pygame.key.name(event.key).upper())
#         elif event.type == pygame.KEYUP:
#             if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
#                 stop()

# time.sleep(1)
# robot.stop()
# time.sleep(1)
# pygame.quit()
# sys.exit()