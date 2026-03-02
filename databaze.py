#databaze.py
#autor: Sára Jirkalová <jirkalovas@jirovcovka.net>

import sqlite3

class Db_otazek(object):
    """
    Třída Db_otazek slouží ke správě databáze otázek v SQLite.
    Umožňuje:
    - vytvoření databáze a tabulky
    - přidávání otázek
    - načítání konkrétní otázky
    - zjištění počtu otázek
    - práci s tématy otázek
    """

    def __init__(self):
        """
        Konstruktor třídy.
        Vytvoří připojení k databázi a zajistí existenci tabulky 'otazky'.
        """
        self.connection = sqlite3.connect("otazky.db")
        self.cursor = self.connection.cursor()

        # Vytvoření tabulky, pokud ještě neexistuje
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
        """
        Přidá novou otázku do databáze.

        :param tema: téma otázky
        :param otazka: text otázky
        :param spravna_odpoved: správná odpověď
        :param spatna_odpoved1: špatná odpověď 1
        :param spatna_odpoved2: špatná odpověď 2
        :param spatna_odpoved3: špatná odpověď 3
        """
        values = (tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3)

        query = "INSERT INTO otazky (tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3) VALUES (?,?,?,?,?,?)"
        self.cursor.execute(query, values)
        self.connection.commit()

    def otazka(self, cislo_otazky):
        """
        Vrátí konkrétní otázku podle jejího ID.

        :param cislo_otazky: ID otázky v databázi
        :return: n-tice s daty otázky nebo None, pokud neexistuje
        """
        query = f"SELECT id, tema, otazka, spravna_odpoved, spatna_odpoved1, spatna_odpoved2, spatna_odpoved3 FROM otazky WHERE id = {cislo_otazky}"
        vysledek = self.cursor.execute(query)
        otazka = vysledek.fetchone()
        self.connection.commit()
        return otazka
    
    def pocet_otazek(self):
        """
        Zjistí celkový počet otázek v databázi.

        :return: počet otázek (int)
        """
        query = "SELECT COUNT(id) FROM otazky;"
        vysledek = self.cursor.execute(query)
        self.connection.commit()
        pocet = vysledek.fetchone()
        return pocet[0]
    
    def tema(self, tema):
        """
        Vrátí seznam ID otázek, které patří k danému tématu.

        :param tema: název tématu
        :return: seznam ID otázek
        """
        query = "SELECT id FROM otazky WHERE tema = ?;"
        vysledek = self.cursor.execute(query, [tema])
        self.connection.commit()

        ids = vysledek.fetchall()
        otazky = []

        # Převedení výsledků z n-tic na seznam ID
        for i in ids:
            otazky.append(i[0])

        return otazky

    def vsechna_temata(self):
        """
        Vrátí seznam všech unikátních témat v databázi.

        :return: seznam témat
        """
        query = "SELECT DISTINCT tema FROM otazky;"
        vysledek = self.cursor.execute(query)
        self.connection.commit()

        temata = vysledek.fetchall()
        n_temata = []

        # Převedení výsledků z n-tic na seznam řetězců
        for i in temata:
            n_temata.append(i[0])
        return n_temata