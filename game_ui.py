"""
Handle all game menu like intro, outro and pause menu.
"""
import pygame as pg
from blit_text import blit_text

def intro(screen, font_title, font_text, font_color):
    """
    Intro screen.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    font: Font used for the text (font)
    font_color: Color for the text (tuple)
    """

    screen_half_width = screen.get_width() / 2
    screen_half_heigth = screen.get_height() / 2

    text_to_print_intro = "SPACE INVADER"
    text_to_print_intro_2 = "Press SPACE to play or\n press ESCAPE to exit."

    blit_text(screen, text_to_print_intro,
              (screen_half_width - 125, screen_half_heigth - 110), font_title, font_color)

    blit_text(screen, text_to_print_intro_2,
              (screen_half_width - 75, screen_half_heigth - 25), font_text, font_color)

    pg.display.update()

    wait_input = True
    while wait_input:

        # Quit the game if the quit boutton is pressed or ESCAPE.
        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if keys[pg.K_ESCAPE] or (event.type == pg.QUIT):
                wait_input = False
                quit()

        # Continue to play when SPACE is pressed.
        if keys[pg.K_SPACE]:
            wait_input = False

def outro(result, screen, font_title_result, font, font_color):
    """
    Outro screen.

    Parameters:
    -----------
    result: Result of the game (str)
    screen: Surface of the window (surface)
    font: Font used for the text (font)
    font_color: Color used for the text (tuple or list)
    """
    # Make the screen black to clear the screen.
    screen.fill((0, 0, 0))

    screen_half_width = screen.get_width() / 2
    screen_half_heigth = screen.get_height() / 2

    text_to_print_end_game = "Press SPACE to try again \nor press ESCAPE to exit."

    blit_text(screen, result,
              (screen_half_width - 70, screen_half_heigth - 110), font_title_result, font_color)
    blit_text(screen, text_to_print_end_game,
              (screen_half_width - 85, screen_half_heigth - 25), font, font_color)

    pg.display.update()
    pg.time.delay(1000)

    wait_input = True
    while wait_input:

        # Quit the game if the quit boutton is pressed or ESCAPE.
        keys = pg.key.get_pressed()

        for event in pg.event.get():

            if keys[pg.K_ESCAPE] or (event.type == pg.QUIT):
                wait_input = False
                quit()

        # Quit if ESCAPE is pressed.
        if keys[pg.K_ESCAPE]:
            wait_input = False
            quit()

        # Continue if SPACE is pressed.
        if keys[pg.K_SPACE]:
            wait_input = False


def pause(screen, font_title, font, font_color):
    """
    Pause the game.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    background: Surface of the screen (surface)
    font_title: Font used to print text title on surface (font)
    font: Font used to print text on surface (font)
    font_color: Color of the font (tuple)
    """
    paused = True
    screen.fill((0, 0, 0))

    screen_half_heigth = screen.get_height() / 2
    screen_half_width = screen.get_width() / 2

    text_title = "Pause"
    text = "Press SPACE to resume"

    blit_text(screen, text_title,
              (screen_half_width - 35, screen_half_heigth - 100), font_title, font_color)
    blit_text(screen, text,
              (screen_half_width - 70, screen_half_heigth - 15), font, font_color)

    pg.display.flip()
    screen.blit(screen, (0, 0))

    while paused:

        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                paused = False
                quit()

        if keys[pg.K_SPACE]:
            paused = False


def hud(screen, clock, font, life, score):
    """
    Display information for the player in game.

    Parameters:
    -----------
    screen: Surface of the window(Surface)
    clock: An object to help track time (Clock)
    font: Dictionnary with differente font and color (dict)
    life: Life of the player (int)
    score: Score of the player (int)
    """
    version = "0.1.1"
    ui_text = "Life: {}    Score: {}    FPS: {}    Ver: {}"
    ui_text_to_print = ui_text.format(life, score, int(clock.get_fps()), version)
    blit_text(screen, ui_text_to_print, (0, 0), font["basic"], font["color_white"])
