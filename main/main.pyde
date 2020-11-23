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
        self.projectiles_list = []
        
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

    def collision(self):

        
    def display(self):
        self.update()
        noFill()
        fill(0,0,0)
        rect(self.x, self.y, self.w, self.h)
        pass

class Enemy(Creation):
    def __init__(self, x, y, w, h, g, aspd, xl, xr, vx=3, follow=False, p_gravity=False):
        Creation.__init__(self, x, y, w, h, g)
        self.attackspeed = aspd
        self.p_gravity = p_gravity
        self.vx = vx
        self.follow = follow
        self.xleft = xl
        self.xright = xr
        self.direction = random.choice([LEFT, RIGHT])
        if self.direction == LEFT:
            self.vx *= -1

    def update(self):
        Creation.__init__(self)
        if frameCount % self.attackspeed == 0:
            self.attack()


    def attack(self):
        game.projectiles_list.append(Projectile(placeholder))



#instance of creature so far                
test = Creation(10,10,10,10,500)

game = Game(WIDTH, HEIGHT)
        
def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    game.display()
    test.display()
