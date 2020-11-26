add_library('controlP5')
add_library('minim')

import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1920
HEIGHT = 1080
gameScreen = 0

class Game:
    def __init__(self, w, h, g, hero):
        self.w = w
        self.h = h
        self.enemy_projectiles = []
        self.hero_projectiles = []
        self.enemylist = []
        self.g = g

        self.enemylist.append(Enemy(300, 100, 50, 50, 800, "skeleton.png", 50, 50, 8, 180, 200, 800, 100, vx=3, follow=False, p_gravity=False, dmg = 10))

        #random sprite for hero
        if hero == 'Jack':
            self.hero = Jack(100, 100, 30, 48, self.g, 'SteamMan_run.png', 48, 48, 6, 'SteamMan_idle.png', 4, 'SteamMan_hurt.png', 3)
        elif hero == 'Jill':
            self.hero = Jill(100, 100, 30, 48, self.g, 'GraveRobber_run.png', 48, 48, 6, 'GraveRobber_idle.png', 4, 'GraveRobber_hurt.png', 3)
        elif hero == 'John':
            self.hero = John(100, 100, 30, 48, self.g, 'Woodcutter_run.png', 48, 48, 6, 'Woodcutter_idle.png', 4, 'Woodcutter_hurt.png', 3)
    
    
    def display(self):
        self.hero.display()
        for e in self.enemylist:
            e.display()
        for p in self.enemy_projectiles:
            p.display()
        for p in self.hero_projectiles:
            p.display()
        
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
        
        #slow down animation
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
            
        self.x += self.vx
        self.y += self.vy

    # Collision detection based on rectangle corner distances/overlapping
    def collision_rect_right(self, target):
        if target.x < self.x < target.x + target.w and (self.y < target.y + target.h) and (self.y + self.h > target.y):
            return True
        else:
            return False

    def collision_rect_left(self, target):
        if target.x < self.x + self.w < target.x + target.w and (self.y < target.y + target.h) and (self.y + self.h > target.y):
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
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, time):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.standing_y = y
        self.standing_h = h
        self.direction = RIGHT
        self.img_idle = loadImage(path + "/images/" + img_name_idle)
        self.img_hurt = loadImage(path + '/images/' + img_name_hurt)
        self.idle_num_frames = idle_num_frames
        self.hurt_num_frames = hurt_num_frames
        self.time = time
        self.invincible = 0
        self.hit_right = False

    def update(self):
        self.gravity()
        if frameCount % 60 == 0:
            self.time -= 1
        
        if self.invincible < 0:
            self.hit_right = False


        #if the player has i-frames, he can't be damaged
        if self.invincible < 25:
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

        else:
            if self.invincible == 59:
                self.vy = -5
            if self.hit_right and (self.y + self.h < self.g):
                self.vx = 7
            else:
                self.vx = -7
        
        if frameCount%10 == 0 and self.vx == 0:
            self.frame = (self.frame + 1) % self.idle_num_frames
        elif frameCount%10 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames

        #check for hit
        for enemy in game.enemylist:
            if self.collision_rect_right(enemy) and self.invincible <= 0:
                self.time -= enemy.dmg
                self.invincible = 60
                self.hit_right = True

            elif self.collision_rect_left(enemy) and self.invincible <= 0:
                self.time -= enemy.dmg
                self.invincible = 60

        
        for enemy in game.enemy_projectiles:
            if self.collision_rect_right(enemy) and self.invincible <= 0:
                self.time -= enemy.dmg
                self.invincible = 60
                self.hit_right = True

            elif self.collision_rect_left(enemy) and self.invincible <= 0:
                self.time -= enemy.dmg
                self.invincible = 60

        self.x += self.vx
        self.y += self.vy
        self.standing_y += self.vy
        self.invincible -= 1


        
    def display(self):
        
        #rectangle to show hitbox
        self.update()
        noFill()
        fill(0,0,0)
        rect(self.x, self.y, self.w, self.h)
        
        
        if self.invincible > 0 and self.direction == RIGHT:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 1 * self.img_w, 0, 2 *self.img_w - 18, self.img_h)

        
        elif self.invincible > 0 and self.direction == LEFT:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 2 * self.img_w - 18, 0, 1 * self.img_w, self.img_h)


        elif self.key_handler[DOWN] == True and self.y+self.h == self.g:
            #no animation for crouching yet
            
            pass

        #4 frames of idle but currently only 1
        #Won't implement the rest if this is not a fitting sprite
        elif self.vx == 0 and self.direction == RIGHT:
            image(self.img_idle, self.x, self.y, self.img_w - 18, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) *self.img_w - 18, self.img_h)
        elif self.vx == 0 and self.direction == LEFT:
            image(self.img_idle, self.x, self.y, self.img_w - 18, self.img_h, (self.frame + 1) * self.img_w - 18, 0, self.frame * self.img_w, self.img_h)
        elif self.direction == RIGHT:
            image(self.img, self.x, self.y, self.img_w - 18, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w - 18, self.img_h)
        elif self.direction == LEFT:
            image(self.img, self.x, self.y, self.img_w - 18, self.img_h, (self.frame + 1) * self.img_w - 18, 0, self.frame * self.img_w, self.img_h)
        
        textSize(20)
        text('Remaining time: ' + str(self.time), 50, 30)

class Jack(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames):
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, 100)

        
    def special_ability(self):
        pass
    
class Jill(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames):
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, 30)
        
    def special_ability(self):
        pass
    
class John(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames):
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, 120)
        
    def special_ability(self):
        pass

class Enemy(Creation):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, aspd, xl, xr, hp, dmg, vx=3, follow=False, p_gravity=False):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)

        self.dmg = dmg #touch damage
        self.vx = vx
        self.xleft = xl
        self.xright = xr
        self.follow = follow
        self.hp = hp
        self.attackspeed = aspd # How many frames must pass per attack?
        self.p_gravity = p_gravity
        self.framestart = frameCount
        self.direction = random.choice([LEFT, RIGHT])
        if self.direction == LEFT:
            self.vx *= -1

    def update(self):
        Creation.update(self)
        if frameCount - self.framestart > self.attackspeed:
            self.attack()
            self.framestart = frameCount

        if self.x < self.xleft:
            self.vx *= -1
            self.direction = RIGHT
        elif self.x > self.xright:
            self.vx *= -1
            self.direction = LEFT

    # Here we will be able to define the specifics of attacks 
    def attack(self):
        game.enemy_projectiles.append(Projectile(self.x, self.y+20, 10, 10, self.g, "bone.png", 10, 10, 4, self.vx*2, -6, 150, False, 10)) # Testing projectile

    def death(self):
        if self.hp <= 0:
            game.enemylist.remove(self)

class Projectile(Creation):

    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, vx, vy, framespan, gravity, dmg):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)
        self.vx = vx
        self.vy = vy
        self.framespan = framespan #How many frames should the projectile exist
        self.framestart = frameCount # When was the projectile created
        self.gravitycheck = gravity # Should gravity apply? T/F
        self.dmg = dmg # How much damage should this projectile cause?

        if self.vx > 0:
            self.direction = RIGHT
        else:
            self.direction = LEFT 

    def update(self):

        #slow down animation
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
        
        if self.gravitycheck == True:
            self.gravity()
            self.y += self.vy    
        self.x += self.vx

        # If the projectile exceeds its framespan, it ought not exist anymore
        if frameCount - self.framestart > self.framespan:
            self.destroy()

    def destroy(self):

        if self in game.enemy_projectiles:
            game.enemy_projectiles.remove(self)
        elif self in game.hero_projectiles:
            game.hero_projectiles.remove(self)

    def gravity(self):
        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.15
            if self.y + self.h + self.vy > self.g:
                self.vy = self.g - (self.y + self.h)
        


            
def drawMenu():
    background(255, 255, 255)
    fill(0)
    textSize(50)
    text('Choose your champion', 100, 100)
    noFill()
    rect(100, 200, 300, 100)
    text('Jack', 200, 270)
    rect(100, 400, 300, 100)
    text('Jill', 200, 470)
    rect(100, 600, 300, 100)
    text('John', 200, 670)
    
    pass

def drawGame():
    global game
    background(255, 255, 255)
    game.display()
    if game.hero.time < 0:
        game = Game(WIDTH, HEIGHT, 800, hero)
        
def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    if gameScreen == 0:
        drawMenu()
    else:
        drawGame()
    

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
        
def mousePressed():
    global gameScreen
    global game
    global hero
    #Choose Jack
    if gameScreen == 0 and 100<=mouseX<=400 and 200<=mouseY<=300:
        hero = 'Jack'
        game = Game(WIDTH, HEIGHT, 800, hero)
        gameScreen = 1
    #Choose Jill
    if gameScreen == 0 and 100<=mouseX<=400 and 400<=mouseY<=500:
        hero = 'Jill'
        game = Game(WIDTH, HEIGHT, 800, hero)
        gameScreen = 1
    #Choose John
    if gameScreen == 0 and 100<=mouseX<=400 and 600<=mouseY<=700:
        hero = 'John'
        game = Game(WIDTH, HEIGHT, 800, hero)        
        gameScreen = 1
        
