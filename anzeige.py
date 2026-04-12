# ============================================================
# Modul: anzeige.py
# Enthält Funktionen für die Darstellung (Galgen, Wort, Status).
# ============================================================

import os


def bildschirm_leeren():
    """Leert den Bildschirm für eine übersichtliche Darstellung."""
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

    return stufen[fehler]


def wort_darstellen(wort, erratene_buchstaben):
    """
    Zeigt das Wort mit Strichen für nicht erratene Buchstaben
    und den bereits erratenen Buchstaben an.
    Gibt den dargestellten String zurück.
    """
    anzeige = ""
    for buchstabe in wort:
        if buchstabe in erratene_buchstaben:
            anzeige += buchstabe + " "
        else:
            anzeige += "_ "
    return anzeige.strip()


def spiel_status_anzeigen(wort, erratene_buchstaben, falsche_buchstaben, fehler):
    """Zeigt den aktuellen Spielstatus an: Galgen, Wort und benutzte Buchstaben."""
    print("=" * 50)
    print("               H A N G M A N")
    print("=" * 50)
    print(hangman_zeichen(fehler))
    print(f"  Wort:  {wort_darstellen(wort, erratene_buchstaben)}")
    print(f"\n  Falsche Buchstaben: {', '.join(falsche_buchstaben) if falsche_buchstaben else '---'}")
    print(f"  Verbleibende Versuche: {8 - fehler}")
    print("=" * 50)
