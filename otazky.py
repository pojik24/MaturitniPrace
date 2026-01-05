#otazky.py
#autor: Sára Jirkalová <jirkalovas@jirovcovka.net>

import random
import databaze

class Otazka(object):
    '''
    Třída otázek.

    Attributes: 
        cisloOtazky (integer):  číslo otázky
    '''
    def __init__(self, cisloOtazky):
        self.cislo = cisloOtazky
        # vybrání požadované otázky z databáze
        self.otazky = databaze.Db_otazek()
        self.celaOtazka = self.otazky.otazka(cisloOtazky)
        id, self.typ, self.jenOtazka, self.spravnaOdpoved, spatnaOdpoved1, spatnaOdpoved2, spatnaOdpoved3 = self.celaOtazka
        self.vsechnyOdpovedi = [self.spravnaOdpoved, spatnaOdpoved1, spatnaOdpoved2, spatnaOdpoved3]
   
    def __repr__(self):                
        """
        stringová reprezentace otazky
        """
        return str(self.celaOtazka)
    
    def kontrola(self, odpoved): 
        """
        kontrola správnosti zadané odpovědi

        Attributes: 
            odpoved (string):  odpověď, jejíž správnost chcete otestovat
        """      
        if odpoved == self.spravnaOdpoved:
            return True
        else:
            return False
        
    def pocet(self):
        return self.otazky.pocet_otazek()

class DemoHrac(object):
    '''
    Třída otázek

    Attributes: 
        jmeno (string):  jméno hráče
    '''
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.skore = 0    
    
class Demo(object):
    def __init__(self, pocetKol, jmenoHrace1, jmenoHrace2):
        self.pocetKol = pocetKol
        self.hrac1 = DemoHrac(jmenoHrace1)
        self.hrac2 = DemoHrac(jmenoHrace2)

    def zeptej(self, otazka):
        ABCD = {"A":0, "B":1, "C":2, "D":3}
        print(otazka.jenOtazka)
        random.shuffle(otazka.vsechnyOdpovedi)
        print(otazka.vsechnyOdpovedi)
        while True:
            print("Zadej jednu z možností: A, B, C, D")
            odpoved = input("Zadej odpověď: ")
            if odpoved in ABCD:
                break
        odpoved = otazka.vsechnyOdpovedi[ABCD[odpoved]]
        if otazka.kontrola(odpoved):
            print("Správně!")
            return True
        else:
            print("Špatně!")
            return False
           
    def tah(self, hrac):
            otazka = Otazka(random.randint(1,10))
            spravnost = self.zeptej(otazka)
            if spravnost:
                hrac.skore += 1

    def run(self):
        for _ in range(self.pocetKol):
            self.tah(self.hrac1)
            self.tah(self.hrac2)
            print(f"Aktuální skóre: {self.hrac1.jmeno}:{self.hrac1.skore} / {self.hrac2.jmeno}:{self.hrac2.skore}")
        
if __name__ == "__main__":
    aplikace = Demo(3, "Lubomír", "Miroslav")
    aplikace.run()
          