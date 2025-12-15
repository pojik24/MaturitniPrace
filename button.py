import pygame

#button class
class Button():
	def __init__(self, x, y, image, text=""):
		self.width = image.get_width()
		self.height = image.get_height()
		self.x = x
		self.y = y
		self.text = text
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.rect.collidepoint(event.pos):
				return True
		return False
		
	def draw(self, surface):
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		font = pygame.font.SysFont("arial", 40)

		text_img = font.render(self.text, True, (0,0,0))
		text_len = text_img.get_width()
		text_height = text_img.get_height()
		surface.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + int(self.height/2) - int(text_height/2)))

	
class Textbox():
	def __init__(self, x, y, image):
		self.width = image.get_width()
		self.height = image.get_height()
		self.x = x
		self.y = y
		self.image = image
		self.state = False
		self.text = ""
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.rect.collidepoint(event.pos):
				self.state = True

			else:
				self.state = False

		if event.type == pygame.TEXTINPUT and self.state:
			self.text += event.text

		if event.type == pygame.KEYDOWN and self.state:
			if event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]

	def draw(self, surface):
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		font = pygame.font.SysFont("arial", 40)

		text_img = font.render(self.text, True, (0,0,0))
		text_len = text_img.get_width()
		text_height = text_img.get_height()
		surface.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + int(self.height/2) - int(text_height/2)))

	