import pygame
import os
import sys
clock = pygame.time.Clock()
FPS = 10


def load_image(name, colorkey=None):
    fullname = os.path.join('C:\data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
         if colorkey == -1:
             colorkey = image.get_at((0,0))
         image.set_colorkey(colorkey)
    return image


size = WIDTH, HEIGHT = 650, 550
screen = pygame.display.set_mode(size)
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def middle_screen():
    intro_text = ["ДЕД МОРОЗ",
                  "Для выбора щелкните мышью 2 раза",
                  "Перейти на следующий уровень     Пройти уровень заново",
                  '', '', '', '', '', '', 'Выход из игры'
                  ]

    fon = pygame.transform.scale(load_image('fon_ded_moroz.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.circle(screen, (200, 30, 30), (100, 220), 50, 50)
    pygame.draw.circle(screen, (0, 0, 0), (100, 440), 50, 50)
    pygame.draw.circle(screen, (100, 200, 255), (500, 220), 50, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] - 100) ** 2 + (event.pos[1] - 220) ** 2 <= 2500:
                    fon = pygame.transform.scale(load_image('fon_norm.jpg'), (WIDTH, HEIGHT))
                    screen.blit(fon, (0, 0))
                    return 'new_level'
                elif (event.pos[0] - 500) ** 2 + (event.pos[1] - 220) ** 2 <= 2500:
                    fon = pygame.transform.scale(load_image('fon_norm.jpg'), (WIDTH, HEIGHT))
                    screen.blit(fon, (0, 0))
                    return 'previous_level' # начинаем игру
                elif (event.pos[0] - 100) ** 2 + (event.pos[1] - 440) ** 2 <= 2500:
                    fon = pygame.transform.scale(load_image('fon_norm.jpg'), (WIDTH, HEIGHT))
                    screen.blit(fon, (0, 0))
                    return 'finish'
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["ДЕД МОРОЗ",
                  "Правила игры:",
                  "Для прыжка щелкните мышью.",
                  "Игра кончается при столкновении с препятствием.",
                  "Щелкните мышью",
                  "для начала игры"]

    fon = pygame.transform.scale(load_image('fon_ded_moroz.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                fon = pygame.transform.scale(load_image('fon_norm.jpg'), (WIDTH, HEIGHT))
                screen.blit(fon, (0, 0))
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)