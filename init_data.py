"""
This module handle the data structure creation for the game.
"""

from pygame import Rect

def create_invader(pixel_size, invader_position):
    """
    Spec...
    """

    invader_matrix = [
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
    ]

    x_pos, y_pos = invader_position
    invader_array = []

    for line in invader_matrix:

        x_pos = invader_position[0]
        for column in line:

            if column == 0:
                x_pos += pixel_size
                continue

            rect = Rect(x_pos, y_pos, pixel_size, pixel_size)
            invader_array.append(rect)

            x_pos += pixel_size

        y_pos += pixel_size

    return invader_array


def invader(screen_width, screen_height):
    """
    Create the dictionnay with all invader information.

    Return:
    -------
    invader_data: Dictionnary with invader information (dict)
    """

    # Create invader data structur.
    invader_data_structure = {
        "hitBox": {},
        "rect": {},
        "lasers": []}

    # Create 2 data structure, one for the position and one for the rect
    # used in the collision systeme using pygame found in the laser module.
    # Could store position and rect in one list but may complexifie even more the program.
    invader_data_structure["hitBox"] = {
        "mysterySpaceShip": [],
        "topRow": [],
        "middleRow": [],
        "bottomRow": []}

    invader_data_structure["rect"] = {
        "mysterySpaceShip": [],
        "topRow": [],
        "middleRow": [],
        "bottomRow": []}

    # Set the size of the pixel for pixel art shape.
    pixel_size = 2

    # Compute the size of the defence based on the size of the pixel
    # and the number of square used for the invader shape.
    invader_width = 12 * pixel_size

    # Compute the void between 2 defences.
    # Screen width - the width of the defences divided by the number of defences + 1.
    void_bt_invader = (screen_width - 11 * invader_width) // 12

    x_pos = void_bt_invader
    y_pos = screen_height - (screen_height - 50)
    offset = void_bt_invader + invader_width

    for row_name in invader_data_structure["hitBox"]:

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
            invader_hit_box = Rect(invader_position, (pixel_size * 12, pixel_size * 9))

            invader_array = create_invader(pixel_size, invader_position)

            # Add to rows to the data structure.
            invader_data_structure["hitBox"][row_name].append(invader_hit_box)
            invader_data_structure["rect"][row_name].append(invader_array)

            # Move 25 pixels to the right.
            x_pos += offset

            if (row_name != "topRow" and
                    len(invader_data_structure["hitBox"][row_name]) == 11):

                x_pos = void_bt_invader
                y_pos += 25

        # Change row.
        y_pos += 25

        # Reset to the left of the screen.
        x_pos = void_bt_invader

    return invader_data_structure


def defence(screen_height, screen_width):
    """
    Initialize the defences datastructure.

    Parameters:
    -----------
    screen_width: Width of the screen (int)
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

    # Set the size of the pixel for pixel art shape.
    pixel_size = 5

    # Compute the size of the defence based on the size of the pixel
    # and the number of square used for the defence shape.
    defence_width = len(matrix[0]) * pixel_size

    # Compute the void between 2 defences.
    # Screen width - the width of the defences divided by the number of defences + 1.
    void_bt_defence = (screen_width - 4 * defence_width) // 5


    x_pos = void_bt_defence
    y_pos = screen_height - 80
    offset = x_pos + defence_width

    defence_array = []
    for i, _ in enumerate(coord):

        coord[i] = [x_pos, y_pos]
        x_pos += offset

        y_coord = coord[i][1]

        # Use the maxtrix to create the defence shape with square.
        for line in matrix:

            x_coord = coord[i][0]
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


def player(screen_height, screen_width):
    """
    Create player data.

    Parameters:
    -----------
    screen_width: Width of the screen (int)
    screen_height: Height of the screen (int)

    Return:
    -------
    player_data: Player information (dict)
    """

    # Player matrix.
    player_matrix = [
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]

    pixel_size = 5

    player_coordinate = [screen_width // 2, screen_height - 30] # center of the screen.
    player_hit_box = Rect(player_coordinate[0], player_coordinate[1], 25, 15)

    player_array = []
    y_pos = player_coordinate[1]

    for line in player_matrix:

        x_pos = player_coordinate[0]

        for column in line:

            if column == 0:

                x_pos += pixel_size
                continue

            player_rect = Rect(x_pos, y_pos, pixel_size, pixel_size)
            player_array.append(player_rect)

            x_pos += pixel_size

        y_pos += pixel_size

    # Create player data.
    player_data = {
        "life": 3,
        "rect": player_array,
        "hitBox": player_hit_box,
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
        "player": player(screen_height, screen_width),

        "invader":  invader(screen_width, screen_height),

        "defence": defence(screen_height, screen_width),

        "score": 0,

        "direction": 1,

        "Cheat": {
            "showHitBox" : False
        },

        "Window" : (screen_width, screen_height),

        "tick": {
            "game": 0,
            "mystery": 0,
            "moving": 0,
            "shooting": 0,
            "keyDelay" : 0}
        }

    return game_data
