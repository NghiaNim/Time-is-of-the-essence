add_library('minim')

import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1920
HEIGHT = 1080

class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
    def display(self):
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

class Enemy(Creation):
    def __init__(self, x, y, w, h, g, vx=3):
        Creation.__init__(self, x, y, w, h, g):
        self.vx = vx
        self.direction = random.choice([LEFT, RIGHT])
        if self.direction == LEFT:
            self.vx *= -1

#instance of creature so far                
test = Creation(10,10,10,10,500)

game = Game(WIDTH, HEIGHT)
        
def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    game.display()
    test.display()
