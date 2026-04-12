# ============================================================
# Modul: wort.py
# Enthält Funktionen zum Erzeugen und Prüfen des Ratewortes.
# ============================================================

import random

# Schwierigkeitsstufen nach Wortlänge
SCHWIERIGKEIT = {
    "1": ("Leicht",  1,  6),   # bis 6 Buchstaben
    "2": ("Mittel",  7, 10),   # 7–10 Buchstaben
    "3": ("Schwer", 11, 99),   # ab 11 Buchstaben
}


def schwierigkeit_waehlen():
    """
    Lässt das Team eine Schwierigkeitsstufe wählen.
    Robuste Eingabe: nur 1, 2 oder 3 erlaubt.
    Gibt den gewählten Schlüssel zurück.
    """
    print("\nWaehlt eine Schwierigkeitsstufe:")
    print("  1 - Leicht   (kurze Woerter, bis 6 Buchstaben)")
    print("  2 - Mittel   (mittlere Woerter, 7-10 Buchstaben)")
    print("  3 - Schwer   (lange Woerter, ab 11 Buchstaben)")
    while True:
        eingabe = input("Schwierigkeitsstufe (1/2/3): ").strip()
        if eingabe in SCHWIERIGKEIT:
            name, _, _ = SCHWIERIGKEIT[eingabe]
            print(f"\nSchwierigkeitsstufe: {name}")
            return eingabe
        print("Ungueltige Eingabe! Bitte 1, 2 oder 3 eingeben.")


# Cache: Wörter werden nur einmal aus der Datei gelesen
_woerter_cache = {}


def wort_erzeugen(stufe=None, dateipfad="woerter.txt"):
    """
    Liest die Textdatei mit den Wörtern ein und wählt per
    Zufallsgenerator ein Wort aus. Filtert nach Schwierigkeitsstufe,
    falls angegeben. Gibt das Wort in Großbuchstaben zurück.
    Nutzt Caching, um die Datei nur einmal zu lesen.
    """
    # Wörter aus Cache laden oder einmalig einlesen
    if dateipfad not in _woerter_cache:
        try:
            with open(dateipfad, "r", encoding="utf-8") as datei:
                alle_woerter = [zeile.strip().upper() for zeile in datei if zeile.strip()]
        except FileNotFoundError:
            print(f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden!")
            print("Bitte stelle sicher, dass die Datei im gleichen Ordner liegt.")
            exit()

        if not alle_woerter:
            print("Fehler: Die Wörterdatei ist leer!")
            exit()

        # Wörter nach Stufe vorsortiert cachen
        _woerter_cache[dateipfad] = {
            "alle": alle_woerter,
        }
        for key, (_, min_len, max_len) in SCHWIERIGKEIT.items():
            _woerter_cache[dateipfad][key] = [
                w for w in alle_woerter if min_len <= len(w) <= max_len
            ]

    cache = _woerter_cache[dateipfad]

    # Nach Schwierigkeitsstufe filtern
    if stufe and stufe in SCHWIERIGKEIT and cache.get(stufe):
        woerter = cache[stufe]
    else:
        if stufe and stufe in SCHWIERIGKEIT:
            print("Keine Woerter fuer diese Stufe gefunden – waehle aus allen.")
        woerter = cache["alle"]

    return random.choice(woerter)


def wort_erraten(wort, erratene_buchstaben):
    """Prüft, ob alle Buchstaben des Wortes erraten wurden."""
    for buchstabe in wort:
        if buchstabe not in erratene_buchstaben:
            return False
    return True
