"""
Little Space Invader game just for fun ;)
"""
import pygame as pg
from pygame import surface # for pylint bug only, this is necessary.

from game_update import game_update
from blit_text import blit_text
from game_menu import intro, outro, pause


def invader():
    """
    Setup all invader position into a list of coordinate.

    Return:
    -------
    invader_data: list of coordinate (list)
    """

    # Create invader data structur.
    invader_data = []
    for j in range(3):
        for invader_pos in range(10):

            # offset the X axis by 25 pixel to center the invader platoon
            # and offset the Y axis by 50 pixel to let place for the UI on the top.
            invader_position = [(invader_pos * 25) + 25, j * 25 + 50]

            invader_data.append(invader_position)

    return invader_data


def draw(screen, game_data):
    """
    Drawn object on the screen, like player, lasers and invaders.

    Parameters:
    -----------
    screen: surface of the window (surface)
    dataInvader: coordinate of the invaders (list)
    player: information about the player (list)
    invader_laser: coordinate of the lasers shoot by the invaders (list)
    """

    # RGB colors.
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    color_defence = (
        (50, 0, 50),
        (100, 0, 100),
        (150, 0, 150))

    # Draw _invader.
    for invader_position in game_data["invader"]["coordinate"]:
        invader_rect = pg.Rect(invader_position, (15, 15))
        pg.draw.ellipse(screen, yellow, invader_rect)

    # Draw the player lasers.
    for player_laser_position in game_data["player"]["lasers"]:
        player_laser_rect = pg.Rect(player_laser_position, (2, 7))
        pg.draw.rect(screen, blue, player_laser_rect)

    # Draw the _invader lasers.
    for invader_laser_position in game_data["invader"]["lasers"]:
        invader_laser_rect = pg.Rect(invader_laser_position, (2, 7))
        pg.draw.rect(screen, green, invader_laser_rect)

    # Draw defences.
    for defences in game_data["defence"]:

        if defences["life"] > 0:
            defences_rect = pg.Rect(defences["coordinate"], (30, 20))
            pg.draw.rect(screen, color_defence[defences["life"] - 1], defences_rect)

    # Draw player.
    player_pos_x = game_data["player"]["coordinate"][0]
    player_pos_y = game_data["player"]["coordinate"][1]

    triangle_coordinate = (
        (player_pos_x, player_pos_y),
        (player_pos_x + 10, player_pos_y - 15),
        (player_pos_x + 20, player_pos_y))

    pg.draw.polygon(screen, red, triangle_coordinate)


def game(screen, background, clock, font_title, font):
    """
    Function with the game loop.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    background: Surface of the screen (surface)
    clock: Object who track time (clock)
    font_title: Font used to print text title on surface (font)
    font: Font used to print text on surface (font)

    Return:
    -------
    resulte: resulte of the game win or lost (str)
    """

    # Setup game_data.
    direction = 1
    game_tick = 0

    game_data = {
        "player": {"life": 3, "coordinate": [150, 270], "lasers": []},
        "invader":  {"coordinate": invader(), "lasers": []},
        "defence": [
            {"coordinate": (60, 220), "life": 3},
            {"coordinate": (135, 220), "life": 3},
            {"coordinate": (210, 220), "life": 3}],
        "score": 0}

    font_color = (255, 255, 255)

    runnning = True
    while runnning:

        # Set the game to 60 update per second.
        clock.tick(60)

        # Quit the game if the quit boutton is pressed.
        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                runnning = False
                quit()

        if keys[pg.K_ESCAPE]:
            pause(screen, background, font_title, font, font_color)

        # Unpack variable from game_data for easier reading.
        player_life = game_data["player"]["life"]
        score = game_data["score"]

        # Game Update.
        game_data, direction, runnning, game_tick = game_update(game_data, direction, game_tick)

        # UI update.
        ui_text_to_print = "Life: {}    Score: {}".format(player_life, score)
        blit_text(screen, ui_text_to_print, (0, 0), font, font_color)

        # Game Drawn.
        draw(screen, game_data)

        # Display update pygame.
        pg.display.update()
        screen.blit(background, (0, 0))

    # Check If game win or lost.
    if game_data["invader"]["coordinate"] == [] and player_life > 0:
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
    font_basic = pg.font.SysFont("Comic Sans MS", 15)
    font_title = pg.font.SysFont("Comic Sans MS", 30)
    font_color = (255, 255, 255)

    # Setup window and game clock.
    display_size = [300, 300]
    screen = pg.display.set_mode(display_size)
    # import surface separetly to remove "too many positional arguments for lambda call" bug.
    background = surface.Surface(screen.get_size())
    clock = pg.time.Clock()

    # Start intro screen and wait for player.
    intro(screen, font_title, font_basic, font_color)

    # Game.
    play = True
    while play:

        # Game logic
        result = game(screen, background, clock, font_title, font_basic)

        # Game terminated draw outro screen
        # and wait for player input to continue or stop.
        outro(result, screen, font_title, font_basic, font_color)


if __name__ == "__main__":
    main()
