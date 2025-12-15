#databaze.py
#autor: Sára Jirkalová <jirkalovas@jirovcovka.net>

import sqlite3

class SQLite(object):
    """
    Třída pro zjednodušenou práci s SQLite databází.
    Zapouzdřuje základní operace - vytvoření spojení, vykonání SQL příkazů, uzavření spojení.
    """
    def __init__(self, filename):
        """
        Inicializace databázového spojení.
        
        Args:
            filename (str): Název souboru databáze (např. "kontakty.db")
        """
        self.filename = filename
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
    
    def sql(self, query, data=None):
        if data is None: 
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        self.connection.commit()
        return self.cursor

    def __del__(self):
        """
        Uzavření databázového spojení při zániku objektu.
        """
        self.connection.close()

class Db_otazek(object):
    def __init__(self):
        self.db = SQLite("otazky.db")
        self.db.sql("""CREATE TABLE IF NOT EXISTS otazky (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tema TEXT NOT NULL,
                       otazka TEXT NOT NULL, 
                       spravna_odpoved TEXT NOT NULL, 
                       spatna_odpoved1 TEXT NOT NULL, 
                       spatna_odpoved2 TEXT NOT NULL, 
                       spatna_odpoved3 TEXT NOT NULL);""")
        
    def pridejOtazku(self, tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3):
        values = (tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3)
        query = "INSERT INTO otazky (tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3) VALUES (?,?,?,?,?,?)"
        self.db.sql(query, values)

    def otazka(self, cislo_otazky):
        query = f"SELECT id, tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3 FROM otazky WHERE ID = {cislo_otazky}"
        vysledek = self.db.sql(query)
        vsechna_data = vysledek.fetchone()
        return vsechna_data
    
    def pocet_otazek(self):
        query = "SELECT COUNT(id) FROM otazky;"
        vysledek = self.db.sql(query)
        pocet = vysledek.fetchone()
        return pocet[0]

if __name__ == "__main__" :
    databaze = Db_otazek()
    print(databaze.pocet_otazek())
