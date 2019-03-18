"""
Blit text on screen and return to the line automaticly.
"""

def blit_text(screen, text, pos, font, color):
    """
    Print text on a surface.

    Parameters:
    -----------
    screen: Surface to print the text on (surface)
    text: text to print (str)
    pos: Top left position to print the text (tuple or list)
    font: Font used for the text (font)
    color: Color of the text (list)
    """

    text = [text.split(' ') for text in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width = 300
    x_pos = pos[0]
    y_pos = pos[1]

    for line in text:

        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()

            # If the word go further
            if x_pos + word_width >= max_width:
                x_pos = pos[0]  # Reset the x_pos.
                y_pos += word_height  # Start on new row.

            # Draw to the screen and pass to the nex x_pos value.
            screen.blit(word_surface, (x_pos, y_pos))
            x_pos += word_width + space

        # Reset x_pos axis and start a new row.
        x_pos = pos[0]
        y_pos += word_height
