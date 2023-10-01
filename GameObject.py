import time
import copy
import pygame
from Location import *
from Hitbox import *
SUBPIXELS_PER_PIXEL = 10
from movementStates import movementStates
circle_color = (0,255 , 10)
def in_range(value, lower_limit, upper_limit):
    return lower_limit <= value <= upper_limit
def clamp(value, lower_limit, upper_limit):
    if value > upper_limit:
        return upper_limit
    elif value < lower_limit:
        return lower_limit
    else: return value

def toPixels(value_subpixels):
    return value_subpixels / SUBPIXELS_PER_PIXEL

def toSubPixels(value_pixels):
    return value_pixels * SUBPIXELS_PER_PIXEL


class GameObject:

    def __init__(self, location, hitbox, image, velocity, color, moveable):
# Hitbox should track X and Y coordinates as well as height and width.
# Hitbox is for the computer to track the object, the image is for the human playing to see that it is there.
        self.location = Location(toSubPixels(location.left_x), toSubPixels(location.top_y)) # in subpixels
        self.hitbox = Hitbox(toSubPixels(hitbox.width), toSubPixels(hitbox.height)) # in subpixels
        self.image = image
        self.velocity = velocity # in subpixels
        self.color = color
        self.moveable = moveable
        self.state = movementStates.STATIONARY
        self.prevlocation = self.location # in subpixels

        #dx and dy are in subpixels

    def move(self, dx, dy):

        self.prevlocation = copy.deepcopy(self.location)
        (x,y) = (self.location.left_x, self.location.top_y)
        # (dx, dy) = self.velocity
        self.location.left_x = x + dx
        self.location.top_y = y + dy

    def inRange(self, value, lowerLimit, upperLimit):
        return lowerLimit <= value and value <= upperLimit



    def collidesWith(self, other):
        object1TopY = (self.location.top_y)
        object1BottomY = object1TopY + self.hitbox.height
        object1LeftX = (self.location.left_x)
        object1RightX = object1LeftX + self.hitbox.width

        object2TopY = (other.location.top_y)
        object2BottomY = object2TopY + other.hitbox.height
        object2LeftX = (other.location.left_x)
        object2RightX = object2LeftX + other.hitbox.width

        left_in_range = in_range(object1LeftX, object2LeftX, object2RightX)
        right_in_range = in_range(object1RightX, object2LeftX, object2RightX)

        x_overlap = 0
        if (not left_in_range and not right_in_range):
            x_overlap = 0
        elif (not left_in_range and right_in_range):
            x_overlap = object1RightX - object2LeftX
        elif (left_in_range and not right_in_range):
            x_overlap = object2RightX - object1LeftX
        else:
            x_overlap = self.hitbox.width

        top_in_range = in_range(object1TopY, object2TopY, object2BottomY)
        bottom_in_range = in_range(object1BottomY, object2TopY, object2BottomY)

        y_overlap = 0
        if (not top_in_range and not bottom_in_range):
            y_overlap = 0
        elif (not top_in_range and bottom_in_range):
            y_overlap = abs(object1BottomY - object2TopY)
        elif (top_in_range and not bottom_in_range):
            y_overlap = abs(object2BottomY - object1TopY)
        else:
            y_overlap = self.hitbox.height

        # # if object1.top_y <= object2BottomY or object1BottomY >= object2.top_y and object1.top_y <= object2BottomY or object1BottomY <= object2BottomY
        # BottomCollision = other.location.top_y <= object1BottomY and object1BottomY <= object2BottomY
        # TopCollision = other.location.top_y <= self.location.top_y and self.location.top_y <= object2BottomY
        # VerticalCollision = BottomCollision or TopCollision
        # LeftCollision = other.location.left_x <= self.location.left_x and self.location.left_x <= object2RightX
        # RightCollision = other.location.left_x <= object1RightX and object1RightX <= object2RightX
        # HorizontalCollision = LeftCollision or RightCollision
        # CollisionDetected = VerticalCollision and HorizontalCollision
        # return (CollisionDetected, TopCollision, BottomCollision, LeftCollision, RightCollision)

        NO_COLLISION = 0
        VERTICAL_COLLISION = 1
        HORIZONTAL_COLLISION = 2

        if (x_overlap == 0 or y_overlap == 0):
            return NO_COLLISION
        elif (x_overlap < y_overlap):
            return HORIZONTAL_COLLISION
        else:  # (y_overlap <= x_overlap)
            return VERTICAL_COLLISION

    # #  check top and bottom edges of object 1 to see if they are in the range of object 2's hitbox
    #     # if there is no overlap, there is no collision
    #     # if there is overlap, calculate how much and save it as the Y_overlap
    # # check left and right edges of object 1 to see if they are in the range of object 2's hitbox
    #     #if there is no overlap, there is no collision
    #     #if there is overlap, calculate how much and save it as X_overlap
    #
    #
    #     #if x_overlap < y_overlap:
    #         return horizontal_collision
    #     else x_overlap > y_overlap:
    #         return vertical_collision



    # def collidesWith(self, other):
    #     object1BottomY = self.location.top_y + self.hitbox.height
    #     object2BottomY = other.location.top_y + other.hitbox.height
    #     object1RightX = self.location.left_x + self.hitbox.width
    #     object2RightX = other.location.left_x + other.hitbox.width
    #     xAxisOverlap = object1RightX - object2RightX
    #     yAxisOverlap = object1BottomY - object2BottomY
    #     #  check top and bottom edges of object 1 to see if they are in the range of object 2's hitbox
    #     if in_range():
    #     # if there is no overlap, there is no collision
    #
    #     # if there is overlap, calculate how much and save it as the Y_overlap
    #
    #     # check left and right edges of object 1 to see if they are in the range of object 2's hitbox
    #
    #     # if there is no overlap, there is no collision
    #
    #     # if there is overlap, calculate how much and save it as X_overlap
    #
    #     # if x_overlap < y_overlap:
    #
    #     return horizontal_collision
    #
    # else x_overlap > y_overlap:
    #
    # return vertical_collision
    #     # if object1.top_y <= object2BottomY or object1BottomY >= object2.top_y and object1.top_y <= object2BottomY or object1BottomY <= object2BottomY
    #     BottomCollision = other.location.top_y <= object1BottomY and object1BottomY <= object2BottomY
    #     TopCollision = other.location.top_y <= self.location.top_y and self.location.top_y <= object2BottomY
    #     VerticalCollision = BottomCollision or TopCollision
    #     LeftCollision = other.location.left_x <= self.location.left_x and self.location.left_x <= object2RightX
    #     RightCollision = other.location.left_x <= object1RightX and object1RightX <= object2RightX
    #     HorizontalCollision = LeftCollision or RightCollision
    #     CollisionDetected = VerticalCollision and HorizontalCollision
    #     return (CollisionDetected, TopCollision, BottomCollision, LeftCollision, RightCollision)

    def draw(self, screen):
        s = screen
        cc = self.color
        l = self.location
        r = pygame.Rect(toPixels(l.left_x), toPixels(l.top_y), toPixels(self.hitbox.width), toPixels(self.hitbox.height))
        pygame.draw.rect(s, cc, r)
    def changeVelocity(self, dx, dy):
        MAXVELOCITY = 40
        newXvel = clamp(self.velocity[0] + dx,-MAXVELOCITY, MAXVELOCITY)
        newYvel = clamp(self.velocity[1] + dy, -MAXVELOCITY, MAXVELOCITY)
        self.velocity = (newXvel, newYvel)



    def applyGravity(self):
        # gravity is 1/8
        gravity = SUBPIXELS_PER_PIXEL / 8
        # gravity = 0
        if self.moveable == True:
            self.changeVelocity(0,gravity)
# Need a image as well as a hitbox as part of the class.

# Need a location so the game can update properly.

# Speed = Rate at which location changes/ Velocity = How far it travels in how much time.