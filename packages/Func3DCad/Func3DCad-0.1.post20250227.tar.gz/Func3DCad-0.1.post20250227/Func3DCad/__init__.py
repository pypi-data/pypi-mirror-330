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