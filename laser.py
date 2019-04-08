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
    for row_key, row in invader_list.items():
        if row_key != "mysterySpaceShip":
            for invader_pos in row:

                ref = str(invader_pos[0])
                if ref in first_invader_list and invader_pos[1] > first_invader_list[ref][1]:

                    first_invader_list[ref] = invader_pos

                else:
                    first_invader_list.update({ref: invader_pos})

    for ref, position in first_invader_list.items():

        if player_pos_x - 50 < int(ref) < player_pos_x + 50 and randint(0, 100) > 85:

            invader_laser_rect = Rect(position, (2, 7))
            invader_laser.append(invader_laser_rect.move(6, 17))

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

    for laser_index, invader_laser in enumerate(invader_laser_list):

        # Remove laser out of the screen
        if invader_laser[1] > 400:

            invader_laser_to_delete.append(laser_index)

        # Check if the laser hit something.
        else:

            # Defence.
            for defences in defence_list:

                if (laser_index not in invader_laser_to_delete and defences["life"] > 0
                        and defences["rect"].colliderect(invader_laser)):

                    invader_laser_to_delete.append(laser_index)
                    defences["life"] -= 1

            # Player.
            if (invader_laser not in invader_laser_to_delete
                    and player["hitBox"].colliderect(invader_laser)):

                invader_laser_to_delete.append(laser_index)
                player["life"] -= 1

    # Delete _invader laser who hit.
    for index_to_del in reversed(invader_laser_to_delete):

        del invader_laser_list[index_to_del]


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
    for laser_index, player_laser in enumerate(player_laser_list):

        # Remove laser out of the screen
        if player_laser[1] < 0:

            player_laser_to_delete.append(laser_index)

        # Check if a laser hit something.
        else:

            for defences in defence_list:

                # Check if the laser hasn't already been added to the delete
                #  list and if the player hit the defence wall.
                if (laser_index not in player_laser_to_delete and defences["life"] > 0
                        and defences["rect"].colliderect(player_laser)):

                    # Delete the player laser who hit.
                    player_laser_to_delete.append(laser_index)

            for row_key, invader_row in invader_rect_list.items():

                for invader_index, _invader in enumerate(invader_row):

                    # Check if the invader has been hit.
                    if player_laser.colliderect(_invader):

                        # Add point to the player score.
                        if row_key == "bottomRow":
                            score += 10

                        elif row_key == "middleRow":
                            score += 20

                        elif row_key == "topRow":
                            score += 30

                        else:
                            score += randint(50, 150)

                        # Delete the player laser who hit.
                        player_laser_to_delete.append(laser_index)

                        # Append a dict with invader index to be deleted later.
                        invader_to_delete.append({"row_key": row_key, "index": invader_index})

    # Delete player laser who hit.
    for index_to_del in reversed(player_laser_to_delete):

        del player_laser_list[index_to_del]

    # Delete invader who has been destroyed.
    for invader_deleted in invader_to_delete:

        del invader_rect_list[invader_deleted["row_key"]][invader_deleted["index"]]
        del invader_coord_list[invader_deleted["row_key"]][invader_deleted["index"]]

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
