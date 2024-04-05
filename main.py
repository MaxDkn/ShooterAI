import pygame
from programs.gui import Text
from programs.game import Game
#  https://www.youtube.com/watch?v=rDwaeXuQaEI&ab_channel=MaxonTech


class MainWindow:
    pygame.init()
    background_color = (100, 50, 100)
    width = 1000
    height = 725

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('MENU - SHOOTER AI')
        self.text = Text('Press <Ctrl> and <Tab> to start the game', 20, (self.width/2, self.height/2+50))
        self.game = None

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_TAB] and pygame.key.get_pressed()[pygame.K_LCTRL]:
                        Game(1, False, False, False).run()
            self.text.draw(self.screen)
            pygame.display.update()
            self.screen.fill(self.background_color)


if __name__ == "__main__":
    window = MainWindow()
    window.run()
