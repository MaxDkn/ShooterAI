import pygame
from programs.gui import Text
from programs.game import Game


class MainWindow:
    pygame.init()
    background_color = '#DCD7D0'
    width = 1000
    height = 725
    background = pygame.image.load(r'img/background.png')
    background = pygame.transform.scale(background, (height, height))
    background_rect = background.get_rect(center=(width-height/2 + 40, height/2))

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('MENU - SHOOTER AI')
        self.text = Text('Press <Ctrl> and <Tab> to start the game', 20, (20, 390), 'black', 'topleft')
        self.game = None

    def draw_background(self):
        self.screen.blit(self.background, self.background_rect)

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_TAB] and pygame.key.get_pressed()[pygame.K_LCTRL]:
                        Game(1, False, False, False).run()

            self.draw_background()
            self.text.draw(self.screen)
            pygame.display.update()
            self.screen.fill(self.background_color)


if __name__ == "__main__":
    window = MainWindow()
    window.run()
