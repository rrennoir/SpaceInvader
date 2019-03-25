"""
Game update
"""
from random import randint

import pygame as pg

from laser import laser_hit, invader_shoot


def keyboard_input(game_data, game_tick):
    """
    Handle every keyboard input for the player.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    game_tick: Number of tick elapsed this second, 1 tick = 16ms, 60 tick = 1s (int)
    """

    player_pos = game_data["player"]["coordinate"]
    player_laser = game_data["player"]["lasers"]

    keys = pg.key.get_pressed()

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

    return game_data


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

    empty = True

    for row in invader_data:

        if invader_data[row] == []:
            empty = False

        for invader_pos in invader_data[row]:
            if invader_pos[1][0] + 15 >= 300:
                return False

    if empty or player["life"] <= 0:
        return False

    return True


def change_direction(invader_data, direction):
    """
    Change the direction of all invader alive every time an invader hit the screen border

    Parameters:
    -----------
    invader_data: coordinate of the invaders (list)
    direction: Direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)

    Return:
    -------
    direction: Updated Direction in witch way the invader array is going 1 or -1 (int)
    """

    change = False
    for row in invader_data:
        for sub_row in invader_data[row]:
            for _invader in sub_row:

                invader_pos_x = _invader[0]
                if ((invader_pos_x >= 280 and direction == 1)
                        or (invader_pos_x <= 10 and direction == -1)):

                    change = True

    if change:
        direction *= -1

    return direction


def update_invader(game_data, direction, game_tick):
    """
    Update invaders, like position, laser position they have shootted and make them shoot randomly.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)
    game_tick: Number of tick elapsed this second, 1 tick = 16ms, 60 tick = 1s (int)

    Return:
    -------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1,
                 if set -1 the direction will be reversed (int)
    """

    # Unpack varaible for easier reading.
    invader_list = game_data["invader"]["coordinate"]
    invader_laser = game_data["invader"]["lasers"]
    player_laser = game_data["player"]["lasers"]

    # update _invader position every second aka every 60 frames.
    if game_tick == 60:
        shift_down = 0
        direction_new = change_direction(invader_list, direction)

        # If direction change, shift down
        if direction != direction_new:
            shift_down = 10

        # Update _invader position.
        for row in invader_list:
            for sub_row in invader_list[row]:
                for _invader in sub_row:

                    _invader[0] = _invader[0] + (10 * direction_new)
                    _invader[1] = _invader[1] + shift_down

        player_pos_x = game_data["player"]["coordinate"][0]
        invader_laser = invader_shoot(invader_list, invader_laser, player_pos_x)

        direction = direction_new

    # Update laser position by 2 pixel every frame.
    for laser in player_laser:
        laser[1] -= 2

    for _laser in invader_laser:
        _laser[1] += 2

    return game_data, direction


def game_update(game_data, direction, game_tick):
    """
    Update the game.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)
    game_tick: Number of tick elapsed this second, 1 tick = 16ms, 60 tick = 1s (int)
    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    direction: Updated direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)
    running: If the game is finished (bool)
    """

    # Add one tick to the tick counter and reset at 0 if reach 60.
    if game_tick == 60:
        game_tick = 0

    game_tick += 1

    # Get keyboard input and update the player.
    game_data = keyboard_input(game_data, game_tick)

    # Update lasers and invaders.
    # game_data = laser_hit(game_data)
    game_data, direction = update_invader(game_data, direction, game_tick)

    # Check if the game is finished.
    running = check_end_game(game_data["invader"]["coordinate"], game_data["player"])

    return game_data, direction, running, game_tick
