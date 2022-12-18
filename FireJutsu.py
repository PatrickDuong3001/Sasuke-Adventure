import pygame

class FireJutsu(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, fire_flip, width):
        self.width = width
        fire_ball = pygame.image.load('animation/fire.png').convert_alpha()
        fire_ball_flip = pygame.transform.flip(fire_ball,True,False)        
        pygame.sprite.Sprite.__init__(self)
        if fire_flip:
            self.image = fire_ball_flip
        else:
            self.image = fire_ball
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.character_direct = direction

    def update(self):
        self.rect.x += (self.character_direct * 5)
        if self.rect.right < 0 or self.rect.left > self.width:
            self.kill()
    
    def getFireX(self):   #get x coordinate of the fire ball
        return self.rect.x
    
    def getFireY(self):   #get y coordinate of the fire ball
        return self.rect.y
    
    def explicitKill(self):   #kill the fire ball, used for explosion
        self.kill()