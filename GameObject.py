import time
import pygame
circle_color = (0,255 , 10)
class GameObject:

    def __init__(self, location, hitbox, image, velocity):
# Hitbox should track X and Y coordinates as well as height and width.
# Hitbox is for the computer to track the object, the image is for the human playing to see that it is there.
        self.location = location
        self.hitbox = hitbox
        self.image = image
        self.velocity = velocity
    def move(self):
        (x,y) = (self.location.left_x, self.location.top_y)
        (dx, dy) = self.velocity
        self.location.left_x = x + dx
        self.location.top_y = y + dy

    def collidesWith(self, other):
        object1BottomY = self.location.top_y + self.hitbox.height
        object2BottomY = other.location.top_y + other.hitbox.height
        object1RightX = self.location.left_x + self.hitbox.width
        object2RightX = other.location.left_x + other.hitbox.width
        # if object1.top_y <= object2BottomY or object1BottomY >= object2.top_y and object1.top_y <= object2BottomY or object1BottomY <= object2BottomY
        BottomCollision = other.location.top_y <= object1BottomY and object1BottomY <= object2BottomY
        TopCollision = other.location.top_y <= self.location.top_y and self.location.top_y <= object2BottomY
        VerticalCollision = BottomCollision or TopCollision
        LeftCollision = other.location.left_x <= self.location.left_x and self.location.left_x <= object2RightX
        RightCollision = other.location.left_x <= object1RightX and object1RightX <= object2RightX
        HorizontalCollision = LeftCollision or RightCollision
        CollisionDetected = VerticalCollision and HorizontalCollision
        return (CollisionDetected, TopCollision, BottomCollision, LeftCollision, RightCollision)

    def draw(self, screen):
        s = screen
        cc = circle_color
        l = self.location
        r = pygame.Rect(l.left_x, l.top_y, self.hitbox.width, self.hitbox.height)
        pygame.draw.rect(s, cc, r)
    def changeVelocity(self, dx, dy):
        self.velocity = (self.velocity[0] + dx, self.velocity[1] + dy)
# Need a image as well as a hitbox as part of the class.

# Need a location so the game can update properly.

# Speed = Rate at which location changes/ Velocity = How far it travels in how much time.