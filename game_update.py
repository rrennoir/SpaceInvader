"""
Game update
"""
from random import randint

import pygame as pg

from laser import laser_hit, invader_shoot


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

    player_coord = game_data["player"]["coordinate"]
    player_laser = game_data["player"]["lasers"]

    keys = pg.key.get_pressed()

    # Check if LEFT or RIGHT arrow key is pressed and allow only 10 update per second.
    if keys[pg.K_LEFT] and player_coord[0] >= 2:

        player_coord[0] -= 2
        new_rect = game_data["player"]["rect"].move(-2, 0)
        game_data["player"]["rect"] = new_rect

    elif keys[pg.K_RIGHT] and player_coord[0] <= 280:

        player_coord[0] += 2
        new_rect = game_data["player"]["rect"].move(2, 0)
        game_data["player"]["rect"] = new_rect


    # Check if SPACE is pressed and allow only 1 update per second (so 1 shoot/s).
    if keys[pg.K_SPACE] and (game_data["tick"]["shooting"] == 0):

        player_laser_position = [player_coord[0] + 10, player_coord[1] - 15]
        player_laser_rect = pg.Rect(player_laser_position, (2, 7))

        player_laser.append(player_laser_rect)

        game_data["tick"]["shooting"] = 45

    elif game_data["tick"]["shooting"] > 0:

        game_data["tick"]["shooting"] -= 1

    # Cheat mode.
    # Kill all invaders.
    if keys[pg.K_F8]:

        game_data["invader"]["rect"] = {
            "mysterySpaceShip": [],
            "topRow": [],
            "middleRow": [],
            "bottomRow": []}

        game_data["invader"]["coordinate"] = {
            "mysterySpaceShip": [],
            "topRow": [],
            "middleRow": [],
            "bottomRow": []}

    return game_data


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

            if invader_pos[0] + 15 >= 400:
                return False

    if empty or player["life"] <= 0:
        return False

    return True


def change_direction(invader_data, direction):
    """
    Change the direction of all invader alive every time an invader hit the screen border

    Parameters:
    -----------
    invader_data: Coordinate of the invaders (list)
    direction: Direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)

    Return:
    -------
    direction: Updated Direction in witch way the invader array is going 1 or -1 (int)
    """

    change = False
    for _, row in invader_data.items():

        for invader_pos in row:

            if ((invader_pos[0] >= 280 and direction == 1)
                    or (invader_pos[0] <= 10 and direction == -1)):

                change = True

    if change:
        direction *= -1

    return direction


def update_lasers(invader_lasers, player_lasers):
    """
    Spec...
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


def move_invader(invader_data, direction, shift_down):
    """
    Spec...
    """

    invader_coord = invader_data["coordinate"]
    invader_rect = invader_data["rect"]

    velocity = 10
    if shift_down > 0:
        velocity = 0

    for row_key, row in invader_coord.items():

        if row_key != "mysterySpaceShip":
            for invader_index, _invader in enumerate(row):

                _invader[0] += (velocity * direction)
                _invader[1] += shift_down

                old_invader_rect = invader_rect[row_key][invader_index]

                new_invader_rect = old_invader_rect.move(velocity * direction, shift_down)
                invader_rect[row_key][invader_index] = new_invader_rect

    return invader_data


def update_invader(game_data, direction):
    """
    Update invaders, like position, laser position they have shootted and make them shoot randomly.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Data structure containing most of the information about the game. (dict)
    """

    # Unpack varaible for easier reading.
    invader_list = game_data["invader"]["coordinate"]
    invader_lasers = game_data["invader"]["lasers"]

    # If direction change, shift down
    shift_down = 0
    direction_new = change_direction(invader_list, direction)

    if direction != direction_new:
        shift_down = 7

    # Update _invader position.
    move_invader(game_data["invader"], direction_new, shift_down)

    player_pos_x = game_data["player"]["coordinate"][0]
    invader_lasers = invader_shoot(invader_list, invader_lasers, player_pos_x)

    game_data["direction"] = direction_new

    return game_data


def mystery_space_ship(game_data):
    """
    Spec ...

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    """

    mystery_s_s_coord = game_data["invader"]["coordinate"]["mysterySpaceShip"]
    mystery_s_s_rect = game_data["invader"]["rect"]["mysterySpaceShip"]
    cooldown = game_data["tick"]["mystery"]
    tick = game_data["tick"]["game"]

    if tick == 0 and cooldown == 0 and mystery_s_s_coord == [] and randint(0, 10) > 9:

        starting_coord = [15, 20]

        mystery_s_s_coord.append(starting_coord)
        mystery_s_s_rect.append(pg.Rect(starting_coord, (30, 10)))

    elif mystery_s_s_coord != []:

        if mystery_s_s_coord[0][0] > 280:
            del mystery_s_s_coord[0]
            del mystery_s_s_rect[0]

            game_data["tick"]["mystery"] = 60

        else:
            mystery_s_s_coord[0][0] += 2
            new_rect = mystery_s_s_rect[0].move(2, 0)
            mystery_s_s_rect[0] = new_rect

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
    running = check_end_game(game_data["invader"]["coordinate"], game_data["player"])

    return game_data, running
