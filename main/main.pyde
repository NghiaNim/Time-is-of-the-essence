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
        self.projectiles_list = []
        self.enemylist = []
        self.g = g
        #random sprite for hero
        self.hero = Hero(100, 100, 48, 48, self.g, 'SteamMan_run.png', 48, 48, 6, 'SteamMan_idle.png', 4)
        
    def display(self):
        self.hero.display()
        for e in self.enemylist:
            e.display()
        
class Creation:
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.g = g
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.num_frames = num_frames
        self.frame= 0
        
    def gravity(self):
        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.h + self.vy > self.g:
                self.vy = self.g - (self.y + self.h)
                
    def update(self):
        self.gravity()
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
        
        #slow down animation
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
            
        self.x += self.vx
        self.y += self.vy

    # Collision detection based on rectangle corner distances/overlapping
    def collision_rect(self, target):
        if (self.x < target.x + target.w) and (self.x + self.w > target.x) and (self.y < target.y + target.h) and (self.y + self.h > target.y):
            return True
        else:
            return False

        
    def display(self):
        self.update()       
        if self.direction == RIGHT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.direction == LEFT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)


class Hero(Creation):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.standing_y = y
        self.standing_h = h
        self.direction = RIGHT
        self.img_idle = loadImage(path + "/images/" + img_name_idle)
        self.idle_num_frames = idle_num_frames

    def update(self):
        self.gravity()
        
        if self.key_handler[DOWN] == True and self.y+self.h == self.g:    
            self.vx = 0
            self.y = self.standing_y + self.standing_h/2
            self.h = self.standing_h/2
        else:
            self.y = self.standing_y
            self.h = self.standing_h
            
            if self.key_handler[LEFT]:
                self.vx = -10
                self.direction = LEFT
            elif self.key_handler[RIGHT]:
                self.vx = 10
                self.direction = RIGHT
            else:
                self.vx = 0
    
            if self.key_handler[UP] == True and self.y+self.h == self.g:
                self.vy = -10
        
        #haven't added idle animation
        if frameCount%5 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames
        elif self.vx == 0:
            self.frame = 0    
            
        self.x += self.vx
        self.y += self.vy
        self.standing_y += self.vy
        
    def display(self):
        
        #rectangle to show hitbox
        self.update()
        noFill()
        fill(0,0,0)
        rect(self.x, self.y, self.w, self.h)
        
        
        if self.key_handler[DOWN] == True and self.y+self.h == self.g:
            #no animation for crouching yet
            
            pass
        #4 frames of idle but currently only 1
        #Won't implement the rest if this is not a fitting sprite
        elif self.vx == 0 and self.direction == RIGHT:
            image(self.img_idle, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) *self.img_w, self.img_h)
        elif self.vx == 0 and self.direction == LEFT:
            image(self.img_idle, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
        elif self.direction == RIGHT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.direction == LEFT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)

class Enemy(Creation):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, aspd, xl, xr, hp, vx=3, follow=False, p_gravity=False):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)

        self.vx = vx
        self.xleft = xl
        self.xright = xr
        self.follow = follow
        self.hp = hp
        self.attackspeed = aspd
        self.p_gravity = p_gravity

        self.direction = random.choice([LEFT, RIGHT])
        if self.direction == LEFT:
            self.vx *= -1

    def update(self):
        Creation.update(self)

        if self.x < self.xleft:
            self.vx *= -1
            self.direction = RIGHT
        elif self.x > self.xright:
            self.vx *= -1
            self.direction = LEFT

        if frameCount % self.attackspeed == 0:
            pass
            #self.attack()

    # Here we will be able to define the specifics of attacks 
    def attack(self):
        game.projectiles_list.append(Projectile(placeholder))

    def death(self):
        if self.hp <= 0:
            game.enemylist.remove(self)
        
def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    game.display()

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
        
game = Game(WIDTH, HEIGHT, 800)
game.enemylist.append(Enemy(100, 50, 50, 50, 800, "skeleton.png", 50, 50, 8, 180, 50, 600, 100, 3))
