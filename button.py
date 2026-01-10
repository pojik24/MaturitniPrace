import pygame

#button class
class Button():
	def __init__(self, x, y, obrazek, text=""):
		self.sirka = obrazek.get_width()
		self.vyska = obrazek.get_height()
		self.x = x
		self.y = y
		self.text = text
		self.obrazek = obrazek
		self.rect = self.obrazek.get_rect()
		self.rect.topleft = (x, y)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.rect.collidepoint(event.pos):
				return True
		return False
		
	def zobraz(self, surface):
		surface.blit(self.obrazek, (self.rect.x, self.rect.y))

		font = pygame.font.SysFont("arial", 40)

		text_img = font.render(self.text, True, (0,0,0))
		text_delka = text_img.get_width()
		text_vyska = text_img.get_height()
		surface.blit(text_img, (self.x + int(self.sirka / 2) - int(text_delka / 2), self.y + int(self.vyska/2) - int(text_vyska/2)))

	
class Textbox():
	def __init__(self, x, y, obrazek):
		self.sirka = obrazek.get_width()
		self.vyska = obrazek.get_height()
		self.x = x
		self.y = y
		self.obrazek = obrazek
		self.aktivni = False
		self.text = ""
		self.rect = self.obrazek.get_rect()
		self.rect.topleft = (x, y)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.rect.collidepoint(event.pos):
				self.aktivni = True
			else:
				self.aktivni = False

		if event.type == pygame.TEXTINPUT and self.aktivni:
			self.text += event.text

		if event.type == pygame.KEYDOWN and self.aktivni:
			if event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]

	def zobraz(self, surface):
		surface.blit(self.obrazek, (self.rect.x, self.rect.y))

		font = pygame.font.SysFont("arial", 40)

		text_img = font.render(self.text, True, (0,0,0))
		text_delka = text_img.get_width()
		text_vyska = text_img.get_height()
		surface.blit(text_img, (self.x + int(self.sirka / 2) - int(text_delka / 2), self.y + int(self.vyska/2) - int(text_vyska/2)))
		