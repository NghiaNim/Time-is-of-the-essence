add_library('controlP5')
add_library('minim')

import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1920
HEIGHT = 1080
gameScreen = 0
gameground = 920
player = Minim(this)
main_theme = player.loadFile(path + "/Sound/main_theme.mp3")
main_theme.rewind()
main_theme.loop()


### The one class to contain them all ###
class Game:
    def __init__(self, w, h, g, hero):
        self.w = w # Width
        self.h = h # Height
        self.enemy_projectiles = [] # List of enemy projectiles
        self.hero_projectiles = [] # List of hero projectiles
        self.enemylist = [] # List of enemies
        self.itemlist = [] # List of items
        self.platformlist = [] # List of platfroms
        self.obstaclelist = [] # List of obstacles
        self.g = g # Ground level

        self.next_level = False
        self.background = loadImage(path + "/images/background.png")
        self.groundimg = loadImage(path + "/images/ground.png")
        self.freeze_lenght = 240 # Duration of freeze in frames
        self.frozen = False
        
        for line in level: # Text-file based level builder
            if line == '\n':
                break
            
            
            line = line.strip().split(',')
            if line[0] == 'TimeWraith':
                line = list(map(int, line[1:]))
                self.enemylist.append(TimeWraith(line[0],line[1],line[2],line[3],line[4]))

            if line[0] == 'Sound':
                global main_theme
                main_theme.close()
                main_theme = player.loadFile(path + "/Sound/" + line[1] + '.mp3')
                main_theme.rewind()
                main_theme.loop()
                
                
            elif line[0] == 'Worm':
                line = list(map(int, line[1:]))
                self.enemylist.append(Worm(line[0],line[1],line[2],line[3],line[4]))

            elif line[0] == 'TimeWizard':
                line = list(map(int, line[1:]))
                self.enemylist.append(TimeWizard(line[0],line[1],line[2],line[3],line[4]))

            elif line[0] == 'Bat':
                line = list(map(int, line[1:]))
                self.enemylist.append(Bat(line[0],line[1],line[2],line[3],line[4]))

            elif line[0] == 'Boss':
                line = list(map(int, line[1:]))
                self.enemylist.append(Reaper(line[0],line[1],line[2],line[3],line[4]))

            elif line[0] == 'BuffItem':
                line = list(map(int, line[1:]))
                self.itemlist.append(BuffItem(line[0],line[1],self.g,line[2]))

            elif line[0] == 'Wall':
                line = list(map(int, line[1:]))
                self.obstaclelist.append(Wall(line[0], line[1]))

            elif line[0] == 'SmallWall':
                line = list(map(int, line[1:]))
                self.obstaclelist.append(SmallWall(line[0], line[1]))

            elif line[0] == 'Platform':
                line = list(map(int, line[1:]))
                self.platformlist.append(Platform(line[0], line[1]))

            elif line[0] == 'ShortPlatform':
                line = list(map(int, line[1:]))
                self.platformlist.append(ShortPlatform(line[0], line[1]))

            elif line[0] == 'LongPlatform':
                line = list(map(int, line[1:]))
                self.platformlist.append(LongPlatform(line[0], line[1]))

            elif line[0] == 'end':
                global gameScreen
                gameScreen += 1


        #random sprite for hero
        if hero == 'Jack':
            self.hero = Jack(100, 752, 30, 48, self.g, 'SteamMan_run.png', 48, 48, 6, 'SteamMan_idle.png', 4, 'SteamMan_hurt.png', 3, 'SteamMan_jump.png', 6, 10, 4)
        elif hero == 'Jill':
            self.hero = Jill(100, 752, 30, 48, self.g, 'GraveRobber_run.png', 48, 48, 6, 'GraveRobber_idle.png', 4, 'GraveRobber_hurt.png', 3, 'GraveRobber_jump.png', 6, 17, 6)
        elif hero == 'John':
            self.hero = John(100, 752, 30, 48, self.g, 'Woodcutter_run.png', 48, 48, 6, 'Woodcutter_idle.png', 4, 'Woodcutter_hurt.png', 3, 'Woodcutter_jump.png', 6, 12, 5)
    
    def update(self):
        
        if self.enemylist == []:
            #random portal spawn
            random_cor = random.randint(500,1800)

            #check if portal will spawn in wall
            for obstacle in self.obstaclelist:
                while random_cor < obstacle.x < random_cor + 120 or random_cor < obstacle.x + obstacle.w < random_cor + 120:
                    random_cor = random.randint(120, 1800)
            self.enemylist.append(Portal(random_cor, self.g - 120, 120, 120))

        if self.frozen == True and frameCount - self.freezeStart > self.freeze_lenght: # Defreeze enemies after the duration has passed
            self.defreeze_enemies()

    
    def display(self): # Display all elements in the game
        self.update()
        fill(0,0,0)
        stroke(0,0,0)
        rect(0,self.g,WIDTH,HEIGHT)
        image(self.background, 0, 0)
        image(self.groundimg,0, 0)
        
        for e in self.enemylist:
            e.display()
            
        self.hero.display()

        for p in self.enemy_projectiles:
            p.display()
        for p in self.hero_projectiles:
            p.display()
        for i in self.itemlist:
            i.display()
        for o in self.obstaclelist:
            o.display()
        for p in self.platformlist:
            p.display()


    def freeze_enemies(self): # Causes enemies to freeze

        for e in self.enemylist:
            e.freeze = True
        self.freezeStart = frameCount # Makes framestamp of when it happened
        self.frozen = True

    def defreeze_enemies(self): # Enemie defreeze

        for e in self.enemylist:
            e.freeze = False
        self.frozen = False


### Mother of all classes - CREATION ###        
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

        # Changes the ground level if above platfrom or wall, bit more complex in order to avoid certain bugs
        changedg = False # registers if the ground should (and have) changed
        tmp_ground = 920
        if len(game.obstaclelist) != 0:
            for o in game.obstaclelist: # If above obstacle
                if self.y + self.h <= o.y and ((self.x + self.w >= o.x and self.x + self.w <= o.x + o.w) or (self.x <= o.x + o.w and self.x >= o.x)) or ((2*self.x+self.w)/2 <= o.x + o.w and (2*self.x+self.w)/2 >= o.x)  :
                    if tmp_ground > o.y:
                        tmp_ground = o.y
                    changedg = True
                    #break
        if len(game.platformlist) != 0: 
            for p in game.platformlist: # If above platform
                if self.y + self.h <= p.y and self.x + self.w >= p.x and self.x <= p.x + p.w:
                    if tmp_ground > p.y:
                        tmp_ground = p.y
                    changedg = True
                    #break
        if changedg == False: # If none is detected set the ground to the game ground
            self.g = game.g
        else:
            self.g = tmp_ground
                
    def update(self):
        self.gravity()
        
        #slow down animation
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
            
        self.x += self.vx
        self.y += self.vy


    # Collision detection which check for side overlaping, or more exactly whether the middle, left point or right point overlap with the target
    def collision_rect(self, target):
        if (((self.x < target.x + target.w) and (self.x + self.w > target.x)) or (((self.x*2+self.w)/2 < target.x+target.w) and ((self.x*2+self.w)/2) > target.x)) and (((self.y < target.y + target.h) and (self.y + self.h > target.y)) or ((self.y*2+self.h)/2 > target.y and ((self.y*2+self.h)/2 < target.y+target.h))):
            return True
        else:
            return False

    # Collision that would occur if the creation moves
    def collision_future(self, target):
        if (self.x + self.vx < target.x + target.w) and (self.x + self.w + self.vx > target.x) and (self.y + self.vy < target.y + target.h) and (self.y + self.vy + self.h > target.y):
            return True
        else:
            return False

    # Collision detection based on rectangle corner distances/overlapping detecting the side as well
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

        
    def display(self): # Basic display method
        self.update()
        #rect(self.x, self.y, self.w, self.h)      
        if self.direction == RIGHT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.direction == LEFT:
            image(self.img, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)

### Hero Class ###
class Hero(Creation):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, time, dmg, speed):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)
        self.key_handler = {LEFT:False, RIGHT:False, SHIFT:False, UP:False, DOWN:False, 'Q':False, 'E':False}
        self.standing_y = y
        self.standing_h = h
        self.direction = RIGHT
        self.img_idle = loadImage(path + "/images/" + img_name_idle)
        self.img_hurt = loadImage(path + '/images/' + img_name_hurt)
        self.img_jump = loadImage(path + '/images/' + img_name_jump)
        self.idle_num_frames = idle_num_frames
        self.hurt_num_frames = hurt_num_frames
        self.jump_num_frames = jump_num_frames

        self.autofire = False
        self.autofiretime = 0
        self.charges = self.base_charges

        self.reloadtime = 0

        self.time = time
        self.freeze = False
        self.freeze_time = 0

        self.buffed_time = 0

        self.knockback = False
        
        self.collission_countdown = 30 # How for how many frames should be hero invincible after detecting collsion?

        self.col_framestamp = frameCount

        self.shoot_framestamp = frameCount
        
        self.invincible = 0
        
        self.hit_right = False
        self.dmg = dmg
        self.base_dmg = dmg #default weapon damage

        self.active_ability_time = 0
        self.real_active_ability_cooldown = 0


        
        self.bullet_img = 'bullet.png'

        self.base_speed = speed
        self.speed = speed

        self.active_speed = 0 #for speed buff
        self.active_damage = 0 #for damage buff
        self.active_shooting_speed = 0 #for shooting speed buff
        
        self.gravityBullet = False
        self.gravityTime = 0

    def update(self):
        if self.autofire == True and frameCount%60 == 0:
            self.autofiretime -= 1
            if self.autofiretime == 0:
                self.autofire = False

        else:
            if self.charges == 0:
                self.charges -= 1
                self.reloadtime = 1*60

            if self.reloadtime > 0:
                self.reloadtime -= 1

                if self.reloadtime == 0:
                    self.charges = self.base_charges
                    
        if self.gravityBullet == True and frameCount%60 == 0:
            self.gravityTime -= 1
            if self.gravityTime < 0:
                self.gravityBullet = False



        self.gravity()
        if frameCount % 60 == 0 :
            if not self.freeze:
                self.time -= 1
            else:
                self.freeze_time -= 1
                if self.freeze_time < 0:
                    self.freeze = False
        
        if self.invincible < 0:
            self.hit_right = False
            
        if self.active_damage == 0:
            self.dmg = self.base_dmg

        elif frameCount %60 == 0:
            self.active_damage -= 1
        
        if self.gravityBullet == True:
            self.dmg = self.base_dmg * 1.2
            
        if self.active_speed == 0:
            self.speed = self.base_speed
        elif frameCount %60 == 0:
            self.active_speed -= 1

        if self.active_shooting_speed == 0:
            self.shootingspeed = self.base_shootingspeed
        elif frameCount %60 == 0:
            self.active_shooting_speed -= 1

        if frameCount %60 == 0 and self.real_active_ability_cooldown > 0:
            self.real_active_ability_cooldown -= 1

        #the player get hits, he won't be able to move for 35 frames but will retain invincibility for 25 more frames
        if self.knockback == False or self.invincible < 25:
            if self.invincible == 24:
                self.knockback = False
                
            if self.key_handler['Q'] == True and self.autofire == True:
                self.attack()
                    
            if self.key_handler[DOWN] == True and self.y+self.h == self.g:    
                self.vx = 0
                self.y = self.standing_y + self.standing_h/2
                self.h = self.standing_h/2
                
            else:
                
            
                self.y = self.standing_y
                self.h = self.standing_h
                
                if self.key_handler[LEFT]:
                    self.vx = -self.speed
                    self.direction = LEFT
                elif self.key_handler[RIGHT]:
                    self.vx = self.speed
                    self.direction = RIGHT
                else:
                    self.vx = 0
        
                if self.key_handler[SHIFT] == True and self.y+self.h == self.g:
                    if isinstance(self, Jill):
                        jump = player.loadFile(path + '/Sound/jump_Jill.mp3')
                    elif isinstance(self, Jack):
                        jump = player.loadFile(path + '/Sound/jump_Jack.mp3')
                    elif isinstance(self, John):
                        jump = player.loadFile(path + '/Sound/jump_John.mp3')
                        
                    jump.rewind()
                    jump.play()
                    self.vy = -9

            if self.key_handler['E'] == True and self.real_active_ability_cooldown == 0:
                self.special_ability()


        
        #knockback on hit
        else:
            if self.key_handler[DOWN] == True:
                self.y = self.standing_y
                self.h = self.standing_h
            if self.invincible == 59:

                #play random hurt sounds
                temp = random.randint(1,3)
                if isinstance(self, Jill):
                    hurt = player.loadFile(path + '/Sound/hurt_' + str(temp) + '_Jill.mp3')
                elif isinstance(self, Jack):
                    hurt = player.loadFile(path + '/Sound/hurt_' + str(temp) + '_Jack.mp3')
                elif isinstance(self, John):
                    hurt = player.loadFile(path + '/Sound/hurt_' + str(temp) + '_John.mp3') 

                hurt.rewind()
                hurt.play()
                self.vy = -5
            if self.hit_right and (self.y + self.h < self.g):
                self.vx = 7
            else:
                self.vx = -7
    
            if self.key_handler[SHIFT] == True and self.y+self.h == self.g:
                self.vy = -10


        
        #frames of animation based on action
        if frameCount%10 == 0 and self.vy != 0:
            self.frame = (self.frame + 1) % self.jump_num_frames
        elif frameCount%10 == 0 and self.vx == 0:
            self.frame = (self.frame + 1) % self.idle_num_frames
        elif frameCount%10 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames

        #chance to dodge attack
        if isinstance(self, Jill):
            temp = random.randint(1,8)
        elif isinstance(self, Jack):
            temp = random.randint(1,4)
        elif isinstance(self,John):
            temp = random.randint(1,13)

        #check for hit
        for enemy in game.enemylist:
            
            #check for endgame
            if isinstance(enemy, Portal) and (self.collision_rect_right(enemy) or self.collision_rect_left(enemy)) and enemy.frame > 40 :
                game.next_level = True

            elif isinstance(enemy, Portal):
                continue

            elif self.collision_rect_right(enemy) and self.invincible <= 0 and enemy.alive == True and not self.freeze:
                if temp != 1:
                    self.time -= int(enemy.dmg - self.armor)
                self.invincible = 60
                self.hit_right = True
                self.knockback = True

            elif self.collision_rect_left(enemy) and self.invincible <= 0 and enemy.alive == True and not self.freeze:
                if temp != 1:
                    self.time -= int(enemy.dmg - self.armor)
                self.invincible = 60
                self.knockback = True

        
        for projectile in game.enemy_projectiles:
            if self.collision_rect_right(projectile) and self.invincible <= 0 and not self.freeze:
                projectile.destroy()
                if temp != 1:               
                    self.time -= int(projectile.dmg - self.armor)
                self.invincible = 60
                self.hit_right = True
                self.knockback = True

            elif self.collision_rect_left(projectile) and self.invincible <= 0 and not self.freeze:
                projectile.destroy()
                if temp != 1:                
                    self.time -= int(projectile.dmg - self.armor)
                self.invincible = 60
                self.knockback = True

        future_collision = False
        if len(game.obstaclelist) != 0:
            for o in game.obstaclelist:
                if self.collision_future(o) == True:
                    future_collision = True
        if future_collision == False:
            self.x += self.vx
            
        if self.x < 0:
            self.x = 0
            
        elif self.x + self.w > 1920:
            self.x = 1920 - self.w
        
        self.y += self.vy
        self.standing_y += self.vy
        self.invincible -= 1


    def display(self):
        self.update()
        #rectangle to show hitbox

        # noFill()
        # fill(0,0,0)
        # # rect(self.x, self.y, self.w, self.h)
        
        
        if self.key_handler[DOWN] == True and self.y+self.h == self.g and self.direction == RIGHT:
            image(self.img_crouch, self.x, self.y, self.img_w - 9, 24, 2 * self.img_w, 16, 3 * self.img_w - 9, self.img_h)
            
        elif self.key_handler[DOWN] == True and self.y+self.h == self.g and self.direction == LEFT:
            image(self.img_crouch, self.x, self.y, self.img_w - 9, 24, 3 * self.img_w - 9, 16, 2 * self.img_w, self.img_h)

        elif self.invincible > 0 and self.direction == RIGHT and self.knockback == True:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 1 * self.img_w, 0, 2 * self.img_w - 18, self.img_h)

        
        elif self.invincible > 0 and self.direction == LEFT and self.knockback == True:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 2 * self.img_w - 18, 0, 1 * self.img_w, self.img_h)

        #animation for jumping
        elif self.vy != 0 and self.direction == RIGHT:
            image(self.img_jump, self.x, self.y, self.img_w - 18, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) *self.img_w - 18, self.img_h)
        elif self.vy != 0 and self.direction == LEFT:
            image(self.img_jump, self.x, self.y, self.img_w - 18, self.img_h, (self.frame + 1) * self.img_w - 18, 0, self.frame * self.img_w, self.img_h)

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

        #show invincible effect
        if self.invincible > 0:
            noFill()
            strokeWeight(1.5)
            stroke(255,255,0)

            ellipse(self.x + 15, self.y , 20, 8)
        
        textSize(20)
        fill(255,255,255)
        text('Remaining time: ' + str(self.time), 50, 30)
        text('(E) Ability cooldown: ' + str(self.real_active_ability_cooldown), 300, 30)

        if self.reloadtime != 0:
            fill(255,255,255)
            text('Reloading...', 100, 1000)

        if self.autofire == True:
            fill(0,255,0)
            text('Rapid-fire mode!', 400, 1000)

        if game.hero.buffed_time > 0:
            fill(0,255,0)
            text('DAMAGE UP!', 400, 1030)
            if frameCount % 60 == 0:
                game.hero.buffed_time -= 1
                
        if self.gravityBullet == True:
            fill(0,255,0)
            text('Heavy shots!', 400, 1060)

        if game.frozen == True:
            fill(0,255,0)
            text('Enemies are frozen!', 600, 1030)

        if game.hero.freeze == True:
            fill(0,255,0)
            text('Invincibility!', 600, 1060)



    def attack(self):
        
        if self.direction == LEFT:
            p_vx = -1
            p_vy = 0
            
        elif self.direction == RIGHT:
            p_vx = 1
            p_vy = 0        
            
        
        if self.key_handler[UP] == True:
            p_vy = -1
            if self.key_handler[LEFT]:
                p_vy = -.5
            elif self.key_handler[RIGHT]:
                p_vy = -.5
            else:
                p_vx = 0
            
        #Jill's passive
        if isinstance(self, Jill) and self.time <= 10:
            self.active_damage = 1

        if frameCount - self.shoot_framestamp > self.shootingspeed:
            self.shoot_framestamp = frameCount
            if not self.autofire:
                self.charges -= 1
            if self.active_damage == 0:
                self.bullet_img = 'bullet.png'
            else:
                self.bullet_img = 'bullet_up.png'
            
            if self.gravityBullet == True and not self.key_handler[UP]:
                game.hero_projectiles.append(Projectile(self.x, self.y+10, 10, 10, self.bullet_img, 16, 16, 5, 8*p_vx, -1.5, 150, self.gravityBullet, self.dmg))
            else:
                game.hero_projectiles.append(Projectile(self.x, self.y+10, 10, 10, self.bullet_img, 16, 16, 5, 8*p_vx, 8*p_vy, 150, self.gravityBullet, self.dmg))


    def invincible_buff(self, time):
        self.invincible = time*60

    def damage_buff(self, time):
        self.dmg = self.base_dmg * 2
        self.active_damage += time

    def shooting_speed_buff(self, time):
        self.shootingspeed = self.base_shootingspeed/2
        self.active_shooting_speed += time

    def speed_buff(self,time):
        self.speed = self.base_speed * 1.5
        self.active_speed += time

### Predefined heroes ###
class Jack(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, dmg, speed):
        self.base_charges = 8
        self.base_shootingspeed = 20
        self.shootingspeed = self.base_shootingspeed
        self.img_crouch = loadImage(path + "/images/Jack_crouch.png")
        
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, 85, dmg, speed)
        self.armor = 2
        self.active_ability_cooldown = 10
        self.active_ability_time = 3


        
    def special_ability(self):
        #blank 
        color(255,255,255)
        rect(0,0,WIDTH,HEIGHT)
        for projectile in game.enemy_projectiles:
            projectile.destroy()
        self.real_active_ability_cooldown = self.active_ability_cooldown
        pass
    
class Jill(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, dmg, speed):
        self.base_charges = 10
        self.base_shootingspeed = 15
        self.shootingspeed = self.base_shootingspeed
        self.img_crouch = loadImage(path + "/images/Jill_crouch.png")

        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, 45, dmg, speed)
        self.armor = 0
        self.active_ability_cooldown = 10
        self.active_ability_time = 3


    def special_ability(self):
        #beserk
        self.invincible_buff(self.active_ability_time)
        self.damage_buff(self.active_ability_time)
        self.shooting_speed_buff(self.active_ability_time)
        self.speed_buff(self.active_ability_time)
        
        self.real_active_ability_cooldown = self.active_ability_cooldown 

        
        pass
    
class John(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, dmg, speed):
        self.base_charges = 6
        self.base_shootingspeed = 22
        self.shootingspeed = self.base_shootingspeed
        self.img_crouch = loadImage(path + "/images/John_crouch.png")
        
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, 105, dmg, speed)
        self.armor = 4
        self.active_ability_time = 1
        self.active_ability_cooldown = 30


        
    def special_ability(self):

        #tank stomp
        stomp = self.dmg*3
        for enemy in game.enemylist:
            if isinstance(enemy,Portal):
                continue
            if enemy.flying == False:
                enemy.damage(stomp, LEFT)
                enemy.vy -= 3
                enemy.y += enemy.vy
                
            self.time -= self.dmg//2


        
        self.real_active_ability_cooldown = self.active_ability_cooldown 
        pass

### The base enemy class ###
class Enemy(Creation):

    def __init__(self, x, y, w, h, g, img_name, img_name_idle, img_name_death, img_w, img_h, num_frames, num_idle_frames, num_death_frames, attack_frame, aspd, xl, xr, hp, vx, dmg_projectile, dmg_collision, attack_count, droprate, follow=False, p_gravity=False, followdistance=0):

        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)

        # Attributes for idle animations
        self.img_idle = loadImage(path + "/images/" + img_name_idle)
        self.idle_frame = 0
        self.idle_count = 0
        self.num_idle_frames = num_idle_frames
        self.attack_frame = attack_frame
        self.idle = False
        # Attributes for death animations
        self.img_death = loadImage(path + "/images/" + img_name_death)
        self.num_death_frames = num_death_frames
        self.death_frame = 0
        # Atributes for attacks and behaviour
        self.alive = True
        self.hp = hp # Health points
        self.dmg = dmg_collision # Collision damage
        self.follow_bol = follow # Should the enemy follow the hero if within distance
        self.followdistance = followdistance # Following distance
        self.attackspeed = aspd # How many frames must pass per attack?
        self.projectile_bol = True # Does the enemy cast projectiles?
        self.projectile_speed = 4 # VX attribute of the casted projectile
        self.p_gravity = p_gravity # should the gravity apply on its projectiles
        self.dmg_projectile = dmg_projectile # Projectile dmg
        self.droprate = droprate
        self.attack_count = attack_count
        self.attacked_cnt = 0 #records the series of attacks
        self.time_buff = 15 # Time buff for the time item
        # Attributes for backend functions
        self.framestart = frameCount # Gives framestamp of initioation
        self.direction = random.choice([LEFT, RIGHT]) # Walking direction
        self.flying = False # Flying boolean
        self.freeze = False # Is timefreeze active?
        self.death_sound = player.loadFile(path + "/Sound/enemy_death.mp3")
        self.hit_sound = player.loadFile(path + "/Sound/enemy_hit.mp3")
        self.sfx = False # Boolean for ability sfx (mainly for bosses only so there aren't too many sounds mixing)
        
        # Movement values
        self.vx = vx
        if self.direction == LEFT:
            self.vx *= -1
        self.xleft = xl #left X boundary
        self.xright = xr # right x boundary
        self.tmp_vx = 0
        


    def update(self):
        if self.alive == True:
            self.gravity()


            # Idle and attack loop (enemy will stop walking so he can attack), won't trigger when the enemy is frozen
            if self.freeze == False:
                if frameCount - self.framestart > self.attackspeed: # Checks for attack cooldown
                    if self.idle == False:
                        self.tmp_vx = self.vx #stores the vx value
                        self.vx = 0
                        self.idle = True
                        if self.sfx == True:
                            self.ability_sound.rewind()
                            self.ability_sound.play()
                    if self.attacked_cnt < self.attack_count and self.attack_frame-1 == self.idle_frame and frameCount%10 == 0:
                        if self.projectile_bol == True: #Does the enemy shoot projectiles?
                            self.attack()
                        self.attacked_cnt += 1 # Counter for how many attacks were made   
                    if self.idle_frame == 0 and self.attacked_cnt == self.attack_count: # If the animation finished its loop and the enemy made enough attacks resume walking
                        self.framestart = frameCount
                        self.vx = self.tmp_vx
                        self.idle = False
                        self.attacked_cnt = 0
            
            # If the enemy should follow the hero this will change its direction
            if self.follow_bol == True:
                self.follow()

            # Checks for the "boundaries", if the next step shall make move it outside the boundary turn around
            if self.x+self.vx < self.xleft:
                self.vx *= -1
                self.direction = RIGHT
            elif self.x+self.vx > self.xright:
                self.vx *= -1
                self.direction = LEFT

            # Check for obstacles
            for o in game.obstaclelist:
                # This will check whether the next "step" will be within the obstacle, if so, turn around
                if (self.x + self.vx >= o.x and self.x + self.vx <= o.x + o.w) or (self.x + self.w + self.vx >= o.x and self.x+self.w + self.vx <= o.x + o.w) and ((self.y>=o.y and self.y<=o.y+o.h) or (self.y+self.h >= o.y and self.y+self.h <= o.y+o.h)):
                    self.vx *= -1
                    if self.direction == LEFT:
                        self.direction = RIGHT
                    else:
                        self.direction = LEFT

            # Collision with projectiles
            for p in game.hero_projectiles:
                if self.collision_rect(p) == True:
                    self.damage(p.dmg, RIGHT)
                    p.destroy()
                # if self.collision_rect_left(p) == True:
                #     self.damage(p.dmg, LEFT) # Cause damage to self
                #     p.destroy() # Destroy the projectile
                # elif self.collision_rect_right(p) == True:
                #     self.damage(p.dmg, RIGHT)
                #     p.destroy()

            #slow down animation
            if frameCount%10 == 0:
                self.frame = (self.frame + 1) % self.num_frames
            # slow down idle frames
            if self.vx == 0 and frameCount%10 == 0:
                self.idle_frame = (self.idle_frame + 1) % self.num_idle_frames
            elif self.vx != 0:
                self.idle_frame = 0
                self.idle_count = 0

            if self.hp <= 0: # If the HP falls below zero, trigger death animation and turn of some behaviour (e.g. collision)
                self.death()
                self.death_sound.rewind()
                self.death_sound.play()

            if self.freeze == False:
                self.x += self.vx
                self.y += self.vy

        elif self.alive == False: # Cause death animation and self-removal
            if frameCount%10 == 0:
                self.death_frame = self.death_frame + 1
                if self.death_frame >= self.num_death_frames: # has the aniamation completed?
                    self.destroy()

    def display(self):
        self.update() 
        #rect(self.x, self.y, self.w, self.h)
        if self.alive == True:      
            if self.vx != 0 and self.direction == RIGHT: # Walking animation
                image(self.img, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.vx != 0 and self.direction == LEFT:
                image(self.img, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == RIGHT: # Idle animation
                image(self.img_idle, self.x, self.y, self.img_w, self.img_h, self.idle_frame * self.img_w, 0, (self.idle_frame + 1) * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == LEFT:
                image(self.img_idle, self.x, self.y, self.img_w, self.img_h, (self.idle_frame + 1) * self.img_w, 0, self.idle_frame * self.img_w, self.img_h)
        elif self.alive == False: #Death animation
            if self.direction == RIGHT:
                image(self.img_death, self.x, self.y, self.img_w, self.img_h, self.death_frame * self.img_w, 0, (self.death_frame + 1) * self.img_w, self.img_h)
            if self.direction == LEFT:
                image(self.img_death, self.x, self.y, self.img_w, self.img_h, (self.death_frame + 1) * self.img_w, 0, self.death_frame * self.img_w, self.img_h)


    # This is default projectile attack, though this one is used mainly in developement stage 
    def attack(self):
        if self.direction == LEFT:
            game.enemy_projectiles.append(Projectile(self.x, self.y+25, 15, 15, "clock.png", 15, 15, 4, self.projectile_speed*-1, -6, 150, self.p_gravity, self.dmg_projectile))
        elif self.direction == RIGHT:
            game.enemy_projectiles.append(Projectile(self.x+self.w, self.y+25, 15, 15, "clock.png", 15, 15, 4, self.projectile_speed, -6, 150, self.p_gravity, self.dmg_projectile))
    
    def follow(self): # This will detect where the hero (which side) is and change the direction of the enemy accordingly

        if ((game.hero.x - self.x)**2 + (game.hero.y - self.y)**2)**0.5 < self.followdistance: # Is the enemy in the follow distance?
            if game.hero.x < self.x: # Is the enemy to the left?
                if self.vx > 0: # Is the enemy going the opposite direction?
                    self.vx *= -1
                    self.direction = LEFT
                elif self.vx < 0: # 
                    pass
                    #potentional new behaviour
            elif game.hero > self.x: # Is the enemy to the right?
                if self.vx < 0: # Is the enemy going the opposite direction?
                    self.vx *= -1
                    self.direction = RIGHT
                elif self.vx > 0:
                    pass
        else:
            pass


    def death(self): # Simply changes the boolean upon which other conditions depend
        self.alive = False

    def damage(self, dmg, dir): #Knockback and self-damage implication, theoretical knockback to the sides if desirable, but without it the game is harder which is desirable
        self.hit_sound.rewind()
        self.hit_sound.play()
        self.vy -= 3
        self.hp -= dmg

    def destroy(self): # Trigger self-removal form the enemy list and potentially cause an item to drop
        rand_int = random.randint(0,100)
        if rand_int < self.droprate:
            rand_int2 = random.choice([0,1])
            if rand_int2 == 0:
                game.itemlist.append(TimeItem(self.x, self.y, self.g, self.time_buff)) #Time Item
            elif rand_int2 == 1:
                game.itemlist.append(BuffItem(self.x, self.y, self.g)) # Random buff item
        game.enemylist.remove(self)

class TimeWraith(Enemy): # Predefined enemy - Wraith
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 40, 52, g, "wraith.png", "wraith_shriek.png", "wraith_death.png", 64, 52, 7, 7, 7, 4, 140, x_left, x_right, 75, 2.5, 10, 5.5, 2, 50, True, False, 100)

    def attack(self): #Wraith unique attack
        if self.direction == LEFT:
            game.enemy_projectiles.append(ClockProjectile(self.x, self.y+5, -self.projectile_speed, self.dmg_projectile))
        elif self.direction == RIGHT:
            game.enemy_projectiles.append(ClockProjectile(self.x+self.w, self.y+5, self.projectile_speed, self.dmg_projectile))

    # Wraith has its own display method for discrepancies in its sprite. Given my lack of experience with photoshop or any graphical program this is easier
    def display(self):
        self.update()
        if self.alive == True:      
            if self.vx != 0 and self.direction == RIGHT:
                image(self.img, self.x-14, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.vx != 0 and self.direction == LEFT:
                image(self.img, self.x-14, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == RIGHT:
                image(self.img_idle, self.x-14, self.y, self.img_w, self.img_h, self.idle_frame * self.img_w, 0, (self.idle_frame + 1) * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == LEFT:
                image(self.img_idle, self.x-14, self.y, self.img_w, self.img_h, (self.idle_frame + 1) * self.img_w, 0, self.idle_frame * self.img_w, self.img_h)
        elif self.alive == False:
            if self.direction == RIGHT:
                image(self.img_death, self.x-14, self.y, self.img_w, self.img_h, self.death_frame * self.img_w, 0, (self.death_frame + 1) * self.img_w, self.img_h)
            if self.direction == LEFT:
                image(self.img_death, self.x-14, self.y, self.img_w, self.img_h, (self.death_frame + 1) * self.img_w, 0, self.death_frame * self.img_w, self.img_h)

class Worm(Enemy): # Predefined enemy - Worm, or snail, whichever makes you happier
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 36, 64, g, "worm.png", "worm_idle.png", "worm_death.png", 36, 64, 6, 6, 3, 2, 220, x_left, x_right, 60, 2, 0, 12, 1, 70, True, False, 350)
        self.projectile_bol = False # Does the enemy cast projectiles?

class TimeWizard(Enemy): # Predefined enemy - Time Wizard, probably biggest PITA
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 60, 80, g, "TimeWizard.png", "TimeWizard.png", "TimeWizard_death.png", 320, 320, 4, 4, 12, 4, 200, x_left, x_right, 100, 3, 10, 5.5, 3, 70, False, False, 100)
        self.projectile_speed = 7 # VX attribute of the casted projectile

    def display(self): # Again hitbox didn't match the sprite and yada yada, this this fixes the image display
        self.update()
        if self.alive == True:      
            if self.vx != 0 and self.direction == RIGHT:
                image(self.img, self.x-50, self.y-80, self.img_w//2, self.img_h//2, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.vx != 0 and self.direction == LEFT:
                image(self.img, self.x-50, self.y-80, self.img_w//2, self.img_h//2, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == RIGHT:
                image(self.img_idle, self.x-50, self.y-80, self.img_w//2, self.img_h//2, self.idle_frame * self.img_w, 0, (self.idle_frame + 1) * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == LEFT:
                image(self.img_idle, self.x-50, self.y-80, self.img_w//2, self.img_h//2, (self.idle_frame + 1) * self.img_w, 0, self.idle_frame * self.img_w, self.img_h)
        elif self.alive == False:
            if self.direction == RIGHT:
                image(self.img_death, self.x-50, self.y-80, self.img_w//2, self.img_h//2, self.death_frame * self.img_w, 0, (self.death_frame + 1) * self.img_w, self.img_h)
            if self.direction == LEFT:
                image(self.img_death, self.x-50, self.y-80, self.img_w//2, self.img_h//2, (self.death_frame + 1) * self.img_w, 0, self.death_frame * self.img_w, self.img_h)

    def attack(self): # TimeWizard specific attack
            game.enemy_projectiles.append(SmallFireball(self.x, self.y+5, -self.projectile_speed, self.dmg_projectile, self.p_gravity))
            game.enemy_projectiles.append(SmallFireball(self.x+self.w, self.y+5, self.projectile_speed, self.dmg_projectile, self.p_gravity))

class Bat(Enemy): # A flying enemy!
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 32, 32, g, "bat.png", "bat_attack.png", "bat_death.png", 32, 32, 7, 5, 3, 3, 60, x_left, x_right, 30, 2, 10, 5, 1, 70, False, True, 100)
        self.flying = True
        self.g = y

    def attack(self):
            game.enemy_projectiles.append(BatBall(self.x, self.y, 0, self.dmg_projectile, self.p_gravity))

    def gravity(self): # Customized gravity, without check for platforms and walls
        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.h + self.vy > self.g:
                self.vy = self.g - (self.y + self.h)

class Reaper(Enemy): # The boss, the one and only, or until we add another
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 75, 100, g, "reaper.png", "reaper_attack.png", "reaper_death.png", 100, 100, 8, 12, 20, 7, 200, x_left, x_right, 350, 3, 10, 5.5, 1, 100, False, False, 100)
        self.attackmode = 0 # Yes! He has multiple attack modes :)
        self.barrage_cnt = 13 # Number of projectiles
        self.sidebarrage_cnt = 40 # Number of projectiles
        self.death_sound = player.loadFile(path + "/Sound/reaper_death.mp3")
        self.ability_sound = player.loadFile(path + "/Sound/reaper_ability.mp3")
        self.sfx = True

    def display(self): # It is hard to find the perfect sprite
        self.update()
        if self.alive == True:      
            if self.vx != 0 and self.direction == RIGHT:
                image(self.img, self.x-50, self.y-65, self.img_w*2, self.img_h*2, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.vx != 0 and self.direction == LEFT:
                image(self.img, self.x-70, self.y-65, self.img_w*2, self.img_h*2, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == RIGHT:
                image(self.img_idle, self.x-50, self.y-65, self.img_w*2, self.img_h*2, self.idle_frame * self.img_w, 0, (self.idle_frame + 1) * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == LEFT:
                image(self.img_idle, self.x-70, self.y-65, self.img_w*2, self.img_h*2, (self.idle_frame + 1) * self.img_w, 0, self.idle_frame * self.img_w, self.img_h)
        elif self.alive == False:
            if self.direction == RIGHT:
                image(self.img_death, self.x-70, self.y-65, self.img_w*2, self.img_h*2, self.death_frame * self.img_w, 0, (self.death_frame + 1) * self.img_w, self.img_h)
            if self.direction == LEFT:
                image(self.img_death, self.x-70, self.y-65, self.img_w*2, self.img_h*2, (self.death_frame + 1) * self.img_w, 0, self.death_frame * self.img_w, self.img_h)

        # Health bar
        stroke(0)
        fill(255,255,255)
        textSize(25)
        text('Time Reaper', 300,62)
        fill(255,0,0)
        noFill()
        rect(300,80,self.hp*5, 25)
        fill(255,0,0)
        rect(300,80,self.hp*5, 25)

    def attack(self):
        if self.attackmode == 0: # Different attack per mode
            for n in range(self.barrage_cnt): # Projectiles rain from the above!
                game.enemy_projectiles.append(BigClock((1920/self.barrage_cnt*n)-64, random.randint(0,200), 0, self.dmg_projectile, True))
        elif self.attackmode == 1:
            for n in range(self.sidebarrage_cnt): # Projectiles rain from the sides?
                x = random.choice([0, 1920])
                if x == 0:
                    p_dir = 1
                else:
                    p_dir = -1
                game.enemy_projectiles.append(MiniFireball(x, 920/self.sidebarrage_cnt*n, self.projectile_speed*p_dir, self.dmg_projectile, False))
        elif self.attackmode == 2: # Enemies rain at oddly specfic locations
            for n in range(random.choice([1,2,2,2,3])): # 20% chance for 1 or 3 enemies, 60% chance for 2
                rand_enemy = random.choice([1,2,3,4])
                x = random.choice([300, 1600])
                y = random.choice([300, 600, 700, 750, 800])
                if rand_enemy == 1:
                    game.enemylist.append(Bat(x, y, y, 0, 1920))
                elif rand_enemy == 2:
                    game.enemylist.append(TimeWraith(x, y, game.g, 0, 1920))
                elif rand_enemy == 3:
                    game.enemylist.append(TimeWizard(x, y, game.g, 0, 1920))
                elif rand_enemy == 4:
                    game.enemylist.append(Worm(x, y, game.g, 0, 1920))
        elif self.attackmode == 3: # Simple projectile attack
            game.enemy_projectiles.append(ClockProjectile(self.x, self.y, 7, self.dmg_projectile, True))
            game.enemy_projectiles.append(BigClock(self.x, self.y, 3.5, self.dmg_projectile, False))
            game.enemy_projectiles.append(ClockProjectile(self.x+self.w, self.y, -7, self.dmg_projectile, True))
            game.enemy_projectiles.append(BigClock(self.x+self.w, self.y, -3.5, self.dmg_projectile, False))
        self.attackmode = (self.attackmode+1)%4 # Attack mode alternator

### Projectile class ###
class Projectile(Creation):

    def __init__(self, x, y, w, h, img_name, img_w, img_h, num_frames, vx, vy, framespan, gravity, dmg, wallhack=False):
        Creation.__init__(self, x, y, w, h, game.g, img_name, img_w, img_h, num_frames)
        self.vx = vx
        self.vy = vy
        self.framespan = framespan #How many frames should the projectile exist
        self.framestart = frameCount # When was the projectile created
        self.gravitycheck = gravity # Should gravity apply? T/F
        self.dmg = dmg # How much damage should this projectile cause?
        self.wallhack = wallhack # If true, the projectile won't get destroyed upon impact with obstacle

        if self.vx > 0: # Detects the direction
            self.direction = RIGHT
        else:
            self.direction = LEFT 

    # Projectiles will have stripped gravity as we don't want their ground level to change
    def gravity(self):

        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.1
            if self.y + self.h + self.vy > self.g:
                self.vy = self.g - (self.y + self.h)

    def update(self):

        #slow down animation
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
        
        if self.gravitycheck == True:
            self.gravity()
            self.y += self.vy    
        self.x += self.vx
        self.y += self.vy

        # If the projectile exceeds its framespan, it ought not to exist anymore
        if frameCount - self.framestart > self.framespan:
            self.destroy()

        if self.y+self.h > game.g: # If the projectiles hits the ground, it shall perish
            self.destroy()

    def destroy(self): # Plain projectile self-removal

        if self in game.enemy_projectiles:
            game.enemy_projectiles.remove(self)
        elif self in game.hero_projectiles:
            game.hero_projectiles.remove(self)

#### Predefined projectiles ####
class ClockProjectile(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity=True):
        Projectile.__init__(self, x, y, 15, 15, "clock.png", 15, 15, 4, projectile_speed, -2, 150, gravity, dmg)

class SmallFireball(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity):
        Projectile.__init__(self, x, y, 50, 29, "SmallFireball.png", 72, 29, 4, projectile_speed, 0, 150, gravity, dmg)

class MiniFireball(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity):
        Projectile.__init__(self, x, y, 19, 16, "minifireball.png", 19, 16, 3, projectile_speed, 0, 230, gravity, dmg, True)

class BatBall(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity):
        Projectile.__init__(self, x, y, 32, 32, "batball.png", 32, 32, 4, projectile_speed, 0, 350, gravity, dmg)

class BigClock(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity):
        Projectile.__init__(self, x, y, 64, 64, "bigclock.png", 64, 64, 5, projectile_speed, 0, 350, gravity, dmg, True)

### Item Class ###
class Item(Creation):

    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, autopick):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)
        self.autopick = autopick # possible change if we decide to make non-autopickable items
        self.direction = RIGHT #Just so that the image displayment works

    def destroy(self): # Easy self removal
        game.itemlist.remove(self)

class TimeItem(Item): # Adds time to the hero

    def __init__(self, x, y, g, time):
        Item.__init__(self, x, y, 32, 32, g, "clockitem.png", 32, 32, 6, True)
        self.time = time


    def update(self):
        Creation.update(self)

        if self.collision_rect(game.hero) == True:
            game.hero.time += self.time
            self.destroy()

class BuffItem(Item): # Various buffs for the hero
    def __init__(self, x, y, g, effect = random.randint(1,5)):
        if effect == 1:
            self.item = 'Apple'
        elif effect == 2:
            self.item = 'Bananas'
        elif effect == 3:
            self.item = 'Melon'
        elif effect == 4:
            self.item = 'Orange'
        elif effect == 5:
            self.item = 'Pineapple'
            
        Item.__init__(self, x, y, 32, 32, g, self.item + ".png", 32, 32, 17, True)

    def update(self):
        Creation.update(self)

        if self.collision_rect(game.hero) == True:
                    
            #double damage and attack speed
            if self.item == 'Apple':
                game.hero.damage_buff(5)
                game.hero.shooting_speed_buff(5)
                game.hero.buffed_time = 5
                pass
            
            #rapid-fire
            elif self.item == 'Bananas':
                game.hero.autofire = True
                game.hero.autofiretime = 10 
                pass 
                    
            #time stands (or basically can't take damage)
            elif self.item == 'Melon':
                game.hero.freeze = True
                game.hero.freeze_time = 7
                pass
                
            #gravity bullet
            elif self.item == 'Orange':
                game.hero.gravityBullet = True
                game.hero.gravityTime = 10
                pass

            #time freeze
            elif self.item  == 'Pineapple':
                game.freeze_enemies()

            self.destroy()

### Obstacle class which doesn't allow enemies and heroes to pass, changes ground level and consumes projectiles ###
class Obstacle(Creation): 

    def __init__(self, x, y, w, h, img_name, img_w, img_h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.num_frames = 1
        self.frame= 0
        self.direction = RIGHT

    def update(self):
        
        # Destroy all projectiles that hit the obstacle
        for p in game.enemy_projectiles:
            if self.collision_rect(p) and p.wallhack == False:
                p.destroy()
        for p in game.hero_projectiles:
            if self.collision_rect(p) and p.wallhack == False:
                p.destroy()

class Wall(Obstacle):
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, 69, 80, "wall.png", 69, 80)

class SmallWall(Obstacle):
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, 46, 40, "smallwall.png", 46, 40)

class Platform(Obstacle):
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, 256, 30, "platform.png", 256, 30)

class ShortPlatform(Obstacle):
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, 100, 30, "shortplatform.png", 100, 30)

class LongPlatform(Obstacle):
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, 448, 30, "longplatform.png", 448, 30)

### Portal to next "level"
class Portal(Creation):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img_w = 320
        self.img_h = 320
        self.frame = 0
        self.img = loadImage(path + "/images/portal_sprites/sprite_0" + str(self.frame) + '.png')


    def update(self):
            if self.frame < 10 and frameCount % 2 == 0:
                self.img = loadImage(path + "/images/portal_sprites/sprite_0" + str(self.frame) + '.png')
                self.frame += 1
            elif self.frame <= 40 and frameCount % 2 == 0:
                self.img = loadImage(path + "/images/portal_sprites/sprite_" + str(self.frame) + '.png')
                self.frame += 1

        

    def display(self):
        self.update()
        image(self.img, self.x, self.y, self.w, self.h)

    
### Menu ###           
def drawMenu_1():
    img = loadImage(path + "/images/main_menu.jpg")
    image(img,0,0)

    img_title = loadImage(path + "/images/title.png")
    image(img_title, 1250, 0)

    textSize(50)
    fill(255,255,255)
    text('Play', 200, 270)

    text('Control', 200, 470)

    text('Quit', 200, 670)

    if 100<=mouseX<=400 and 200<=mouseY<=300:
        fill(0,255,0)
        text('Play', 200, 270)

    elif 100<=mouseX<=400 and 400<=mouseY<=500:
        fill(0,255,0)
        text('Control', 200, 470)
    
    elif 100<=mouseX<=400 and 600<=mouseY<=700:
        fill(0,255,0)
        text('Quit', 200, 670)

def drawMenu_2():
    img = loadImage(path + "/images/menu_2.jpg")
    image(img,0,0)

    img_title = loadImage(path + "/images/title.png")
    image(img_title, 1250, 0)

    fill(0,68,129)
    textSize(70)
    text('CHARACTER SELECT', 200, 150)

    fill(255,255,255)
    text('McMillian Sondai\'el', 200, 370)

    text('Jody Howar Glas', 200, 570)

    text('Peterpen Julumn', 200, 770)

    if 100<=mouseX<=850 and 300<=mouseY<=400:
        fill(0,255,0)
        text('McMillian Sondai\'el', 200, 370)

        #description
        fill(255,255,255)
        textSize(25)
        text('In the year 2092, robots have risen up to become the dominant', 1000, 350)
        text('species on Earth. Despite their machine minds and machine', 1000, 380)
        text('hearts, they too cannot escape the unstoppable grasp of time.', 1000, 410)
        text('Robots too must work to buy oil and pay electricity bills', 1000, 440)
        text('of course! McMillian is one such robot, and he is determined', 1000, 470)
        text('once and for all to set the bill with time!', 1000, 500)
        fill(220,20,30)
        textSize(35)
        text('Active ability: Blank', 1000, 570)
        fill(255,255,255)
        textSize(25)
        text('Removes all enemies projectile',1000, 610)
        fill(220,20,30)
        textSize(35)
        text('Passive ability: Robot armor', 1000, 670)
        fill(255,255,255)
        textSize(25)
        text("Thanks to the advance of modern technology, and ol' reliable duct", 1000, 710)
        text("tape, McMillian is equipped with the state of the art Model MXXI Steel", 1000, 740)
        text("Back Hydro-powered X15600008 A46 B80 C1 (New Gen) D808 RGB-CMYK", 1000, 770)
        text("Z00000P B-side RevolverZ RTX 300080 Cs306900TXT Pure-Bred Non-GMO", 1000, 800)
        text("FFS SME SMB Wifi 80001.01 Nvidia AMD Intel@ Trade-marked Armor", 1000, 830)
        text("This allows him to have a chance of absorbing hits and protect", 1000, 860)
        text("his time! The armor is at least harder than paper so he can take", 1000, 890)
        text("some hits and pack a punch!", 1000, 920)
        fill(220,20,30)
        textSize(35)
        text('Description: medium defense, medium damage,', 1000, 990)
        text('as much time as a robot can have', 1000, 1030)

        
    
    elif 100<=mouseX<=760 and 500<=mouseY<=600:
        fill(0,255,0)
        text('Jody Howar Glas', 200, 570)

        #description
        fill(255,255,255)
        textSize(25)
        text('Born in one of the harshest place in the world, filled with dangerous,', 1000, 350)
        text('cut-throat criminals who swindle, steal from others for their livelihood', 1000, 380)
        text('(I\'m of course talking about New York City), Jody had grown up to be a ', 1000, 410)
        text('very tough girl, who always carries with her her grandmother\'s cherished', 1000, 440)
        text('blade. Her father was a typical businessman on WallStreet who died', 1000, 470)
        text('because of overworking, and because of this, she could never spend time ', 1000, 500)
        text('with him. With a desire to take back those lost time, she goes on a quest ', 1000, 530)
        text('to kill Time!', 1000, 560)
        fill(220,20,30)
        textSize(35)
        text('Active ability: Bezerk', 1000, 600)
        fill(255,255,255)
        textSize(25)
        text('Daddy issues and years of neglect have made Jody\'s temper very short.',1000, 640)
        text('Gains double damage and double attackspeed on activation',1000, 670)
        fill(220,20,30)
        textSize(35)
        text('Passive ability: Cursed blade', 1000, 730)
        fill(255,255,255)
        textSize(25)
        text("Unknown to Jody herself, the blade she carries with her holds immense ", 1000, 770)
        text("power, she can attack very fast with very high damage. This becomes ", 1000, 800)
        text("especially true when her time nears its limit. Her movement speed is", 1000, 830)
        text("exceptionally high due to years and years of running away from her  ", 1000, 860)
        text("emotional problems. In return for the blade's power, her time is very  ", 1000, 890)
        text("limited and she must always be on the attack!", 1000, 920)
        fill(220,20,30)
        textSize(35)
        text('Description: low defense, very high damage,', 1000, 960)
        text('average attention span of a teenager for time', 1000, 1000)
    
    elif 100<=mouseX<=760 and 700<=mouseY<=800:       
        fill(0,255,0)
        text('Peterpen Julumn', 200, 770)
        
        #description
        fill(255,255,255)
        textSize(25)
        text('Born in the wild Scandinavian woods, Pete was raised by a pack of', 1000, 350)
        text('snow wolves and became a natural hunter at a young age. He does' , 1000, 380)
        text('not remember his real parents; the only clue he had was an axe', 1000, 410)
        text('that was there besides him ever since he could remember. Regardless,', 1000, 440)
        text('Pete would not trade a single thing for the exciting life he has had.', 1000, 470)
        text('Everyday is a struggle, being the hunter or the hunted, though he was ' , 1000, 500)
        text('almost always the former. He loves this life, but time is threatening', 1000, 530)
        text('to take him away! Before his old age catches up, better take care of time!', 1000, 560)
        fill(220,20,30)
        textSize(35)
        text('Active ability: Stomp', 1000, 600)
        fill(255,255,255)
        textSize(25)
        text('His extremely large and muscular stature grants him immense strength. On',1000, 640)
        text('activation, he stomps the ground hard enough to cause a mini earthquake,',1000, 670)
        text('dealing damage to all ground enemies while hurting his foot in the process.',1000, 700)
        fill(220,20,30)
        textSize(35)
        text('Passive ability: Bigfoot', 1000, 760)
        fill(255,255,255)
        textSize(25)
        text("His giant feet are not the only defining feature of Pete (although it", 1000, 800)
        text("does explain somewhat his powerful stomp). Pete is Bigfoot. Literally.", 1000, 830)
        text("The infamous bigfoot photo was just him taking a stroll in his usual wood!", 1000, 860)
        text("But as expected of bigfoot, he is strong and tanky, having thick skin but", 1000, 890)
        text("slow movement because of it. His armor stat is very high.", 1000, 920)
        fill(220,20,30)
        textSize(35)
        text('Description: very high defense, low damage,', 1000, 960)
        text('as much time he has left if not for his', 1000, 1000)
        text('inability to count.', 1000, 1040)
    pass

def drawGame():
    global game, level
    game.display()
    if game.hero.time < 0:
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)

    if game.next_level == True:
        global real_time
        real_time = game.hero.time
        game = Game(WIDTH, HEIGHT, gameground, hero) 
        game.hero.time = real_time

def drawControl():
    background(0)
    fill(255,255,255)
    
    textSize(50)
    text('MOVEMENTS', 200, 370)
    text('ATTACKS', 1000, 370)
    text('BACK', 1700, 900)
    
    textSize(30)
    text('LEFT RIGHT ARROW KEYS: move sideways', 200, 450)
    text('LEFT SHIFT: jump', 200, 500)
    text('DOWN ARROW KEY: crouch', 200, 550)
    text('UP ARROW KEY: aim up', 200, 600)

    text('Q (Normal): Fire (press and release)', 1000, 450)
    text('Q (Rapid-fire-mode): Fire (hold)', 1000, 500)
    text('E: Special ability', 1000, 550)

    if 1650<=mouseX<=1850 and 820<=mouseY<=920:
        textSize(50)
        fill(0,255,0)
        text('BACK', 1700, 900)



### End screen ###
def drawEnd():
    end_img = loadImage(path + "/images/end_menu.jpg")
    image(end_img,0,0)

    stroke(0,0,0)
    fill(48,93,228)
    textSize(50)
    text('You have successfully destroyed time', 500, 200)
    text('Enjoy your eternal meaningless existence', 460, 260)
    textSize(20)
    text('(Or press R to go back to character select)', 750, 300)
        
def setup():
    size(WIDTH, HEIGHT)
    fullScreen()
    
def draw():
    if gameScreen == 0:
        drawMenu_1()
    elif gameScreen == 1:
        drawMenu_2()
    elif gameScreen == 2:
        drawGame()
    elif gameScreen == 3:
        drawEnd()
    elif gameScreen == 'help':
        drawControl()
    
### Key & Mouse-click Handlers ###
def keyPressed():
    global gameScreen, main_theme
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = True
    elif keyCode == SHIFT:
        game.hero.key_handler[SHIFT] = True
    elif keyCode == UP:
        game.hero.key_handler[UP] = True        
    elif keyCode == DOWN:
        game.hero.key_handler[DOWN] = True 
    elif key == 'Q' or key == 'q':
        game.hero.key_handler['Q'] = True
    elif key == 'E' or key == 'e':
        game.hero.key_handler['E'] = True
    if gameScreen == 3 and (key == 'R' or key == 'r'):
        main_theme.close()
        main_theme = player.loadFile(path + "/Sound/main_theme.mp3")
        main_theme.rewind()
        main_theme.loop()
        gameScreen = 1
        
def keyReleased():
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = False
    elif keyCode == SHIFT:
        game.hero.key_handler[SHIFT] = False
    elif keyCode == UP:
        game.hero.key_handler[UP] = False
    elif keyCode == DOWN:
        game.hero.key_handler[DOWN] = False 
    elif key == 'Q' or key == 'q':
        game.hero.key_handler['Q'] = False
        if game.hero.reloadtime == 0:
            game.hero.attack()

    elif key == 'E' or key == 'e':
        game.hero.key_handler['E'] = False
        
def mousePressed():
    global gameScreen,game,hero,level
    #Choose Jack
    if gameScreen == 0 and 100<=mouseX<=400 and 400<=mouseY<=500:
        gameScreen = 'help'

    if gameScreen == 'help' and 1700<=mouseX<=1900 and 800<=mouseY<=1000:
        gameScreen = 0

    if gameScreen == 0 and 100<=mouseX<=400 and 600<=mouseY<=700:
        exit()

    if gameScreen == 0 and 100<=mouseX<=400 and 200<=mouseY<=300:
        gameScreen = 1

    #Choose Jack
    elif gameScreen == 1 and 100<=mouseX<=850 and 300<=mouseY<=400:
        hero = 'Jack'
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)
        gameScreen = 2
    #Choose Jill
    elif gameScreen == 1 and 100<=mouseX<=760 and 500<=mouseY<=600:
        hero = 'Jill'
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)
        gameScreen = 2
    #Choose John
    elif gameScreen == 1 and 100<=mouseX<=760 and 700<=mouseY<=800:
        hero = 'John'
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)        
        gameScreen = 2
        
