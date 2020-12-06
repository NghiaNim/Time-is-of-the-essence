add_library('controlP5')
add_library('minim')

import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1920
HEIGHT = 1080
gameScreen = 0
gameground = 920

class Game:
    def __init__(self, w, h, g, hero):
        self.w = w
        self.h = h
        self.enemy_projectiles = []
        self.hero_projectiles = []
        self.enemylist = []
        self.itemlist = []
        self.platformlist = []
        self.obstaclelist = []
        self.g = g
        self.next_level = False
        self.background = loadImage(path + "/images/background.png")
        self.groundimg = loadImage(path + "/images/ground.png")
        
        for line in level:
            if line == '\n':
                break

            line = line.strip().split(',')
            if line[0] == 'TimeWraith':
                line = list(map(int, line[1:]))
                self.enemylist.append(TimeWraith(line[0],line[1],line[2],line[3],line[4]))


            elif line[0] == 'Worm':
                line = list(map(int, line[1:]))
                self.enemylist.append(Worm(line[0],line[1],line[2],line[3],line[4]))

            elif line[0] == 'TimeWizard':
                line = list(map(int, line[1:]))
                self.enemylist.append(TimeWizard(line[0],line[1],line[2],line[3],line[4]))

            elif line[0] == 'Bat':
                line = list(map(int, line[1:]))
                self.enemylist.append(Bat(line[0],line[1],line[2],line[3],line[4]))

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
            self.hero = Jill(100, 752, 30, 48, self.g, 'GraveRobber_run.png', 48, 48, 6, 'GraveRobber_idle.png', 4, 'GraveRobber_hurt.png', 3, 'GraveRobber_jump.png', 6, 20, 6)
        elif hero == 'John':
            self.hero = John(100, 752, 30, 48, self.g, 'Woodcutter_run.png', 48, 48, 6, 'Woodcutter_idle.png', 4, 'Woodcutter_hurt.png', 3, 'Woodcutter_jump.png', 6, 10, 5)
    
    def update(self):
        
        if self.enemylist == []:
            #random portal spawn
            random_cor = random.randint(500,1800)

            #check if portal will spawn in wall
            for obstacle in self.obstaclelist:
                while random_cor < obstacle.x < random_cor + 120 or random_cor < obstacle.x + obstacle.w < random_cor + 120:
                    random_cor = random.randint(120, 1800)
            self.enemylist.append(Portal(random_cor, self.g - 120, 120, 120))

    
    def display(self):
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


        changedg = False
        if len(game.obstaclelist) != 0:
            for o in game.obstaclelist:
                if self.y + self.h <= o.y and ((self.x + self.w >= o.x and self.x + self.w <= o.x + o.w) or (self.x <= o.x + o.w and self.x >= o.x)) or ((2*self.x+self.w)/2 <= o.x + o.w and (2*self.x+self.w)/2 >= o.x)  :
                    self.g = o.y
                    changedg = True
                    break
        if len(game.platformlist) != 0:
            for p in game.platformlist:
                if self.y + self.h <= p.y and self.x + self.w >= p.x and self.x <= p.x + p.w:
                    self.g = p.y
                    changedg = True
                    break
        if changedg == False:
            self.g = game.g
                
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

    def collision_future(self, target):
        if (self.x + self.vx < target.x + target.w) and (self.x + self.w + self.vx > target.x) and (self.y + self.vy < target.y + target.h) and (self.y + self.vy + self.h > target.y):
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

    def update(self):
        if self.autofire == True and frameCount%60 == 0:
            self.autofiretime -= 1
            if self.autofiretime == 0:
                self.autofire = False

        else:
            if self.charges == 0:
                self.charges -= 1
                self.reloadtime = 2*60

            if self.reloadtime > 0:
                self.reloadtime -= 1

                if self.reloadtime == 0:
                    self.charges = self.base_charges


        self.gravity()
        if frameCount % 60 == 0:
            self.time -= 1
        
        if self.invincible < 0:
            self.hit_right = False

        if self.active_damage == 0:
            self.dmg = self.base_dmg
        elif frameCount %60 == 0:
            self.active_damage -= 1
        
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
                    self.vy = -7

            if self.key_handler['E'] == True and self.real_active_ability_cooldown == 0:
                self.special_ability()


        
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
    
            if self.key_handler[SHIFT] == True and self.y+self.h == self.g:
                self.vy = -10


        
        #frames of animation based on action
        if frameCount%10 == 0 and self.vy != 0:
            self.frame = (self.frame + 1) % self.jump_num_frames
        elif frameCount%10 == 0 and self.vx == 0:
            self.frame = (self.frame + 1) % self.idle_num_frames
        elif frameCount%10 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames

        #check for hit
        for enemy in game.enemylist:
            
            #check for endgame
            if isinstance(enemy, Portal) and (self.collision_rect_right(enemy) or self.collision_rect_left(enemy)) and enemy.frame > 40 :
                game.next_level = True

            elif isinstance(enemy, Portal):
                continue

            elif self.collision_rect_right(enemy) and self.invincible <= 0 and enemy.alive == True:
                self.time -= enemy.dmg
                self.invincible = 60
                self.hit_right = True
                self.knockback = True

            elif self.collision_rect_left(enemy) and self.invincible <= 0 and enemy.alive == True:
                self.time -= enemy.dmg
                self.invincible = 60
                self.knockback = True

        
        for projectile in game.enemy_projectiles:
            if self.collision_rect_right(projectile) and self.invincible <= 0:
                projectile.destroy()
                self.time -= projectile.dmg
                self.invincible = 60
                self.hit_right = True
                self.knockback = True
            elif self.collision_rect_left(projectile) and self.invincible <= 0:
                projectile.destroy()
                self.time -= projectile.dmg
                self.invincible = 60
                self.knockback = True

        future_collision = False
        if len(game.obstaclelist) != 0:
            for o in game.obstaclelist:
                if self.collision_future(o) == True:
                    future_collision = True
        if future_collision == False:
            self.x += self.vx
        self.y += self.vy
        self.standing_y += self.vy
        self.invincible -= 1


    def display(self):
        self.update()
        #rectangle to show hitbox

        # noFill()
        # fill(0,0,0)
        # # rect(self.x, self.y, self.w, self.h)
        
        
        if self.key_handler[DOWN] == True and self.y+self.h == self.g:
            #no animation for crouching yet
            
            pass
        elif self.invincible > 0 and self.direction == RIGHT and self.knockback == True:
            image(self.img_hurt, self.x, self.y, self.img_w - 18, self.img_h, 1 * self.img_w, 0, 2 *self.img_w - 18, self.img_h)

        
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

            ellipse(self.x + 15, self.y - 15 , 20, 8)
        
        textSize(20)
        fill(255,255,255)
        text('Remaining time: ' + str(self.time), 50, 30)
        text('(E) Ability cooldown: ' + str(self.real_active_ability_cooldown), 300, 30)

        if self.reloadtime != 0:
            fill(255,255,255)
            text('Recharging...', 100, 900)

        if self.autofire == True:
            fill(0,255,0)
            text('Rapid-fire mode', 100, 940)

        if game.hero.buffed_time > 0:
            fill(0,255,0)
            text('DAMAGE UP!', 100, 920)
            if frameCount % 60 == 0:
                game.hero.buffed_time -= 1



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
            
            
        if frameCount - self.shoot_framestamp > self.shootingspeed:
            self.shoot_framestamp = frameCount
            if not self.autofire:
                self.charges -= 1
            if self.active_damage == 0:
                self.bullet_img = 'bullet.png'
            else:
                self.bullet_img = 'bullet_up.png'

            game.hero_projectiles.append(Projectile(self.x, self.y+10, 10, 10, self.bullet_img, 16, 16, 5, 8*p_vx, 8*p_vy, 150, False, self.dmg))



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


class Jack(Hero):
    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, dmg, speed):
        self.base_charges = 8
        self.base_shootingspeed = 20
        self.shootingspeed = self.base_shootingspeed
        
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, 100, dmg, speed)
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

        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, 30, dmg, speed)
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
        
        Hero.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, img_name_idle, idle_num_frames, img_name_hurt, hurt_num_frames, img_name_jump, jump_num_frames, 120, dmg, speed)
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
        # Attributes for backend functions
        self.framestart = frameCount 
        self.direction = random.choice([LEFT, RIGHT])
        self.flying = False
        
        self.vx = vx
        if self.direction == LEFT:
            self.vx *= -1
        self.xleft = xl #left X boundary
        self.xright = xr # right x boundary
        self.tmp_vx = 0
        

    def update(self):
        if self.alive == True:
            self.gravity()


            # Idle and attack loop (enemy will stop walking so he can attack)
            if frameCount - self.framestart > self.attackspeed:
                if self.idle == False:
                    self.tmp_vx = self.vx
                    self.vx = 0
                    self.idle = True
                if self.attacked_cnt < self.attack_count and self.attack_frame-1 == self.idle_frame and frameCount%10 == 0:
                    if self.projectile_bol == True: #Does the enemy shoot projectiles?
                        self.attack()
                    self.attacked_cnt += 1       
                if self.idle_frame == 0 and self.attacked_cnt == self.attack_count:
                    self.framestart = frameCount
                    self.vx = self.tmp_vx
                    self.idle = False
                    self.attacked_cnt = 0
            
            # If the enemy should follow the hero this will change its direction
            if self.follow_bol == True:
                self.follow()

            # Checks for the "boundaries"
            if self.x+self.vx < self.xleft:
                self.vx *= -1
                self.direction = RIGHT
            elif self.x+self.vx > self.xright:
                self.vx *= -1
                self.direction = LEFT

            # Check for obstacles
            for o in game.obstaclelist:
                # This will check whether the next "step" will be within the obstacle,
                if (self.x + self.vx >= o.x and self.x + self.vx <= o.x + o.w) or (self.x + self.w + self.vx >= o.x and self.x+self.w + self.vx <= o.x + o.w) and ((self.y>=o.y and self.y<=o.y+o.h) or (self.y+self.h >= o.y and self.y+self.h <= o.y+o.h)):
                    self.vx *= -1
                    if self.direction == LEFT:
                        self.direction = RIGHT
                    else:
                        self.direction = LEFT

            # Collision with projectiles
            for p in game.hero_projectiles:
                if self.collision_rect_left(p) == True:
                    self.damage(p.dmg, LEFT)
                    p.destroy()
                elif self.collision_rect_right(p) == True:
                    self.damage(p.dmg, RIGHT)
                    p.destroy()

            #slow down animation
            if frameCount%10 == 0:
                self.frame = (self.frame + 1) % self.num_frames
            # slow down idle frames
            if self.vx == 0 and frameCount%10 == 0:
                self.idle_frame = (self.idle_frame + 1) % self.num_idle_frames
            elif self.vx != 0:
                self.idle_frame = 0
                self.idle_count = 0

            if self.hp <= 0:
                self.death()

            self.x += self.vx
            self.y += self.vy

        elif self.alive == False:
            if frameCount%10 == 0:
                self.death_frame = self.death_frame + 1
                if self.death_frame >= self.num_death_frames:
                    self.destroy()

    def display(self):
        self.update() 
        #rect(self.x, self.y, self.w, self.h)
        if self.alive == True:      
            if self.vx != 0 and self.direction == RIGHT:
                image(self.img, self.x, self.y, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.vx != 0 and self.direction == LEFT:
                image(self.img, self.x, self.y, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == RIGHT:
                image(self.img_idle, self.x, self.y, self.img_w, self.img_h, self.idle_frame * self.img_w, 0, (self.idle_frame + 1) * self.img_w, self.img_h)
            elif self.vx == 0 and self.direction == LEFT:
                image(self.img_idle, self.x, self.y, self.img_w, self.img_h, (self.idle_frame + 1) * self.img_w, 0, self.idle_frame * self.img_w, self.img_h)
        elif self.alive == False:
            if self.direction == RIGHT:
                image(self.img_death, self.x, self.y, self.img_w, self.img_h, self.death_frame * self.img_w, 0, (self.death_frame + 1) * self.img_w, self.img_h)
            if self.direction == LEFT:
                image(self.img_death, self.x, self.y, self.img_w, self.img_h, (self.death_frame + 1) * self.img_w, 0, self.death_frame * self.img_w, self.img_h)


    # Here we will be able to define the specifics of attacks 
    def attack(self):
        if self.direction == LEFT:
            game.enemy_projectiles.append(Projectile(self.x, self.y+25, 15, 15, "clock.png", 15, 15, 4, self.projectile_speed*-1, -6, 150, self.p_gravity, self.dmg_projectile))
        elif self.direction == RIGHT:
            game.enemy_projectiles.append(Projectile(self.x+self.w, self.y+25, 15, 15, "clock.png", 15, 15, 4, self.projectile_speed, -6, 150, self.p_gravity, self.dmg_projectile))
    
    def follow(self):

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


    def death(self):
        self.alive = False

    def damage(self, dmg, dir): 
        self.vy -= 3
        self.hp -= dmg

    def destroy(self):
        rand_int = random.randint(0,100)
        if rand_int < self.droprate:
            game.itemlist.append(TimeItem(self.x, self.y, self.g, 15))
        game.enemylist.remove(self)

class TimeWraith(Enemy):
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 40, 52, g, "wraith.png", "wraith_shriek.png", "wraith_death.png", 64, 52, 7, 7, 7, 4, 140, x_left, x_right, 100, 3, 10, 5.5, 2, 50, True, False, 100)

    def attack(self):
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

class Worm(Enemy):
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 36, 64, g, "worm.png", "worm_idle.png", "worm_death.png", 36, 64, 6, 6, 3, 2, 220, x_left, x_right, 70, 3, 0, 12, 1, 50, True, False, 350)
        self.projectile_bol = False # Does the enemy cast projectiles?

class TimeWizard(Enemy):
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 60, 80, g, "TimeWizard.png", "TimeWizard.png", "TimeWizard_death.png", 320, 320, 4, 4, 12, 4, 200, x_left, x_right, 100, 3, 10, 5.5, 3, 50, False, False, 100)
        self.projectile_speed = 7 # VX attribute of the casted projectile

    def display(self):
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

    def attack(self):
            game.enemy_projectiles.append(SmallFireball(self.x, self.y+5, -self.projectile_speed, self.dmg_projectile, self.p_gravity))
            game.enemy_projectiles.append(SmallFireball(self.x+self.w, self.y+5, self.projectile_speed, self.dmg_projectile, self.p_gravity))

class Bat(Enemy):
    def __init__(self, x, y, g, x_left, x_right):
        Enemy.__init__(self, x, y, 32, 32, g, "bat.png", "bat_attack.png", "bat_death.png", 32, 32, 7, 5, 3, 3, 60, x_left, x_right, 40, 2, 10, 5, 1, 50, False, True, 100)
        self.flying = True
        self.g = y

    def attack(self):
            game.enemy_projectiles.append(BatBall(self.x, self.y, 0, self.dmg_projectile, self.p_gravity))

    def gravity(self):
        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.h + self.vy > self.g:
                self.vy = self.g - (self.y + self.h)


class Projectile(Creation):

    def __init__(self, x, y, w, h, img_name, img_w, img_h, num_frames, vx, vy, framespan, gravity, dmg):
        Creation.__init__(self, x, y, w, h, game.g, img_name, img_w, img_h, num_frames)
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

        if self.y+self.h > game.g:
            self.destroy()

    def destroy(self):

        if self in game.enemy_projectiles:
            game.enemy_projectiles.remove(self)
        elif self in game.hero_projectiles:
            game.hero_projectiles.remove(self)

class ClockProjectile(Projectile):
    def __init__(self, x, y, projectile_speed, dmg):
        Projectile.__init__(self, x, y, 15, 15, "clock.png", 15, 15, 4, projectile_speed, -2, 150, True, dmg)

class SmallFireball(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity):
        Projectile.__init__(self, x, y, 72, 29, "SmallFireball.png", 72, 29, 4, projectile_speed, 0, 150, gravity, dmg)

class BatBall(Projectile):
    def __init__(self, x, y, projectile_speed, dmg, gravity):
        Projectile.__init__(self, x, y, 32, 32, "batball.png", 32, 32, 4, projectile_speed, 0, 200, gravity, dmg)

class Item(Creation):

    def __init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames, autopick):
        Creation.__init__(self, x, y, w, h, g, img_name, img_w, img_h, num_frames)
        self.autopick = autopick
        self.direction = RIGHT #This should be an attribute whether the item is going to be autopicked, but we could theoretically remove it whatsoever

    def destroy(self):
        game.itemlist.remove(self)

class TimeItem(Item):

    def __init__(self, x, y, g, time):
        Item.__init__(self, x, y, 32, 32, g, "clockitem.png", 32, 32, 6, True)
        self.time = time


    def update(self):
        Creation.update(self)

        if self.collision_rect(game.hero) == True:
            game.hero.time += self.time
            self.destroy()

class BuffItem(Item):
    def __init__(self, x, y, g, effect = random.randint(1,4)):
        if effect == 1:
            self.item = 'Apple'
        elif effect == 2:
            self.item = 'Bananas'
        elif effect == 3:
            self.item = 'Melon'
        elif effect == 4:
            self.item = 'Orange'
            
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
            
            #time freeze
            elif self.item == 'Bananas':
                game.hero.autofire = True
                game.hero.autofiretime = 10 
                pass 
                    
            #insta kill
            elif self.item == 'Melon':
                pass
                
            #invincibility
            elif self.item == 'Orange':
                pass
        
            self.destroy()

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
            if self.collision_rect(p):
                p.destroy()
        for p in game.hero_projectiles:
            if self.collision_rect(p):
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
    global game, level
    background(255, 255, 255)
    game.display()
    if game.hero.time < 0:
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)

    if game.next_level == True:
        global real_time
        real_time = game.hero.time
        game = Game(WIDTH, HEIGHT, gameground, hero) 
        game.hero.time = real_time

def drawEnd():
    background(255, 255, 255)
    stroke(0,0,0)
    fill(0)
    textSize(50)
    text('You have successfully destroyed time', 500, 200)
    text('Enjoy your eternal meaningless existence', 460, 260)
    textSize(20)
    text('Or press R to go back to character select', 750, 300)
        
def setup():
    size(WIDTH, HEIGHT)
    fullScreen()
    
def draw():
    if gameScreen == 0:
        drawMenu()
    elif gameScreen == 1:
        drawGame()
    elif gameScreen == 2:
        drawEnd()
    

def keyPressed():
    global gameScreen
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
    if gameScreen == 2 and (key == 'R' or key == 'r'):
        gameScreen = 0



        
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
    if gameScreen == 0 and 100<=mouseX<=400 and 200<=mouseY<=300:
        hero = 'Jack'
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)
        gameScreen = 1
    #Choose Jill
    if gameScreen == 0 and 100<=mouseX<=400 and 400<=mouseY<=500:
        hero = 'Jill'
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)
        gameScreen = 1
    #Choose John
    if gameScreen == 0 and 100<=mouseX<=400 and 600<=mouseY<=700:
        hero = 'John'
        level = open('level_design.txt','r')
        game = Game(WIDTH, HEIGHT, gameground, hero)        
        gameScreen = 1
        
