# ============================================================
# Modul: eingabe.py
# Enthält Funktionen für Spieler- und Buchstabeneingaben.
# ============================================================


def eingabe_Spieler():
    """
    Fragt die Anzahl der Spieler (2–5) und deren Namen ab.
    Die Eingabe ist robust: nur Buchstaben sind als Name erlaubt.
    Gibt eine Liste der Spielernamen zurück.
    """
    # Anzahl der Spieler abfragen (robust)
    while True:
        eingabe = input("Wie viele Spieler spielen mit? (2-5): ").strip()
        if eingabe.isdigit() and 2 <= int(eingabe) <= 5:
            anzahl = int(eingabe)
            break
        print("Ungueltige Eingabe! Bitte eine Zahl zwischen 2 und 5 eingeben.\n")

    # Namen der einzelnen Spieler abfragen (robust)
    spieler = []
    for i in range(1, anzahl + 1):
        while True:
            name = input(f"Name von Spieler {i}: ").strip()
            if name.isalpha():
                spieler.append(name)
                break
            print("Ungueltige Eingabe! Der Name darf nur Buchstaben enthalten "
                  "(keine Zahlen, Sonderzeichen oder Leerzeichen).\n")

    return spieler


def buchstaben_raten(spieler_name, wort, erratene_buchstaben, falsche_buchstaben):
    """
    Ermöglicht die Eingabe eines Buchstabens oder eines ganzen Wortes.
    Robuste Eingabe: nur Buchstaben erlaubt, keine Sonderzeichen/Zahlen.

    Rückgabewerte:
      (True,  False) – Buchstabe war richtig, kein Fehler
      (False, False) – Buchstabe war falsch, Fehler
      (True,  True)  – ganzes Wort richtig geraten → gewonnen
      (False, True)  – ganzes Wort falsch geraten → Fehler
    """
    while True:
        eingabe = input(f"\n{spieler_name}, rate einen Buchstaben (oder das ganze Wort): ").strip().upper()

        # Leere Eingabe abfangen
        if not eingabe:
            print("Ungueltige Eingabe! Bitte gib mindestens einen Buchstaben ein.")
            continue

        # Nur Buchstaben erlaubt
        if not eingabe.isalpha():
            print("Ungueltige Eingabe! Nur Buchstaben sind erlaubt "
                  "(keine Zahlen, Sonderzeichen oder Leerzeichen).")
            continue

        # --- Ganzes Wort geraten ---
        if len(eingabe) > 1:
            if eingabe == wort:
                # Alle Buchstaben als erraten markieren
                for b in wort:
                    if b not in erratene_buchstaben:
                        erratene_buchstaben.append(b)
                print(f"\n*** Fantastisch! '{eingabe}' ist das gesuchte Wort! ***")
                return (True, True)
            else:
                print(f"\n'{eingabe}' ist leider nicht das gesuchte Wort!")
                return (False, True)

        # --- Einzelner Buchstabe ---
        buchstabe = eingabe

        # Bereits geraten?
        if buchstabe in erratene_buchstaben or buchstabe in falsche_buchstaben:
            print(f"Der Buchstabe '{buchstabe}' wurde bereits geraten! Versuche einen anderen.")
            continue

        # Buchstabe im Wort?
        if buchstabe in wort:
            erratene_buchstaben.append(buchstabe)
            print(f"\nRichtig! '{buchstabe}' kommt im Wort vor!")
            return (True, False)
        else:
            falsche_buchstaben.append(buchstabe)
            print(f"\nLeider! '{buchstabe}' kommt nicht im Wort vor.")
            return (False, False)
