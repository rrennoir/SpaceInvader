"""
Laser hit systeme.
"""
from random import randint


def invader_shoot(invader_list, invader_laser, player_pos_x):
    """
    Make the invader shoot.

    Parameters:
    -----------
    invader_list: (dict)
    invader_laser: (list)
    player_pos: (int)

    Return:
    -------
    invader_laser: (list)
    """

    first_invader_list = {}
    for row in invader_list:
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
                invader_laser.append([invader_pos[0], invader_pos[1]])

    return invader_laser


def invader_laser_hit(player, invader_laser_list, defence_list):
    """
    Check if a invader lasers is in the player or defence hit box.

    Parameters:
    -----------
    player: (dict)
    invader_laser_list: (list)
    defence_list: (list)
    """

    player_pos_x = player["coordinate"][0]
    player_pos_y = player["coordinate"][1]

    invader_laser_to_delete = []

    for invader_laser in invader_laser_list:

        # Remove laser out of the screen
        if invader_laser[1] > 400:

            invader_laser_to_delete.append(invader_laser)

        # Check if the laser hit something.
        else:

            laser_pos_x = invader_laser[0]
            laser_pos_y = invader_laser[1]

            # Defence.
            for defences in defence_list:

                if defences["life"] > 0:
                    defences_pos_x = defences["coordinate"][0]
                    defences_pos_y = defences["coordinate"][1]

                    if ((defences_pos_x < laser_pos_x < defences_pos_x + 30)
                            and (defences_pos_y < laser_pos_y < defences_pos_y + 20)):

                        invader_laser_to_delete.append(invader_laser)
                        defences["life"] -= 1

            # Player.
            if ((player_pos_x < laser_pos_x + 7 < player_pos_x + 20)
                    and (player_pos_y < laser_pos_y + 7 < player_pos_y + 15)):

                invader_laser_to_delete.append(invader_laser)
                player["life"] -= 1

    # Delete _invader laser who hit.
    for invader_laser_deleted in invader_laser_to_delete:
        invader_laser_list.pop(invader_laser_list.index(invader_laser_deleted))


def player_laser_hit(player_laser_list, invader_list, defence_list, score):
    """
    Find if a laser hit an invader hit box.

    Parameters:
    -----------
    player_laser_list: List of laser position shoot by the player (list)
    invader_list: List of invader position (list)
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

            laser_pos_x = player_laser[0]
            laser_pos_y = player_laser[1]

            for defences in defence_list:

                if defences["life"] > 0:
                    defences_pos_x = defences["coordinate"][0]
                    defences_pos_y = defences["coordinate"][1]

                    if ((defences_pos_x < laser_pos_x < defences_pos_x + 30)
                            and (defences_pos_y < laser_pos_y < defences_pos_y + 20)):

                        player_laser_to_delete.append(player_laser)

            for invader_row in invader_list:
                for sub_row in invader_list[invader_row]:
                    for _invader in sub_row:

                        invader_pos_x = _invader[0]
                        invader_pos_y = _invader[1]

                        if ((invader_pos_x < laser_pos_x < invader_pos_x + 15)
                                and (invader_pos_y < laser_pos_y < invader_pos_y + 15)):

                            if invader_row == "bottomRow":
                                score += 10
                            elif invader_row == "middleRow":
                                score += 20

                            elif invader_row == "topRow":
                                score += 30

                            player_laser_to_delete.append(player_laser)
                            invader_to_delete.append([invader_row, sub_row, _invader])

    # Delete player laser who hit.
    for player_laser_deleted in player_laser_to_delete:
        player_laser_list.pop(player_laser_list.index(player_laser_deleted))

    # Delete _invader destroyed.
    for invader_deleted_info in invader_to_delete:
        row = invader_deleted_info[0]
        sub_row = invader_list[row].index(invader_deleted_info[1])
        position = invader_deleted_info[2]
        invader_list[row][sub_row].pop(invader_list[row][sub_row].index(position))

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
    invader_list = game_data["invader"]["coordinate"]
    defence_list = game_data["defence"]
    score = game_data["score"]

    invader_laser_hit(player, invader_laser_list, defence_list)

    game_data["score"] = player_laser_hit(player_laser_list, invader_list, defence_list, score)

    return game_data
