import time
import pygame
from GameObject import *
from Location import *
from Hitbox import *
import random
import sdl2
import sdl2.ext
pygame.init()
# Set up the drawing window
SCREEN_WIDTH = 500 # pixels
SCREEN_HEIGHT = 500 # pixels
SCREEN_WIDTH_SUBPIXELS = toSubPixels(SCREEN_WIDTH)
SCREEN_HEIGHT_SUBPIXELS = toSubPixels(SCREEN_HEIGHT)
CENTERPOINT = (SCREEN_HEIGHT_SUBPIXELS / 2, SCREEN_WIDTH_SUBPIXELS / 2)
dashing = False
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
circle_position = (50, 400)
circle_radius = 25
refresh_rate = 60
frame_time = 1/refresh_rate
enemyMovementCounter = 0






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
        if o1.location.top_y + o1.hitbox.height >= (SCREEN_HEIGHT_SUBPIXELS):
            yvel = o1.velocity[1] * -0.1
            xvel = o1.velocity[0] * 0.95
            if yvel >= -1 and yvel <= 1:
                yvel = 0

            o1.velocity = (xvel, yvel)
            o1.location.top_y = SCREEN_HEIGHT_SUBPIXELS - o1.hitbox.height
        if o1.location.left_x >= (SCREEN_WIDTH_SUBPIXELS - o1.hitbox.width):
            o1.velocity = (-0.75 * o1.velocity[0], o1.velocity[1])
            o1.location.left_x = SCREEN_WIDTH_SUBPIXELS - o1.hitbox.width
        if o1.location.left_x <= (0 + o1.hitbox.width):
            o1.velocity = (-0.75 * o1.velocity[0], o1.velocity[1])
            o1.location.left_x = o1.hitbox.width



            do.velocity = (do.velocity[0], -1 * do.velocity[1])
    #(CollisionDetected, TopCollision, BottomCollision, LeftCollision, RightCollision)
    for go in game_objects:
        go.applyGravity()
        (dx, dy) = go.velocity
        go.move(dx, dy)
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
            OFFSET = toSubPixels(0)
            if flipXVelocity1:
                if do.velocity[0] > 0:
                    do.location.left_x = so.location.left_x - do.hitbox.width - OFFSET
                    # not_player.left_x = not_player.left_x - OFFSET
                elif do.velocity[0] < 0:
                    do.location.left_x = so.location.left_x + so.hitbox.width + OFFSET
                else:
                    pass
                do.velocity = (-1 * do.velocity[0], do.velocity[1])
            # if flipXVelocity2:
            #     do.velocity = (-1 * do.velocity[0], do.velocity[1])
            #     do.location.left_x = so.location.left_x - do.hitbox.width
            if flipYVelocity1:
                if do.velocity[1] > 0:
                    do.location.top_y = so.location.top_y - do.hitbox.height
                elif do.velocity[1] < 0:
                    do.location.top_y = so.location.top_y + so.hitbox.height
                else:
                    pass
                do.velocity = (do.velocity[0], -0.1 * do.velocity[1])
                do.velocity = (do.velocity[0], 0)

            # if flipYVelocity2:
            #     do.velocity = (do.velocity[0], -1 * do.velocity[1])
            #     do.location.top_y = so.location.top_y - do.hitbox.height
            if do not in game_enemies:
                update_movementState(key, do, collision)

        #Need to fix interaction generating collision with floor

    # o1.velocity= (o1.velocity[0], o1.velocity[1] + gravity)
    # badGuy.velocity = (badGuy.velocity[0], badGuy.velocity[1] + gravity)
    # (dx, dy) = badGuy.velocity
    # badGuy.move(dx, dy)




    # --------------------------------

def update_screen(screen, game_objects, clouds):
    # Fill the background with sky
    screen.fill((80, 153, 217))
    for go in game_objects:
        go.draw(screen)
    for c in clouds:
        if in_range(c.location.left_x, 0, SCREEN_WIDTH_SUBPIXELS) and in_range(c.location.top_y, 0, SCREEN_HEIGHT_SUBPIXELS):
            c.draw(screen)
    pygame.display.flip()

from movementStates import movementStates


def update_movementState(key, game_object, collision):
    global dashing
    match game_object.state:
        case movementStates.STATIONARY:
            dashing = False
            if key == "up":
                # game_object.location.top_y -= 30
                game_object.state = movementStates.JUMPING
                game_object.changeVelocity(0, -15)
            if key == "left":
                game_object.changeVelocity(-30,0)
                # game_object.location.left_x -= 30
            if key == "right":
                game_object.changeVelocity(30,0)
                # game_object.location.left_x += 30
            if key == "down":
                game_object.changeVelocity(0,30)

        case movementStates.JUMPING:
            if key == "up":
                # game_object.location.top_y -= 50
                game_object.state = movementStates.STATIONARY
                # game_object.state = movementStates.DOUBLEJUMPING
                game_object.changeVelocity(0,-50)
            if key == "left":
                game_object.changeVelocity(-50,0)
                # game_object.location.left_x -= 50
            if key == "right":
                game_object.changeVelocity(50,0)
                # game_object.location.left_x += 50
            if key == "down":
                game_object.changeVelocity(0,50)
            # if game_object.location.top_y > SCREEN_HEIGHT - 20:
            #     game_object.state = movementStates.STATIONARY
            # if collision[0] == True and collision[2] == True:
            #     game_object.state = movementStates.STATIONARY

        case movementStates.DOUBLEJUMPING:
            if key == "up":
                pass
            if key == "down":
                game_object.changeVelocity(0,50)
            if key == "left":
                game_object.changeVelocity(-50,0)
            if key == "right":
                game_object.changeVelocity(50,0)
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
    player = GameObject(location=Location(400 - width - 20, 300 ), hitbox=Hitbox(10, 10), image=None, velocity=(0, 0),color=(0,255,0), moveable = True)
    platform = GameObject(location=Location(400 - width, 300), hitbox=Hitbox(width, 20), image=None, velocity=(0, 0),color=(0,0,255), moveable=False)
    platform2 = GameObject(location=Location(220 - width, 400), hitbox=Hitbox(width - 30, 20), image=None, velocity=(0, 0),color=(0,0,255), moveable=False)
    bg1 = GameObject(location=Location(400 - 10, 300-10), hitbox=Hitbox(10,10), image=None, velocity=(-5,0),color=(255,0,0), moveable=True)
    bg2 = GameObject(location=Location(400 - 40, 300-10), hitbox=Hitbox(10,10), image=None, velocity=(0,-5),color=(255,0,100), moveable=True)
    bg3 = GameObject(location=Location(400 - 80, 300-10), hitbox=Hitbox(10,10), image=None, velocity=(5,0),color=(255,50,0), moveable=True)
    ground = GameObject(location=Location(-1000, SCREEN_HEIGHT - 20), hitbox=Hitbox(SCREEN_WIDTH * 10, 400), image=None, velocity=(0, 0),color=(86, 173, 85), moveable=False)
    clouds = []
    cloudXOffset = 0
    cloudYOffset = 0
    minimum_cloud_spacing = 100
    for i in range(0, 1000):
        cloudXOffset = (minimum_cloud_spacing * i) + random.randrange(0, minimum_cloud_spacing / 2)
        cloudYOffset = random.randrange(-50, 50)
        cloud = GameObject(location=Location(200 + cloudXOffset, 200 + cloudYOffset), hitbox=Hitbox(70, 10), image=None, velocity=(0,0),color=(255,255,255), moveable = False)
        clouds.append(cloud)
    dynamic_objects = [player, bg1, bg2, bg3]
    static_objects = [platform, ground, platform2]
    # dynamic_objects = [player]
    # static_objects = [platform]
    game_objects = dynamic_objects + static_objects
    game_enemies = [bg1, bg2, bg3]
    not_player = dynamic_objects + static_objects + clouds
    not_player.remove(player)
    not_player_chunk = []
    STARTWIDTH = 0
    ENDWIDTH = SCREEN_WIDTH_SUBPIXELS
    for i in range(0, 10):
        itemsInChunk = []
        for n in not_player:
            if n.inRange(n.location.left_x, STARTWIDTH, ENDWIDTH):
                itemsInChunk.append(n)
        STARTWIDTH += SCREEN_WIDTH_SUBPIXELS
        ENDWIDTH += SCREEN_WIDTH_SUBPIXELS
        not_player_chunk.append(itemsInChunk)





    running = True
    while running:
        player.location.left_x = CENTERPOINT[0]
        player.location.top_y = CENTERPOINT[1]
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
                        (dx, dy) = player.velocity
                        dx = -1 if dx < 0 else 1
                        player.move(dx * 35, dy)
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
        for no in not_player_chunk[0]:
            no.move(-player.velocity[0], -player.velocity[1])
        update_screen(screen, game_objects, clouds)
        time.sleep(frame_time)

    # Done! Time to quit.
    pygame.quit()

test2()
#test()
#exit()
