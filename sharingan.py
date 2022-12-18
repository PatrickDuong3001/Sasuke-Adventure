import pygame
import os

class Sharingan(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.sharingan_sprite = []
        self.current_sprite = 0
        self.sharingan_sprite.append(pygame.image.load('animation/sharingan/0.png').convert_alpha())
        self.sharingan_sprite.append(pygame.image.load('animation/sharingan/1.png').convert_alpha())
        self.sharingan_sprite.append(pygame.image.load('animation/sharingan/2.png').convert_alpha())
        
        self.update_time = pygame.time.get_ticks()
        self.image = self.sharingan_sprite[int(self.current_sprite)]
        self.rect = self.image.get_rect(midbottom = (x,y))
    
    def update(self):
        if pygame.time.get_ticks() - self.update_time > 100:
            self.current_sprite += 1
            self.update_time = pygame.time.get_ticks()
        if int(self.current_sprite) >= len(self.sharingan_sprite):
            self.current_sprite = 0
        self.image = self.sharingan_sprite[int(self.current_sprite)]
    
    def deactivate(self):
        self.kill()
    