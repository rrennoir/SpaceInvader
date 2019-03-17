import pygame as pg
import pygame.freetype
from random import randint


def invader():
    """
    Setup all invader position into a list of coordinate.

    Return:
    -------
    invaderData: list of coordinate (list)
    """

    # Create invader data structur.
    invaderData = []
    for j in range(3):
        for invader in range(10):

            # offset the X axis by 25 pixel to center the invader platoon and offset the Y axis by 50 pixel to let place for the UI on the top.
            invaderPosition = [(invader * 25) + 25, j * 25 + 50] 

            invaderData.append(invaderPosition)

    return invaderData


def draw(screen, gameData):
    """
    Drawn object on the screen, like player, lasers and invaders.

    Parameters:
    -----------
    screen: surface of the window (surface)
    dataInvader: coordinate of the invaders (list)
    player: information about the player (list)
    invaderLaser: coordinate of the lasers shoot by the invaders (list)
    """

    # Sizes.
    sizeInvater = (15, 15)
    sizeLaser = (2, 7)
    sizeDefence = (30, 20)

    # RGB colors.
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    colorDefence = (
        (50, 0, 50),
        (100, 0, 100),
        (150, 0, 150))

    # Draw invader.
    for invaderPosition in gameData["invaderData"]:
        invaderRect = pg.Rect(invaderPosition, sizeInvater)
        pg.draw.ellipse(screen, yellow, invaderRect)

    # Draw the player lasers.
    for playerLaserPosition in gameData["player"]["lasers"]:
        playerLaserRect = pg.Rect(playerLaserPosition, sizeLaser)
        pg.draw.rect(screen, blue, playerLaserRect)
        
    # Draw the invader lasers.
    for invaderLaserPosition in gameData["invaderLaserList"]:
        invaderLaserRect = pg.Rect(invaderLaserPosition, sizeLaser)
        pg.draw.rect(screen, green, invaderLaserRect)

    # Draw defences.
    for defences in gameData["defence"]:

        if defences["life"] > 0:
            defencesRect = pg.Rect(defences["coordinate"], sizeDefence)
            pg.draw.rect(screen, colorDefence[defences["life"] - 1], defencesRect)

    # Draw player.
    playerPosX = gameData["player"]["coordinate"][0]
    playerPosY = gameData["player"]["coordinate"][1]

    triangleCoordinate = (
        (playerPosX, playerPosY),
        (playerPosX + 10, playerPosY - 15), 
        (playerPosX + 20, playerPosY))

    pg.draw.polygon(screen, red, triangleCoordinate)


def updateInvader(gameData, direction, gameTick):
    """
    Update invaders, like position, laser position they have shootted and make them shoot randomly.

    Parameters:
    -----------
    gameData: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1, if set -1 the direction will be reversed (int)
    gameTick: Number of tick elapsed this second, 1 tick = 16ms, 60 tick = 1s (int)

    Return:
    -------
    gameData: Data structure containing most of the information about the game. (dict)
    direction: Direction in witch way the invader array is going 1 or -1, if set -1 the direction will be reversed (int)
    """

    # Check if lasers hit something.
    gameData = laserHit(gameData)

    # Unpack varaible for easier reading.
    invaderList = gameData["invaderData"]
    invaderLaser = gameData["invaderLaserList"]
    playerLaser = gameData["player"]["lasers"]

    # update invader position every second aka every 60 frames.
    if gameTick == 60:
        shiftDown = 0
        directionNew = changeDirection(invaderList, direction)

        # If direction change, shift down
        if direction != directionNew:
            shiftDown = 10
        
        # Update invader position.
        for invader in invaderList:

            invader[0] = invader[0] + (10 * directionNew)
            invader[1] = invader[1] + shiftDown

            invaderPosX = invader[0]
            playerPosX = gameData["player"]["coordinate"][0]

            # if player is in the area of attack shoot a laser (20% chance).
            if (invaderPosX - 50 < playerPosX) and (invaderPosX + 65 > playerPosX):
                if randint(0, 100) > 80:
                    invaderLaser.append([invader[0], invader[1]])

        direction = directionNew
    
    # Update laser position by 2 pixel every frame.
    for laser in playerLaser:
        laser[1] -= 2

    for invader_laser in invaderLaser:
        invader_laser[1] += 2

    return gameData, direction


def changeDirection(invaderData, direction):
    """
    Change the direction of all invader alive every time an invader hit the screen border

    Parameters:
    -----------
    invaderData: coordinate of the invaders (list)
    direction: Direction in witch way the invader array is going 1 or -1, if set -1 the direction will be reversed (int)

    Return:
    -------
    direction: Updated Direction in witch way the invader array is going 1 or -1 (int)
    """

    change = False
    for invader in invaderData:

        invaderPosX = invader[0]
        if (invaderPosX >= 280 and direction == 1) or (invaderPosX <= 10 and direction == -1):
            change = True
            
    if change == True:
        direction *= -1

    return direction          


def laserHit(gameData):
    """
    Check if a laser hit a player or an invader, update the hitted target and delete the laser.

    Parameters:
    -----------
    gameData: Data structure containing most of the information about the game. (dict)

    Return:
    -------
    gameData: Updated data structure containing most of the information about the game. (dict)
    """

    player = gameData["player"]
    playerLaser = player["lasers"]
    playerPosX = player["coordinate"][0]
    playerPosY = player["coordinate"][1]
    invaderList = gameData["invaderData"]
    invaderLaser = gameData["invaderLaserList"]

    # Lists empty get out of the function.
    if playerLaser == [] and invaderList == []:
        return gameData

    # Init the function data. 
    playerLaserToDelete = []
    invaderLaserToDelete = []
    invaderToDelete = []

    # Find if a laser is in an invader hit box.
    for player_laser in playerLaser:

        laserPosX = player_laser[0]
        laserPosY = player_laser[1]

        for defences in gameData["defence"]:

            if defences["life"] > 0:
                defencesPosX = defences["coordinate"][0]
                defencesPosY = defences["coordinate"][1]

                if (laserPosX >= defencesPosX and laserPosX <= defencesPosX + 30) and (laserPosY + 20 >= defencesPosY and laserPosY + 20 <= defencesPosY + 20):
                    
                    playerLaserToDelete.append(player_laser)

        for invader in invaderList:
            
            invaderPosX = invader[0]
            invaderPosY = invader[1]

            if (laserPosX >= invaderPosX and laserPosX <= invaderPosX + 15) and (laserPosY <= invaderPosY + 15 and laserPosY >= invaderPosY):

                gameData["score"] += 10
                playerLaserToDelete.append(player_laser)
                invaderToDelete.append(invader)

    # Check if a invader lasers is in the player or defence hit box.
    for invader_laser in invaderLaser:
        
        laserPosX = invader_laser[0]
        laserPosY = invader_laser[1]

        # Defence.
        for defences in gameData["defence"]:

            if defences["life"] > 0:
                defencesPosX = defences["coordinate"][0]
                defencesPosY = defences["coordinate"][1]

                if (laserPosX >= defencesPosX and laserPosX <= defencesPosX + 30) and (laserPosY + 20 >= defencesPosY and laserPosY + 20 <= defencesPosY + 20):
                    
                    invaderLaserToDelete.append(invader_laser)
                    defences["life"] -= 1

        # Player.
        if (laserPosX >= playerPosX and laserPosX <= playerPosX + 20) and (laserPosY + 7 >= playerPosY and laserPosY + 7 <= playerPosY + 15):
            
            invaderLaserToDelete.append(invader_laser)
            player["life"] -= 1

            
    # Delete player laser who hit.
    for playerLaserDeleted in playerLaserToDelete:
        playerLaser.pop(playerLaser.index(playerLaserDeleted))

    # Delete invader laser who hit.
    for invaderLaserDeleted in invaderLaserToDelete:
        invaderLaser.pop(invaderLaser.index(invaderLaserDeleted))

    # Delete invader destroyed.
    for invaderDeleted in invaderToDelete:
        invaderList.pop(invaderList.index(invaderDeleted))

    return gameData


def checkEndGame(invaderData, player):
    """
    Check if the game is finished.

    Parameters:
    -----------
    invaderData: coordinate of the invaders (list)
    player: Information about the player (dict)

    return:
    -------
    Result: if the game is finished retrun false, true otherwise.
    """

    if invaderData == [] or player["life"] <= 0:
        return False

    for invader in invaderData:
        if invader[1] + 15 >= 300:
            return False

    return True


def blitText(screen, text, pos, font, color):
    """
    Print text on a surface.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    text: Text to print (str)
    pos: Top left position to print the text (list)
    font: Font of the text to print (font)
    color: Color of the text to print (list)
    """

    textToPrint = [text.split(' ') for text in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    maxWidth = 300
    maxHeight = 300
    x = pos[0]
    y = pos[1]

    for line in textToPrint:

        for word in line:
            word_surface = font.render(word, 0, color)
            wordWidth, wordHeight = word_surface.get_size()

            # If the word go further
            if x + wordWidth >= maxWidth:
                x = pos[0]  # Reset the x.
                y += wordHeight  # Start on new row.

            # Draw to the screen and pass to the nex x value.
            screen.blit(word_surface, (x, y))
            x += wordWidth + space

        # Reset x axis and start a new row. 
        x = pos[0]
        y += wordHeight


def game(screen, background, clock, font):
    """
    Function with the game loop.

    Parameters:
    -----------
    screen: Surface of the window (surface)
    background: Surface of the screen (surface)
    clock: Object who track time (clock)
    font: Font used to print text on surface (font)

    Return:
    -------
    resulte: resulte of the game win or lost (str)
    """

    # Setup GameData.
    direction = 1
    gameTick = 0 

    gameData = {
        "player": {"life": 3, "coordinate": [150, 270], "lasers": []},
        "invaderData":  invader(), 
        "invaderLaserList": [],
        "defence": [
            {"coordinate": (60, 220), "life": 3},
            {"coordinate": (135, 220), "life": 3},
            {"coordinate": (210, 220), "life": 3}],
        "score": 0}

    textColor = (255, 255, 255)
    
    runnning = True
    while runnning:
        
        # Set the game to 60 update per second and count gameTick
        clock.tick(60)
        if gameTick == 60:
            gameTick = 0
        gameTick +=1

        # Quit the game if the quit boutton is pressed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                runnning = False
                quit()
        
        # Unpack variable from gameData for easier reading.
        playerPos = gameData["player"]["coordinate"]
        playerLaser = gameData["player"]["lasers"]
        playerLife = gameData["player"]["life"]
        score = gameData["score"]

        # Check if LEFT or RIGHT arrow key is pressed and allow only 10 update per second.  
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and (gameTick % 6):

            
            playerPos[0] -= 2
            if playerPos[0] <= 0:
                playerPos[0] = 0

        if keys[pg.K_RIGHT] and (gameTick % 6):

            playerPos[0] += 2
            if playerPos[0] >= 280:
                playerPos[0] = 280

        # Check if SPACE is pressed and allow only 5 update per second (so 5 shoot/s).
        if keys[pg.K_SPACE] and (gameTick % 12 == 0):
            
            playerLaser.append([playerPos[0] + 10, playerPos[1] - 15])

        # Game Update.
        runnning = checkEndGame(gameData["invaderData"], gameData["player"])
        gameData, direction = updateInvader(gameData, direction, gameTick)

        # UI update.
        uiText = "Life: {}    Score: {}".format(playerLife, score)
        blitText(screen, uiText, (0, 0), font, textColor)

        # Game Drawn.
        draw(screen, gameData)

        # Display update pygame.
        pg.display.update()
        screen.blit(background, (0, 0))

    # Check If game win or lost.
    if gameData["invaderData"] == [] and playerLife > 0:
        return "Game Win"

    else:
        return "Game Lost"


def main():
    """
    Main function who manage everything.
    """

    pg.init()

    # Setup the font.
    font = pg.font.SysFont("Comic Sans MS", 15)
    fontIntro = pg.font.SysFont("Comic Sans MS", 30)
    textColor = (255, 255, 255)

    # Setup window and game clock.
    displaySize = [300, 300]
    screen = pg.display.set_mode(displaySize)
    background = pg.Surface(screen.get_size())
    clock = pg.time.Clock()

    # Intro
    textIntro = "SPACE INVADER"
    textIntroInput = "Press SPACE to play or\n press ESCAPE to exit."
    textIntroSurface = fontIntro.render(textIntro, 0, textColor)
    blitText(screen, textIntroInput, (65, 125), font, textColor)
    screen.blit(textIntroSurface, (25, 45))

    # blitText(screen, textIntro, (0,0), fontIntro, textColor)
    pg.display.update()

    input = True
    while input:

        # Quit the game if the quit boutton is pressed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                input = False
                quit()
        
        # Continue to play when SPACE is pressed.
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            input = False

    play = True
    while play:

        result = game(screen, background, clock, font)

        screen.fill((0, 0, 0))

        textEndGame = "Press SPACE to try again \nor press ESCAPE to exit."
        wordSurface = font.render(result, 0, textColor)
        screen.blit(wordSurface, (115, 80))
        blitText(screen, textEndGame, (65, 125), font, textColor)

        pg.display.update()

        input = True
        while input:

            # Quit the game if the quit boutton is pressed
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    input = False
                    quit()
            
            # Continue to play when SPACE is pressed.
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                input = False

            # Quit if ESCAPE is pressed.
            if keys[pg.K_ESCAPE]:
                input = False
                quit()


if __name__ == "__main__":
    main()