"""
This module handle the data structure creation for the game.
"""

from pygame import Rect

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
                    invader_rect = Rect(invader_position, invader_size)

                    invader_row.append(invader_position)
                    invader_row_rect.append(invader_rect)
                    x_pos += 25

                invader_data_structure["coordinate"][row_name].append(invader_row)
                invader_data_structure["rect"][row_name].append(invader_row_rect)
                y_pos += 25  # Change row
                x_pos = 15  # Reset to the left of the screen

    return invader_data_structure


def defence(screen_height):
    """
    initialize the defences datastructure.

    Parameters:
    -----------
    screen_height: height of the screen (int)

    Return:
    -------
    defence_list: List of dictionnary containing all defences data (list)
    """

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

    defence_size = (10, 10)
    defence_list = []

    for _defence in defence_coordinate:

        defence_rect = Rect(_defence, defence_size)
        defence_info = {"rect": defence_rect, "life": 3}

        defence_list.append(defence_info)

    return defence_list

def player(screen_height):
    """
    Create player data.
    Parameters:
    -----------
    screen_height: (int)

    Return:
    -------
    player_data: (dict)
    """
    player_coordinate = [140, screen_height - 30]
    player_rect = Rect(player_coordinate[0], player_coordinate[1] - 15, 20, 15)

    player_data = {
        "life": 3,
        "coordinate": player_coordinate,
        "rect": player_rect,
        "lasers": []}

    return player_data


def setup_data(screen_height):
    """
    Setup game_data.

    Parameters:
    -----------
    screen_height: Height of the screen (int)

    Return:
    -------
    game_data: Data sturcture containing all informations needed for the game (dict)
    """

    game_data = {
        "player": player(screen_height),

        "invader":  invader(),

        "defence": defence(screen_height),

        "score": 0,

        "direction": 1,

        "tick": {
            "game": 0,
            "moving": 0,
            "shooting": 0}}

    return game_data
