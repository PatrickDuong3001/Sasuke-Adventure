import pygame

class waterDragon(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, water_flip, width):
        self.width = width
        water_dragon = pygame.image.load('animation/water.png').convert_alpha()
        water_dragon_flip = pygame.transform.flip(water_dragon,True,False)        
        pygame.sprite.Sprite.__init__(self)
        if water_flip:
            self.image = water_dragon_flip
        else:
            self.image = water_dragon
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dragon_direct = direction

    def update(self):
        self.rect.x += (self.dragon_direct * 5)
        if self.rect.right < 0 or self.rect.left > self.width:
            self.kill()
    
    def getDragonX(self):   #get x coordinate of the water dragon
        return self.rect.x
    
    def getDragonY(self):   #get y coordinate of the water dragon
        return self.rect.y
    
    def explicitKill(self):   #kill the water dragon
        self.kill()