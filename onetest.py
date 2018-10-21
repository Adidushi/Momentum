class bullet(object):
    def __init__(self, speed, startpos):
        self.projectile = sphere(pos=startpos + speed, radius=0.2, color=BULLETCOLOR)
        self.speed = speed
        self.startpos = startpos


class asteroid(object):
    def __init__(self, speed, startpos):
        self.projectile = sphere(pos=startpos, radius=0.3, color=ASTCOLOR)
        self.speed = speed
        self.startpos = startpos


from vpython import *
# GlowScript 2.7 VPython
import threading
import time
import random

# CONSTANT SETUP

WALLCOLOR = color.magenta
BULLETCOLOR = color.cyan
PLAYERCOLOR = color.blue
ASTCOLOR = color.green
WALLSIZE = 5
ASTSECONDS = 0.5
ASTSPEED = 0.05

scene.userpan = False
scene.userzoom = False
scene.userspin = False
scene.fullscreen = True
scene.width = 900
scene.height = 900

bullets = []
asteroids = []

spd = vec(0, 0, 0)
asteroidCounter = 0

player = sphere(radius=0.5, color=PLAYERCOLOR)

wallleft = box(pos=vec(-6, 0, 0), size=vec(1, -13, 1), color=WALLCOLOR)
wallright = box(pos=vec(6, 0, 0), size=vec(1, -13, 1), color=WALLCOLOR)
walltop = box(pos=vec(0, 6, 0), size=vec(13, -1, 1), color=WALLCOLOR)
wallbottom = box(pos=vec(0, -6, 0), size=vec(13, 1, 1), color=WALLCOLOR)
wallback = box(pos=vec(0, 0, -1), size=vec(13, 13, 0.5))


# GENERAL

def checkBounds(pos):
    return (-1 * WALLSIZE) < pos.x < WALLSIZE and (-1 * WALLSIZE) < pos.y < WALLSIZE


# PLAYER

def playerBounds(player):
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


# BULLETS

def shoot():
    global spd
    global bullets

    diff = norm(vec((player.pos.x - scene.mouse.pos.x), (player.pos.y - scene.mouse.pos.y), 0))
    spd += diff / 4
    bullets.append(bullet(diff / -4, player.pos))

    print("Shot! There are now", len(bullets), "bullets!")


def bulletCheck(bulletList):
    for shot in bulletList:
        if not checkBounds(shot.projectile.pos):
            shot.projectile.visible = False
            bulletList.remove(shot)
            print("delet bulet")


def moveBullets(bulletList):
    for shot in bulletList:
        shot.projectile.pos += shot.speed


# ASTEROIDS

def astBounds(pos):
    return (-6) < pos.x < 6 and (-6) < pos.y < 6


def randomAsteroid():
    global asteroids

    wall = random.randint(1, 4)
    spot = random.randint(-550, 500) / 100  # get random spot with accuracy and remove margin from wall
    astSpeed = vec(ASTSPEED, 0, 0)

    if wall == 1:
        angle = random.randint(-135, -45)
        startPos = vec(spot, WALLSIZE - 0.1, 0)
    elif wall == 2:
        angle = random.randint(135, 235)
        startPos = vec(WALLSIZE - 0.1, spot, 0)
    elif wall == 3:
        angle = random.randint(45, 135)
        startPos = vec(spot, -WALLSIZE + 0.1, 0)
    elif wall == 4:
        angle = random.randint(-45, 45)
        startPos = vec(-WALLSIZE + 0.1, spot, 0)
    else:
        raise ValueError('wall is not between 1-4!!!')
    astSpeed = astSpeed.rotate(angle=radians(angle))
    asteroids.append(asteroid(astSpeed, startPos))

    print("OH SHIT! There are now", len(asteroids), "asteroids!")


def spawnAsteroid():
    global asteroids
    global asteroidCounter

    asteroidCounter += 1  # Advance counter
    # Check if it's time to spawn the asteroid
    if asteroidCounter % (ASTSECONDS * 120) == 0:
        randomAsteroid()


def checkAsteroids():
    global asteroids
    for asteroid in asteroids:
        if not astBounds(asteroid.projectile.pos):
            asteroid.projectile.visible = False
            asteroids.remove(asteroid)
            print("delet asteroid")


def moveAsteroids():
    global asteroids

    for asteroid in asteroids:
        asteroid.projectile.pos += asteroid.speed


# INTERACTIONS

def bulletHit():
    global bullets
    global asteroids

    for bullet in bullets:
        for asteroid in asteroids:
            if mag(bullet.projectile.pos - asteroid.projectile.pos) <= bullet.projectile.radius+asteroid.projectile.radius:
                asteroid.projectile.visible = False
                asteroids.remove(asteroid)
                bullet.projectile.visible = False
                bullets.remove(bullet)
                print("IMPACT HOLY SHET")


def playerHit():
    global asteroids
    global player

    for asteroid in asteroids:
        if mag(player.pos - asteroid.projectile.pos) <= player.radius+asteroid.projectile.radius:
            asteroid.projectile.visible = False
            asteroids.remove(asteroid)
            print("ow")


# START AND STUFF

scene.bind('click', shoot)

while True:
    rate(120)
    time.sleep(1 / 120)
    # Check player speed and bounds
    playerBounds(player)
    # Add speed
    player.pos += spd
    spd *= 0.92
    # Move bullets
    moveBullets(bullets)
    # Check all bullets and remove
    bulletCheck(bullets)
    # Check and WRECK the asteroids
    checkAsteroids()
    # Spawn asteroid once every 2 seconds
    spawnAsteroid()
    # Move asteroids
    moveAsteroids()
    # Check for any collision between bullets and asteroids
    bulletHit()
    # Check for player collision with asteroids
    playerHit()
