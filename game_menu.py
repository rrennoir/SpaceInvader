"""
Handle all game menu like intro, outro and pause menu.
"""
import pygame as pg
from blit_text import blit_text

def intro(screen, font_title, font_text, font_color):
    """
    Intro screen

    Parameters:
    -----------
    screen: (surface)
    font: (font)
    font_color: (tuple)
    """
    text_to_print_intro = "SPACE INVADER"
    text_to_print_intro_2 = "Press SPACE to play or\n press ESCAPE to exit."

    blit_text(screen, text_to_print_intro, (25, 45), font_title, font_color)
    blit_text(screen, text_to_print_intro_2, (65, 125), font_text, font_color)

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
    result: (str)
    screen: (surface)
    font: (font)
    font_color: (tuple or list)
    """
    # Make the screen black to clear the screen.
    screen.fill((0, 0, 0))

    text_to_print_end_game = "Press SPACE to try again \nor press ESCAPE to exit."

    blit_text(screen, result, (80, 80), font_title_result, font_color)
    blit_text(screen, text_to_print_end_game, (65, 125), font, font_color)

    pg.display.update()

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


def pause(screen, background, font, font_color):
    """
    Pause the game.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    background: Surface of the screen (surface)
    font: Font used to print text on surface (font)
    font_color: Color of the font (tuple)
    """
    paused = True
    screen.fill((0, 0, 0))
    text_to_print_pause = "Pause\n press SPACE to resume"

    while paused:

        keys = pg.key.get_pressed()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                paused = False
                quit()

        if keys[pg.K_SPACE]:
            paused = False

        blit_text(screen, text_to_print_pause, (65, 125), font, font_color)
        pg.display.update()
        screen.blit(background, (0, 0))
