"""
Little Space Invader game just for fun ;)
"""
from random import randint

import pygame as pg
from pygame import surface # for pylint bug only, this is necessary.

from laser import laser_hit
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
    for invader_position in game_data["invader_data"]:
        invader_rect = pg.Rect(invader_position, (15, 15))
        pg.draw.ellipse(screen, yellow, invader_rect)

    # Draw the player lasers.
    for player_laser_position in game_data["player"]["lasers"]:
        player_laser_rect = pg.Rect(player_laser_position, (2, 7))
        pg.draw.rect(screen, blue, player_laser_rect)

    # Draw the _invader lasers.
    for invader_laser_position in game_data["invaderLaserList"]:
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


def update_invader(game_data, direction, game_tick):
    """
    Update invaders, like position, laser position they have shootted and make them shoot randomly.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the _invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)
    game_tick: Number of tick elapsed this second, 1 tick = 16ms, 60 tick = 1s (int)

    Return:
    -------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the _invader array is going 1 or -1,
                 if set -1 the direction will be reversed (int)
    """

    # Check if lasers hit something.
    game_data = laser_hit(game_data)

    # Unpack varaible for easier reading.
    invader_list = game_data["invader_data"]
    invader_laser = game_data["invaderLaserList"]
    player_laser = game_data["player"]["lasers"]

    # update _invader position every second aka every 60 frames.
    if game_tick == 60:
        shift_down = 0
        direction_new = change_direction(invader_list, direction)

        # If direction change, shift down
        if direction != direction_new:
            shift_down = 10

        # Update _invader position.
        for _invader in invader_list:

            _invader[0] = _invader[0] + (10 * direction_new)
            _invader[1] = _invader[1] + shift_down

            invader_pos_x = _invader[0]
            player_pos_x = game_data["player"]["coordinate"][0]

            # if player is in the area of attack shoot a laser (20% chance).
            if (invader_pos_x - 50 < player_pos_x) and (invader_pos_x + 65 > player_pos_x):
                if randint(0, 100) > 80:
                    invader_laser.append([_invader[0], _invader[1]])

        direction = direction_new

    # Update laser position by 2 pixel every frame.
    for laser in player_laser:
        laser[1] -= 2

    for invader_laser in invader_laser:
        invader_laser[1] += 2

    return game_data, direction


def change_direction(invader_data, direction):
    """
    Change the direction of all _invader alive every time an _invader hit the screen border

    Parameters:
    -----------
    invader_data: coordinate of the invaders (list)
    direction: Direction in witch way the _invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)

    Return:
    -------
    direction: Updated Direction in witch way the _invader array is going 1 or -1 (int)
    """

    change = False
    for _invader in invader_data:

        invader_pos_x = _invader[0]
        if (invader_pos_x >= 280 and direction == 1) or (invader_pos_x <= 10 and direction == -1):
            change = True

    if change:
        direction *= -1

    return direction


def check_end_game(invader_data, player):
    """
    Check if the game is finished.

    Parameters:
    -----------
    invader_data: coordinate of the invaders (list)
    player: Information about the player (dict)

    return:
    -------
    Result: if the game is finished retrun false, true otherwise.
    """

    if invader_data == [] or player["life"] <= 0:
        return False

    for invader_pos in invader_data:
        if invader_pos[1] + 15 >= 300:
            return False

    return True


def game(screen, background, clock, font):
    """
    Function with the game loop.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    background: Surface of the screen (surface)
    clock: Object who track time (clock)
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
        "invader_data":  invader(),
        "invaderLaserList": [],
        "defence": [
            {"coordinate": (60, 220), "life": 3},
            {"coordinate": (135, 220), "life": 3},
            {"coordinate": (210, 220), "life": 3}],
        "score": 0}

    font_color = (255, 255, 255)

    runnning = True
    while runnning:

        # Set the game to 60 update per second and count game_tick
        clock.tick(60)
        if game_tick == 60:
            game_tick = 0
        game_tick += 1

        # Quit the game if the quit boutton is pressed.
        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                runnning = False
                quit()

        if keys[pg.K_ESCAPE]:
            pause(screen, background, font, font_color)

        # Unpack variable from game_data for easier reading.
        player_pos = game_data["player"]["coordinate"]
        player_laser = game_data["player"]["lasers"]
        player_life = game_data["player"]["life"]
        score = game_data["score"]

        # Check if LEFT or RIGHT arrow key is pressed and allow only 10 update per second.
        if keys[pg.K_LEFT] and (game_tick % 6):

            player_pos[0] -= 2
            if player_pos[0] <= 0:
                player_pos[0] = 0

        if keys[pg.K_RIGHT] and (game_tick % 6):

            player_pos[0] += 2
            if player_pos[0] >= 280:
                player_pos[0] = 280

        # Check if SPACE is pressed and allow only 5 update per second (so 5 shoot/s).
        if keys[pg.K_SPACE] and (game_tick % 12 == 0):

            player_laser.append([player_pos[0] + 10, player_pos[1] - 15])

        # Game Update.
        runnning = check_end_game(game_data["invader_data"], game_data["player"])
        game_data, direction = update_invader(game_data, direction, game_tick)

        # UI update.
        ui_text_to_print = "Life: {}    Score: {}".format(player_life, score)
        blit_text(screen, ui_text_to_print, (0, 0), font, font_color)

        # Game Drawn.
        draw(screen, game_data)

        # Display update pygame.
        pg.display.update()
        screen.blit(background, (0, 0))

    # Check If game win or lost.
    if game_data["invader_data"] == [] and player_life > 0:
        return "Game Win"

    return "Game Lost"


def main():
    """
    Main function who manage everything.
    """

    pg.init()

    # Setup the font.
    font = pg.font.SysFont("Comic Sans MS", 15)
    font_title = pg.font.SysFont("Comic Sans MS", 30)
    font_color = (255, 255, 255)

    # Setup window and game clock.
    display_size = [300, 300]
    screen = pg.display.set_mode(display_size)
    # import surface separetly to remove "too many positional arguments for lambda call" bug.
    background = surface.Surface(screen.get_size())
    clock = pg.time.Clock()

    # Start intro screen and wait for player.
    intro(screen, font_title, font, font_color)

    play = True
    while play:

        result = game(screen, background, clock, font)

        outro(result, screen, font_title, font, font_color)


if __name__ == "__main__":
    main()
