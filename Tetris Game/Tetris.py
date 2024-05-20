from Classes import *
from random import randint
import pygame

pygame.init()
clock = pygame.time.Clock()
HEIGHT = 600
WIDTH  = 600
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (192,192,192)

#---------------------------------------#
COLUMNS = 10  #
ROWS = 22  #
LEFT = 9  #
RIGHT = LEFT + COLUMNS  #
MIDDLE = LEFT + COLUMNS // 2  #
TOP = 1  #
FLOOR = TOP + ROWS  #

shapeNo = randint(1, 7)
tetra = Shape(MIDDLE - 1, 2, shapeNo)
shadow = Shape(MIDDLE - 1, 2, shapeNo, shadow=True)
nextShapeNo = randint(1, 7)
nextShape = Shape(LEFT - 6, 3, nextShapeNo)
oldShape = shapeNo
holdShapeNo = 0
holdShape = Shape(LEFT-6, 12, holdShapeNo)

bottom = Floor(LEFT,BOTTOM,COLUMNS)
lastRow = Floor(LEFT,BOTTOM+1,COLUMNS)
floor = Floor(LEFT,FLOOR,COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obst = Obstacles(LEFT, BOTTOM-1)
counter = 0
level = 0
time = 0
font = pygame.font.SysFont("Ariel Black", 60) 
swap = False
stored = False


def redrawScreen():
    screen.fill(BLACK)
    shadow.row = 0

    while not (shadow.collides(bottom) or shadow.collides(obst)):
        shadow.moveDown()
    shadow.moveUp()

    if shadow.row > tetra.row:
        shadow.draw(screen, GRIDSIZE)
    tetra.draw(screen, GRIDSIZE)
    for ob in obst.blocks:
        ob.draw(screen, GRIDSIZE)
    
    nextShape.draw(screen, GRIDSIZE)
    holdShape.draw(screen, GRIDSIZE)
    bottom.draw(screen, GRIDSIZE)
    leftWall.draw(screen, GRIDSIZE)
    rightWall.draw(screen, GRIDSIZE)

    pygame.display.update()


def findBottom(col: int):
    bot = 0
    for ob in obst.blocks:
        if ob.col == col and bot < ob.row:
            bot = ob.row
    if bot == 0:
        return 22
    return bot



inPlay = True

while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                tetra.rotateClkwise()
                shadow.rotateClkwise()
                if tetra.collides(leftWall) or tetra.collides(
                        rightWall) or tetra.collides(bottom) or tetra.collides(
                            obst):
                    tetra.rotateCntclkwise()
                    shadow.rotateCntclkwise()

            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
                shadow.moveLeft()
                if tetra.collides(leftWall) or tetra.collides(obst):
                    tetra.moveRight()
                    shadow.moveRight()

            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
                shadow.moveRight()

                if tetra.collides(rightWall) or tetra.collides(obst):
                    tetra.moveLeft()
                    shadow.moveLeft()
            if event.key == pygame.K_c and not swap:
                if not stored:
                    tetra, shadow, holdShape = Shape(
                        MIDDLE - 1, 2, nextShapeNo), Shape(MIDDLE - 1,
                                                           2,
                                                           nextShapeNo,
                                                           shadow=True), Shape(
                                                               LEFT - 6, 12,
                                                               oldShape)
                    oldShape, nextShapeNo = nextShapeNo, oldShape
                    holdShapeNo = nextShapeNo
                    swap = True
                    stored = True
                else:
                    tetra, shadow, holdShape = Shape(
                        MIDDLE - 1, 2, holdShapeNo), Shape(MIDDLE - 1,
                                                           2,
                                                           holdShapeNo,
                                                           shadow=True), Shape(
                                                               LEFT - 6, 12,
                                                               oldShape)
                    oldShape, holdShapeNo = holdShapeNo, oldShape
                    swap = True

            if event.key == pygame.K_SPACE:
                while not (tetra.collides(bottom) or tetra.collides(obst)):
                    tetra.moveDown()

            if event.key == pygame.K_DOWN:
                counter = 0
                tetra.moveDown()


    if counter > 1000:
        counter = 0
        tetra.moveDown()

    if tetra.collides(bottom) or tetra.collides(obst):
        for block in tetra.blocks:
            if block.row <= 2:
                inPlay = False
        if inPlay:
            tetra.moveUp()
            obst.append(tetra)
            obst.show()
            tetra = Shape(MIDDLE - 1, 2, nextShapeNo)
            shadow = Shape(MIDDLE - 1, 2, nextShapeNo, shadow=True)
            oldShape = nextShapeNo
            print(oldShape)
            nextShapeNo = randint(1, 7)
            nextShape = Shape(LEFT - 6, 3, nextShapeNo)
            swap = False

        fullRows = obst.findFullRows(
            TOP, FLOOR, COLUMNS
        )  # finds the full rows and removes their blocks from the obstacles
        print(
            "full rows: ", fullRows
        )  # printing the full rows is done to visualize the process remove it afterwards
        obst.removeFullRows(fullRows)

    counter += clock.get_time() * (1 + (level / 10))  #gets faster as level goes up


    redrawScreen()
    clock.tick(10000)
    pygame.time.delay(30)

pygame.quit()