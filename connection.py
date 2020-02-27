from interface_level import start_level
from screens import start_screen
from screens import middle_screen
import pygame
start_screen()
start_level(0)
count = 0
while middle_screen() != 'finish' and count < 5:
    word = middle_screen()
    if word == 'previous_level':
        start_level(count)
    elif word == 'new_level':
        count += 1
        if count < 5:
            start_level(count)

pygame.quit()