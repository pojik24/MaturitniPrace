#otazky.py
#autor: Sára Jirkalová <jirkalovas@jirovcovka.net>

import random
import databaze

class Otazka(object):
    
    """
    Třída Otazka reprezentuje jednu otázku načtenou z databáze.
    Obsahuje text otázky, správnou odpověď a seznam všech odpovědí.
    """

    def __init__(self, cisloOtazky):
        """
        Konstruktor třídy Otazka.

        :param cisloOtazky: ID otázky v databázi
        """
        self.cislo = cisloOtazky

        # Připojení k databázi otázek
        self.otazky = databaze.Db_otazek()

        # Načtení celé otázky z databáze
        self.celaOtazka = self.otazky.otazka(cisloOtazky)

        # Rozbalení n-tice s daty otázky
        id, self.typ, self.jenOtazka, self.spravnaOdpoved, spatnaOdpoved1, spatnaOdpoved2, spatnaOdpoved3 = self.celaOtazka

        # Seznam všech odpovědí (správná + špatné)
        self.vsechnyOdpovedi = [self.spravnaOdpoved,spatnaOdpoved1,spatnaOdpoved2,spatnaOdpoved3]
   
    def __repr__(self):
        """
        Textová reprezentace objektu (pro ladění).
        """
        return str(self.celaOtazka)
    
    def kontrola(self, odpoved):
        """
        Zkontroluje, zda je odpověď správná.

        :param odpoved: odpověď zvolená hráčem
        :return: True pokud je správná, jinak False
        """
        if odpoved == self.spravnaOdpoved:
            return True
        else:
            return False
        
    def pocet(self):
        """
        Vrátí celkový počet otázek v databázi.

        :return: počet otázek
        """
        return self.otazky.pocet_otazek()

class DemoHrac(object):
    """
    Třída DemoHrac reprezentuje hráče v demo aplikaci.
    Uchovává jméno a aktuální skóre.
    """

    def __init__(self, jmeno):
        """
        Konstruktor třídy DemoHrac.

        :param jmeno: jméno hráče
        """
        self.jmeno = jmeno
        self.skore = 0    

class Demo(object):
    """
    Třída Demo představuje jednoduchou konzolovou kvízovou hru
    pro dva hráče.
    """

    def __init__(self, pocetKol, jmenoHrace1, jmenoHrace2):
        """
        Konstruktor třídy Demo.

        :param pocetKol: počet herních kol
        :param jmenoHrace1: jméno prvního hráče
        :param jmenoHrace2: jméno druhého hráče
        """
        self.pocetKol = pocetKol
        self.hrac1 = DemoHrac(jmenoHrace1)
        self.hrac2 = DemoHrac(jmenoHrace2)

    def zeptej(self, otazka):
        """
        Položí hráči otázku a vyhodnotí odpověď.

        :param otazka: objekt třídy Otazka
        :return: True pokud hráč odpověděl správně, jinak False
        """
        ABCD = {"A": 0, "B": 1, "C": 2, "D": 3}

        # Výpis otázky
        print(otazka.jenOtazka)

        # Náhodné promíchání odpovědí
        random.shuffle(otazka.vsechnyOdpovedi)
        print(otazka.vsechnyOdpovedi)

        # Opakování, dokud hráč nezadá platnou odpověď
        while True:
            print("Zadej jednu z možností: A, B, C, D")
            odpoved = input("Zadej odpověď: ")
            if odpoved in ABCD:
                break

        # Převod písmene na konkrétní odpověď
        odpoved = otazka.vsechnyOdpovedi[ABCD[odpoved]]

        # Kontrola správnosti
        if otazka.kontrola(odpoved):
            print("Správně!")
            return True
        else:
            print("Špatně!")
            return False
           
    def tah(self, hrac):
        """
        Provede jeden tah hráče.

        :param hrac: objekt třídy DemoHrac
        """
        # Náhodný výběr otázky (ID 1–10)
        otazka = Otazka(random.randint(1, 10))

        # Položení otázky
        spravnost = self.zeptej(otazka)

        # Zvýšení skóre při správné odpovědi
        if spravnost:
            hrac.skore += 1

    def run(self):
        """
        Spustí celou hru.
        """
        for _ in range(self.pocetKol):
            self.tah(self.hrac1)
            self.tah(self.hrac2)

            # Výpis aktuálního skóre
            print(f"Aktuální skóre: {self.hrac1.jmeno}:{self.hrac1.skore} / {self.hrac2.jmeno}:{self.hrac2.skore}")
        
if __name__ == "__main__":
    """
    Spuštění demo aplikace.
    """
    aplikace = Demo(3, "Lubomír", "Miroslav")
    aplikace.run()