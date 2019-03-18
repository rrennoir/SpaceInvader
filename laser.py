"""
Laser hit systeme.
"""

def invader_laser_hit(game_data):
    """
    Check if a _invader lasers is in the player or defence hit box.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    """

    player = game_data["player"]
    player_pos_x = player["coordinate"][0]
    player_pos_y = player["coordinate"][1]
    invader_laser_list = game_data["invaderLaserList"]
    invader_laser_to_delete = []

    for invader_laser in invader_laser_list:

        laser_pos_x = invader_laser[0]
        laser_pos_y = invader_laser[1]

        # Defence.
        for defences in game_data["defence"]:

            if defences["life"] > 0:
                defences_pos_x = defences["coordinate"][0]
                defences_pos_y = defences["coordinate"][1]

                if ((laser_pos_x >= defences_pos_x
                     and laser_pos_x <= defences_pos_x + 30)
                        and (laser_pos_y + 20 >= defences_pos_y
                             and laser_pos_y + 20 <= defences_pos_y + 20)):

                    invader_laser_to_delete.append(invader_laser)
                    defences["life"] -= 1

        # Player.
        if ((laser_pos_x >= player_pos_x
             and laser_pos_x <= player_pos_x + 20)
                and (laser_pos_y + 7 >= player_pos_y
                     and laser_pos_y + 7 <= player_pos_y + 15)):

            invader_laser_to_delete.append(invader_laser)
            player["life"] -= 1

    # Delete _invader laser who hit.
    for invader_laser_deleted in invader_laser_to_delete:
        invader_laser_list.pop(invader_laser_list.index(invader_laser_deleted))

    return game_data


def player_laser_hit(game_data):
    """
    Find if a laser hit an invader hit box.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    game_data: Updated data structure containing most of the information about the game. (dict)
    """
    player = game_data["player"]
    player_laser_list = player["lasers"]
    invader_list = game_data["invader_data"]

    # Init the function data.
    player_laser_to_delete = []
    invader_to_delete = []

    # Find if a laser is in an _invader hit box.
    for player_laser in player_laser_list:

        laser_pos_x = player_laser[0]
        laser_pos_y = player_laser[1]

        for defences in game_data["defence"]:

            if defences["life"] > 0:
                defences_pos_x = defences["coordinate"][0]
                defences_pos_y = defences["coordinate"][1]

                if ((laser_pos_x >= defences_pos_x
                     and laser_pos_x <= defences_pos_x + 30)
                        and (laser_pos_y + 20 >= defences_pos_y
                             and laser_pos_y + 20 <= defences_pos_y + 20)):

                    player_laser_to_delete.append(player_laser)

        for _invader in invader_list:

            invader_pos_x = _invader[0]
            invader_pos_y = _invader[1]

            if ((laser_pos_x >= invader_pos_x
                 and laser_pos_x <= invader_pos_x + 15)
                    and (laser_pos_y <= invader_pos_y + 15
                         and laser_pos_y >= invader_pos_y)):

                game_data["score"] += 10
                player_laser_to_delete.append(player_laser)
                invader_to_delete.append(_invader)

    # Delete player laser who hit.
    for player_laser_deleted in player_laser_to_delete:
        player_laser_list.pop(player_laser_list.index(player_laser_deleted))

    # Delete _invader destroyed.
    for invader_deleted in invader_to_delete:
        invader_list.pop(invader_list.index(invader_deleted))

    return game_data


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
    invader_list = game_data["invader_data"]

    # Lists empty get out of the function.
    if player_laser_list == [] and invader_list == []:
        return game_data

    game_data = invader_laser_hit(game_data)

    game_data = player_laser_hit(game_data)

    return game_data
