"""
Space Invader game just for fun ;)

Version:
--------
0.2.0

Controls:
---------
going left: Left arrows key or Q. (A in the code because pygame think it's a qwerty keyboard)
going right: Right arrows key or D.
shoot laser: Space bar.
pause the game: Escape.

By Ryan Rennoir
Using Python 3.6.5
"""
import pygame as pg

from init_data import setup_data
from game_update import game_update
from game_ui import intro, outro, pause, hud
from draw import draw_on_screen


def game(screen, clock, font):
    """
    Function with the game loop.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    clock: Object who track time (clock)
    font: Dictionnary with differente font and color (dict)

    Return:
    -------
    result: Result of the game win or lost (str)
    """

    # Setup game_data.
    game_data = setup_data(screen.get_height(), screen.get_width())
    running = True
    while running:

        # Clear the screen from previous frame.
        screen.fill((0, 0, 0))

        # Quit the game if the quit button is pressed.
        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        # Pause the game is ESCAPE is pressed.
        if keys[pg.K_ESCAPE]:
            pause(screen, font["title"], font["basic"], font["color_white"])

        # Game Update.
        game_data, running = game_update(game_data)

        # UI update.
        hud(screen, clock, font, game_data["player"]["life"], game_data["score"])

        # Game Drawn.
        draw_on_screen(screen, game_data)

        # Display update pygame.
        screen.blit(screen, (0, 0))
        pg.display.flip()

        # Set the game to 60 update per second.
        clock.tick(60)

    # Check If game win or lost.
    if game_data["player"]["life"] > 0:
        return "Game Win"

    return "Game Lost"


def main():
    """
    Starting point of the game code.
    Manage everything form the intro screen to the outro screen and allow to play again.
    """

    # init pygame, import every module in pygame.
    pg.init()

    # Setup the font.
    font = {
        "basic": pg.font.SysFont("Comic Sans MS", 15),
        "title": pg.font.SysFont("Comic Sans MS", 30),
        "color_white": (255, 255, 255)
    }


    # Setup window of 300 by 400 pixel.
    display_size = [300, 400]
    screen = pg.display.set_mode(display_size)

    # Set the windows title
    pg.display.set_caption("Space Invader")

    clock = pg.time.Clock()

    # Start intro screen and wait for player.
    intro(screen, font["title"], font["basic"], font["color_white"])

    # Game.
    play = True
    while play:

        # Game logic
        result = game(screen, clock, font)

        # Game terminated draw outro screen
        # and wait for player input to continue or stop.
        outro(result, screen, font["title"], font["basic"], font["color_white"])


if __name__ == "__main__":
    main()
