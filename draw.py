"""
Draw module.
"""

from pygame import draw

from invader import create_invader_shape


def draw_invader(screen, invader_hit_box, color, hit_box):
    """
    Draw invader on the screen.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    invader_hit_box: List of Rect for the invader hit box (list)
    color: Dictionnary of RGB color (dict)
    hit_box: Setting if the hit box must be show (bool)
    """

    pixel_size = 2

    for row_key, row in invader_hit_box.items():

        draw_color = color["yellow"]

        if row_key == "mysterySpaceShip":

            draw_color = color["cyan"]

        for rect_hit_box in row:

            if hit_box:
                draw.rect(screen, (255, 50, 255), rect_hit_box, 1)

            invader_array = create_invader_shape(pixel_size, rect_hit_box.topleft)
            for rect in invader_array:

                draw.rect(screen, draw_color, rect)


def draw_player(screen, player, color, hit_box):
    """
    Draw player on the screen.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    player: Player data (dict)
    color: Dictionnary of RGB color (dict)
    hit_box: Setting if the hit box must be show (bool)
    """

    player_rect = player["rect"]
    for rect in player_rect:
        draw.rect(screen, color["red"], rect)

    if hit_box:
        draw.rect(screen, (50, 255, 255), player["hitBox"], 1)


def draw_lasers(screen, player_lasers, invader_lasers, color, hit_box):
    """
    Draw laser on the screen.

    Parameters:
    -----------
    screen: Surface of the window (Surface)
    player_lasers: List of rect of the player laser (Rect)
    invader_lasers: List of rect of the invader laser (Rect)
    color: Dictionnary of RGB color (dict)
    hit_box: Setting if the hit box must be show (bool)
    """

    # Draw the player lasers.
    for player_laser_rect in player_lasers:
        draw.rect(screen, color["blue"], player_laser_rect)

        if hit_box:
            draw.rect(screen, (50, 255, 255), player_laser_rect, 1)

    # Draw the _invader lasers.
    for invader_laser_rect in invader_lasers:
        draw.rect(screen, color["green"], invader_laser_rect)

        if hit_box:
            draw.rect(screen, (255, 255, 50), invader_laser_rect, 1)


def draw_on_screen(screen, game_data):
    """
    Drawn object on the screen, like player, lasers, defences and invaders.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    game_data: Data structure containing most of the information about the game. (dict)
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

    hit_box = game_data["Cheat"]["showHitBox"]

    # Draw defences.
    for defences in game_data["defence"]:

        if defences["life"] > 0:
            draw.rect(screen, color_defence[defences["life"] - 1], defences["rect"])

            if hit_box:
                draw.rect(screen, (255, 255, 255), defences["rect"], 1)

    # Draw _invader.
    invader = game_data["invader"]
    draw_invader(screen, invader["hitBox"], color_rgb, hit_box)

    # Draw lasers.
    draw_lasers(screen, game_data["player"]["lasers"],
                game_data["invader"]["lasers"], color_rgb, hit_box)

    # Draw player.
    draw_player(screen, game_data["player"], color_rgb, hit_box)
