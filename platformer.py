import time
import pygame
from GameObject import *
import sdl2
import sdl2.ext
pygame.init()
# Set up the drawing window
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
circle_position = (50, 400)

circle_radius = 25
refresh_rate = 60
frame_time = 1/refresh_rate
gravity = 1/8
yVelocity = -10
xVelocity = 2
class Location:
    def __init__(self, left_x, top_y):
        self.left_x = left_x
        self.top_y = top_y
class Hitbox:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# Run until the user asks to quit

b = GameObject(location = Location(400, 200), hitbox = Hitbox(circle_radius * 2, circle_radius * 2), image = None, velocity = (2, -10))
p = GameObject(location = Location(400, 300), hitbox = Hitbox(50, 20), image = None, velocity = (0, 0))
def test():
    o1 = GameObject(location = Location(400, 200), hitbox = Hitbox(10, 10), image = None, velocity = (2, -10))
    o2 = GameObject(location = Location(400, 300), hitbox = Hitbox(10, 10), image = None, velocity = (0, 0))
    result = o1.collidesWith(o2)
    print(result)
    o1 = GameObject(location=Location(400, 290), hitbox=Hitbox(10, 10), image=None, velocity=(2, -10))
    o2 = GameObject(location=Location(400, 300), hitbox=Hitbox(10, 10), image=None, velocity=(0, 0))
    result = o1.collidesWith(o2)
    print(result)
    o1 = GameObject(location=Location(390, 300), hitbox=Hitbox(10, 10), image=None, velocity=(2, -10))
    o2 = GameObject(location=Location(400, 300), hitbox=Hitbox(10, 10), image=None, velocity=(0, 0))
    result = o1.collidesWith(o2)
    print(result)
def update_screen(screen, game_objects):
    o1 = game_objects[0]
    o2 = game_objects[1]
    # Fill the background with white
    screen.fill((255, 255, 255))
    if o1.location.top_y + o1.hitbox.height >= (SCREEN_HEIGHT):
        yvel = o1.velocity[1] * -0.75
        xvel = o1.velocity[0] * 0.95
        if yvel >= -1 and yvel <= 1:
            yvel = 0

        o1.velocity = (xvel, yvel)
        o1.location.top_y = SCREEN_HEIGHT - o1.hitbox.height
    if o1.location.left_x >= (SCREEN_WIDTH - o1.hitbox.width):
        o1.velocity = (-0.75 * o1.velocity[0], o1.velocity[1])
    if o1.location.left_x <= (0 + o1.hitbox.width):
        o1.velocity = (-0.75 * o1.velocity[0], o1.velocity[1])

    #(CollisionDetected, TopCollision, BottomCollision, LeftCollision, RightCollision)

    collision = o1.collidesWith(o2)

    flipXVelocity = collision[0] and (collision[3] ^ collision[4])
    flipYVelocity = collision[0] and (collision[1] ^ collision[2])
    if flipXVelocity:
        o1.velocity = (-1 * o1.velocity[0], o1.velocity[1])
    if flipYVelocity:
        o1.velocity = (o1.velocity[0], -1 * o1.velocity[1])


    o1.move()
    o1.velocity= (o1.velocity[0], o1.velocity[1] + gravity)
    for go in game_objects:
        go.draw(screen)
    pygame.display.flip()


from enum import Enum

class movementStates(Enum):
    STATIONARY = 0
    JUMPING = 1
    DOUBLEJUMPING = 2
    RUNNING = 3
    SLIDING = 4
    SWIMMING = 5

state = movementStates.STATIONARY
def update_input(key, game_object):
    global state
    print(state)
    match state:
        case movementStates.STATIONARY:
            if key == "up":
                state = movementStates.JUMPING
                game_object.changeVelocity(0, -8)
            if key == "left":
                game_object.changeVelocity(-5,0)
            if key == "right":
                game_object.changeVelocity(5,0)
        case movementStates.JUMPING:
            if key == "up":
                state = movementStates.DOUBLEJUMPING
                game_object.changeVelocity(0,-5)
            if key == "left":
                game_object.changeVelocity(-5,0)
            if key == "right":
                game_object.changeVelocity(5,0)
            if game_object.velocity[1] == 0.125:
                state = movementStates.STATIONARY
        case movementStates.DOUBLEJUMPING:
            if key == "up":
                pass
            if key == "down":
                pass
            if key == "left":
                game_object.changeVelocity(-5,0)
            if key == "right":
                game_object.changeVelocity(5,0)
            if game_object.velocity[1] == 0.125:
                state = movementStates.STATIONARY
    #jumping: in the air
    #doubleJumping: jumping while mid-air
    #running: on normal ground, player inputing controls
    #sliding: on slippery/special ground, player not giving input
    #swimming: in liquid
    #stationary: on ground, no inputs

def test2():
    width = 160
    o1 = GameObject(location=Location(30, SCREEN_HEIGHT - 10), hitbox=Hitbox(10, 10), image=None, velocity=(0, 0))
    o2 = GameObject(location=Location(400 - width, 300), hitbox=Hitbox(width, 20), image=None, velocity=(0, 0))
    game_objects = [o1, o2]

    running = True
    while running:
        key = "none"
        #	current_time = time.getTime
        # Did the user click the window close button?
        for event in pygame.event.get(pump = True):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key = "up"
                elif event.key == pygame.K_DOWN:
                    key = "down"
                elif event.key == pygame.K_LEFT:
                    key = "left"
                elif event.key == pygame.K_RIGHT:
                    key = "right"
                elif event.key == pygame.K_w:
                    key = "up"
                elif event.key == pygame.K_s:
                    key = "down"
                elif event.key == pygame.K_a:
                    key = "left"
                elif event.key == pygame.K_d:
                    key = "right"
            if event.type == pygame.QUIT:
                running = False

        update_input(key, o1)
        update_screen(screen, game_objects)
        time.sleep(frame_time)

    # Done! Time to quit.
    pygame.quit()

test2()
#test()
#exit()
