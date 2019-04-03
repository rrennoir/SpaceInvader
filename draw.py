"""
Draw module.
"""

from pygame import draw

def draw_invader(screen, invader_rect, color):
    """
    Spec ...
    """

    for row_key, row in invader_rect.items():

        draw_color = color["yellow"]

        if row_key == "mysterySpaceShip":

            draw_color = color["cyan"]

        for rect in row:

            draw.ellipse(screen, draw_color, rect)


def draw_player(screen, player_coord, color):
    """
    Spec...
    """

    # Triangle coordinate.
    player_pos_x = player_coord[0]
    player_pos_y = player_coord[1]

    triangle_coordinate = (
        (player_pos_x, player_pos_y),
        (player_pos_x + 10, player_pos_y - 15),
        (player_pos_x + 20, player_pos_y))

    draw.polygon(screen, color["red"], triangle_coordinate)


def draw_lasers(screen, player_lasers, invader_lasers, color):
    """
    Spec...
    """

    # Draw the player lasers.
    for player_laser_rect in player_lasers:
        draw.rect(screen, color["blue"], player_laser_rect)

    # Draw the _invader lasers.
    for invader_laser_rect in invader_lasers:
        draw.rect(screen, color["green"], invader_laser_rect)



def draw_on_screen(screen, game_data):
    """
    Drawn object on the screen, like player, lasers and invaders.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    dataInvader: Coordinate of the invaders (list)
    player: information about the player (list)
    invader_laser: Coordinate of the lasers shoot by the invaders (list)
    """

    # RGB colors.
    color_rgb = {
        "yellow": (255, 255, 0),
        "red":    (255, 0, 0),
        "blue":   (0, 0, 255),
        "green":  (0, 255, 0),
        "cyan":   (0, 255, 255)}

    color_defence = (
        (50, 0, 50),
        (100, 0, 100),
        (150, 0, 150))

    # Draw defences.
    for defences in game_data["defence"]:

        if defences["life"] > 0:
            draw.rect(screen, color_defence[defences["life"] - 1], defences["rect"])

    # Draw _invader.
    draw_invader(screen, game_data["invader"]["rect"], color_rgb)

    # Draw lasers.
    draw_lasers(screen, game_data["player"]["lasers"], game_data["invader"]["lasers"], color_rgb)

    # Draw player.
    draw_player(screen, game_data["player"]["coordinate"], color_rgb)
