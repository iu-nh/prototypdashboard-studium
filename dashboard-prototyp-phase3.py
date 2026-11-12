#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk
from tkinter import messagebox
import json 
from abc import ABC, abstractmethod
# json ist für das Speichern zuständig

def sag_etwas():
    name = eingabe_name.get()
    studiengang = eingabe_studiengang.get()
    modul = eingabe_modul.get()
    prüfungsleistung = eingabe_prüfungsleistung.get()
    semester = eingabe_semester.get()
    
    if name or studiengang or modul or semester or prüfungsleistung:
        ausgabe.config(text=f"Name: {name}, Studiengang: {studiengang} , Modul: {modul} , Semester: {semester} , Prüfungsleistung: {prüfungsleistung} !")
   
    else:
        messagebox.showwarning("Eingabefehler", "Bitte füllen Sie die Felder aus.")

# json code zum speicherm

def speichern():
    daten = {
        "Name": eingabe_name.get(),
        "Studiengang": eingabe_studiengang.get(),
        "Modul": eingabe_modul.get(),
        "Semester": eingabe_semester.get(),
        "Prüfungsleistung": eingabe_prüfungsleistung.get()
    }
#name, studiengang, etc: wird in "daten" gespeichert
    with open("studium.json", "w", encoding="utf-8") as datei:
        json.dump(daten, datei, ensure_ascii=False, indent=4)

    messagebox.showinfo("Gespeichert", "Deine Daten wurden gespeichert!")


class Pruefungsleistung(ABC):
    """Abstrakte Basisklasse: Jede Prüfung kann eine Note berechnen."""
#docstrings für help commands
    def __init__(self, datum=None):
        self.datum = datum #datum ist hier einfach auf none festgelegt, init ist der konstruktor, 

    @abstractmethod
    def berechne_note(self):
        """Gibt die Note zurück oder None, wenn noch keine vorliegt."""

    def ist_bestanden(self):
        note = self.berechne_note()
        return note is not None and note <= 4.0
#mehrere unterklassen und methoden

class Klausur(Pruefungsleistung):
    """Note wird aus den erreichten Punkten berechnet."""

    def __init__(self, datum=None, dauer_min=90, punkte=None, max_punkte=100):
        super().__init__(datum)
        self.dauer_min = dauer_min
        self.punkte = punkte
        self.max_punkte = max_punkte
#standardmäßges klausurformat mit datum integriert dauer 90min
    def berechne_note(self):
        if self.punkte is None:
            return None
        prozent = self.punkte / self.max_punkte * 100
#einfache berechnung für die berechnung der noten
        if prozent >= 90:
            return 1.0
        if prozent >= 80:
            return 2.0
        if prozent >= 70:
            return 3.0
        if prozent >= 50:
            return 4.0
        return 5.0


class Portfolio(Pruefungsleistung):
    """Note wird direkt von der Bewertung übernommen."""

    def __init__(self, datum=None, bewertung=None):
        super().__init__(datum)
        self.bewertung = bewertung

    def berechne_note(self):
        return self.bewertung
#unterklasse von portfolio, gibt die note aus "prüfungsleistung" aus

class Modul:
    def __init__(self, name, ects, pruefung):
        self.name = name
        self.ects = ects
        self.pruefung = pruefung  # genau eine Prüfungsleistung

    @property #aus note wird nun ein attribut statt einer methode
    def note(self):
        return self.pruefung.berechne_note()

    def ist_bestanden(self):
        return self.pruefung.ist_bestanden()
#ruft die note auf

class Semester:
    def __init__(self, nummer):
        self.nummer = nummer
        self.module = []

    def modul_hinzufuegen(self, modul):
        self.module.append(modul)
#hier werden alle module zusammengefasst aus "modul"

class Studiengang:
    def __init__(self, name, ects_gesamt, ziel_note):
        self.name = name
        self.ects_gesamt = ects_gesamt
        self.ziel_note = ziel_note
        self.semester = []

    def alle_module(self):
        return [m for s in self.semester for m in s.module]

    def ects_erreicht(self):
        return sum(m.ects for m in self.alle_module() if m.ist_bestanden())

    def durchschnitt(self):
        bestanden = [m for m in self.alle_module() if m.ist_bestanden()]
        if not bestanden:
            return None
        return sum(m.note * m.ects for m in bestanden) / sum(m.ects for m in bestanden)

    def dashboard(self):
        print(f"=== Dashboard: {self.name} ===")
        print(f"ECTS: {self.ects_erreicht()} / {self.ects_gesamt}")
        schnitt = self.durchschnitt()
        if schnitt is None:
            print("Notenschnitt: noch keine Noten")
        else:
            status = "im Ziel" if schnitt <= self.ziel_note else "über dem Ziel"
            print(f"Notenschnitt: {schnitt:.2f} (Ziel: {self.ziel_note}) -> {status}")
        print("\nModule:")
        for m in self.alle_module():
            art = type(m.pruefung).__name__
            print(f"  {m.name:<25} {m.ects} ECTS  {art:<10}  Note: {m.note}")
#alles zusammengefasst: gesammtkonstrukt "studiengang" 

# beispieldaten für den dashboard-prototyp
s1 = Semester(1)
s1.modul_hinzufuegen(Modul("Mathematik", 5, Klausur(punkte=82)))
s1.modul_hinzufuegen(Modul("Programmieren", 5, Portfolio(bewertung=1.7)))
s1.modul_hinzufuegen(Modul("Datenbanken", 5, Klausur()))  # noch offen

studium = Studiengang("Softwareentwicklung", 180, 2.0)
studium.semester.append(s1)
studium.dashboard()

            
# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("Studium UI - Dein Studium")
fenster.geometry("700x600")

# Eingabefeld
tk.Label(fenster, text="Name:").pack(pady=5)
eingabe_name = tk.Entry(fenster)
eingabe_name.pack()

#Eingabe Modul
tk.Label(fenster, text="Modul:").pack(pady=5)
eingabe_modul = tk.Entry(fenster)
eingabe_modul.pack()


#Eingabe Semester
tk.Label(fenster, text="Semester:").pack(pady=5)
eingabe_semester = tk.Entry(fenster)
eingabe_semester.pack()


#Eingabe Studiengang
tk.Label(fenster, text="Studiengang:").pack(pady=5)
eingabe_studiengang = tk.Entry(fenster)
eingabe_studiengang.pack()


#Eingabe Prüfungsleistung
tk.Label(fenster, text="Prüfungsleistung:").pack(pady=5)
eingabe_prüfungsleistung = tk.Entry(fenster)
eingabe_prüfungsleistung.pack()
#BUTTON UNTER JEDEM DER FELDER
tk.Button(fenster, text="Ok!", command=sag_etwas).pack(pady=10)

tk.Button(fenster, text="Alles speichern", command=speichern).pack(pady=10)

# ausgabeeee
ausgabe = tk.Label(fenster, text="")
ausgabe.pack()

# GUI starten
fenster.mainloop()


# In[ ]:




