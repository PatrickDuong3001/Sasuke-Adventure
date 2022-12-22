
import pygame
import os
import math

class zetsu(pygame.sprite.Sprite): 
    def __init__(self, x, y, width, height, screen):
        pygame.sprite.Sprite.__init__(self)
        self.width = width 
        self.height = height
        self.screen = screen
        
        self.health = 100
        self.update_time = pygame.time.get_ticks()
        self.action_type = 0
        self.flip_character = False
        self.f_ind = 0    
        self.animation_list = []    
        animation_types = ["run", "attack","die"]
        
        for animation in animation_types:
            temp = []
            for i in range(len(os.listdir(f'animation/zetsu/{animation}'))):
                img = pygame.image.load(f'animation/zetsu/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(0.9*img.get_width()), int(0.9*img.get_height())))
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
    
    def move_towards_player(self, player, speed):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        
        if player.rect.x - self.rect.x < 0:
            self.flip_character = True
        else: 
            self.flip_character = False
        
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        if dist >= 60:
            self.action_updater(0)
            self.rect.x += dx * speed
            self.rect.y += dy * speed
        else:
            self.action_updater(1)
            
    def enemyTakeFireDamage(self):
        self.health -= 50
    
    def enemyTakeSwingDamage(self):
        self.health -= 2
    
    def draw_character(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip_character, False), self.rect)
    
    def getHealth(self):
        return self.health