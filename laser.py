"""
Laser hit systeme.
"""
from random import randint
from pygame import Rect


def invader_shoot(invader_list, invader_laser, player_pos_x):
    """
    Make the invader shoot.

    Parameters:
    -----------
    invader_list: Dictionnary with invader coordinate (dict)
    invader_laser: List of laser position shoot by the invaders (list)
    player_pos_x: Position of the player on the X axis (int)

    Return:
    -------
    invader_laser: List of laser position shoot by the invaders (list)
    """

    first_invader_list = {}
    for row in invader_list:
        if row != "mysterySpaceShip":
            for invader_row in invader_list[row]:
                for invader_pos in invader_row:

                    ref = str(invader_pos[0])
                    if ref in first_invader_list:

                        if invader_pos[1] > first_invader_list[ref][1][1]:
                            first_invader_list[ref][1] = invader_pos

                        if row != first_invader_list[ref][0]:
                            first_invader_list[ref][0] = row

                    else:
                        first_invader_list.update({ref: [row, invader_pos]})

    for pos in first_invader_list:
        if player_pos_x - 50 < int(pos) < player_pos_x + 50:

            if randint(0, 100) > 85:
                invader_pos = first_invader_list[pos][1]
                invader_laser_rect = Rect(invader_pos, (2, 7))
                invader_laser.append(invader_laser_rect)

    return invader_laser


def invader_laser_hit(player, invader_laser_list, defence_list):
    """
    Check if a invader lasers is in the player or defence hit box.

    Parameters:
    -----------
    player: Player information (dict)
    invader_laser_list: List of laser position shoot by the invaders (list)
    defence_list: List of dictionnary defences (list)
    """

    invader_laser_to_delete = []

    for invader_laser in invader_laser_list:

        # Remove laser out of the screen
        if invader_laser[1] > 400:

            invader_laser_to_delete.append(invader_laser)

        # Check if the laser hit something.
        else:

            # Defence.
            for defences in defence_list:

                if defences["life"] > 0 and defences["rect"].colliderect(invader_laser):

                    if invader_laser not in invader_laser_to_delete:
                        invader_laser_to_delete.append(invader_laser)
                        defences["life"] -= 1

            # Player.
            if player["rect"].colliderect(invader_laser):

                if invader_laser not in invader_laser_to_delete:
                    invader_laser_to_delete.append(invader_laser)
                    player["life"] -= 1

    # Delete _invader laser who hit.
    for invader_laser_deleted in invader_laser_to_delete:
        invader_laser_list.pop(invader_laser_list.index(invader_laser_deleted))


def player_laser_hit(player_laser_list, invader_coord_list, invader_rect_list, defence_list, score):
    """
    Find if a laser hit an invader hit box.

    Parameters:
    -----------
    player_laser_list: List of laser position shoot by the player (list)
    invader_coord_list: Dictionnary of invader position (dict)
    invader_rect_list: Dictionnary of invader rect (dict)
    defence_list: List of dictionnary defences (list)
    score: Score of the player (int)

    Return:
    -------
    score: updated score of the player (int)
    """

    # Init the function data.
    player_laser_to_delete = []
    invader_to_delete = []

    # Find if a laser is in an _invader hit box.
    for player_laser in player_laser_list:

        # Remove laser out of the screen
        if player_laser[1] < 0:

            player_laser_to_delete.append(player_laser)

        # Check if a laser hit something.
        else:

            for defences in defence_list:

                if defences["life"] > 0 and defences["rect"].colliderect(player_laser):

                    if player_laser not in player_laser_to_delete:
                        player_laser_to_delete.append(player_laser)

            for invader_row in invader_rect_list:

                if invader_row != "mysterySpaceShip":

                    for sub_row in invader_rect_list[invader_row]:
                        for _invader in sub_row:

                            if player_laser.colliderect(_invader):

                                if invader_row == "bottomRow":
                                    score += 10
                                elif invader_row == "middleRow":
                                    score += 20

                                elif invader_row == "topRow":
                                    score += 30

                                player_laser_to_delete.append(player_laser)
                                invader_to_delete.append([invader_row, sub_row, _invader])

                elif invader_rect_list[invader_row] != []:
                    _invader = invader_rect_list[invader_row][0]
                    if player_laser.colliderect(_invader):
                        score += randint(50, 150)

                        player_laser_to_delete.append(player_laser)
                        invader_to_delete.append([invader_row, 0, _invader])

    # Delete player laser who hit.
    for player_laser_deleted in player_laser_to_delete:

        player_laser_list.pop(player_laser_list.index(player_laser_deleted))

    # Delete _invader destroyed.
    for invader_deleted_info in invader_to_delete:

        row = invader_deleted_info[0]

        if row != "mysterySpaceShip":
            sub_row = invader_rect_list[row].index(invader_deleted_info[1])
            position = invader_deleted_info[2]

            index = invader_rect_list[row][sub_row].index(position)
            invader_rect_list[row][sub_row].pop(index)
            invader_coord_list[row][sub_row].pop(index)

        else:

            invader_rect_list[row].pop(0)
            invader_coord_list[row].pop(0)

    return score


def laser_hit(game_data):
    """
    Check if a laser hit a player or an _invader, update the hitted target and delete the laser.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    """

    player_laser_list = game_data["player"]["lasers"]
    invader_laser_list = game_data["invader"]["lasers"]

    # Lists empty get out of the function.
    if player_laser_list == [] and invader_laser_list == []:
        return game_data

    # Unpack data structure.
    player = game_data["player"]
    invader_data = game_data["invader"]
    defence_list = game_data["defence"]
    score = game_data["score"]

    invader_laser_hit(player, invader_laser_list, defence_list)

    game_data["score"] = player_laser_hit(player_laser_list, invader_data["coordinate"],
                                          invader_data["rect"], defence_list, score)

    return game_data
