import pygame
import json
from random import randint, choice

pygame.init()
size = width, height = 1700, 900
screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)
player_sprite = pygame.sprite.Group()
enemies_sprite = pygame.sprite.Group()
bullets_sprite = pygame.sprite.Group()
sparks_sprite = pygame.sprite.Group()
meteorits_sprite = pygame.sprite.Group()
screen.fill((0, 0, 0))
fps = 100
PATH_TO_RECORD_FILE = 'record.json'
PATH_TO_START_SCREEN = 'img/start_screen.jpg'
PATH_TO_BUTTON_START_GAME = 'img/button_start_game.png'
PATH_TO_FONS = 'img/fons/'
PATH_TO_ROCKET_SPRITES = 'img/sprites/rockets'
PATH_TO_ENEMIES_SPRITES = 'img/sprites/enemies'
PATH_TO_BULLETS_SPRITES = 'img/sprites/enemies/bullets'
PATH_TO_METEORITES_SPRITES = 'img/sprites/meteorites'
PATH_TO_SPARKS_SPRITE = 'img\sprites\particles\sparks'
COUNT_SPARCKS = 5
COUNT_ROCKETS = 1
COUNT_ENEMIES = 2
COUNT_BULLETS = 2
COUNT_METEORITES = 3


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


class Health:
    def __init__(self, health, all_health):
        self.height = 100
        pygame.draw.rect(screen2, (0, 255, 0), (500, 10, self.height, 10))
        pygame.draw.rect(screen2, (0, 0, 0), (499, 9, self.height + 2, 12), 1)
        font = pygame.font.Font(None, 20).render('100 %', 1, pygame.Color('white'))
        screen2.blit(font, (605, 8))
        self.health = health
        self.all_health = all_health
        screen.blit(screen2, (0, 0))

    def update(self):
        if self.health > 0:
            procent = (self.health / (self.all_health / 100)) / 100
            pygame.draw.rect(screen2, (0, 255, 0),
                             (500, 10, self.height * procent, 10))
            pygame.draw.rect(screen2, (0, 0, 0), (499, 9, self.height + 2, 12), 1)
            font = pygame.font.Font(None, 20).render(str(int(procent * 100)) + ' %', 1, pygame.Color('white'))
            screen2.blit(font, (605, 8))
        else:
            pygame.draw.rect(screen2, (0, 0, 0), (499, 4, self.height + 2, 12), 1)
            font = pygame.font.Font(None, 20).render('0 %', 1, pygame.Color('white'))
            screen2.blit(font, (605, 8))

    def take_health(self, count):
        self.health -= count


class Background:
    def __init__(self):
        self.fon_img = pygame.image.load(PATH_TO_FONS + 'fon' + str(randint(1, 3)) + '.jpg')
        screen.blit(self.fon_img, (0, 0))
        self.speed = 2
        self.count_iter = 0
        self.enemies = []
        self.meteorites = []
        self.sparks = []

    def get_fon(self):
        return self.fon_img

    def update(self):
        who_is = randint(1, 3)
        if who_is == 2 and (not self.enemies or self.count_iter % 100 == 0):
            self.enemies.append(
                Enemy(PATH_TO_ENEMIES_SPRITES + '/' + str(randint(1, COUNT_ENEMIES)) + '.png', randint(100, 1500), 0,
                      self.speed))
        if who_is == 1 and (not self.meteorites or self.count_iter % 150 == 0):
            self.meteorites.append(
                Meteorite(PATH_TO_METEORITES_SPRITES + '/' + str(randint(1, COUNT_METEORITES)) + '.png',
                          randint(60, 1830), 0, self.speed))
        self.update_enemies()
        self.update_meteorites()
        self.update_sparks()
        self.count_iter += 1
        if self.count_iter > 1000:
            self.count_iter = 0

    def update_enemies(self):
        to_delete = []
        for i in range(len(self.enemies)):
            if player.rocket_level > 1:
                self.enemies[i].move(player, True)
            else:
                self.enemies[i].move(player, False)
            if not self.enemies[i].bullet or self.count_iter % 100 == 0:
                self.enemies[i].shoot()
            for j in range(len(self.enemies[i].bullet)):
                self.enemies[i].bullet[j].move()
                if self.enemies[i].bullet[j].is_collidle(player) and not self.sparks:
                    sparks_count = 50
                    nums = range(-6, 10)
                    for _ in range(sparks_count):
                        self.sparks.append(
                            Sparks(self.enemies[i].bullet[j].rect.x, self.enemies[i].bullet[j].rect.y, choice(nums),
                                   choice(nums),
                                   self.speed))
                    player.take_health(200)
            is_del = False
            if self.enemies[i].is_collidle(player):
                is_del = True
                to_delete.append(i)
                sparks_count = 80
                nums = range(-6, 10)
                is_del = True
                for _ in range(sparks_count):
                    self.sparks.append(
                        Sparks(self.enemies[i].rect.x, self.enemies[i].rect.y, choice(nums), choice(nums),
                               self.speed))
                player.take_health(100)
            if not self.enemies[i].in_screen() and not is_del:
                to_delete.append(i)

        enemies_sprite.draw(screen2)
        bullets_sprite.draw(screen2)
        screen.blit(screen2, (0, 0))
        for i in to_delete:
            del self.enemies[i]

    def update_meteorites(self):
        to_delete = []
        for i in range(len(self.meteorites)):
            self.meteorites[i].move()
            is_del = False
            if self.meteorites[i].is_collidle(player) and not self.sparks:
                to_delete.append(i)
                sparks_count = 30
                nums = range(-6, 10)
                is_del = True
                for _ in range(sparks_count):
                    self.sparks.append(
                        Sparks(self.meteorites[i].rect.x, self.meteorites[i].rect.y, choice(nums), choice(nums),
                               self.speed))
                player.take_health(300)
            if not self.meteorites[i].in_screen() and not to_delete:
                to_delete.append(i)
        for i in to_delete:
            del self.meteorites[i]
        meteorits_sprite.draw(screen2)
        screen.blit(screen2, (0, 0))

    def update_sparks(self):
        to_delete = []
        for i in range(len(self.sparks)):
            self.sparks[i].move()
            if not self.sparks[i].in_screen():
                to_delete.append(i)

        sparks_sprite.draw(screen2)
        screen.blit(screen2, (0, 0))
        for i in to_delete:
            if i < len(self.sparks):
                self.sparks[i].kill()
                del self.sparks[i]


class Sparks(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed):
        super().__init__(sparks_sprite)
        image = pygame.image.load(PATH_TO_SPARKS_SPRITE + '/' + str(randint(1, COUNT_SPARCKS)) + '.png')
        sparks = [image]
        for scale in (5, 10):
            sparks.append(pygame.transform.scale(sparks[0], (scale, scale)))
        self.image = choice(sparks)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [dx, dy]
        self.speed = speed

    def move(self):
        self.velocity[1] += self.speed
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def in_screen(self):
        if self.rect.y < 900:
            return True
        else:
            self.kill()
            return False


class Meteorite(pygame.sprite.Sprite):
    # В этом классе генерируются метеориты и есть функция контроля пересечения метеорита и игрока
    def __init__(self, sprite_path, x, y, speed):
        super().__init__(meteorits_sprite)
        self.image = pygame.image.load(sprite_path)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y += self.speed

    def is_collidle(self, elem):
        if pygame.sprite.collide_mask(self, elem):
            print('Врезался в метеорит')
            self.kill()
            return True
        return False

    def in_screen(self):
        if self.rect.colliderect(screen_rect):
            return True
        else:
            self.kill()
            return False


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

    def move(self, user, is_gui):
        if self.count_iter == 1:
            if is_gui:
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
        elif self.number_enemy == '2':
            x = self.rect.x
        y = self.rect.y + 130
        self.bullet.append(Bullet(PATH_TO_BULLETS_SPRITES + '/' + self.number_enemy + '.png', self.speed * 4, x, y))

    def in_screen(self):
        if self.rect.colliderect(screen_rect):
            return True
        else:
            self.kill()
            return False

    def is_collidle(self, elem):
        if pygame.sprite.collide_mask(self, elem):
            print('попался')
            self.kill()
            for i in range(len(self.bullet)):
                self.bullet[i].kill()
            return True
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
            self.kill()
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
        self.rocket_level = 1
        self.health = 1000
        self.all_health = 1000
        self.sprite_number = 1
        self.rect.x = x
        self.speed = 10
        self.rect.y = y
        self.line_health = Health(self.health, self.all_health)

    def update(self):
        if self.sprite_number < 13:
            self.sprite_number += 1
        else:
            self.sprite_number = 1
        self.path_ro_sprite = '/'.join(self.path_ro_sprite.split('/')[:-1]) + '/' + str(self.sprite_number) + '.png'
        self.image = pygame.image.load(self.path_ro_sprite)
        player_sprite.draw(screen2)
        self.line_health.update()
        screen.blit(screen2, (0, 0))

    def move(self, key):
        if key == 276:
            if self.rect.x > 5:
                self.rect.x -= self.speed
            else:
                self.rect.x = 1680
        elif key == 275:
            if self.rect.x < 1680:
                self.rect.x += self.speed
            else:
                self.rect.x = 5
        elif key == 273 and self.rect.y > 20:
            self.rect.y -= self.speed
        elif key == 274 and self.rect.y < 700:
            self.rect.y += self.speed

    def take_health(self, count):
        self.health -= count
        self.line_health.take_health(count)
        print(self.health)
        if self.health <= 0:
            print('Вы проиграли')

    def get_health(self, count):
        self.health += count


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
screen2 = pygame.Surface(screen.get_size())
player = Player(PATH_TO_ROCKET_SPRITES + '/1/1.png', 500, 700)
clock = pygame.time.Clock()

is_move = False
key = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            is_move = True
            key = event.key
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
