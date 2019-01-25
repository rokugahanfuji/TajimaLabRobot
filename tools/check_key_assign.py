import time
import pygame

pygame.init()
joys = pygame.joystick.Joystick(0)
joys.init()

while True:
    events = pygame.event.get()
    for event in events:
        if not event == []:
             print(event)
        time.sleep(0.01)
