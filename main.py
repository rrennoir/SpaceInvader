"""
Little Space Invader game just for fun ;)
"""
import pygame as pg

from init_data import setup_data
from game_update import game_update
from game_ui import intro, outro, pause, hud


def draw(screen, game_data):
    """
    Drawn object on the screen, like player, lasers and invaders.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    dataInvader: Coordinate of the invaders (list)
    player: information about the player (list)
    invader_laser: Coordinate of the lasers shoot by the invaders (list)
    """

    # RGB colors.
    rgb = {
        "yellow": (255, 255, 0),
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0)}

    color_defence = (
        (50, 0, 50),
        (100, 0, 100),
        (150, 0, 150))

    # Draw _invader.
    invader_coord = game_data["invader"]["rect"]
    for row_name in invader_coord:
        for invader_row in invader_coord[row_name]:
            for invader_rect in invader_row:
                pg.draw.ellipse(screen, rgb["yellow"], invader_rect)

    # Draw the player lasers.
    for player_laser_rect in game_data["player"]["lasers"]:
        pg.draw.rect(screen, rgb["blue"], player_laser_rect)

    # Draw the _invader lasers.
    for invader_laser_rect in game_data["invader"]["lasers"]:
        pg.draw.rect(screen, rgb["green"], invader_laser_rect)

    # Draw defences.
    for defences in game_data["defence"]:

        if defences["life"] > 0:
            pg.draw.rect(screen, color_defence[defences["life"] - 1], defences["rect"])

    # Draw player.
    # Triangle coordinate.
    player_pos_x = game_data["player"]["coordinate"][0]
    player_pos_y = game_data["player"]["coordinate"][1]

    triangle_coordinate = (
        (player_pos_x, player_pos_y),
        (player_pos_x + 10, player_pos_y - 15),
        (player_pos_x + 20, player_pos_y))

    pg.draw.polygon(screen, rgb["red"], triangle_coordinate)


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
    game_data = setup_data(screen.get_height())
    running = True
    while running:

        # Clear the screen from previous frame.
        screen.fill((0, 0, 0))

        # Quit the game if the quit button is pressed.
        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False
                quit()

        # Pause the game is ESCAPE is pressed.
        if keys[pg.K_ESCAPE]:
            pause(screen, font["title"], font["basic"], font["color_white"])

        # Game Update.
        game_data, running = game_update(game_data)

        # UI update.
        hud(screen, clock, font, game_data["player"]["life"], game_data["score"])

        # Game Drawn.
        draw(screen, game_data)

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
