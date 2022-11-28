import pygame
import os
from waterDragon import waterDragon
import math

class minion(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.screen = screen
        
        self.alive = True
        self.health = 1000
        self.max_health = self.health
        self.update_time = pygame.time.get_ticks()
        self.action_type = 0
        self.character_direct = 1
        self.original_time = 0
        self.f_ind = 0    
        self.animation_list = []    
        animation_types = ["stand"]
        
        self.water = None
        self.water_sprite_group = pygame.sprite.Group()
        
        for animation in animation_types:
            temp = []
            for i in range(len(os.listdir(f'animation/minion/{animation}'))):
                img = pygame.image.load(f'animation/minion/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(2.0*img.get_width()), int(2.0*img.get_height())))
                temp.append(img)
            self.animation_list.append(temp)
        self.image = self.animation_list[self.action_type][self.f_ind]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
            
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
            
    def waterJutsu(self):
        self.water = waterDragon(0.6*self.rect.size[0] * self.character_direct + self.rect.centerx - 80, self.rect.centery-5, self.character_direct,self.width)
        self.water_sprite_group.add(self.water)

    def movements(self, new_time): 
        self.action_updater(0)       
        if (new_time - self.original_time) % 100 == 0: 
            self.waterJutsu()
        
    def water_sprite_update(self):
        self.water_sprite_group.update()
        self.water_sprite_group.draw(self.screen)
    
    def draw_character(self):
        self.screen.blit(self.image, self.rect)
    
    def getWaterSprite(self):       #return the fire ball sprite. Used for collision detection with enemies
        return self.water_sprite_group

    def getWaterX(self):            #return the x coordinate of the fire ball for the main file
        return self.water.getDragonX()
        
    def getWaterY(self):            #return the y coordinate of the fire ball for the main file
        return self.water.getDragonY()
    
    def explicitWaterKill(self):    #kill the fire ball sprite after an explosion
        self.water.explicitKill()
    