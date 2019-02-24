import pygame as pg
from random import randint


def invader():

    invaderData = []
    for j in range(3):
        for invader in range(10):

            invaderPosition = [(invader * 25) + 25, j * 25 + 75]
            invaderData.append(invaderPosition)

    return invaderData


def draw(screen, dataInvader, player, playerLaser, invaderLaser):

    # Elipse size.
    sizeInvater = (15, 15)
    sizePlayer = (20, 15)
    sizeLaser = (5, 9)

    # RGB colors.
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    # Draw invader.
    for element in dataInvader:
        baseRect = pg.Rect(element, sizeInvater)
        pg.draw.ellipse(screen, yellow, baseRect)

    # Draw the player lasers.
    for laser in playerLaser:
        baseRect = pg.Rect(laser, sizeLaser)
        pg.draw.ellipse(screen, blue, baseRect)

    # Draw the invader lasers.
    for laser in invaderLaser:
        baseRect = pg.Rect(laser, sizeLaser)
        pg.draw.ellipse(screen, green, baseRect)

    # Draw player
    baseRect = pg.Rect(player[1], sizePlayer)
    pg.draw.ellipse(screen, red, baseRect)


def updateInvader(invaderData, direction, laserList, invaderLaserList, player, gameTick):

    laserList, invaderData, invaderLaserList, player = laserHit(laserList, invaderData, invaderLaserList, player)

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
    
    # Update laser position
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

    if playerLaserList == [] or invaderLaserList == []:
        return playerLaserList, invaderData, invaderLaserList, player

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

        if (laser[0] >= player[1][0] and laser[0] <= player[1][0] + 15) and (laser[1] <= player[1][1] + 15 and laser[1] >= player[1][1]):
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
        return True

    for invader in invaderData:
        if invader[1] + 15 >= 300:
            return True

    return False


def main():

    pg.init() 

    # Setup window and game clock.
    displaySize = [300, 300]
    screen = pg.display.set_mode(displaySize)
    background = pg.Surface(screen.get_size())
    clock = pg.time.Clock()

    # Setup GameData.
    invaderData = invader()
    direction = 1
    gameTick = 0 
    player = [3, [150, 270]]
    laserList = []
    invaderLaserList = []
    
    Ended = False
    while not Ended:
        
        # Set the game to 60 update per second and count gameTick
        clock.tick(60)
        if gameTick == 60:
            gameTick = 0
        gameTick +=1

        # Quit the game if the quit boutton is pressed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Ended = False
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
                laserList.append([player[1][0] + 3, player[1][1] + 10])

        # Game Update.
        Ended = checkEndGame(invaderData, player)
        invaderData , direction, laserList, invaderLaserList, player = updateInvader(invaderData, direction, laserList, invaderLaserList, player, gameTick)

        # Game Drawn.
        draw(screen, invaderData, player, laserList, invaderLaserList)

        # Display update pygame.
        pg.display.update()
        screen.blit(background, (0, 0))

    
    # Check If game win or lost.
    if invaderData == [] and player[0] > 0:
        print("Win")
    
    else:
        print("Lost")


if __name__ == "__main__":
    main()