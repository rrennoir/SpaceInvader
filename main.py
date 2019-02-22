import pygame as pg


def invader():

    invaderData = []
    for j in range(3):
        for invader in range(10):

            invaderPosition = [(invader * 25) + 25, j * 25 + 75]
            invaderData.append(invaderPosition)

    return invaderData


def draw(screen, dataInvader, playerData, laser):

    sizeInvater = (15, 15)
    sizePlayer = (20, 15)
    sizeLaser = (5, 9)

    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    for element in dataInvader:
        baseRect = pg.Rect(element, sizeInvater)
        pg.draw.ellipse(screen, yellow, baseRect)

    for element in laser:
        baseRect = pg.Rect(element, sizeLaser)
        pg.draw.ellipse(screen, blue, baseRect)

    baseRect = pg.Rect(playerData, sizePlayer)
    pg.draw.ellipse(screen, red, baseRect)


def updateInvader(invaderData, direction, laserList, gameTick):

    laserList, invaderData = laserHit(laserList, invaderData)

    if gameTick == 60:
        shiftDown = 0
        directionNew = changeDirection(invaderData, direction)

        if direction != directionNew:
            shiftDown = 15

        for invader in invaderData:
                invader[0] = invader[0] + (15 * directionNew)
                invader[1] = invader[1] + shiftDown

        direction = directionNew

    for i in range(len(laserList)):
        laserList[i][1] -= 2

    return invaderData, direction, laserList


def changeDirection(invaderData, direction):

    change = False
    for element in invaderData:
    
            if (element[0] >= 280 and direction == 1) or (element[0] <= 10 and direction == -1):
                change = True
            
    if change == True:
        direction *= -1

    return direction          


def laserHit(laserList, invaderData):

    if laserList == []:
        return laserList, invaderData

    laserToDelete = []
    invaderToDelete = []

    for laser in laserList:
        for invader in invaderData:

            if (laser[0] >= invader[0] and laser[0] <= invader[0] + 15) and (laser[1] <= invader[1] + 15 and laser[1] >= invader[1]):
                laserToDelete.append(laser)
                invaderToDelete.append(invader)

    for laser in laserToDelete:
        laserList.pop(laserList.index(laser))

    for invader in invaderToDelete:
        invaderData.pop(invaderData.index(invader))

    return laserList, invaderData


def checkEndGame(invaderData):
    
    if invaderData == []:
        return True

    for invader in invaderData:
        if invader[1] + 15 >= 300:
            return True

    return False


def main():

    pg.init()

    displaySize = [300, 300]
    screen = pg.display.set_mode(displaySize)
    background = pg.Surface(screen.get_size())
    clock = pg.time.Clock()

    invaderData = invader()
    direction = 1
    gameTick = 0
    player = [150, 270]
    laserList = []
    
    Ended = False
    while not Ended:

        clock.tick(60)
        if gameTick == 60:
            gameTick = 0
        gameTick +=1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Ended = False
                quit()
            
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] and (gameTick % 6):

                player[0] -= 2
                if player[0] <= 0:
                    player[0] = 0

        if keys[pg.K_RIGHT] and (gameTick % 6):

                player[0] += 2
                if player[0] >= 280:
                    player[0] = 280

        if keys[pg.K_SPACE] and (gameTick % 12 == 0):
                laserList.append([player[0] + 3, player[1] + 10])


        draw(screen, invaderData, player, laserList)

        Ended = checkEndGame(invaderData)
        invaderData , direction, laserList = updateInvader(invaderData, direction, laserList, gameTick)

        pg.display.update()
        screen.blit(background, (0, 0))


    if invaderData == []:
        print("Win")
    
    else:
        print("Lost")


if __name__ == "__main__":
    main()