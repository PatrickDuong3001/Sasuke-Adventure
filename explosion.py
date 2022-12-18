import pygame 
class explosion(pygame.sprite.Sprite):   #class for different types of explosion
	def __init__(self, x, y, explodeType):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(0, 4):
			img = pygame.image.load(f"animation/element_explosion/{explodeType}/{num}.png")
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()
  
		