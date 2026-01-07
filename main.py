import pygame
from pygame.locals import *
import button
import otazky
import random
import databaze
 
class Tvor(object):
    def __init__(self, jmeno, dflt_zivoty, obrazek, utok, gold=0, biom=None):
        self.jmeno = jmeno
        self.max_zivoty = dflt_zivoty
        self.dflt_zivoty = dflt_zivoty
        self.zivoty = dflt_zivoty
        self.img = pygame.image.load(obrazek)
        self.utok = utok
        self.gold = gold
        self.biom = biom
        
class Hrac(Tvor):
    def __init__(self, jmeno, zivoty, obrazek, pozice, utok, gold=0):
        super().__init__(jmeno, zivoty, obrazek, utok, gold)
        self.img = pygame.image.load(obrazek)
        self.pozice = pozice
        self.score = 0
        self.pocatecni_utok = utok

class Predmet(object):
    def __init__(self, nazev, obrazek, cena):
        self.nazev = nazev
        self.img = pygame.image.load(obrazek)
        self.cena = cena

    def pouzit(self):
        if self.nazev == "Lektvar síly":
            hrac.utok = hrac.utok + 5
        elif self.nazev == "Lektvar života":
            hrac.zivoty = hrac.max_zivoty
            hrac.max_zivoty = hrac.max_zivoty + 20

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((0,0), pygame.HWSURFACE | pygame.DOUBLEBUF, pygame.FULLSCREEN)
        self._running = True
        self.sirka, self.vyska = self._display_surf.get_size()

        self.db = databaze.Db_otazek()
        
        #načtení obrázků
        self.img_tlacitkoOdpoved = pygame.image.load("obrazky/TlacitkoV3.png").convert_alpha()
        self.img_quit = pygame.image.load("obrazky/Quit.png").convert_alpha()
        self.img_mapaButt = pygame.image.load("obrazky/Mapa_butt.png").convert_alpha()
        self.img_add = pygame.image.load("obrazky/add.png").convert_alpha()
        self.img_mapa = pygame.image.load("obrazky/Mapa2.png").convert_alpha()        
        self.img_mapaOverlay = pygame.image.load("obrazky/Mapa_overlay.png").convert_alpha()
        self.img_healthBar = pygame.image.load("obrazky/healthBar.png").convert_alpha()
        self.img_healthBarC = pygame.image.load("obrazky/healthBarC.png").convert_alpha()
        self.img_GameOver = pygame.image.load("obrazky/Game_over.png").convert_alpha()
        self.img_predmetButton = pygame.image.load("obrazky/predmetButton.png").convert_alpha()
        self.img_zpet = pygame.image.load("obrazky/zpet.png").convert_alpha()
        self.img_addotazka = pygame.image.load("obrazky/add_otazka.png").convert_alpha()
        self.img_addtema = pygame.image.load("obrazky/add_tema.png").convert_alpha()
        self.img_button_m = pygame.image.load("obrazky/tlacitko_mensi.png").convert_alpha()
        self.img_obchod = pygame.image.load("obrazky/obchod.png").convert_alpha()
        self.img_obchod = pygame.transform.scale(self.img_obchod, (self.sirka, self.vyska))

        self.sirkaTlacitkaOdpovedi = self.img_tlacitkoOdpoved.get_width()
        self.sirkaTlacitkaQuit = self.img_quit.get_width()

        self.zobrazuj_otazku = False
        self.zobrazuj_mapu = False
        self.zobrazuj_menu = True
        self.zobrazuj_game_over = False
        self.zobrazuj_obchod = False
        self.zobrazuj_add = False

        #tlacitka a tboxy pro přidání otázky
        self.tlacitkoZpet = button.Button(20,20,self.img_zpet)
        self.tbox_tema = button.Textbox(50, 200, self.img_addtema)
        self.tbox_otazka = button.Textbox(50, 300, self.img_addotazka)
        self.tbox_SpravnaO = button.Textbox(50, 400, self.img_addtema)
        self.tbox_SpatnaO1 = button.Textbox(50, 500, self.img_addtema)
        self.tbox_SpatnaO2 = button.Textbox(50, 600, self.img_addtema)
        self.tbox_SpatnaO3 = button.Textbox(50, 700, self.img_addtema)
        self.tlacitkoSubmit = button.Button(1200, 700, self.img_button_m, "Submit")

        #talacitka pro obchod
        self.tlacitkoPredmet1 = button.Button((self.sirka/2)-455, 345, self.img_predmetButton)
        self.tlacitkoPredmet2 = button.Button((self.sirka/2)+155, 345, self.img_predmetButton)

        #tlačítka pro game over menu
        self.tlacitkoRestart = button.Button(self.sirka/2 - 550, 550, self.img_GameOver, "Hrát zvovu")
        self.tlacitkoQuit2 = button.Button(self.sirka/2 + 20, 550, self.img_GameOver, "Ukončit")

        #tlačítka pro main menu
        self.tlacitkoMapa = button.Button(int(self.sirka/2 - self.sirkaTlacitkaQuit/2), 300, self.img_mapaButt)
        self.tlacitkoAdd = button.Button(int(self.sirka/2 - self.sirkaTlacitkaQuit/2), 400, self.img_add)
        self.tlacitkoQuit = button.Button(int(self.sirka/2 - self.sirkaTlacitkaQuit/2), 500, self.img_quit)

        self.tvori = [Tvor("pavouk", 50, "obrazky/potvůrky_2.png", 10, 30, "les"),
                      Tvor("sirena", 60, "obrazky/potvůrky_3.jpg", 15, 45, "jezero"),
                      Tvor("ryba", 40, "obrazky/potvůrky_1.jpg", 10, 25, "jezero"),]
                    
        
        self.predmety = [Predmet("Lektvar síly", "obrazky/lektvar2.png", 150),
                         Predmet("Lektvar zdraví", "obrazky/lektvar1.png", 100)]
        
        self.mapa = {(1,1):"L", (2,1):"L", (3,1):"L", (4,1):"V", (5,1):"V", (6,1):"L", (7,1):"L", (8,1):"L", (9,1):"L", (10,1):"L",
                     (1,2):"L", (2,2):"L", (3,2):"V", (4,2):"V", (5,2):"O", (6,2):"L", (7,2):"J", (8,2):"C", (9,2):"L", (10,2):"L",
                     (1,3):"V", (2,3):"V", (3,3):"V", (4,3):"V", (5,3):"C", (6,3):"L", (7,3):"L", (8,3):"C", (9,3):"L", (10,3):"H",
                     (1,4):"J", (2,4):"C", (3,4):"C", (4,4):"C", (5,4):"C", (6,4):"C", (7,4):"C", (8,4):"C", (9,4):"H", (10,4):"H",
                     (1,5):"B", (2,5):"B", (3,5):"C", (4,5):"B", (5,5):"B", (6,5):"C", (7,5):"C", (8,5):"H", (9,5):"H", (10,5):"H",
                     (1,6):"L", (2,6):"B", (3,6):"C", (4,6):"B", (5,6):"J", (6,6):"V", (7,6):"C", (8,6):"H", (9,6):"H", (10,6):"H",
                     (1,7):"L", (2,7):"L", (3,7):"C", (4,7):"L", (5,7):"L", (6,7):"L", (7,7):"L", (8,7):"V", (9,7):"J", (10,7):"H",
                     (1,8):"V", (2,8):"V", (3,8):"L", (4,8):"L", (5,8):"J", (6,8):"L", (7,8):"V", (8,8):"V", (9,8):"V", (10,8):"H",
                     (1,9):"V", (2,9):"V", (3,9):"L", (4,9):"L", (5,9):"H", (6,9):"H", (7,9):"V", (8,9):"V", (9,9):"H", (10,9):"H",
                     (1,10):"V",(2,10):"L",(3,10):"J",(4,10):"H",(5,10):"H",(6,10):"H",(7,10):"H",(8,10):"H",(9,10):"H",(10,10):"H",}
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False

            #handler eventů mapy
            if event.key == pygame.K_w and self.zobrazuj_mapu and hrac.pozice[1]>1:
                hrac.pozice = (hrac.pozice[0],hrac.pozice[1]-1)
                self.mapa_update()
            if event.key == pygame.K_s and self.zobrazuj_mapu and hrac.pozice[1]<10:
                hrac.pozice = (hrac.pozice[0],hrac.pozice[1]+1)
                self.mapa_update()
            if event.key == pygame.K_a and self.zobrazuj_mapu and hrac.pozice[0]>1:
                hrac.pozice = (hrac.pozice[0]-1,hrac.pozice[1])
                self.mapa_update()
            if event.key == pygame.K_d and self.zobrazuj_mapu and hrac.pozice[0]<10:
                hrac.pozice = (hrac.pozice[0]+1,hrac.pozice[1])
                self.mapa_update()

        #handler eventů main menu
        if self.zobrazuj_menu:
            if self.tlacitkoQuit.handle_event(event):
                self._running = False

            elif self.tlacitkoMapa.handle_event(event):
                self.zobrazuj_menu = False
                self.zobrazuj_mapu = True

            elif self.tlacitkoAdd.handle_event(event):
                self.zobrazuj_menu = False
                self.zobrazuj_add = True

        #handler eventů game over menu
        if self.zobrazuj_game_over:
            if self.tlacitkoQuit2.handle_event(event):
                self._running = False
            
            elif self.tlacitkoRestart.handle_event(event):
                hrac.zivoty = hrac.dflt_zivoty
                hrac.gold = 0
                hrac.score = 0
                hrac.pozice = (5,5)
                hrac.utok = hrac.pocatecni_utok
                self.zobrazuj_mapu = True
                self.zobrazuj_game_over = False

        #handler eventů souboje/otázky
        if self.zobrazuj_otazku:
            if self.tlacitkoOdpoved0.handle_event(event) and str(self.otazka.vsechnyOdpovedi[0]) == str(self.otazka.spravnaOdpoved):
                if self.souboj(hrac, self.tvor):
                    hrac.gold = hrac.gold + self.tvor.gold
                    hrac.score = hrac.score + self.tvor.gold
            elif self.tlacitkoOdpoved0.handle_event(event):
                if self.souboj(self.tvor, hrac):
                    self.zobrazuj_game_over = True
                    self.zobrazuj_mapu = False

            elif self.tlacitkoOdpoved1.handle_event(event) and str(self.otazka.vsechnyOdpovedi[1]) == str(self.otazka.spravnaOdpoved):
                if self.souboj(hrac, self.tvor):
                    hrac.gold = hrac.gold + self.tvor.gold
                    hrac.score = hrac.score + self.tvor.gold
            elif self.tlacitkoOdpoved1.handle_event(event):
                if self.souboj(self.tvor, hrac):
                    self.zobrazuj_game_over = True
                    self.zobrazuj_mapu = False

            elif self.tlacitkoOdpoved2.handle_event(event) and str(self.otazka.vsechnyOdpovedi[2]) == str(self.otazka.spravnaOdpoved):
                if self.souboj(hrac, self.tvor):
                    hrac.gold = hrac.gold + self.tvor.gold
                    hrac.score = hrac.score + self.tvor.gold
            elif self.tlacitkoOdpoved2.handle_event(event):
                if self.souboj(self.tvor, hrac):
                    self.zobrazuj_game_over = True
                    self.zobrazuj_mapu = False

            elif self.tlacitkoOdpoved3.handle_event(event) and str(self.otazka.vsechnyOdpovedi[3]) == str(self.otazka.spravnaOdpoved):
                if self.souboj(hrac, self.tvor):
                    hrac.gold = hrac.gold + self.tvor.gold
                    hrac.score = hrac.score + self.tvor.gold
            elif self.tlacitkoOdpoved3.handle_event(event):
                if self.souboj(self.tvor, hrac):
                    self.zobrazuj_game_over = True
                    self.zobrazuj_mapu = False

        #handler eventů obchodu
        if self.zobrazuj_obchod:
            if self.tlacitkoPredmet1.handle_event(event) and self.predmety[0].cena <= hrac.gold:
                self.predmety[0].pouzit()
                hrac.gold = hrac.gold - self.predmety[0].cena
            elif self.tlacitkoPredmet2.handle_event(event) and self.predmety[1].cena <= hrac.gold:
                self.predmety[1].pouzit()
                hrac.gold = hrac.gold - self.predmety[1].cena
            elif self.tlacitkoZpet.handle_event(event):
                self.zobrazuj_obchod = False
                self.zobrazuj_mapu = True

        #handler eventů menu na přidání otázky
        if self.zobrazuj_add:
            if self.tlacitkoZpet.handle_event(event):
                self.zobrazuj_add = False
                self.zobrazuj_menu = True
            self.tbox_tema.handle_event(event)
            self.tbox_otazka.handle_event(event)
            self.tbox_SpravnaO.handle_event(event)
            self.tbox_SpatnaO1.handle_event(event)
            self.tbox_SpatnaO2.handle_event(event)
            self.tbox_SpatnaO3.handle_event(event)
            if self.tlacitkoSubmit.handle_event(event):
                self.db.pridejOtazku(self.tbox_tema.text, self.tbox_otazka.text, self.tbox_SpravnaO.text, self.tbox_SpatnaO1.text, self.tbox_SpatnaO2.text, self.tbox_SpatnaO3.text)
                self.tbox_tema.text = self.tbox_otazka.text = self.tbox_SpravnaO.text = self.tbox_SpatnaO1.text = self.tbox_SpatnaO2.text = self.tbox_SpatnaO3.text = ""

    def on_render(self):
        if self.zobrazuj_otazku:
            self.zobraz_otazku()
                
        elif self.zobrazuj_menu:
            self.zobraz_menu()

        elif self.zobrazuj_mapu:
            self.zobraz_mapu()
        
        elif self.zobrazuj_obchod:
            self.zobraz_obchod()

        elif self.zobrazuj_add:
            self.zobraz_add()

        elif self.zobrazuj_game_over:
            self.game_over()
                               
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
       
        while( self._running ):
            self._display_surf.fill((255,255,255))

            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        
        self.on_cleanup()

    def zobraz_otazku(self):
        #vykreslení hráče
        self.img_hrac = pygame.transform.scale(hrac.img, (496, 1000))
        self._display_surf.blit(self.img_hrac, (0, 50))

        #vyykreslení tvora        
        self.img_tvor = pygame.transform.scale(self.tvor.img, (800, 800))
        self._display_surf.blit(self.img_tvor, (850, 100))

        #vykreslení otázky na display
        font = pygame.font.SysFont("calibri", 40)
        img = font.render(str(self.otazka.jenOtazka), True, (0,0,0))
        self._display_surf.blit(img, (int(self.sirka/2 - img.get_width()/2), 80))

        #vykreslení tlačítek s odpovědí
        self.tlacitkoOdpoved0.zobraz(self._display_surf)   
        self.tlacitkoOdpoved1.zobraz(self._display_surf)
        self.tlacitkoOdpoved2.zobraz(self._display_surf)
        self.tlacitkoOdpoved3.zobraz(self._display_surf)

        #health bary
        img_healthBarH = pygame.transform.scale(self.img_healthBarC, (700/hrac.max_zivoty*hrac.zivoty, 63))
        self._display_surf.blit(img_healthBarH, (25,780))
        self._display_surf.blit(self.img_healthBar, (20,775))
        img_healthBarT = pygame.transform.scale(self.img_healthBarC, (700/self.tvor.max_zivoty*self.tvor.zivoty, 63))
        self._display_surf.blit(img_healthBarT, (810,780))
        self._display_surf.blit(self.img_healthBar, (805,775))

        zfont = pygame.font.SysFont("calibri", 41)
        text_img = zfont.render(f"{hrac.zivoty}/{hrac.max_zivoty}", True, (0,0,0))
        text2_img = zfont.render(f"{self.tvor.zivoty}/{self.tvor.max_zivoty}", True, (0,0,0))
        self._display_surf.blit(text_img, (36, 791))
        self._display_surf.blit(text2_img, (1400, 791))

    def zobraz_menu(self):
        self.tlacitkoMapa.zobraz(self._display_surf)
        self.tlacitkoAdd.zobraz(self._display_surf)
        self.tlacitkoQuit.zobraz(self._display_surf)

    def zobraz_mapu(self):
        self._display_surf.blit(self.img_mapa, (int(self.sirka/2 - 300), int(self.vyska/2 - 300)), ((hrac.pozice[0]*200)-400, (hrac.pozice[1]*200)-400, 600, 600))
        self._display_surf.blit(self.img_mapaOverlay, (int(self.sirka/2 - 50), int(self.vyska/2 - 50)))
        font = pygame.font.SysFont("calibri", 41)
        text_img1 = font.render("Pro pohyb použij W,A,S,D", True, (0,0,0))
        self._display_surf.blit(text_img1, (20, 800))


    def mapa_update(self):
        if self.mapa[hrac.pozice] == "L":
            self.tvor = self.tvori[0]
            self.priprava_otazky()
        elif self.mapa[hrac.pozice] == "V":
            self.tvor = self.tvori[2]
            self.priprava_otazky()
        elif self.mapa[hrac.pozice] == "O":
            self.zobrazuj_obchod = True
            self.zobrazuj_mapu = False

    def priprava_otazky(self):
        #resetování životů tvora a škálování
        self.tvor.max_zivoty = int(self.tvor.dflt_zivoty + hrac.score/10)
        self.tvor.zivoty = self.tvor.max_zivoty
        self.tvor.utok = int(self.tvor.utok + hrac.score/100)

        self.vyber_otazky()
        self.zobrazuj_mapu = False
        self.zobrazuj_otazku = True

    def vyber_otazky(self):
        self.otazka = otazky.Otazka(random.randint(1, self.db.pocet_otazek()))
        random.shuffle(self.otazka.vsechnyOdpovedi)
        self.tlacitkoOdpoved0 = button.Button(int(self.sirka/2 - self.sirkaTlacitkaOdpovedi/2), 220, self.img_tlacitkoOdpoved, str(self.otazka.vsechnyOdpovedi[0]))
        self.tlacitkoOdpoved1 = button.Button(int(self.sirka/2 - self.sirkaTlacitkaOdpovedi/2), 360, self.img_tlacitkoOdpoved, str(self.otazka.vsechnyOdpovedi[1]))
        self.tlacitkoOdpoved2 = button.Button(int(self.sirka/2 - self.sirkaTlacitkaOdpovedi/2), 500, self.img_tlacitkoOdpoved, str(self.otazka.vsechnyOdpovedi[2]))
        self.tlacitkoOdpoved3 = button.Button(int(self.sirka/2 - self.sirkaTlacitkaOdpovedi/2), 640, self.img_tlacitkoOdpoved, str(self.otazka.vsechnyOdpovedi[3]))        

    def souboj(self, vyherce, porazeny):
        porazeny.zivoty = porazeny.zivoty - vyherce.utok
        if porazeny.zivoty <= 0:
            self.zobrazuj_mapu = True
            self.zobrazuj_otazku = False
            return True
        else:
            self.vyber_otazky()
            return False
        
    def zobraz_obchod(self):
        self._display_surf.blit(self.img_obchod, (0,0))

        self.tlacitkoZpet.zobraz(self._display_surf)

        self.img_predmet1 = pygame.transform.scale(self.predmety[0].img, (270,270))
        self.tlacitkoPredmet1.zobraz(self._display_surf)
        self._display_surf.blit(self.img_predmet1, ((self.sirka/2)-440, 360))

        self.img_predmet2 = pygame.transform.scale(self.predmety[1].img, (200,200))
        self.tlacitkoPredmet2.zobraz(self._display_surf)
        self._display_surf.blit(self.img_predmet2, ((self.sirka/2)+195, 395))

        font = pygame.font.SysFont("calibri", 41)
        text_img1 = font.render(f"{self.predmety[0].nazev}", True, (0,0,0))
        sirka1 = text_img1.get_width()
        self._display_surf.blit(text_img1, (int((self.sirka/2)-310-(sirka1/2)), 660))

        text_img3 = font.render(f"{self.predmety[0].cena}g", True, (0,0,0))
        sirka3 = text_img3.get_width()
        self._display_surf.blit(text_img3, (int((self.sirka/2)-310-(sirka3/2)), 700))

        text_img2 = font.render(f"{self.predmety[1].nazev}", True, (0,0,0))
        sirka2 = text_img2.get_width()
        self._display_surf.blit(text_img2, (int((self.sirka/2)+310-(sirka2/2)), 660))

        text_img4 = font.render(f"{self.predmety[1].cena}g", True, (0,0,0))
        sirka4 = text_img4.get_width()
        self._display_surf.blit(text_img4, (int((self.sirka/2)+310-(sirka4/2)), 700))

        text_img5 = font.render(f"Tvoje goldy: {hrac.gold}", True, (0,0,0))
        self._display_surf.blit(text_img5, (20, 800))

    def zobraz_add(self):
        self.tlacitkoZpet.zobraz(self._display_surf)

        font = pygame.font.SysFont("calibri", 20)
        self.tbox_tema.zobraz(self._display_surf)
        self.tbox_otazka.zobraz(self._display_surf)
        self.tbox_SpravnaO.zobraz(self._display_surf)
        self.tbox_SpatnaO1.zobraz(self._display_surf)
        self.tbox_SpatnaO2.zobraz(self._display_surf)
        self.tbox_SpatnaO3.zobraz(self._display_surf)
        self.tlacitkoSubmit.zobraz(self._display_surf)
        
        
    def game_over(self):
        self.zobrazuj_mapu = False
        self.zobrazuj_menu = False
        self.zobrazuj_otazku = False

        font = pygame.font.SysFont("calibri", 100, bold=True)
        text_img = font.render("Prohrál jsi!", True, (0,0,0))
        self._display_surf.blit(text_img, ((self.sirka/2)-(text_img.get_width()/2), 350))
        font2 = pygame.font.SysFont("calibri", 60)
        text_img2 = font2.render(f"Konečné skóre: {hrac.score}", True, (0,0,0))
        self._display_surf.blit(text_img2, ((self.sirka/2)-(text_img2.get_width()/2), 450))
        self.tlacitkoRestart.zobraz(self._display_surf)
        self.tlacitkoQuit2.zobraz(self._display_surf)

if __name__ == "__main__" :
    hrac = Hrac("Smil Flek z Nohavic", 50, "obrazky/ritíř_1.png", (5,5), 10)
    theApp = App()
    theApp.on_execute()