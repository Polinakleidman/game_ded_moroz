import pygame
import os
import random
GRAVITY = 0.3
win = True
killed_stars = 0
running = True

clock = pygame.time.Clock()
FPS = 50


def winner(im):
    def load_image(name, colorkey=None):
        fullname = os.path.join('C:\data', name)
        image = pygame.image.load(fullname)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image

    size = WIDTH, HEIGHT = 650, 550
    screen = pygame.display.set_mode(size)
    pygame.init()
    screen_rect = (0, 0, WIDTH, HEIGHT)


    class Particle(pygame.sprite.Sprite):
        # сгенерируем частицы разного размера
        fire = [load_image(im)]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))

        def __init__(self, pos, dx, dy):
            super().__init__(all_sprites)
            self.image = random.choice(self.fire)
            self.rect = self.image.get_rect()

            # у каждой частицы своя скорость — это вектор
            self.velocity = [dx, dy]
            # и свои координаты
            self.rect.x, self.rect.y = pos

            # гравитация будет одинаковой (значение константы)
            self.gravity = GRAVITY

        def update(self):
            # применяем гравитационный эффект:
            # движение с ускорением под действием гравитации
            self.velocity[1] += self.gravity
            # перемещаем частицу
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            # убиваем, если частица ушла за экран
            if not self.rect.colliderect(screen_rect):
                self.kill()
                global killed_stars
                killed_stars += 1
                global running
                if killed_stars == 200:#10 раз по 20 звезд
                    running = False

    def create_particles(position):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))


    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    global running
    count_stars = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # создаём частицы по щелчку мыши
        if count_stars < 10:
            count_stars += 1
            create_particles((325, 50))
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    #pygame.quit()