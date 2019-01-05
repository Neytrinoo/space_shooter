import pygame
import json

pygame.init()
size = width, height = 1700, 900
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
fps = 100
PATH_TO_RECORD_FILE = 'record.json'
PATH_TO_START_SCREEN = 'img/start_screen.jpg'
PATH_TO_BUTTON_START_GAME = 'img/button_start_game.png'


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
    # В этом классе создаются дропы и враги
    def __init__(self):
        pass


class Meteorite(pygame.sprite.Sprite):
    # В этом классе генерируются метеориты и есть функция контроля пересечения метеорита и игрока
    def __init__(self):
        super().__init__()


class Enemy(pygame.sprite.Sprite):
    # В этом классе генерируются враги все их функции
    def __init__(self):
        super().__init__()


class Bullet(pygame.sprite.Sprite):
    # В этом классе генерируются пули врагов и отслеживается их пересечение с игроком
    def __init__(self):
        super().__init__()


class Player(pygame.sprite.Sprite):
    # Это класс игрока. В нем отслеживается его уровень, рекорд, скорость, здоровье, подобранный дроп и все, связанное с ракетой
    def __init__(self):
        super().__init__()


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
    return button


button = start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if button.is_clicked(event.pos):
                print('нажата')
    pygame.display.flip()
