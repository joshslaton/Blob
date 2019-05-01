import pygame
from pygame.locals import *
# from settings import *
import time
import math
import random

pygame.init()
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

size = windowWidth, windowHeight = 800, 500
display_surf = pygame.display.set_mode(size)
food_list = list()

RESET, t, trail = pygame.USEREVENT+1, 10000, []
pygame.time.set_timer(RESET, t)

class Food():
    # Self replicating food based on location inside dimension given
    def __init__(self, surface):
        self.x = random.randint(0+20, windowWidth)
        self.y = random.randint(0+20, windowHeight)
        self.surface = surface;
        self.chanceToBePoison = .10
        self.isPoison = True if random.random() < self.chanceToBePoison else False
        self.radius = 5
    def draw(self):
        if(self.isPoison == 0):
            pygame.draw.circle(self.surface, BLUE, (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(self.surface, RED, (self.x, self.y), self.radius)

class Blob():
    def __init__(self, surface):
        self.pos = pygame.Vector2(0, 0)
        print(self.pos)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.surface = surface
        self.radius = 10
        self.health = 10
        self.speed = 2.5
        self.pressed_keys = {'right':False, 'up':False, 'left':False, 'down':False}

    def update(self):
        self.collisionDetect()
        if self.pressed_keys["up"]:
            self.y -= self.speed
        if self.pressed_keys["down"]:
            self.y += self.speed
        if self.pressed_keys["left"]:
            self.x -= self.speed
        if self.pressed_keys["right"]:
            self.x += self.speed

    def collisionDetect(self):
        for f in food_list:
            if(getDistance((blob.x, blob.y),(f.x, f.y)) <= ((blob.radius)/2)):
                food_list.remove(f)

    def draw(self):
        pygame.draw.circle(self.surface, GREEN, (int(self.x), int(self.y)), self.radius)

    #  Movement
    def moveUp(self, isPressed):
        if isPressed:
            self.pressed_keys["up"] = True
        else:
            self.pressed_keys["up"] = False

    def moveDown(self, isPressed):
        if isPressed:
            self.pressed_keys["down"] = True
        else:
            self.pressed_keys["down"] = False

    def moveLeft(self, isPressed):
        if isPressed:
            self.pressed_keys["left"] = True
        else:
            self.pressed_keys["left"] = False

    def moveRight(self, isPressed):
        if isPressed:
            self.pressed_keys["right"] = True
        else:
            self.pressed_keys["right"] = False

def resetDay():
    food_list.clear()
    spawn_food(50)

def spawn_food(numOfFood):
    for i in range(numOfFood):
        food = Food(display_surf)
        food_list.append(food)

def getDistance(pos1, pos2):
    blobX, blobY = pos1
    foodX, foodY = pos2
    diffX = math.fabs(blobX - foodX)
    diffY = math.fabs(blobY - foodY)
    # r = (math.sqrt((diffX**2) + (diffY**2)))
    r = ((diffX**2)+(diffY*2)**0.5)
    # print(r)
    # print(str(diffX**2)+", "+str(diffY**2))
    # print(str(diffX)+ " "+str(diffY))
    # print(((diffX**2)+(diffY**2))**(0.5))
    return r

blob = Blob(display_surf)
spawn_food(50)
while(True):

    clock.tick(60)
    display_surf.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if(keys[pygame.K_ESCAPE]):
            pygame.quit()
            quit()

        if (e.type == RESET):
            resetDay()

        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_r):
                blob.x = windowWidth/2
                blob.y = windowHeight/2
                # food_list.clear()
                # spawn_food(100)

            # if(e.key == pygame.K_SPACE):
                # food_list.clear()


            if(e.key == pygame.K_w):
                blob.moveUp(True)
            if(e.key == pygame.K_s):
                blob.moveDown(True)
            if(e.key == pygame.K_a):
                blob.moveLeft(True)
            if(e.key == pygame.K_d):
                blob.moveRight(True)

        if(e.type == pygame.KEYUP):
            if(e.key == pygame.K_w):
                blob.moveUp(False)
            if(e.key == pygame.K_s):
                blob.moveDown(False)
            if(e.key == pygame.K_a):
                blob.moveLeft(False)
            if(e.key == pygame.K_d):
                blob.moveRight(False)


    blob.update()
    blob.draw()
    for f in food_list:
        f.draw()

    pygame.display.flip()
