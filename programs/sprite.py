import math
import pygame
from programs.gui import Text
from programs.ai import ArtificialIntelligence
from programs.data import CONSTANT


input_direction_key = [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d]


def normalized(a, b):
    if ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) == 0:
        return 0, 0
    else:
        k = 1 / ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
        return k * (b[0] - a[0]), k * (b[1] - a[1])


def dist(a, b):
    d_sq = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    return math.sqrt(d_sq)


class Player(pygame.sprite.Sprite):
    color = CONSTANT['SPRITE_COLOR']

    #  ----------FUNDAMENTAL SPRITE ATTRIBUTE---------- #
    input_delay: float = CONSTANT['AI_INPUT_DELAY']
    size: int = CONSTANT['SPRITE_SIZE']
    speed: int = CONSTANT['SPRITE_SPEED']
    reload_time: int = CONSTANT['RELOAD_TIME']
    hp: int = CONSTANT['SPRITE_HEAL_POINTS']

    #  -------------AMMUNITION MANAGEMENT-------------  #

    #  The length between the player positions and the start position of the bullet
    bullet_start_pos_length: int = CONSTANT['BULLET_START_POS_LENGTH']
    ammo_max: int = CONSTANT['AMMO_MAX']
    ammo_that_already_touch_me: list = []

    def __init__(self, start_pos, map_size, player_index, team_index):
        super().__init__()
        self.pos = pygame.math.Vector2(start_pos)
        self.map_size = map_size
        self.index = player_index
        self.team_index = team_index
        if CONSTANT['SHOW_INDEX_TEXT']:
            self.index_text = Text(f'p{self.index}', 13, start_pos, 'black', 'center')

        self.direction = pygame.math.Vector2()
        self.genetic_ai = ArtificialIntelligence(self.map_size)

        self.old_time: float = 0
        self.is_shooting: bool = False
        self.bullet_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.mouse_clicked: bool = False

        self.ammo_count = self.ammo_max
        self.ammo_shot_count = 0
        self.last_movement_time = 0

    def check_bullet(self, sprites):
        for sprite in sprites:
            if isinstance(sprite, BulletFromPlayer):
                if (sprite not in self.ammo_that_already_touch_me and dist((self.pos.x, self.pos.y), (
                        sprite.current_pos_x, sprite.current_pos_y)) <= (self.size + sprite.size) / 2
                        and self.team_index != sprite.team_index):
                    self.ammo_that_already_touch_me.append(sprite)
                    self.hp -= sprite.damage

        for bullet in self.ammo_that_already_touch_me:
            if bullet not in sprites:
                self.ammo_that_already_touch_me.remove(bullet)

    def small_ai(self, current_time):
        if current_time - self.last_movement_time >= self.input_delay:
            self.direction.x, self.direction.y = self.genetic_ai.choose_direction()
            if self.direction.x != 0 or self.direction.y != 0:
                self.last_movement_time = current_time

            shoot_decision = self.genetic_ai.choose_shooting()
            if shoot_decision is not None:
                x_pos, y_pos = shoot_decision
                self.shoot(x_pos, y_pos)
                self.last_movement_time = current_time

    def input(self):
        key_pressed = pygame.key.get_pressed()

        #  Shoot Management
        if self.mouse_clicked:
            if not pygame.mouse.get_pressed()[0]:
                self.mouse_clicked = False
        else:
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.shoot(mouse_x, mouse_y)
                self.mouse_clicked = True

        #  Movement Management
        if key_pressed[input_direction_key[0]] and key_pressed[input_direction_key[1]]:
            self.direction.y = 0
        elif key_pressed[input_direction_key[0]]:
            self.direction.y = -1
        elif key_pressed[input_direction_key[1]]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if key_pressed[input_direction_key[2]] and key_pressed[input_direction_key[3]]:
            self.direction.x = 0
        elif key_pressed[input_direction_key[2]]:
            self.direction.x = -1
        elif key_pressed[input_direction_key[3]]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def shoot(self, x, y):
        if math.floor(self.ammo_count) > 0:
            self.is_shooting = True
            self.ammo_count = self.ammo_count - 1
            self.ammo_shot_count += 1
            self.bullet_direction.x = x - self.pos.x
            self.bullet_direction.y = y - self.pos.y
            if self.bullet_direction.magnitude() != 0:
                self.bullet_direction = self.bullet_direction.normalize()

    def update(self, current_time):
        if self.direction.magnitude() != 0 and self.direction.magnitude() > 1:
            self.direction = self.direction.normalize()
        #  Check if the player goes outside the map
        if (self.pos.x + self.direction.x * self.speed * (current_time - self.old_time) +
                self.size/2 >= self.map_size[0]):
            self.pos.x = self.map_size[0] - self.size/2
        elif self.pos.x + self.direction.x * self.speed * (current_time - self.old_time) - self.size/2 <= 0:
            self.pos.x = self.size / 2
        else:
            self.pos.x += self.direction.x * self.speed * (current_time - self.old_time)

        if (self.pos.y + self.direction.y * self.speed * (current_time - self.old_time) +
                self.size/2 >= self.map_size[1]):
            self.pos.y = self.map_size[1] - self.size/2
        elif self.pos.y + self.direction.y * self.speed * (current_time - self.old_time) - self.size/2 <= 0:
            self.pos.y = self.size / 2
        else:
            self.pos.y += self.direction.y * self.speed * (current_time - self.old_time)

        if self.is_shooting:
            self.is_shooting = False

        if self.ammo_count < self.ammo_max:
            self.ammo_count += (current_time - self.old_time) / self.reload_time
        else:
            self.ammo_count = self.ammo_max
        #  self.ammo_count += (current_time - self.old_time) / self.reload_time
        if CONSTANT['SHOW_INDEX_TEXT']:
            self.index_text.update_pos((self.pos.x, self.pos.y))

        self.old_time = current_time

    def draw_input_movement(self, screen):
        distance = CONSTANT['MOVEMENT_CIRCLE_DIST']
        diameter = CONSTANT['MOVEMENT_CIRCLE_SIZE']
        """pygame.draw.circle(screen, 'white', (int(self.pos.x + dist * self.direction.x),
                                             int(self.pos.y + dist * self.direction.y)), s)"""
        pygame.draw.circle(screen, 'black', (int(self.pos.x + distance * self.direction.x),
                                             int(self.pos.y + distance * self.direction.y)), diameter / 2, 2)

    def draw(self, screen):
        if CONSTANT['SHOW_INPUT_MOVEMENT']:
            self.draw_input_movement(screen)
        #  pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.size / 2)
        pygame.draw.circle(screen, 'black', (int(self.pos.x), int(self.pos.y)), self.size / 2, 4)
        if CONSTANT['SHOW_INDEX_TEXT']:
            self.index_text.draw(screen)


class BulletFromPlayer:
    size = CONSTANT['BULLET_SIZE']
    speed = CONSTANT['BULLET_SPEED']
    color = CONSTANT['BULLET_COLOR']
    damage = CONSTANT['BULLET_DAMAGE']

    def __init__(self, player: Player, start_time):
        self.player = player
        self.direction = self.player.bullet_direction.copy()
        self.start_pos_x = self.player.pos.x + self.player.bullet_start_pos_length * self.direction.x
        self.start_pos_y = self.player.pos.y + self.player.bullet_start_pos_length * self.direction.y
        self.start_time = start_time
        self.current_pos_x = self.start_pos_x
        self.current_pos_y = self.start_pos_y
        self.team_index = self.player.team_index

    def update(self, time):
        self.current_pos_x = self.start_pos_x + self.direction.x * self.speed * (time - self.start_time)
        self.current_pos_y = self.start_pos_y + self.direction.y * self.speed * (time - self.start_time)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.current_pos_x, self.current_pos_y), self.size / 2)
