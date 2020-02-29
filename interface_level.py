Win = False
count = 0
run = True


def start_level(number_of_level):
    import pygame
    import os
    import sys
    clock = pygame.time.Clock()
    FPS = 50
    rect = 405
    list_tiles = []
    list_tubes = []
    now_level = 'level' + str(number_of_level) + '.lvl'

    def load_image(name, colorkey=None):
        fullname = os.path.join(name)
        image = pygame.image.load(fullname)
        if colorkey is not None:
             if colorkey == -1:
                 colorkey = image.get_at((0,0))
             image.set_colorkey(colorkey)
        return image


    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 0
            self.dy = 0

        # сдвинуть объект obj на смещение камеры
        def apply(self, obj):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

        # позиционировать камеру на объекте target
        def update(self, target):
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
            self.dy = 0


    tile_images = {'wall': load_image('snow_box.png'), 'finish': load_image('труба.png')}


    tile_width = tile_height = 50

    size = WIDTH, HEIGHT = 650, 550
    screen = pygame.display.set_mode(size)
    pygame.init()

    # основной персонаж
    player = None

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()


    def generate_level(level):
        new_player, x, y = None, None, None
        while True:
            for y in range(len(level)):
                for x in range(len(level[y])):
                    # if level[y][x] == '.':
                    #     tile = Tile('empty', x, y))
                    if level[y][x] == '#':
                        tile = Tile('wall', x, y)
                        list_tiles.append(tile)
                    if level[y][x] == '%':
                        tube = Tube('finish', x, y)
                        list_tubes.append(tube)
                    if level[y][x] == '@':
                        new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
            return new_player, x, y


    def load_level(filename):
        filename = os.path.join(filename)
        # читаем уровень, убирая символы перевода строки
        print(filename)
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


    def terminate():
        pygame.quit()
        sys.exit()


    class Tile(pygame.sprite.Sprite):
        image = load_image('snow_box.png', -1)

        def __init__(self, type_thing, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = Tile.image
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
            self.mask = pygame.mask.from_surface(self.image)


    class Tube(pygame.sprite.Sprite):
        image = load_image('труба.png', -1)

        def __init__(self, type_thing, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = Tube.image
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
            self.mask = pygame.mask.from_surface(self.image)


    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)
            self.vx = 0
            self.vy = 0

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))


        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


    class Player(pygame.sprite.Sprite):
        image = load_image('player.png', 1)

        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = Player.image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(tile_width * pos_x + 30, tile_height * pos_y -80)
            self.vx = 2
            self.vy = 0

        def movings(self):
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.collide_mask(self, list_tubes[0]) or pygame.sprite.collide_mask(self, list_tubes[1]):
                global run
                global Win
                run = False
                Win = True
            global count
            if count != 0:
                if count < 21:
                    if count < 19:
                        count += 1
                        self.vy = -3
                    elif 18 < count < 21:
                        self.vy = 0
                        count += 1
                    for elem in list_tiles:
                        if pygame.sprite.collide_mask(self, elem) and not \
                                ((int(elem.rect[1]) - int(self.rect[1]) + 5) >= int(self.rect[3]) and \
                                (int(elem.rect[1]) - int(self.rect[1])) < int(self.rect[3])):
                            run = False
                elif count > 20:
                    touch = False
                    self.vy = 3
                    for elem in list_tiles:
                        if pygame.sprite.collide_mask(self, elem) and \
                                (int(elem.rect[1]) - int(self.rect[1]) + 5) >= int(self.rect[3]) and \
                                (int(elem.rect[1]) - int(self.rect[1])) < int(self.rect[3]):
                           touch = True
                        elif pygame.sprite.collide_mask(self, elem):
                            run = False
                    if not touch:
                        count += 1
                        self.vy = 3
                    else:
                        self.vy = 0
                        count = 0
            else:
                touch = False
                for elem in list_tiles:
                    if pygame.sprite.collide_mask(self, elem) and \
                            (int(elem.rect[1]) - int(self.rect[1]) + 5) >= int(self.rect[3]) and \
                            (int(elem.rect[1]) - int(self.rect[1])) < int(self.rect[3]):
                        touch = True
                    elif pygame.sprite.collide_mask(self, elem):
                        run = False
                if not touch:
                    self.vy = 3
                else:
                    self.vy = 0
                    count = 0
                self.vx = 2

    player, level_x, level_y = generate_level(load_level(now_level))
    camera = Camera()
    global run
    run = True
    global count
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if count == 0:
                    count = 1
            # изменяем ракурс камеры
        camera.update(player);
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update(screen)
        player.movings()
        pygame.display.flip()
        clock.tick(FPS)
        fon = pygame.transform.scale(load_image('fon_norm.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

    global Win
    if Win:
        from part_after_level import winner
        winner("star.png")
    else:
        from part_after_level import winner
        winner("sad1.png")