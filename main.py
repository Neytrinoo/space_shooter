import pygame
import json
from random import randint

pygame.init()
size = width, height = 1700, 900
screen = pygame.display.set_mode(size)
player_sprite = pygame.sprite.Group()
enemies_sprite = pygame.sprite.Group()
bullets_sprite = pygame.sprite.Group()
screen.fill((0, 0, 0))
fps = 100
PATH_TO_RECORD_FILE = 'record.json'
PATH_TO_START_SCREEN = 'img/start_screen.jpg'
PATH_TO_BUTTON_START_GAME = 'img/button_start_game.png'
PATH_TO_FONS = 'img/fons/'
PATH_TO_ROCKET_SPRITES = 'img/sprites/rockets'
PATH_TO_ENEMIES_SPRITES = 'img/sprites/enemies'
PATH_TO_BULLETS_SPRITES = 'img/sprites/enemies/bullets'


class ButtonStartGame:
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img_path)

    def render(self):
        screen.blit(self.img, (self.x, self.y))

    def is_clicked(self, event_pos):
        mouse_x, mouse_y = event_pos
        w, h = list(self.img.get_rect())[2:]
        if mouse_x > self.x and mouse_x < self.x + w and mouse_y > self.y and mouse_y < self.y + h:
            return True
        else:
            return False


class Background:
    def __init__(self):
        self.fon_img = pygame.image.load(PATH_TO_FONS + 'fon' + str(randint(1, 3)) + '.jpg')
        screen.blit(self.fon_img, (0, 0))
        self.speed = 2
        self.count_iter = 0
        self.enemies = []

    def get_fon(self):
        return self.fon_img

    def update(self):
        who_is = randint(1, 3)
        if who_is == 2 and (not self.enemies or self.count_iter % 300 == 0):
            self.enemies.append(
                Enemy(PATH_TO_ENEMIES_SPRITES + '/' + str(randint(1, 2)) + '.png', randint(100, 1500), 0, self.speed))
        to_delete = []
        for i in range(len(self.enemies)):
            self.enemies[i].move(player)
            if not self.enemies[i].bullet or self.count_iter % 100 == 0:
                self.enemies[i].shoot()
            for j in range(len(self.enemies[i].bullet)):
                self.enemies[i].bullet[j].move()
            enemies_sprite.draw(screen2)
            bullets_sprite.draw(screen2)
            if not self.enemies[i].in_screen():
                to_delete.append(i)
            screen.blit(screen2, (0, 0))
        self.count_iter += 1
        if self.count_iter > 300:
            self.count_iter = 0
        for i in to_delete:
            del self.enemies[i]


class Meteorite(pygame.sprite.Sprite):
    # В этом классе генерируются метеориты и есть функция контроля пересечения метеорита и игрока
    def __init__(self):
        super().__init__()


class Enemy(pygame.sprite.Sprite):
    # В этом классе генерируются враги все их функции
    def __init__(self, sprite_path, x, y, speed):
        super().__init__(enemies_sprite)
        self.image = pygame.image.load(sprite_path)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count_iter = 0
        self.bullet = []
        self.speed = speed
        self.number_enemy = sprite_path.split('/')[-1][:1]

    def move(self, user):
        if self.count_iter == 1:
            if user.rect.x > self.rect.x:
                self.rect.x += self.speed
            elif user.rect.x < self.rect.x:
                self.rect.x -= self.speed
            self.rect.y += self.speed
        self.count_iter += 1
        if self.count_iter > 1:
            self.count_iter = 0

    def shoot(self):
        if self.number_enemy == '1':
            x = self.rect.x + 35
            y = self.rect.y + 130
        elif self.number_enemy == '2':
            x = self.rect.x
            y = self.rect.y + 130
        self.bullet.append(Bullet(PATH_TO_BULLETS_SPRITES + '/' + self.number_enemy + '.png', self.speed * 4, x, y))

    def in_screen(self):
        if self.rect.y < 900:
            return True
        else:
            self.kill()
            return False


class Bullet(pygame.sprite.Sprite):
    # В этом классе генерируются пули врагов и отслеживается их пересечение с игроком
    def __init__(self, sprite_path, speed, x, y):
        super().__init__(bullets_sprite)
        self.image = pygame.image.load(sprite_path)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def is_collidle(self, elem):
        if pygame.sprite.collide_mask(self, elem):
            print('попался')
            return True

    def move(self):
        self.is_collidle(player)
        self.rect.y += self.speed

    def in_screen(self):
        if self.rect.y < 900:
            return True
        else:
            self.kill()
            return False


class Player(pygame.sprite.Sprite):
    # Это класс игрока. В нем отслеживается его уровень, рекорд, скорость, здоровье,
    # подобранный дроп и все, связанное с ракетой
    def __init__(self, sprite_path, x, y):
        super().__init__(player_sprite)
        self.image = pygame.image.load(sprite_path)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.path_ro_sprite = sprite_path
        self.helth = 1000
        self.sprite_number = 1
        self.rect.x = x
        self.speed = 10
        self.rect.y = y

    def update(self):
        if self.sprite_number < 13:
            self.sprite_number += 1
        else:
            self.sprite_number = 1
        self.path_ro_sprite = '/'.join(self.path_ro_sprite.split('/')[:-1]) + '/' + str(self.sprite_number) + '.png'
        self.image = pygame.image.load(self.path_ro_sprite)
        player_sprite.draw(screen2)
        screen.blit(screen2, (0, 0))

    def move(self, key):
        if key == 276:
            if self.rect.x > 5:
                self.rect.x -= self.speed
            else:
                self.rect.x = 1660
        elif key == 275:
            if self.rect.x < 1660:
                self.rect.x += self.speed
            else:
                self.rect.x = 5
        elif key == 273 and self.rect.y > 20:
            self.rect.y -= self.speed
        elif key == 274 and self.rect.y < 500:
            self.rect.y += self.speed


class Raptor(pygame.sprite.Sprite):
    # В этом классе создается дроп - двигатель раптор, котороый увеличивает скорость на 50 %
    #  и отслеживается время его действия
    def __init__(self):
        super().__init__()


class Fairing(pygame.sprite.Sprite):
    # В этом классе создается дроп - титановый обтекатель, который позволяет ракете выдержать 3 удара
    # и отслеживается его состояние
    def __init__(self):
        super().__init__()


class Fuel(pygame.sprite.Sprite):
    # В этом классе создается дроп - топливо, которое повышает здоровье игрока на 20%.
    def __init__(self):
        super().__init__()


class Upgrade(pygame.sprite.Sprite):
    # В этом классе создается дроп - запчасии. Они увеличивают опыт игрока и с помощью них игрок сменяет ракеты,
    # когда накопит нужное количество опыта.
    def __init__(self):
        super().__init__()


def start_screen():
    record = json.loads(open(PATH_TO_RECORD_FILE).read())['record'][-1]
    record = 'Ваш рекорд: ' + record
    background = pygame.image.load(PATH_TO_START_SCREEN)
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 90).render(record, 1, pygame.Color('white'))
    screen.blit(font, (100, 700))
    button_pos = (300, 400)
    button = ButtonStartGame(button_pos[0], button_pos[1], PATH_TO_BUTTON_START_GAME)
    button.render()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if button.is_clicked(event.pos):
                    return
        pygame.display.flip()


start_screen()

running = True
background = Background()
player = Player(PATH_TO_ROCKET_SPRITES + '/1/1.png', 500, 500)
clock = pygame.time.Clock()
screen2 = pygame.Surface(screen.get_size())
is_move = False
key = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            is_move = True
            key = event.key
            print(key)
        if event.type == pygame.KEYUP:
            if key == 275 or key == 276 or key == 273 or key == 274:
                is_move = False
    if is_move:
        player.move(key)

    clock.tick(60)
    screen2.blit(background.get_fon(), (0, 0))
    player.update()
    background.update()
    pygame.display.flip()
