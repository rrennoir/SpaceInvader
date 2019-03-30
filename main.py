"""
Little Space Invader game just for fun ;)
"""
import pygame as pg

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
    invader_data_structure = {
        "coordinate": {},
        "rect": {},
        "lasers": []}

    invader_data_structure["coordinate"] = {
        "mysterySpaceShip": [],
        "topRow": [],
        "middleRow": [],
        "bottomRow": []}

    invader_data_structure["rect"] = {
        "mysterySpaceShip": [],
        "topRow": [],
        "middleRow": [],
        "bottomRow": []}

    invader_size = (15, 15)
    x_pos = 15
    y_pos = 50

    for row_name in invader_data_structure["coordinate"]:

        if row_name != "mysterySpaceShip":
            for _row in range(2):

                invader_row = []
                invader_row_rect = []
                for _invader in range(11):

                    invader_position = [x_pos, y_pos]
                    invader_rect = pg.Rect(invader_position, invader_size)

                    invader_row.append(invader_position)
                    invader_row_rect.append(invader_rect)
                    x_pos += 25

                invader_data_structure["coordinate"][row_name].append(invader_row)
                invader_data_structure["rect"][row_name].append(invader_row_rect)
                y_pos += 25  # Change row
                x_pos = 15  # Reset to the left of the screen

    return invader_data_structure


def defence(defence_coordinate):
    """
    initialize the defences datastructure.

    Parameters:
    -----------
    defence_coordinate: List of defences coordinate (list)

    Return:
    -------
    defence_list: List of dictionnary containing all defences data (list)
    """

    defence_size = (10, 10)
    defence_list = []

    for _defence in defence_coordinate:

        defence_rect = pg.Rect(_defence, defence_size)
        defence_info = {"rect": defence_rect, "life": 3}

        defence_list.append(defence_info)

    return defence_list


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


def game(screen, clock, font_title, font):
    """
    Function with the game loop.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    clock: Object who track time (clock)
    font_title: Font used to print text title on surface (font)
    font: Font used to print text on surface (font)

    Return:
    -------
    result: result of the game win or lost (str)
    """

    # Setup game_data.
    direction = 1

    screen_height = screen.get_height()

    defence_coordinate = [
        (50, screen_height - 80),
        (60, screen_height - 80),
        (70, screen_height - 80),

        (125, screen_height - 80),
        (135, screen_height - 80),
        (145, screen_height - 80),

        (200, screen_height - 80),
        (210, screen_height - 80),
        (220, screen_height - 80)]

    player_coordinate = [140, screen_height - 30]
    player_rect = pg.Rect(player_coordinate[0], player_coordinate[1] - 15, 20, 15)

    game_data = {
        "player": {
            "life": 3,
            "coordinate": player_coordinate,
            "rect": player_rect,
            "lasers": []},

        "invader":  invader(),

        "defence": defence(defence_coordinate),

        "score": 0,

        "direction": 1,

        "tick": {
            "game": 0,
            "moving": 0,
            "shooting": 0}}

    font_color = (255, 255, 255)

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
            pause(screen, font_title, font, font_color)

        # Game Update.
        game_data, direction, running = game_update(game_data, direction)

        # Unpack variable from game_data for easier reading.
        player_life = game_data["player"]["life"]
        score = game_data["score"]

        # UI update.
        ui_text = "Life: {}    Score: {}    FPS: {}    WIP"
        ui_text_to_print = ui_text.format(player_life, score, int(clock.get_fps()))
        blit_text(screen, ui_text_to_print, (0, 0), font, font_color)

        # Game Drawn.
        draw(screen, game_data)

        # Display update pygame.
        screen.blit(screen, (0, 0))
        pg.display.flip()

        # Set the game to 60 update per second.
        clock.tick(60)

    # Check If game win or lost.
    if player_life > 0:
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

    # Setup window of 300 by 400 pixel.
    display_size = [300, 400]
    screen = pg.display.set_mode(display_size)

    # Set the windows title
    pg.display.set_caption("Space Invader")

    clock = pg.time.Clock()

    # Start intro screen and wait for player.
    intro(screen, font_title, font_basic, font_color)

    # Game.
    play = True
    while play:

        # Game logic
        result = game(screen, clock, font_title, font_basic)

        # Game terminated draw outro screen
        # and wait for player input to continue or stop.
        outro(result, screen, font_title, font_basic, font_color)


if __name__ == "__main__":
    main()
