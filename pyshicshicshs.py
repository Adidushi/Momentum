from vpython import *
# GlowScript 2.7 VPython
import threading
import time
import random
starttime = time.time()

lock = threading.Lock()


WALLCOLOR = color.magenta
BULLETCOLOR = color.cyan
PLAYERCOLOR = color.blue
ASTCOLOR = color.green
WALLSIZE = 5

scene.userpan = False
scene.userzoom = False
scene.userspin = False
scene.fullscreen = True
scene.width = 1900
scene.height = 900

spd = vec(0, 0, 0)

player = sphere(radius=0.5, color=PLAYERCOLOR)
wallleft = box(pos=vec(-6, 0, 0), size=vec(1, -13, 1), color=WALLCOLOR)
wallright = box(pos=vec(6, 0, 0), size=vec(1, -13, 1), color=WALLCOLOR)
walltop = box(pos=vec(0, 6, 0), size=vec(13, -1, 1), color=WALLCOLOR)
wallbottom = box(pos=vec(0, -6, 0), size=vec(13, 1, 1), color=WALLCOLOR)
wallback = box(pos=vec(0, 0, -1), size=vec(13, 13, 0.5))

def checkBounds(pos):
    return (-1 * WALLSIZE) < pos.x < WALLSIZE and (-1 * WALLSIZE) < pos.y < WALLSIZE

def roundFunc(x, base=5):
    return int(base * round(float(x)/base))

##PLAYER##


def shoot():
    print("SHOOT")
    global spd
    global player
    #distance = mag(player.pos-scene.mouse.pos)
    diff = 0.25 * norm(vec((player.pos.x - scene.mouse.pos.x), (player.pos.y - scene.mouse.pos.y), 0))
    spd += diff
    shootThread = threading.Thread(target=throwProj())
    shootThread.start()

def movePlayer():
    global player
    global spd

    while True:
        lock.acquire()
        try:
            frc = spd * -0.08
            spd += frc
            player.pos += spd
            if player.pos.y > 5:
                spd.y = 0
                player.pos.y = 5
            if player.pos.y < -5:
                spd.y = 0
                player.pos.y = -5
            if player.pos.x > 5:
                spd.x = 0
                player.pos.x = 5
            if player.pos.x < -5:
                spd.x = 0
                player.pos.x = -5
            time.sleep(1/120)
        finally:
            lock.release()

##BULLETS##


def throwProj():
    global player
    diff = vec((player.pos.x - scene.mouse.pos.x), (player.pos.y - scene.mouse.pos.y), 0)
    distance = sqrt((scene.mouse.pos.y - player.pos.y) ** 2 + (scene.mouse.pos.x - player.pos.x) ** 2)
    diff /= -6 * distance
    bullet = sphere(pos=player.pos+diff, radius=0.2, color=BULLETCOLOR)
    while checkBounds(bullet.pos):
        bullet.pos += diff
        time.sleep(1/120)

    bullet.visible = False
    del bullet

##ASTEROIDS##


def timeAsteroids():

    while True:
        lock.acquire()
        try:
            wall = random.randint(1,4)
            spot = random.randint(WALLSIZE * -100,WALLSIZE * 100) #for more accuracy in randomness
            angle = random.randint(-45,45)
            throwAst(wall, spot, radians(angle))
            time.sleep(2)
        finally:
            lock.release()

def throwAst(wall, spot, angle):
    startPos = astStartCoord(wall, spot)
    AST_SPEED = 0.25
    x_velocity = AST_SPEED * cos(angle)
    y_velocity = AST_SPEED * sin(angle)
    velocity = vector(x_velocity, y_velocity, 0)
    asteroid = sphere(pos=startPos, radius=0.2, color=ASTCOLOR)
    while checkBounds(asteroid.pos):
        asteroid.pos += velocity
    asteroid.visible = False
    del asteroid
    return

def astStartCoord(wall, spot): #starting at 12:00 going clockwise
    if wall == 1:
        return vec((spot/100), WALLSIZE-0.1, 0)
    elif wall == 2:
        return vec(WALLSIZE-0.1, (spot/100), 0)
    elif wall == 3:
        return vec((spot/100), -1*WALLSIZE+0.1, 0)
    elif wall == 4:
        return vec(-1*WALLSIZE+0.1, (spot/100), 0)
    return vec(WALLSIZE, WALLSIZE, 0)

scene.bind('click', shoot)

##INITIALIZING THREADS##

astThread = threading.Thread(target=timeAsteroids())
astThread.start()
moveThread = threading.Thread(target=movePlayer())
moveThread.start()


while True:
    rate(120)
    print(time.time())





