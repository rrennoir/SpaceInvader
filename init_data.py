"""
This module handle the data structure creation for the game.
"""

from pygame import Rect

def invader():
    """
    Create the dictionnay with all invader information.

    Return:
    -------
    invader_data: Dictionnary with invader information (dict)
    """

    # Create invader data structur.
    invader_data_structure = {
        "coordinate": {},
        "rect": {},
        "lasers": []}

    # Create 2 data structure, one for the position and one for the rect
    # used in the collision systeme using pygame found in the laser module.
    # Could store position and rect in one list but may complexifie even more the program.
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

    # Setup starting position for the x and y.
    x_pos = 15
    y_pos = 50

    for row_name in invader_data_structure["coordinate"]:

        # No invader to create for mystery space ship at the start,
        # only 11 for the top row, 22 other wise
        if row_name == "mysterySpaceShip":
            invader_per_row = 0

        elif row_name == "topRow":
            invader_per_row = 11

        else:
            invader_per_row = 22

        # Based on the row name (top, middle or bottom) there is 1 or 2 row containing 11 column.
        # So 1 row for top, 2 for middle and bottom each, 5 in total.
        # One row contain 11 invaders separeted by 25 pixel on the
        # X axis (from one invader left side to the next invader left side NOT the center).
        # For the Y axis the invaders are separeted by 15 pixel (from one
        # invader top to the next invader top NOT the center)

        for _invader in range(invader_per_row):

            # Create the invader coordinate and rect.
            invader_position = [x_pos, y_pos]
            invader_rect = Rect(invader_position, invader_size)

            # Add to rows to the data structure.
            invader_data_structure["coordinate"][row_name].append(invader_position)
            invader_data_structure["rect"][row_name].append(invader_rect)

            # Move 25 pixels to the right.
            x_pos += 25

            if (row_name != "topRow" and
                    len(invader_data_structure["coordinate"][row_name]) == 11):

                x_pos = 15
                y_pos += 25

        # Change row.
        y_pos += 25

        # Reset to the left of the screen.
        x_pos = 15

    return invader_data_structure


def defence(screen_height, screen_width):
    """
    Initialize the defences datastructure.

    Parameters:
    -----------
    screen_height: Height of the screen (int)

    Return:
    -------
    defence_list: List of dictionnary containing all defences data (list)
    """

    # coord
    coord = [
        [],
        [],
        [],
        [],
    ]

    # Defence coord matrix
    matrix = [
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1]
    ]

    offset = screen_width // 4
    x_pos = offset // 2
    y_pos = screen_height - 80
    pixel_size = 5

    defence_array = []
    for i, _ in enumerate(coord):

        coord[i] = [x_pos, y_pos]
        x_pos += offset

        y_coord = coord[i][1] - pixel_size * 2

        # Use the maxtrix to create the defence shape with square.
        for line in matrix:

            x_coord = coord[i][0] - pixel_size * 2
            for column in line:

                # If the column = 0, offset the x axis and pass to the next column.
                if column == 0:

                    x_coord += pixel_size
                    continue

                # Create the rectangle, create a dictionnary and add the dictionnary to the array.
                defence_rect = Rect((x_coord, y_coord), (pixel_size, pixel_size))
                defence_array.append({"rect": defence_rect, "life": 3})

                # Offset the x axis.
                x_coord += pixel_size

            y_coord += pixel_size

    return defence_array


def player(screen_height):
    """
    Create player data.

    Parameters:
    -----------
    screen_height: Height of the screen (int)

    Return:
    -------
    player_data: Player information (dict)
    """

    # Setup player coordinate and rect.
    player_coordinate = [140, screen_height - 30]
    player_rect = Rect(player_coordinate[0], player_coordinate[1] - 15, 20, 15)

    # Create player data.
    player_data = {
        "life": 3,
        "coordinate": player_coordinate,
        "rect": player_rect,
        "lasers": []}

    return player_data


def setup_data(screen_height, screen_width):
    """
    Setup game_data.

    Parameters:
    -----------
    screen_height: Height of the screen (int)

    Return:
    -------
    game_data: Data sturcture containing all informations needed for the game (dict)
    """

    # Create game data.
    game_data = {
        "player": player(screen_height),

        "invader":  invader(),

        "defence": defence(screen_height, screen_width),

        "score": 0,

        "direction": 1,

        "tick": {
            "game": 0,
            "mystery": 0,
            "moving": 0,
            "shooting": 0}}

    return game_data
