# ============================================================
# Hangman – Hauptprogramm
# Die einzelnen Funktionen sind in separate Module ausgelagert:
#   eingabe.py  – eingabe_Spieler(), buchstaben_raten()
#   anzeige.py  – bildschirm_leeren(), hangman_zeichen(),
#                 wort_darstellen(), spiel_status_anzeigen()
#   wort.py     – wort_erzeugen(), wort_erraten()
# ============================================================

from eingabe import eingabe_Spieler, buchstaben_raten
from anzeige import bildschirm_leeren, spiel_status_anzeigen
from wort import wort_erzeugen, wort_erraten, schwierigkeit_waehlen


# ============================================================
# Hauptprogramm: Spielablauf
# ============================================================
def spiel():
    """Steuert den gesamten Spielablauf."""
    bildschirm_leeren()
    print("=" * 50)
    print("     Willkommen beim Hangman-Spiel!")
    print("     Das Team spielt gegen den Computer.")
    print("=" * 50)
    print()

    # Spieler erfassen
    spieler = eingabe_Spieler()
    print(f"\nSuper! Es spielen mit: {', '.join(spieler)}")
    print("Viel Glueck, Team!\n")
    input("Druecke Enter, um das Spiel zu starten...")

    while True:  # Schleife für "Nochmal spielen?"
        # Schwierigkeitsstufe wählen
        stufe = schwierigkeit_waehlen()

        # Neues Wort erzeugen
        wort = wort_erzeugen(stufe)

        # Spielvariablen initialisieren
        erratene_buchstaben = []   # richtig geratene Buchstaben
        falsche_buchstaben = []    # falsch geratene Buchstaben
        fehler = 0                 # Anzahl der Fehler (max 8)
        max_fehler = 8
        aktueller_spieler = 0      # Index des aktuellen Spielers
        gewonnen = False

        # Spielschleife
        while fehler < max_fehler and not gewonnen:
            bildschirm_leeren()
            spiel_status_anzeigen(wort, erratene_buchstaben, falsche_buchstaben, fehler)

            # Aktuellen Spieler bestimmen
            name = spieler[aktueller_spieler]
            print(f"\n>>> {name} ist an der Reihe! <<<")

            # Buchstabe raten
            richtig, ganzes_wort = buchstaben_raten(
                name, wort, erratene_buchstaben, falsche_buchstaben
            )

            if ganzes_wort and richtig:
                # Ganzes Wort richtig geraten → gewonnen
                gewonnen = True
            elif richtig:
                # Buchstabe war richtig → gleicher Spieler darf nochmal
                if wort_erraten(wort, erratene_buchstaben):
                    gewonnen = True
                # Spieler bleibt gleich (kein Wechsel)
            else:
                # Falsch → Fehler erhöhen, nächster Spieler
                fehler += 1
                aktueller_spieler = (aktueller_spieler + 1) % len(spieler)

            if not gewonnen and fehler < max_fehler:
                input("\nDruecke Enter, um fortzufahren...")

        # Spielende
        bildschirm_leeren()
        spiel_status_anzeigen(wort, erratene_buchstaben, falsche_buchstaben, fehler)

        if gewonnen:
            print("\n*** HERZLICHEN GLUECKWUNSCH! ***")
            print(f"Das Team hat das Wort '{wort}' erraten!")
            print("Ihr habt gegen den Computer gewonnen!\n")
        else:
            print("\n*** LEIDER VERLOREN! ***")
            print(f"Das gesuchte Wort war: '{wort}'")
            print("Der Computer hat gewonnen!\n")

        # Nochmal spielen?
        while True:
            antwort = input("Moechtet ihr noch einmal spielen? (ja/nein): ").strip().lower()
            if antwort in ("ja", "j"):
                break
            elif antwort in ("nein", "n"):
                print("\nDanke fuers Spielen! Bis zum naechsten Mal!")
                return
            else:
                print("Bitte antworte mit 'ja' oder 'nein'.")


# ============================================================
# Programmstart
# ============================================================
if __name__ == "__main__":
    spiel()
