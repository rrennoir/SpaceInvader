import pygame as pg
import pygame.freetype
from random import randint


def invader():

    # Create invader data structur.
    invaderData = []
    for j in range(3):
        for invader in range(10):

            # offset the X axis by 25 pixel to center the invader platoon and offset the Y axis by 75 pixel to let place for the UI on the top.
            invaderPosition = [(invader * 25) + 25, j * 25 + 75] 

            invaderData.append(invaderPosition)

    return invaderData


def draw(screen, dataInvader, player, playerLaser, invaderLaser):

    # Sizes.
    sizeInvater = (15, 15)
    # sizePlayer = (20, 15)
    sizeLaser = (2, 7)

    # RGB colors.
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    # Draw invader.
    for invaderPosition in dataInvader:
        invaderRect = pg.Rect(invaderPosition, sizeInvater)
        pg.draw.ellipse(screen, yellow, invaderRect)

    # Draw the player lasers.
    for playerLaserPosition in playerLaser:
        playerLaserRect = pg.Rect(playerLaserPosition, sizeLaser)
        pg.draw.rect(screen, blue, playerLaserRect)
        
    # Draw the invader lasers.
    for invaderLaserPosition in invaderLaser:
        invaderLaserRect = pg.Rect(invaderLaserPosition, sizeLaser)
        pg.draw.rect(screen, green, invaderLaserRect)

    # Draw player
    playerCoord = player[1]
    pg.draw.polygon(screen, red, ((playerCoord[0], playerCoord[1]), (playerCoord[0] + 10, playerCoord[1] - 15), (playerCoord[0] + 20, playerCoord[1])))


def updateInvader(invaderData, direction, laserList, invaderLaserList, player, gameTick):

    laserList, invaderData, invaderLaserList, player = laserHit(laserList, invaderData, invaderLaserList, player)

    # update invader position every second aka every 60 frames.
    if gameTick == 60:
        shiftDown = 0
        directionNew = changeDirection(invaderData, direction)

        # If direction change shift down
        if direction != directionNew:
            shiftDown = 10
        
        # Update invader position.
        for invader in invaderData:
                invader[0] = invader[0] + (10 * directionNew)
                invader[1] = invader[1] + shiftDown

                # Shoot a laser randomly.
                if randint(0, 100) > 90:
                    invaderLaserList.append([invader[0], invader[1]])

        direction = directionNew
    
    # Update laser position by 2 pixel every frame.
    for i in range(len(laserList)):
        laserList[i][1] -= 2

    for i in range(len(invaderLaserList)):
        invaderLaserList[i][1] += 2

    return invaderData, direction, laserList, invaderLaserList, player


def changeDirection(invaderData, direction):

    change = False
    for element in invaderData:
    
            if (element[0] >= 280 and direction == 1) or (element[0] <= 10 and direction == -1):
                change = True
            
    if change == True:
        direction *= -1

    return direction          


def laserHit(playerLaserList, invaderData, invaderLaserList, player):

    # Lists empty get out of the function.
    if playerLaserList == [] and invaderLaserList == []:
        return playerLaserList, invaderData, invaderLaserList, player

    # Init the fnction data. 
    playerLaserToDelete = []
    invaderLaserToDelete = []
    invaderToDelete = []

    # Find if a laser is in an invader hit box.
    for laser in playerLaserList:
        for invader in invaderData:

            if (laser[0] >= invader[0] and laser[0] <= invader[0] + 15) and (laser[1] <= invader[1] + 15 and laser[1] >= invader[1]):
                playerLaserToDelete.append(laser)
                invaderToDelete.append(invader)

    # Check if a invader lasers is in the player hit box.
    for laser in invaderLaserList:
        
        if (laser[0] >= player[1][0] and laser[0] <= player[1][0] + 20) and (laser[1] + 7 >= player[1][1] and laser[1] + 7 <= player[1][1] + 15):
            invaderLaserToDelete.append(laser)
            player[0] -= 1
            
    # Delete player laser who hit.
    for laser in playerLaserToDelete:
        playerLaserList.pop(playerLaserList.index(laser))

    # Delete invader laser who hit.
    for laser in invaderLaserToDelete:
        invaderLaserList.pop(invaderLaserList.index(laser))

    # Delete invader destroyed.
    for invader in invaderToDelete:
        invaderData.pop(invaderData.index(invader))

    return playerLaserList, invaderData, invaderLaserList, player


def checkEndGame(invaderData, player):
    
    if invaderData == [] or player[0] <= 0:
        return False

    for invader in invaderData:
        if invader[1] + 15 >= 300:
            return False

    return True


def game():

    pg.init() 

    # Setup the font.
    # GAME_FONT = pg.freetype.SysFont("Comic Sans MS", 12)
    
    # Setup window and game clock.
    displaySize = [300, 300]
    screen = pg.display.set_mode(displaySize)
    background = pg.Surface(screen.get_size())
    clock = pg.time.Clock()

    # Setup GameData.
    invaderData = invader()
    direction = 1
    gameTick = 0 
    # score = 0
    player = [3, [150, 270]]
    laserList = []
    invaderLaserList = []
    
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

        # Check if LEFT or RIGHT arrow key is pressed and allow only 10 update per second.  
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and (gameTick % 6):

            player[1][0] -= 2
            if player[1][0] <= 0:
                player[1][0] = 0

        if keys[pg.K_RIGHT] and (gameTick % 6):

            player[1][0] += 2
            if player[1][0] >= 280:
                player[1][0] = 280

        # Check if SPACE is pressed and allow only 5 update per second (so 5 shoot/s).
        if keys[pg.K_SPACE] and (gameTick % 12 == 0):
            laserList.append([player[1][0] + 10, player[1][1] - 15])

        # Game Update.
        runnning = checkEndGame(invaderData, player)
        invaderData , direction, laserList, invaderLaserList, player = updateInvader(invaderData, direction, laserList, invaderLaserList, player, gameTick)

        # UI update.
        # textSurface = GAME_FONT.render("Life: {HP} Score: {SCORE}".format(HP=player[0], SCORE=score), (255, 255, 255))

        # Game Drawn.
        draw(screen, invaderData, player, laserList, invaderLaserList)

        # Display update pygame.
        pg.display.update()
        screen.blit(background, (0, 0))

    # Check If game win or lost.
    if invaderData == [] and player[0] > 0:
        return "Game Win"

    else:
        return "Game Lost"


def main():
    play = True
    while play:

        result = game()

        # screen.pygame.Surface.fill((0, 0, 0))
        # textSurface = GAME_FONT.render("{}\nPress any key to try again or use quit to exit.".format(result)), (255, 255, 255))
        # screen.blit(textSurface, (0, 0))

        print(result)
        print("Press any key to try again or use quit to exit.")


        text = input()
        if text == "quit":
            play = False
            quit()


if __name__ == "__main__":
    main()