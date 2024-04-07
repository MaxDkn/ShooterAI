import sys
import math
import random
import pygame
import datetime
from programs.gui import Text
from programs.data import DataBase, CONSTANT
from programs.sprite import Player, BulletFromPlayer


def convert_s_to_min_and_s(t) -> str:
    if int(t // 60) == 0:
        return f"{str(math.floor(t % 60 * 10) / 10).zfill(4)}"
    elif int(t // 60) > 0:
        return f"{int(t // 60)}:{str(math.floor(t % 60)).zfill(2)}"
    else:
        return "00.0"


class Game:
    pygame.init()

    #  -------TIME MANAGEMENT-------  #
    dt = int
    game_fps = CONSTANT['GAME_FPS']
    current_time: int
    time_is_paused = False
    game_duration = CONSTANT['GAME_DURATION']
    wait_for_the_end = CONSTANT['TIME_BEFORE_CLOSED']

    #  This variable contains the moment of the end game. If it's not over, the variable is empty.
    game_is_finished: int = None
    #  This is an arbitrary value that's mean that the game was interrupted;
    #  -1 mean that was a draw and if it's a win, then the value will be the index of players
    final_score: int or tuple = -2

    #  ----------MAP DATA----------  #
    width = CONSTANT['WIDTH']
    height = CONSTANT['HEIGHT']
    map_size = (CONSTANT['WIDTH'], CONSTANT['HEIGHT'])

    background_color = CONSTANT['BACKGROUND_COLOR']
    #  players_position = [(200, map_size[1]/2), (map_size[0] - 200, map_size[1]/2)]
    players_position = []
    for team_index in range(0, CONSTANT['N_OF_TEAM']):
        team = []
        for _ in range(0, CONSTANT['N_PLAYERS_IN_TEAM']):
            spawn_marge = 100
            team.append((random.randint(spawn_marge, map_size[0] - spawn_marge),
                         random.randint(int(spawn_marge + map_size[1] / 2 * team_index),
                                        int(map_size[1] / 2 + map_size[1] / 2 * team_index - spawn_marge))))
        players_position.append(team)

    def __init__(self, time=1, backup=True, reboot=True, auto_closed: int or bool = False) -> None:
        self.screen = pygame.display.get_surface()
        self.backup = backup
        if self.backup:
            self.key_name = (f'{datetime.date.today().strftime("%d/%m/%Y")} '
                             f'{datetime.datetime.now().time().strftime("%H:%M:%S")}')
            self.database = DataBase(reboot)
        if type(auto_closed) is bool:
            self.auto_closed = auto_closed
        elif type(auto_closed) is int:
            self.auto_closed = True
            self.wait_for_the_end = auto_closed

        if self.screen is None:
            self.screen = pygame.display.set_mode((self.width, self.height))

        self.time_coefficient = time
        pygame.display.set_caption(' ')
        self.clock = pygame.time.Clock()
        self.program_information_text = [Text('', CONSTANT['SHOW_INFO_TEXT_SIZE'], (0, 0), 'black', 'topleft'),
                                         Text('', CONSTANT['CLOCK_SIZE'], (self.width / 2, 0), 'black', 'midtop'),
                                         Text('', CONSTANT['SHOW_INFO_TEXT_SIZE'], (self.width, self.height), 'black',
                                              'bottomright'),
                                         Text('', CONSTANT['SHOW_FINAL_SCORE'], (self.width / 2, self.height / 2),
                                              'black', 'midbottom')]
        self.sprite_alive_group = []
        self.sprite_death = []
        self.load_players()

    def load_players(self):
        for team_index, player_positions in enumerate(self.players_position):
            for index, pos in enumerate(player_positions):
                index += team_index * len(player_positions)
                new_player = Player(pos, self.map_size, index, team_index)
                self.sprite_alive_group.append(new_player)

    def show_clock(self):
        self.program_information_text[1].update_text(convert_s_to_min_and_s(self.game_duration - self.current_time))
        self.program_information_text[1].draw(self.screen)

    def show_system_info(self):
        fps = 1 / self.dt
        self.program_information_text[0].update_text(f"{round(fps)} FPS | x{self.time_coefficient}")
        text = ""

        for sprite in self.sprite_alive_group:
            if isinstance(sprite, Player):
                text += f"p{sprite.index}: {sprite.hp}hp | "
        text = text[:-2]
        self.program_information_text[2].update_text(text)
        #  pygame.display.set_caption(f"{round(self.current_time, 1)}s")
        #  pygame.display.set_caption(f"{convert_s_to_min_and_s(round(self.current_time, 1))}")
        for text in self.program_information_text[:-1]:
            text.draw(self.screen)
        #  Show how many bullet the main player have

    def remove_old_bullet(self):
        margin_error = CONSTANT['MARGIN_TO_REMOVE_BULLET']
        for sprite in self.sprite_alive_group:
            if isinstance(sprite, BulletFromPlayer):
                #  Check for x pos
                if sprite.current_pos_x < 0 - margin_error or sprite.current_pos_x > self.map_size[0] + margin_error:
                    self.sprite_alive_group.remove(sprite)
                #  Check for y pos
                elif sprite.current_pos_y < 0 - margin_error or sprite.current_pos_y > self.map_size[1] + margin_error:
                    self.sprite_alive_group.remove(sprite)

    def player_won(self, player_index):
        self.program_information_text[3].update_text(f"The player {player_index} have won!")

        self.time_is_paused = True
        self.program_information_text[3].draw(self.screen)

    def player_loose(self, player_index):
        self.program_information_text[3].update_text(f"The player {player_index} have loose!")

        self.time_is_paused = True
        self.program_information_text[3].draw(self.screen)

    def team_won(self, team_index):
        self.program_information_text[3].update_text(f"The team {team_index} have won!")

        self.time_is_paused = True
        self.program_information_text[3].draw(self.screen)

    def draw(self):
        self.final_score = -1
        self.program_information_text[3].update_text(f"DRAW !")
        self.time_is_paused = True
        self.program_information_text[3].draw(self.screen)

    def knockout_rules(self):
        if self.current_time >= self.game_duration:
            self.draw()
        team_death = []
        team_alive = []
        for sprite in self.sprite_alive_group:
            if isinstance(sprite, Player):
                if sprite.hp <= 0:
                    self.sprite_alive_group.remove(sprite)
                    self.sprite_death.append(sprite)
        for team_index in range(0, CONSTANT['N_OF_TEAM']):
            count = 0
            for sprite in self.sprite_death:
                if sprite.team_index == team_index:
                    count += 1
            if count >= CONSTANT['N_PLAYERS_IN_TEAM']:
                team_death.append(team_index)
            else:
                team_alive.append(team_index)

        if len(team_death) + 1 == CONSTANT['N_OF_TEAM'] == 2:
            self.team_won(team_alive[0])
            self.final_score = team_alive[0]
        elif len(team_alive) == 0 and len(team_death) == CONSTANT['N_OF_TEAM']:
            self.draw()
            self.final_score = -1
        elif len(team_death) + 1 == CONSTANT['N_OF_TEAM'] >= 2:
            print('We have to see the case where he has more than two teams, lazy to do it now')
            sys.exit(5)

    def rules(self):
        if self.current_time >= self.game_duration:
            self.draw()
        sprites_death = []
        sprites_alive = []
        for sprite in self.sprite_alive_group:
            if isinstance(sprite, Player):
                if sprite.hp <= 0:
                    sprites_death.append(sprite)
                else:
                    sprites_alive.append(sprite)

        if len(sprites_death) == 1:
            self.final_score = []
            self.player_loose(sprites_death[0].index)
            for sprite_who_won in sprites_alive:
                self.final_score.append(sprite_who_won.index)
            self.final_score = tuple(self.final_score)

        elif len(sprites_death) == 2:
            self.final_score = -1
            self.draw()

    def get_end_game_information(self):
        heal_points = []
        ammo_shot = []
        for sprite in self.sprite_alive_group:
            if isinstance(sprite, Player):
                heal_points.insert(sprite.index, sprite.hp)
                ammo_shot.insert(sprite.index, sprite.ammo_shot_count)

        return self.final_score, int(self.current_time), heal_points, ammo_shot

    def run(self):
        self.current_time = 0
        running = True

        while running:
            self.dt = self.clock.tick(self.game_fps) / 1000
            if not self.time_is_paused:
                self.current_time += self.dt * self.time_coefficient

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.backup and (self.current_time >= self.game_duration or self.final_score != -2):
                        final_score, final_time, heal_points, ammo_shot = self.get_end_game_information()
                        self.database.save_game(self.key_name, final_score, final_time, heal_points, ammo_shot)
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        if self.backup and (self.current_time >= self.game_duration or self.final_score != -2):
                            final_score, final_time, heal_points, ammo_shot = self.get_end_game_information()
                            self.database.save_game(self.key_name, final_score, final_time, heal_points, ammo_shot)
                    elif event.key == pygame.K_SPACE:
                        self.time_is_paused = not self.time_is_paused

            for sprite in self.sprite_alive_group:
                if not self.time_is_paused:
                    if isinstance(sprite, Player):
                        sprite.small_ai(self.current_time)
                        sprite.check_bullet(self.sprite_alive_group)
                        if sprite.is_shooting:
                            self.sprite_alive_group.append(BulletFromPlayer(sprite, self.current_time))
                    sprite.update(self.current_time)
                sprite.draw(self.screen)

            self.knockout_rules()

            if (self.auto_closed and (self.current_time >= self.game_duration or self.final_score != -2) and
                    self.game_is_finished is None):
                self.game_is_finished = pygame.time.get_ticks()
            if self.game_is_finished is not None:
                if (pygame.time.get_ticks() - self.game_is_finished) * 10 ** (-3) >= self.wait_for_the_end:
                    if self.backup and (self.current_time >= self.game_duration or self.final_score != -2):
                        final_score, final_time, heal_points, ammo_shot = self.get_end_game_information()
                        self.database.save_game(self.key_name, final_score, final_time, heal_points, ammo_shot)
                    running = False

            self.remove_old_bullet()
            if CONSTANT['SHOW_SYSTEM_INFO']:
                self.show_system_info()
            self.show_clock()
            pygame.display.update()
            self.screen.fill(self.background_color)


if __name__ == '__main__':
    Game(25, True, True, 1).run()
