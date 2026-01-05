#databaze.py
#autor: Sára Jirkalová <jirkalovas@jirovcovka.net>

import sqlite3

class Db_otazek(object):
    def __init__(self):
        self.connection = sqlite3.connect("otazky.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS otazky (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tema TEXT NOT NULL,
                       otazka TEXT NOT NULL, 
                       spravna_odpoved TEXT NOT NULL, 
                       spatna_odpoved1 TEXT NOT NULL, 
                       spatna_odpoved2 TEXT NOT NULL, 
                       spatna_odpoved3 TEXT NOT NULL);""")
        self.connection.commit()
        
    def pridejOtazku(self, tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3):
        values = (tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3)
        query = "INSERT INTO otazky (tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3) VALUES (?,?,?,?,?,?)"
        self.cursor.execute(query, values)
        self.connection.commit()

    def otazka(self, cislo_otazky):
        query = f"SELECT id, tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3 FROM otazky WHERE ID = {cislo_otazky}"
        vysledek = self.cursor.execute(query)
        otazka = vysledek.fetchone()
        self.connection.commit()
        return otazka
    
    def pocet_otazek(self):
        query = "SELECT COUNT(id) FROM otazky;"
        vysledek = self.cursor.execute(query)
        self.connection.commit()
        pocet = vysledek.fetchone()
        return pocet[0]

