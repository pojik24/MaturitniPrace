#button.py
#autor: Sára Jirkalová <jirkalovas@jirovcovka.net>

import pygame

class Button():
    """
    Třída Button představuje klikatelné tlačítko v knihovně pygame.
    Umožňuje:
    - detekci kliknutí myší
    - zobrazení tlačítka s textem
    """

    def __init__(self, x, y, obrazek, text=""):
        """
        Konstruktor třídy Button.

        :param x: x-ová souřadnice tlačítka
        :param y: y-ová souřadnice tlačítka
        :param obrazek: pygame Surface – obrázek tlačítka
        :param text: text zobrazený na tlačítku
        """
        self.sirka = obrazek.get_width()
        self.vyska = obrazek.get_height()
        self.x = x
        self.y = y
        self.text = text
        self.obrazek = obrazek

        # Obdélník pro kolize (kliknutí myší)
        self.rect = self.obrazek.get_rect()
        self.rect.topleft = (x, y)

    def handle_event(self, event):
        """
        Zpracuje události (kliknutí myší).

        :param event: pygame událost
        :return: True pokud bylo tlačítko kliknuto, jinak False
        """
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        return False
        
    def zobraz(self, surface):
        """
        Vykreslí tlačítko a jeho text na obrazovku.

        :param surface: pygame Surface, na který se vykresluje
        """
        # Vykreslení obrázku tlačítka
        surface.blit(self.obrazek, (self.rect.x, self.rect.y))

        # Vytvoření fontu
        font = pygame.font.SysFont("arial", 40)

        # Vykreslení textu
        text_img = font.render(self.text, True, (0, 0, 0))
        text_delka = text_img.get_width()
        text_vyska = text_img.get_height()

        # Vycentrování textu do tlačítka
        surface.blit(text_img,(self.x + int(self.sirka / 2) - int(text_delka / 2), self.y + int(self.vyska / 2) - int(text_vyska / 2)))

class Textbox():
    """
    Třída Textbox představuje textové pole pro zadávání textu.
    Uživatel může kliknout do pole a psát text z klávesnice.
    """

    def __init__(self, x, y, obrazek):
        """
        Konstruktor třídy Textbox.

        :param x: x-ová souřadnice textboxu
        :param y: y-ová souřadnice textboxu
        :param obrazek: pygame Surface – obrázek textboxu
        """
        self.sirka = obrazek.get_width()
        self.vyska = obrazek.get_height()
        self.x = x
        self.y = y
        self.obrazek = obrazek

        # Určuje, zda je textbox aktivní (kliknutý)
        self.aktivni = False

        # Aktuální text v textboxu
        self.text = ""

        # Obdélník pro detekci kliknutí
        self.rect = self.obrazek.get_rect()
        self.rect.topleft = (x, y)

    def handle_event(self, event):
        """
        Zpracuje události myši a klávesnice.

        :param event: pygame událost
        """
        # Aktivace / deaktivace textboxu kliknutím
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.aktivni = True
            else:
                self.aktivni = False

        # Přidávání textu při psaní
        if event.type == pygame.TEXTINPUT and self.aktivni:
            self.text += event.text

        # Mazání znaků pomocí Backspace
        if event.type == pygame.KEYDOWN and self.aktivni:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

    def zobraz(self, surface):
        """
        Vykreslí textbox a zadaný text.

        :param surface: pygame Surface, na který se vykresluje
        """
        # Vykreslení obrázku textboxu
        surface.blit(self.obrazek, (self.rect.x, self.rect.y))

        # Vytvoření fontu
        font = pygame.font.SysFont("arial", 40)

        # Vykreslení textu
        text_img = font.render(self.text, True, (0, 0, 0))
        text_delka = text_img.get_width()
        text_vyska = text_img.get_height()

        # Vycentrování textu do textboxu
        surface.blit(text_img,(self.x + int(self.sirka / 2) - int(text_delka / 2), self.y + int(self.vyska / 2) - int(text_vyska / 2)))
		