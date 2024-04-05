import os
import pickle
import shutil

"""
{
'31/03/2024 18:31:19': {'final score': -1, 'final time': 150, 'hp': [60, 60], 'number of ammo_shot': [2, 5]}, 
'31/03/2024 18:31:28': {'final score': -1, 'final time': 150, 'hp': [60, 60], 'number of ammo_shot': [3, 0]}
}
"""


def load_constant(path_and_file=r'../config.txt'):
    all_constant = {}
    if not os.path.isfile(path_and_file):
        with open(path_and_file, 'w') as file:
            file.write("""GAME_FPS: int = 120
GAME_DURATION: int = 90
TIME_BEFORE_CLOSED: float = 2.5
WIDTH: int = 1000
HEIGHT: int = 725
BACKGROUND_COLOR: str = #E6E6E6
N_OF_TEAM: int = 2
N_PLAYERS_IN_TEAM: int = 3
MARGIN_TO_REMOVE_BULLET: int = 20

FONT_NAME: str = Noto_Sans_Mono
SHOW_INFO_TEXT_SIZE: int = 10
CLOCK_SIZE: int = 15
SHOW_FINAL_SCORE: int = 30
SHOW_SYSTEM_INFO: bool = True

SPRITE_COLOR: str = #E6E6E6
AI_INPUT_DELAY: float = 0.3
SPRITE_SIZE: int = 30
SPRITE_SPEED: int = 150
SPRITE_HEAL_POINTS: int = 60
SHOW_INDEX_TEXT: bool = True

MOVEMENT_CIRCLE_DIST: int = 20
MOVEMENT_CIRCLE_SIZE: int = 10
SHOW_INPUT_MOVEMENT: bool = True

BULLET_START_POS_LENGTH: int = 30
AMMO_MAX: int = 3
RELOAD_TIME: int = 3
BULLET_SIZE: int = 10
BULLET_SPEED: int = 340
BULLET_COLOR: str = black
BULLET_DAMAGE: int = 20
""")
            file.close()

    with (open(path_and_file, 'r') as file):
        for line in file.readlines():
            if line != '\n':
                variable_name, value_information = line.split(':')
                variable_type, value = value_information.split('=')
                variable_name, variable_type, value = variable_name.strip(), eval(variable_type.strip()), value.strip()
                if variable_type == bool and value == 'False':
                    all_constant[variable_name] = False
                else:
                    all_constant[variable_name] = variable_type(value)
        file.close()
        return all_constant


CONSTANT = load_constant()


class DataBase:
    working_path = '..'
    extension_files = '.db'

    def __init__(self, reboot=True):
        if reboot:
            self.clear()
        self.create_files()

    def clear(self):
        if os.path.isdir(f'{self.working_path}/data'):
            shutil.rmtree(f'{self.working_path}/data')
            return 'data was deleted'

    def create_files(self):
        if not os.path.isdir(f'{self.working_path}/data'):
            os.mkdir(f'{self.working_path}/data')
        if not os.path.isfile(f'{self.working_path}/data/main{self.extension_files}'):
            with open(f'{self.working_path}/data/main{self.extension_files}', 'wb') as file:
                file.write(pickle.dumps('{}'))
                file.close()

    def load_data(self):
        with open(f'{self.working_path}/data/main{self.extension_files}', 'rb') as file:
            data = pickle.loads(file.read())
            file.close()
            if data == {}:
                return {}
            else:
                return data

    def save_data(self, data):
        with open(f'{self.working_path}/data/main{self.extension_files}', 'wb') as file:
            file.write(pickle.dumps(data))
            file.close()

    def save_game(self, key_name: str, final_score: str, final_time: int, heal_points: list[int, int],
                  ammo_shot: list[int, int]):
        data_to_save = {'final score': final_score,
                        'final time': final_time,
                        'hp': heal_points,
                        'number of ammo_shot': ammo_shot}
        try:
            all_data = dict(self.load_data())
        except ValueError:
            all_data = {}

        all_data[key_name] = data_to_save
        self.save_data(all_data)
        print(self.load_data())
