"""
Game update
"""
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

        game_data["tick"]["shooting"] = 60

    elif game_data["tick"]["shooting"] > 0:

        game_data["tick"]["shooting"] -= 1

    # Cheat mode.
    # Kill all invaders.
    if keys[pg.K_F8]:

        game_data["invader"]["coordinate"] = {
            "mysterySpaceShip": [],
            "topRow": [[], []],
            "middleRow": [[], []],
            "bottomRow": [[], []]}

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

        if invader_data[row] != [[], []] and row != "mysterySpaceShip":
            empty = False

        for sub_row in invader_data[row]:
            for invader_pos in sub_row:
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


def update_invader(game_data, direction):
    """
    Update invaders, like position, laser position they have shootted and make them shoot randomly.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)

    Return:
    -------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1,
                 if set -1 the direction will be reversed (int)
    """

    # Unpack varaible for easier reading.
    invader_list = game_data["invader"]["coordinate"]
    invader_lasers = game_data["invader"]["lasers"]
    player_lasers = game_data["player"]["lasers"]

    # update _invader position every second aka every 60 frames.
    if game_data["tick"]["game"] == 60:
        shift_down = 0
        direction_new = change_direction(invader_list, direction)

        # If direction change, shift down
        if direction != direction_new:
            shift_down = 10

        # Update _invader position.
        for row in invader_list:
            for sub_row in invader_list[row]:
                for _invader in sub_row:

                    _invader[0] += (10 * direction_new)
                    _invader[1] += shift_down

                    sub_row_index = invader_list[row].index(sub_row)
                    invader_index = sub_row.index(_invader)
                    new_rect = game_data["invader"]["rect"][row][sub_row_index][invader_index].move(10 * direction_new, shift_down)
                    game_data["invader"]["rect"][row][sub_row_index][invader_index] = new_rect

        player_pos_x = game_data["player"]["coordinate"][0]
        invader_laser = invader_shoot(invader_list, invader_lasers, player_pos_x)

        direction = direction_new

    # Update laser position by 2 pixel every frame.
    for player_laser in player_lasers:
        new_rect = player_laser.move(0, -2)
        list_index = player_lasers.index(player_laser)
        player_lasers[list_index] = new_rect

    for invader_laser in invader_lasers:
        new_rect = invader_laser.move(0, 2)
        list_index = invader_lasers.index(invader_laser)
        invader_lasers[list_index] = new_rect

    return game_data, direction


def game_update(game_data, direction):
    """
    Update the game.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    direction: Updated direction in witch way the invader array is going 1 or -1,
                if set -1 the direction will be reversed (int)
    running: If the game is finished (bool)
    """

    # Add one tick to the tick counter and reset at 0 if reach 60.
    if game_data["tick"]["game"] == 60:
        game_data["tick"]["game"] = 0

    game_data["tick"]["game"] += 1

    # Get keyboard input and update the player.
    game_data = keyboard_input(game_data)

    # Update lasers and invaders.
    game_data = laser_hit(game_data)
    game_data, direction = update_invader(game_data, direction)

    # Check if the game is finished.
    running = check_end_game(game_data["invader"]["coordinate"], game_data["player"])

    return game_data, direction, running
