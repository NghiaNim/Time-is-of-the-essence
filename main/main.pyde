add_library('minim')

import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1920
HEIGHT = 1080

class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.hero = Hero(100, 100, 100, 100, self.g)
        
    def display(self):
        self.hero.display()
        pass
        
class Creation:
    def __init__(self, x, y, w, h, g):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.g = g
        self.vx = 0
        self.vy = 0
        
    def gravity(self):
        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.h + self.vy > self.g:
                self.vy = self.g - (self.y + self.h)
                
    def update(self):
        self.gravity()
        
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        noFill()
        fill(0,0,0)
        rect(self.x, self.y, self.w, self.h)
        pass

class Hero(Creation):
    def __init__(self, x, y, w, h, g):
        Creation.__init__(self, x, y, w, h, g)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}

    def update(self):
        self.gravity()
        
        if self.key_handler[DOWN] == True and self.y+self.h == self.g:    
            self.vx = 0
            
        else:
            if self.key_handler[LEFT]:
                self.vx = -10
            elif self.key_handler[RIGHT]:
                self.vx = 10
            else:
                self.vx = 0
    
            if self.key_handler[UP] == True and self.y+self.h == self.g:
                self.vy = -10

            
            
        self.x += self.vx
        self.y += self.vy



#instance of creature so far                
test = Creation(10,10,10,10,500)

game = Game(WIDTH, HEIGHT, 500)
        
def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    game.display()
    test.display()

def keyPressed():
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.hero.key_handler[UP] = True
    elif keyCode == DOWN:
        game.hero.key_handler[DOWN] = True
    
def keyReleased():
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.hero.key_handler[UP] = False
    elif keyCode == DOWN:
        game.hero.key_handler[DOWN] = False
