import pygame as pg
from settings import *
from pygame.sprite import Sprite
from utils import *

from random import randint

from os import path

vec = pg.math.Vector2

import math

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    #check for x collision
    if dir == 'x':
        #checking to see if we've collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to see if we're to the left of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
 #checking to see if we've collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to see if we're above the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                #re position the player (sprite) to the top of the wall
                sprite.pos.y = hits[0].rect.top - 5 - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.width / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y




# player sprite
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "top_down_character.png"))
        self.load_images()
        # self.image = pg.Surface((0, 0))
        # self.image = self.spritesheet.get_image(0,0,TILESIZE * 2, TILESIZE *2)
        # ----- ai help with 1 line -----
        # convert alpha to help w/ transparency
        self.image = pg.image.load(path.join(self.game.img_dir, "top_down_character.png")).convert_alpha()
        # --------------
        self.image = pg.transform.smoothscale(self.image, (96, 72))
        # self.image.set_colorkey(ORANGE)
        self.rect = self.image.get_rect()
        self.base_player_image = self.image
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.acc = vec(0,0)
        self.last_update = 0
        self.current_frame = 0  
        self.coins = 0  
        self.cofric = -0.1
        self.shoot = False
        self.shoot_cooldown = 0
        print('player instantiated')
        print(self.pos)   
        
    def player_rotation(self):
        #gets the position of mouse
        self.mouse_coords = pg.mouse.get_pos()
        #gets difference in x and y
        self.x_change_mouse_player = (self.mouse_coords[0] - self.hit_rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.hit_rect.centery)
        #converts angle to degrees & atan uses x and y dist. into angles (used CS50 for the math and atan stuff)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        #rotates image and -90 to correct difference between atan2() right facing
        self.image = pg.transform.rotate(self.base_player_image, -self.angle - 90)
        #keeps hitbox same
        self.rect = self.image.get_rect(center = self.hit_rect.center)
   
 
    def get_keys(self):
        # reset v to zero
        #listen for events specific to keys
        #change the velocity based on key presses

        # self.vel = vec(0,0)       
        # self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            # self.vel.x = -PLAYER_SPEED
            # print("going left")
 
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            # self.vel.x = PLAYER_SPEED
 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
            # self.vel.y = -PLAYER_SPEED
 
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
            # self.vel.y = PLAYER_SPEED

        # left click & space = shoot 
        if pg.mouse.get_pressed() == (1, 0, 0) or keys[pg.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

  
        if self.vel.x != 0 and self.vel.y !=0:
            self.vel *= 0.7071
            # self.vel.normalize()

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos
            #instantiates it [] for x &y values
            self.bullet = Bullet(self.game, spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
          
    
# gets the ticks to refresh the image making animation
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        # gets ticks for exactly 350 milliseconds


        self.hit_rect.center = self.pos
        self.rect.center = self.hit_rect.center
       
        
        if now - self.last_update > 350:
            self.last_update = now
            # self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            # self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]

    #     # x , y, width, height
    #     self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
    #                         self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
    #                         ]

    def update(self):
        self.acc = vec(0,0)
        self.get_keys()
        # self.animate()
        self.player_rotation()
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        self.rect.center = self.pos
        # self.pos += self.vel + 0.5 * self.acc
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if hits:
            for i in range(25):
                Particle(self.game, hits[0].pos.x, hits[0].pos.y)
            self.coins += 1
            self.game.pickup_snd.play()
            self.game.score += 1
        # self.animate()
        self.rect.center = self.pos
        # self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel* self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall initialized...")
        # print(self.rect.x)
        # print(self.rect.y)
        self.last_update = 0
        self.current_frame = 0    

class Bullet(Sprite):
    def __init__(self, game, x, y, angle):
        #connects game to bulelt
        self.game = game
        #loads into both sprite gruops
        super().__init__(game.all_sprites, game.all_bullets)
        #the angle the player is already rotating at
        self.angle = angle
        #image 
        self.image = pg.image.load(path.join(self.game.img_dir, "bullet.png")).convert_alpha()
        #same issue w/ player rotation just subtract the angle by -90 
        #-90 to offset the image 
        self.image = pg.transform.rotozoom(self.image, -self.angle - 90, BULLET_SCALE)
        #rectangle around image
        self.rect = self.image.get_rect()
        #center of bullet
        self.rect.center = (x, y)
        #x & y positions
        self.x = x
        self.y = y
        
        self.speed = BULLET_SPEED
        #youtube for the math

    
        #the (2*math.pi/360)) is to turn the angles into Radians
          
        #angle_rad = self.angle * (2 * math.pi / 360) ***original math from youtube
        #math did not work and found simplier way to turn into radians
        #pg expects it in radians
        angle_rad = math.radians(self.angle)

        #where to move horizontal velocity
        self.x_vel = math.cos(angle_rad) * BULLET_SPEED
        #where to move vertical velocity
        self.y_vel = math.sin(angle_rad) * BULLET_SPEED

    def bullet_movement(self):
        #actually shoots the bullets by adding the value of x & y
        #each second it is adding value to move
        self.x += self.x_vel
        self.y += self.y_vel

        ##changes it into an integer to be more accurate
        #self.rect.x += int(self.x)
        #self.rect.y += int(self.y)
        #constantly updating the center to draw image
        self.rect.center = (int(self.x), int(self.y))


    def update(self):
        # calls the function
        self.bullet_movement()

class Particle(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(randint(-180,180), randint(-180,180))
        self.pos = vec(x, y)
        self.speed = 5
        self.countdown = Timer()
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        # print(self.rect.x)
        # print(self.rect.y)
        # print(str(len(self.game.all_particles)))
        
    def update(self):
        # countdown ticking
        # self.countdown.ticking()
        print(self.countdown.get_delta())
        self.pos += self.vel * self.speed * self.game.dt
        if self.countdown.get_delta() > 2:
            self.kill()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

      

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        pg.draw.circle(self.image, (YELLOW), (16, 16), 16)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # changes x and y position 
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        print("Coin initialized...")
        # print(self.rect.x)
        # print(self.rect.y)
        self.last_update = 0
        self.current_frame = 0    
    def update(self):
        pass


      

# Mob sprite
class Mob(Sprite):        
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "self.spritesheet(1).png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.vx, self.vy = 100,0
        self.speed = 100
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.dir = "none"
        self.last_update = 0
        self.current_frame = 0
        self.hit_rect = MOB_HIT_RECT
        print("mob initialized...")
        print("Mobs = 1")
        # print(self.rect.x)
        # print(self.rect.y)
         
 

    def load_images(self):
            self.idle_frames = [self.spritesheet.get_image(64,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(96,0,TILESIZE, TILESIZE)
                                ]
            self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                                ]    
    def animate(self):
            # use the time element to get now
            now = pg.time.get_ticks()
            if self.dir == "none":
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                    bottom = self.rect.bottom
                    self.image = self.idle_frames[self.current_frame]
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            elif self.dir == "right":
                pass
    # used auto complete by creating a chase method using pos vectors and obj as a parameter            
    def chase(self, obj):
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0

        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0

    def update(self):
        self.animate()
        if self.game.player:
            self.chase(self.game.player)
            self.rect.center = self.pos
            self.pos += self.vel * self.game.dt
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.all_walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.all_walls, 'y')
            self.rect.center = self.hit_rect.center



