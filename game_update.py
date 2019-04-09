"""
Game update
"""
from random import randint

import pygame as pg

from laser import laser_hit
from invader import update_invader

def keyboard_input(game_data):
    """
    Handle every keyboard input for the player.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Retrun:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    """

    if game_data["tick"]["keyDelay"] > 0:
        game_data["tick"]["keyDelay"] -= 1

    player_coord = game_data["player"]["hitBox"]
    player_laser = game_data["player"]["lasers"]
    window_width = game_data["Window"][0]

    keys = pg.key.get_pressed()

    # Check if LEFT or RIGHT arrow key is pressed and allow only 10 update per second.
    # A key (pg.K_a) because pygame think the keyboard is qwery.
    if (keys[pg.K_LEFT] or keys[pg.K_a]) and player_coord[0] >= 0:

        player_move(game_data["player"], -2)

    elif (keys[pg.K_RIGHT] or keys[pg.K_d]) and player_coord[0] <= window_width - 25:

        player_move(game_data["player"], 2)


    # Check if SPACE is pressed and allow only 1 update per second (so 1 shoot/s).
    if keys[pg.K_SPACE] and (game_data["tick"]["shooting"] == 0):

        player_laser_position = [player_coord.x + 11, player_coord.y - 8]
        player_laser_rect = pg.Rect(player_laser_position, (2, 7))

        player_laser.append(player_laser_rect)

        game_data["tick"]["shooting"] = 45

    elif game_data["tick"]["shooting"] > 0:

        game_data["tick"]["shooting"] -= 1

    # Cheat mode.
    # Kill all invaders.
    if keys[pg.K_F8]:

        game_data["invader"]["hitBox"] = {
            "mysterySpaceShip": [],
            "topRow": [],
            "middleRow": [],
            "bottomRow": []}

    elif keys[pg.K_F7] and game_data["tick"]["keyDelay"] == 0:

        game_data["tick"]["keyDelay"] = 30

        if game_data["Cheat"]["showHitBox"]:
            game_data["Cheat"]["showHitBox"] = False

        else:
            game_data["Cheat"]["showHitBox"] = True

    return game_data


def player_move(player, offset):
    """
    Spec...
    """

    player["hitBox"][0] += offset

    for i, rect in enumerate(player["rect"]):
        player["rect"][i] = rect.move(offset, 0)


def check_end_game(invader_data, player):
    """
    Check if the game is finished.

    Parameters:
    -----------
    invader_data: Coordinate of the invaders (dict)
    player: Information about the player (dict)

    return:
    -------
    Result: If the game is finished retrun false, true otherwise.
    """

    empty = True

    for row_key, row in invader_data.items():

        if row_key != "mysterySpaceShip" and row != []:
            empty = False

        for invader_pos in row:

            if invader_pos.y + 15 >= 400:
                return False

    if empty or player["life"] <= 0:
        return False

    return True


def update_lasers(invader_lasers, player_lasers):
    """
    Update laser position.

    Parameters:
    -----------
    invadder_lasers: List of laser (Rect) shoot by the invaders (list)
    player_lasers: List of laser (Rect) shoot by the player (list)

    Retrun:
    -------
    invadder_lasers: Updated list of laser (Rect) shoot by the invaders (list)
    player_lasers: Updated list of laser (Rect) shoot by the player (list)
    """

    # Update player lasers.
    for player_laser in player_lasers:
        new_rect = player_laser.move(0, -4)
        list_index = player_lasers.index(player_laser)
        player_lasers[list_index] = new_rect

    # Update invaders lasers.
    for invader_laser in invader_lasers:
        new_rect = invader_laser.move(0, 2)
        list_index = invader_lasers.index(invader_laser)
        invader_lasers[list_index] = new_rect

    return invader_lasers, player_lasers


def mystery_space_ship(game_data):
    """
    Handle the mystery space ship spawn, update and deleting.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    """

    mystery_s_s_hb = game_data["invader"]["hitBox"]["mysterySpaceShip"]
    cooldown = game_data["tick"]["mystery"]
    tick = game_data["tick"]["game"]

    if tick == 0 and cooldown == 0 and mystery_s_s_hb == [] and randint(0, 10) > 9:

        starting_coord = [15, 40]

        mystery_s_s_hb.append(pg.Rect(starting_coord, (24, 18)))

    elif mystery_s_s_hb != []:

        if mystery_s_s_hb[0].x > game_data["Window"][0] - 20:

            del mystery_s_s_hb[0]
            game_data["tick"]["mystery"] = 60

        else:
            mystery_s_s_hb[0] = mystery_s_s_hb[0].move(2, 0)


    elif cooldown > 0:

        game_data["tick"]["mystery"] -= 1

    return game_data


def game_update(game_data):
    """
    Update the game.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    running: If the game is finished (bool)
    """

    # Add one tick to the tick counter and reset at 0 if reach 60.
    game_data["tick"]["game"] += 1

    if game_data["tick"]["game"] >= 60:
        game_data["tick"]["game"] = 0

    # Get keyboard input and update the player.
    game_data = keyboard_input(game_data)

    # Check if laser hit.
    game_data = laser_hit(game_data)

    # Update invaders.
    if game_data["tick"]["game"] == 59:
        game_data = update_invader(game_data, game_data["direction"])

    # Update lasers.
    player_lasers = game_data["player"]["lasers"]
    invader_lasers = game_data["invader"]["lasers"]
    invader_lasers, player_lasers = update_lasers(invader_lasers, player_lasers)

    # Update the mystery space ship.
    game_data = mystery_space_ship(game_data)

    # Check if the game is finished.
    running = check_end_game(game_data["invader"]["hitBox"], game_data["player"])

    return game_data, running
