import time
import pygame
from GameObject import *
import sdl2
import sdl2.ext
pygame.init()
# Set up the drawing window
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
dashing = False
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
circle_position = (50, 400)
circle_radius = 25
refresh_rate = 60
frame_time = 1/refresh_rate
enemyMovementCounter = 0

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

# b = GameObject(location = Location(400, 200), hitbox = Hitbox(circle_radius * 2, circle_radius * 2), image = None, velocity = (2, -10))
# p = GameObject(location = Location(400, 300), hitbox = Hitbox(50, 20), image = None, velocity = (0, 0))
# def test():
    # o1 = GameObject(location = Location(400, 200), hitbox = Hitbox(10, 10), image = None, velocity = (2, -10))
    # o2 = GameObject(location = Location(400, 300), hitbox = Hitbox(10, 10), image = None, velocity = (0, 0))
    # result = o1.collidesWith(o2)
    # print(result)
    # o1 = GameObject(location=Location(400, 290), hitbox=Hitbox(10, 10), image=None, velocity=(2, -10))
    # o2 = GameObject(location=Location(400, 300), hitbox=Hitbox(10, 10), image=None, velocity=(0, 0))
    # result = o1.collidesWith(o2)
    # print(result)
    # o1 = GameObject(location=Location(390, 300), hitbox=Hitbox(10, 10), image=None, velocity=(2, -10))
    # o2 = GameObject(location=Location(400, 300), hitbox=Hitbox(10, 10), image=None, velocity=(0, 0))
    # result = o1.collidesWith(o2)
    # print(result)
def update_world(screen, game_objects, key, static_objects, dynamic_objects, game_enemies):
    # o1 = dynamic_objects[0]
    # o2 = game_objects[1]
    # badGuy = game_objects[2]
    def keepInBounds(o1, screen_width, screen_height):
        if o1.location.top_y + o1.hitbox.height >= (SCREEN_HEIGHT):
            yvel = o1.velocity[1] * -0.1
            xvel = o1.velocity[0] * 0.95
            if yvel >= -1 and yvel <= 1:
                yvel = 0

            o1.velocity = (xvel, yvel)
            o1.location.top_y = SCREEN_HEIGHT - o1.hitbox.height
        if o1.location.left_x >= (SCREEN_WIDTH - o1.hitbox.width):
            o1.velocity = (-0.75 * o1.velocity[0], o1.velocity[1])
            o1.location.left_x = SCREEN_WIDTH - o1.hitbox.width
        if o1.location.left_x <= (0 + o1.hitbox.width):
            o1.velocity = (-0.75 * o1.velocity[0], o1.velocity[1])
            o1.location.left_x = o1.hitbox.width



            do.velocity = (do.velocity[0], -1 * do.velocity[1])
    #(CollisionDetected, TopCollision, BottomCollision, LeftCollision, RightCollision)
    for do in dynamic_objects:
        for so in static_objects:
            NO_COLLISION = 0
            VERTICAL_COLLISION = 1
            HORIZONTAL_COLLISION = 2
            collision = do.collidesWith(so)
            flipXVelocity1 = collision == HORIZONTAL_COLLISION
            flipXVelocity2 = False
            flipYVelocity1 = collision == VERTICAL_COLLISION
            flipYVelocity2 = False
            if flipXVelocity1 == True:
                do.velocity = (-1 * do.velocity[0], do.velocity[1])
                do.location.left_x = so.location.left_x + so.hitbox.width
            if flipXVelocity2 == True:
                do.velocity = (-1 * do.velocity[0], do.velocity[1])
                do.location.left_x = so.location.left_x - do.hitbox.width
            if flipYVelocity1:
                if do.velocity[1] > 0:
                    do.location.top_y = so.location.top_y - do.hitbox.height
                elif do.velocity[1] < 0:
                    do.location.top_y = so.location.top_y + so.hitbox.height
                else:
                    pass
                do.velocity = (do.velocity[0], -0.1 * do.velocity[1])

            if flipYVelocity2:
                do.velocity = (do.velocity[0], -1 * do.velocity[1])
                do.location.top_y = so.location.top_y - do.hitbox.height
            if do not in game_enemies:
                update_movementState(key, do, collision)

        #Need to fix interaction generating collision with floor

    # o1.velocity= (o1.velocity[0], o1.velocity[1] + gravity)
    # badGuy.velocity = (badGuy.velocity[0], badGuy.velocity[1] + gravity)
    # (dx, dy) = badGuy.velocity
    # badGuy.move(dx, dy)
    for go in game_objects:
        go.applyGravity()
        (dx, dy) = go.velocity
        go.move(dx, dy)
        if go.moveable:
            keepInBounds(go, SCREEN_WIDTH, SCREEN_HEIGHT)


    # --------------------------------

def update_screen(screen, game_objects):
    # Fill the background with sky
    screen.fill((80, 153, 217))
    for go in game_objects:
        go.draw(screen)
    pygame.display.flip()

from movementStates import movementStates


def update_movementState(key, game_object, collision):
    global dashing
    match game_object.state:
        case movementStates.STATIONARY:
            dashing = False
            if key == "up":
                game_object.state = movementStates.JUMPING
                game_object.changeVelocity(0, -8)
            if key == "left":
                game_object.changeVelocity(-5,0)
            if key == "right":
                game_object.changeVelocity(5,0)

        case movementStates.JUMPING:
            if key == "up":
                game_object.state = movementStates.DOUBLEJUMPING
                game_object.changeVelocity(0,-5)
            if key == "left":
                game_object.changeVelocity(-5,0)
            if key == "right":
                game_object.changeVelocity(5,0)
            # if game_object.location.top_y > SCREEN_HEIGHT - 20:
            #     game_object.state = movementStates.STATIONARY
            # if collision[0] == True and collision[2] == True:
            #     game_object.state = movementStates.STATIONARY

        case movementStates.DOUBLEJUMPING:
            if key == "up":
                pass
            if key == "down":
                pass
            if key == "left":
                game_object.changeVelocity(-5,0)
            if key == "right":
                game_object.changeVelocity(5,0)
            # if game_object.location.top_y > SCREEN_HEIGHT - 20:
            #     game_object.state = movementStates.STATIONARY
            # if collision[0] == True and collision[2] == True:
            #     game_object.state = movementStates.STATIONARY
    #jumping: in the air
    #doubleJumping: jumping while mid-air
    #running: on normal ground, player inputing controls
    #sliding: on slippery/special ground, player not giving input
    #swimming: in liquid
    #stationary: on ground, no inputs
# estate = movementStates.ESTATIONARY
# def keyMove(key, game_object):
#     global estate
#     global dashing
#     # print(estate)
#     match estate:
#         case movementStates.ESTATIONARY:
#             dashing = False
#             if key == "up":
#                 estate = movementStates.EJUMPING
#                 game_object.changeVelocity(0, -0.5)
#             if key == "left":
#                 game_object.changeVelocity(-1,0)
#             if key == "right":
#                 game_object.changeVelocity(1,0)
#         case movementStates.EJUMPING:
#             if key == "up":
#                 estate = movementStates.EDOUBLEJUMPING
#                 game_object.changeVelocity(0,-0.5)
#             if key == "left":
#                 game_object.changeVelocity(-1,0)
#             if key == "right":
#                 game_object.changeVelocity(1,0)
#             if game_object.location.top_y > SCREEN_HEIGHT - 15:
#                 estate = movementStates.ESTATIONARY
#         case movementStates.EDOUBLEJUMPING:
#             if key == "up":
#                 pass
#             if key == "down":
#                 pass
#             if key == "left":
#                 game_object.changeVelocity(-2.5, 0)
#             if key == "right":
#                 game_object.changeVelocity(2.5, 0)
#             if game_object.location.top_y > SCREEN_HEIGHT - 15:
#                 estate = movementStates.ESTATIONARY

def test2():
    width = 160
    player = GameObject(location=Location(360, 300 - 10 - 2), hitbox=Hitbox(10, 10), image=None, velocity=(0, 10),color=(0,255,0), moveable = True)
    platform = GameObject(location=Location(400 - width, 300), hitbox=Hitbox(width, 20), image=None, velocity=(0, 0),color=(0,0,255), moveable=False)
    bg1 = GameObject(location=Location(400 - 10, 300-10), hitbox=Hitbox(10,10), image=None, velocity=(-5,0),color=(255,0,0), moveable=True)
    bg2 = GameObject(location=Location(400 - 40, 300-10), hitbox=Hitbox(10,10), image=None, velocity=(0,-5),color=(255,0,100), moveable=True)
    bg3 = GameObject(location=Location(400 - 80, 300-10), hitbox=Hitbox(10,10), image=None, velocity=(5,0),color=(255,50,0), moveable=True)
    ground = GameObject(location=Location(0, SCREEN_HEIGHT - 20), hitbox=Hitbox(SCREEN_WIDTH, 20), image=None, velocity=(0, 0),color=(86, 173, 85), moveable=False)

    dynamic_objects = [player, bg1, bg2, bg3]
    static_objects = [platform, ground]
    # dynamic_objects = [player]
    # static_objects = [platform]
    game_objects = dynamic_objects + static_objects
    game_enemies = [bg1, bg2, bg3]

    running = True
    while running:

        print(player.state)
        print(f"{player.prevlocation.left_x}, {player.prevlocation.top_y}, {player.location.left_x}, {player.location.top_y}")
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
                elif event.key == pygame.K_z:
                    # key = "dash"
                    global dashing, timer
                    if dashing == False:
                        dashing = True
                        # o1.velocity = (o1.velocity[0] * 1.5,o1.velocity[1])
                        (dx, dy) = o1.velocity
                        dx = -1 if dx < 0 else 1
                        o1.move(dx * 35, dy)
            if event.type == pygame.QUIT:
                running = False
        def aiMove(enemy, victim):
            key = ""
            if enemy.location.left_x < victim.location.left_x - 20:
                key = "right"
            elif enemy.location.left_x > victim.location.left_x + 20:
                key = "left"
            else:
                key = "none"
            if enemy.location.top_y > victim.location.top_y + 20:
                key = "up"
                                                    # Fix This later
            update_movementState(key,enemy, (False, False, False, False, False))

        global enemyMovementCounter
        enemyMovementCounter += 1
        if enemyMovementCounter >= 20:
            for enemy in game_enemies:
                    aiMove(enemy,player)
            enemyMovementCounter = 0

        update_world(screen, game_objects, key, static_objects, dynamic_objects, game_enemies)
        update_screen(screen, game_objects)
        time.sleep(frame_time)

    # Done! Time to quit.
    pygame.quit()

test2()
#test()
#exit()
