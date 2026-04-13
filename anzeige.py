# ============================================================
# Modul: anzeige.py
# Enthält Funktionen für die Darstellung (Galgen, Wort, Status).
# Dieses Modul ist rein für die visuelle Ausgabe zuständig –
# hier findet KEINE Spiellogik statt.
# ============================================================

# os wird benötigt, um einen Betriebssystem-Befehl auszuführen:
# "cls" auf Windows oder "clear" auf macOS/Linux → Bildschirm leeren
import os


def bildschirm_leeren():
    """Leert den Bildschirm für eine übersichtliche Darstellung."""
    # os.name == "nt" erkennt Windows; alle anderen Systeme nutzen "clear"
    os.system("cls" if os.name == "nt" else "clear")


def hangman_zeichen(fehler):
    """
    Gibt die Hangman-Zeichnung passend zur Anzahl der falschen
    Versuche (0–8) als String zurück.

    Stufen:
      0 – nichts
      1 – halber Berg
      2 – ganzer Berg
      3 – senkrechter Balken
      4 – Querbalken
      5 – Seil
      6 – Kopf
      7 – Körper
      8 – Beine  → Spiel verloren
    """
    # Jede Zeichnung ist ein mehrzeiliger String (triple-quoted).
    # Der Index der Liste entspricht direkt der Fehleranzahl:
    # stufen[0] = 0 Fehler, stufen[3] = 3 Fehler, usw.
    # Mit jedem Fehler wird die Zeichnung um ein Element erweitert.
    stufen = [
        # 0 – kein Fehler
        """
        
        
        
        
        
        
        
        """,
        # 1 – halber Berg
        """
        
        
        
        
        
        
         /
        """,
        # 2 – ganzer Berg
        """
        
        
        
        
        
        
         / \\
        """,
        # 3 – senkrechter Balken
        """
          |
          |
          |
          |
          |
          |
         / \\
        """,
        # 4 – Querbalken
        """
          +-------+
          |
          |
          |
          |
          |
         / \\
        """,
        # 5 – Seil
        """
          +-------+
          |       |
          |
          |
          |
          |
         / \\
        """,
        # 6 – Kopf
        """
          +-------+
          |       |
          |      (o)
          |
          |
          |
         / \\
        """,
        # 7 – Körper
        """
          +-------+
          |       |
          |      (o)
          |      /|\\
          |
          |
         / \\
        """,
        # 8 – Beine (komplett)
        """
          +-------+
          |       |
          |      (o)
          |      /|\\
          |      / \\
          |
         / \\
        """
    ]

    # Gibt die Zeichnung zurück, die zum aktuellen Fehlerstand passt.
    # fehler = 0 → leere Zeichnung, fehler = 8 → vollständiger Galgen
    return stufen[fehler]


def wort_darstellen(wort, erratene_buchstaben):
    """
    Zeigt das Wort mit Strichen für nicht erratene Buchstaben
    und den bereits erratenen Buchstaben an.
    Gibt den dargestellten String zurück.
    """
    anzeige = ""
    # Jeden Buchstaben des gesuchten Wortes einzeln prüfen
    for buchstabe in wort:
        if buchstabe in erratene_buchstaben:
            # Buchstabe wurde bereits erraten → sichtbar anzeigen
            anzeige += buchstabe + " "
        else:
            # Buchstabe noch nicht erraten → als Strich darstellen
            anzeige += "_ "
    # strip() entfernt das letzte Leerzeichen am Ende des Strings
    return anzeige.strip()


def spiel_status_anzeigen(wort, erratene_buchstaben, falsche_buchstaben, fehler):
    """Zeigt den aktuellen Spielstatus an: Galgen, Wort und benutzte Buchstaben."""
    # Trennlinie und Titel
    print("=" * 50)
    print("               H A N G M A N")
    print("=" * 50)
    # Galgenzeichnung passend zur aktuellen Fehleranzahl ausgeben
    print(hangman_zeichen(fehler))
    # Wort als _ _ A _ _ darstellen (erratene Buchstaben sichtbar)
    print(f"  Wort:  {wort_darstellen(wort, erratene_buchstaben)}")
    # Falsche Buchstaben als Liste, oder "---" wenn noch keine Fehler
    print(f"\n  Falsche Buchstaben: {', '.join(falsche_buchstaben) if falsche_buchstaben else '---'}")
    # Verbleibende Versuche: Maximum (8) minus bisherige Fehler
    print(f"  Verbleibende Versuche: {8 - fehler}")
    print("=" * 50)
