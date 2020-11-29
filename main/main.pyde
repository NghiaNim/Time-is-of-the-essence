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

        #Enemy Test
        self.enemylist.append(TimeWraith(300, 700, 800, 200, 800))

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

    # Simple collision detection, doesn't check for side (needed for enemies class)
    def collision_rect(self, target):
        if (self.x < target.x + target.w) and (self.x + self.w > target.x) and (self.y < target.y + target.h) and (self.y + self.h > target.y):
            return True
        else:
            return False

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
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False, 'Q':False}
        self.standing_y = y
        self.standing_h = h
        self.direction = RIGHT
        self.img_idle = loadImage(path + "/images/" + img_name_idle)
        self.img_hurt = loadImage(path + '/images/' + img_name_hurt)
        self.idle_num_frames = idle_num_frames
        self.hurt_num_frames = hurt_num_frames
        self.time = time
        self.collission_countdown = 30 # How for how many frames should be hero invincible after detecting collsion?
        self.col_framestamp = frameCount
        self.shootingspeed = 30 # Cooldown for shooting in frames
        self.shoot_framestamp = frameCount
        self.invincible = 0
        self.hit_right = False

    def update(self):
        self.gravity()
        if frameCount % 60 == 0:
            self.time -= 1
        
        if self.invincible < 0:
            self.hit_right = False


        #the player get hits, he won't be able to move for 35 frames but will retain invincibility for 25 more frames
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
        
        #knockback on hit
        else:
            if self.key_handler[DOWN] == True:
                self.y = self.standing_y
                self.h = self.standing_h
            if self.invincible == 59:
                self.vy = -5
            if self.hit_right and (self.y + self.h < self.g):
                self.vx = 7
            else:
                self.vx = -7
    
            if self.key_handler[UP] == True and self.y+self.h == self.g:
                self.vy = -10

        #Attack Handler
        if self.key_handler['Q'] == True:
            self.attack()
        
        #animation based on action
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

        
        for projectile in game.enemy_projectiles:
            if self.collision_rect_right(projectile) and self.invincible <= 0:
                projectile.destroy()
                self.time -= projectile.dmg
                self.invincible = 60
                self.hit_right = True

            elif self.collision_rect_left(projectile) and self.invincible <= 0:
                projectile.destroy()
                self.time -= projectile.dmg
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
        
        
        if self.key_handler[DOWN] == True and self.y+self.h == self.g:
            #no animation for crouching yet
            
            pass
        elif self.invincible > 0 and self.direction == RIGHT:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 1 * self.img_w, 0, 2 *self.img_w - 18, self.img_h)

        
        elif self.invincible > 0 and self.direction == LEFT:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 2 * self.img_w - 18, 0, 1 * self.img_w, self.img_h)




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

    def attack(self):
        if self.direction == LEFT:
            p_vx = -1
        elif self.direction == RIGHT:
            p_vx = 1
        if frameCount - self.shoot_framestamp > self.shootingspeed:
            self.shoot_framestamp = frameCount
            game.hero_projectiles.append(Projectile(self.x, self.y+20, 10, 10, self.g, "bone.png", 10, 10, 4, 3*p_vx, -6, 150, False, 10))

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

    def __init__(self, x, y, w, h, g, img_name, img_name_idle, img_w, img_h, num_frames, num_idle_frames, attack_frame, aspd, xl, xr, hp, vx, dmg_projectile, dmg_collision, attack_count, follow=False, p_gravity=False):

        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)

        self.img_idle = loadImage(path + "/images/" + img_name_idle)
        self.idle_frame = 0
        self.idle_count = 0
        self.num_idle_frames = num_idle_frames
        self.attack_frame = attack_frame
        self.idle = False
        self.dmg = dmg_collision # collision damage
        self.vx = vx
        self.xleft = xl #left X boundary
        self.xright = xr # right x boundary
        self.follow = follow # should the enemy follow the hero if in sight?
        self.hp = hp
        self.attackspeed = aspd # How many frames must pass per attack?
        self.projectile_bol = True
        self.projectile_speed = 4
        self.p_gravity = p_gravity # should the gravity apply on its projectiles
        self.framestart = frameCount 
        self.direction = random.choice([LEFT, RIGHT])
        #self.dmg_collision = dmg_collision
        self.dmg_projectile = dmg_projectile
        self.attack_count = attack_count
        if self.direction == LEFT:
            self.vx *= -1

        self.tmp_vx = 0

    def update(self):
        Creation.update(self)

        # Idle and attack loop (enemy will stop to attack)
        if frameCount - self.framestart > self.attackspeed:
            if self.idle == False:
                self.tmp_vx = self.vx
                self.vx = 0
                self.idle = True
            if self.attack_frame-1 == self.idle_frame and frameCount%10 == 0:
                if self.projectile_bol == True: #Does the enemy shoot projectiles?
                    self.attack()
            if self.idle_count-1 == self.num_idle_frames:
                self.framestart = frameCount
                self.vx = self.tmp_vx
                self.idle = False


        if self.x < self.xleft:
            self.vx *= -1
            self.direction = RIGHT
        elif self.x > self.xright:
            self.vx *= -1
            self.direction = LEFT

        for p in game.hero_projectiles:
            if self.collision_rect(p) == True:
                self.hp -= p.dmg
                p.destroy()

        # slow down idle frames
        if self.vx == 0 and frameCount%10 == 0:
            self.idle_frame = (self.idle_frame + 1) % self.num_idle_frames
            self.idle_count += 1
        elif self.vx != 0:
            self.idle_frame = 0
            self.idle_count = 0


        if self.hp <= 0:
            self.death()

    def display(self):
        self.update()       
        if self.vx != 0 and self.direction == RIGHT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.vx != 0 and self.direction == LEFT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
        elif self.vx == 0 and self.direction == RIGHT:
            image(self.img_idle, self.x, self.y, self.img_w, self.img_h, self.idle_frame * self.img_w, 0, (self.idle_frame + 1) * self.img_w, self.img_h)
        elif self.vx == 0 and self.direction == LEFT:
            image(self.img_idle, self.x, self.y, self.img_w, self.img_h, (self.idle_frame + 1) * self.img_w, 0, self.idle_frame * self.img_w, self.img_h)

    # Here we will be able to define the specifics of attacks 
    def attack(self):
        if self.direction == LEFT:
            game.enemy_projectiles.append(Projectile(self.x, self.y+25, 15, 15, self.g, "clock.png", 15, 15, 4, self.projectile_speed*-1, -6, 150, self.p_gravity, 10))
        elif self.direction == RIGHT:
            game.enemy_projectiles.append(Projectile(self.x+self.img_w, self.y+25, 15, 15, self.g, "clock.png", 15, 15, 4, self.projectile_speed, -6, 150, self.p_gravity, 10))
    
    def follow(self):
        if ((game.hero.x - self.x)**2 + (game.hero.y - self.y)**2)**0.5 < self.followdistance:
            if game.hero.x < self.x:
                self.vx = 0

    def death(self):
        game.enemylist.remove(self)

class TimeWraith(Enemy):
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 64, 66, g, "wraith.png", "wraith_shriek.png", 64, 66, 7, 7, 4, 180, x_left, x_right, 100, 3, 10, 5, 3, False, False)

    def attack(self):
        if self.direction == LEFT:
            game.enemy_projectiles.append(ClockProjectile(self.x, self.y+25, self.g, -self.projectile_speed))
        elif self.direction == RIGHT:
            game.enemy_projectiles.append(ClockProjectile(self.x+self.img_w, self.y+25, self.g, self.projectile_speed))

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

class ClockProjectile(Projectile):
    def __init__(self, x, y, g, projectile_speed):
        Projectile.__init__(self, x, y, 15, 15, g, "clock.png", 15, 15, 4, projectile_speed, -6, 150, False, 10)

            
def drawMenu():
    background(255, 255, 255)
    stroke(0,0,0)
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
    if 100<=mouseX<=400 and 200<=mouseY<=300:
        stroke(0,255,0)
        rect(100, 200, 300, 100)
    
    elif 100<=mouseX<=400 and 400<=mouseY<=500:
        stroke(0,255,0)
        rect(100, 400, 300, 100)
    
    elif 100<=mouseX<=400 and 600<=mouseY<=700:
        stroke(0,255,0)
        rect(100, 600, 300, 100)
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
    elif key == 'Q' or key == 'q':
        game.hero.key_handler['Q'] = True

    
def keyReleased():
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.hero.key_handler[UP] = False
    elif keyCode == DOWN:
        game.hero.key_handler[DOWN] = False
    elif key == 'Q' or key == 'q':
        game.hero.key_handler['Q'] = False
        
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
        
