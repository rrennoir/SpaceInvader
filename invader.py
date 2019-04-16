"""
Contain invader function.
"""

from pygame import Rect

from laser import invader_shoot


def create_invader_shape(pixel_size, invader_position):
    """
    Create the invader pixel art in function of the pixel size.

    Parametes:
    ----------
    pixel_size: Size of the pixel (int)
    invader_position: Position (top left corner) of the invader (list)

    Return:
    -------
    invader_array: list of rectangle to create the shape on the screen. (list)
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

            if ((invader_pos.x >= 466 and direction == 1)
                    or (invader_pos.x <= 10 and direction == -1)):

                change = True

    if change:
        direction *= -1

    return direction


def move_invader(invader_hit_box, direction, shift_down):
    """
    Move the invaders.

    Parameters:
    -----------
    invader_hit_box: Dictionnary containing all invader hit box (dict)
    direction: Direction of the invaders, 1 or -1 (int)
    shift_down: Number of pixel to increase on the Y axis, 0 or 7 (int)

    Return:
    -------
    invader_data: Updated dictionnary containing all invader information (dict)
    """

    velocity = 10
    if shift_down > 0:
        velocity = 0

    for row_key, row in invader_hit_box.items():

        if row_key != "mysterySpaceShip":
            for index, _invader in enumerate(row):

                invader_hit_box[row_key][index] = _invader.move(velocity * direction, shift_down)


def update_invader(game_data, direction):
    """
    Update invaders, like position, laser position they have shootted and make them shoot randomly.

    Parameters:
    -----------
    game_data: Data structure containing most of the information about the game. (dict)
    direction: Direction of the invaders, 1 or -1 (int)

    Return:
    -------
    game_data: Data structure containing most of the information about the game. (dict)
    """

    # Unpack varaible for easier reading.
    invader_list = game_data["invader"]["hitBox"]
    invader_lasers = game_data["invader"]["lasers"]

    # If direction change, shift down
    shift_down = 0
    direction_new = change_direction(invader_list, direction)

    if direction != direction_new:
        shift_down = 7

    # Update _invader position.
    move_invader(game_data["invader"]["hitBox"], direction_new, shift_down)

    player_pos_x = game_data["player"]["hitBox"].x
    invader_lasers = invader_shoot(invader_list, invader_lasers, player_pos_x)

    game_data["direction"] = direction_new

    return game_data
