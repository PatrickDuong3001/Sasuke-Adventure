import pygame

class waterDragon(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, width, speed):
        self.width = width
        self.speed = speed
        water_dragon = pygame.image.load('animation/water.png').convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.image = water_dragon
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dragon_direct = direction

    def update(self):
        self.rect.x -= (self.dragon_direct * self.speed)
        if self.rect.right < 0 or self.rect.left > self.width:
            self.kill()
    
    def getDragonX(self):   #get x coordinate of the water dragon
        return self.rect.x
    
    def getDragonY(self):   #get y coordinate of the water dragon
        return self.rect.y
    
    def explicitKill(self):   #kill the water dragon
        self.kill()