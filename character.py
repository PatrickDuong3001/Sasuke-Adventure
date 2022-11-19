import pygame
import os
from FireJutsu import FireJutsu

class character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.screen = screen
        
        self.alive = True
        self.health = 100
        self.max_health = self.health
        self.update_time = pygame.time.get_ticks()
        self.cooldown_jutsu_duration = 0
        self.action_type = 0
        self.character_direct = 1
        self.flip_character = False
        self.f_ind = 0    
        self.animation_list = []    
        animation_types = ["stand", "run","fire","chidori_charge","chidori_attack","swing"]
        
        self.fire_flip = False
        self.fire = None
        self.fire_sprite_group = pygame.sprite.Group()
        
        for animation in animation_types:
            temp = []
            for i in range(len(os.listdir(f'animation/{animation}'))):
                img = pygame.image.load(f'animation/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(2*img.get_width()), int(2*img.get_height())))
                temp.append(img)
            self.animation_list.append(temp)
        self.image = self.animation_list[self.action_type][self.f_ind]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.animate_updater()
        #self.check_alive()
        #update cooldown
        if self.cooldown_jutsu_duration > 0:
            self.cooldown_jutsu_duration -= 1
            
    def animate_updater(self):
        #based on current frame, updating image
        self.image = self.animation_list[self.action_type][self.f_ind]
        if pygame.time.get_ticks() - self.update_time > 100:
            self.update_time = pygame.time.get_ticks()
            self.f_ind += 1
        if self.f_ind >= len(self.animation_list[self.action_type]):
            if self.action_type == 3:
                self.f_ind = len(self.animation_list[self.action_type]) - 1
            else:
                self.f_ind = 0

    def action_updater(self, action):
        #check if the new action is different to the previous one
        if action != self.action_type:
            self.action_type = action
            #update the animation settings
            self.f_ind = 0
            self.update_time = pygame.time.get_ticks()
            
    def fireJutsu(self):
        if self.cooldown_jutsu_duration == 0:
            self.cooldown_jutsu_duration = 30
            self.fire = FireJutsu(0.6*self.rect.size[0] * self.character_direct + self.rect.centerx, self.rect.centery-10, self.character_direct,self.fire_flip,self.width)
            self.fire_sprite_group.add(self.fire)

    def character_movements(self, left_move, right_move, down_move, up_move):
        dx = 0
        dy = 0
        if right_move:
            if self.rect.x <= self.width - 80:
                dx = 4
            self.flip_character = False
            self.fire_flip = False
            self.character_direct = 1
        if left_move:
            if self.rect.x >= 1:
                dx = -4
            self.fire_flip = True
            self.flip_character = True
            self.character_direct = -1
        if down_move:
            if self.rect.y <= self.height - 100:
                dy = 3
        if up_move:
            if self.rect.y >= 10:
                dy = -3        
        self.rect.y += dy
        self.rect.x += dx
    
    def chidori_move(self, left_move, right_move):
        dx = 0
        dy = 0
        if right_move:
            if self.rect.x <= self.width - 80:
                dx = 7
            self.flip_character = False
            self.fire_flip = False
            self.character_direct = 1
        if left_move:
            if self.rect.x >= 1:
                dx = -7
            self.fire_flip = True
            self.flip_character = True
            self.character_direct = -1
        self.rect.y += dy
        self.rect.x += dx
    
    def fire_sprite_update(self):
        self.fire_sprite_group.update()
        self.fire_sprite_group.draw(self.screen)
    
    def draw_character(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip_character, False), self.rect)
    
    def checkAlive(self): 
        return self.alive
    
    def getFireSprite(self):       #return the fire ball sprite. Used for collision detection with enemies
        return self.fire_sprite_group

    def getFireX(self):            #return the x coordinate of the fire ball for the main file
        return self.fire.getFireX()
        
    def getFireY(self):            #return the y coordinate of the fire ball for the main file
        return self.fire.getFireY()
    
    def explicitFireKill(self):    #kill the fire ball sprite after an explosion
        self.fire.explicitKill()