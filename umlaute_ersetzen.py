# ============================================================
# Skript: umlaute_ersetzen.py
# Ersetzt in woerter.txt alle Umlaute (ä, ö, ü, Ä, Ö, Ü)
# durch ae, oe, ue, Ae, Oe, Ue und ß durch ss.
# ============================================================

def umlaute_ersetzen(dateipfad="woerter.txt"):
    """Liest die Datei, ersetzt Umlaute und schreibt sie zurück."""
    ersetzungen = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
    }

    with open(dateipfad, "r", encoding="utf-8") as datei:
        inhalt = datei.read()

    for alt, neu in ersetzungen.items():
        inhalt = inhalt.replace(alt, neu)

    with open(dateipfad, "w", encoding="utf-8") as datei:
        datei.write(inhalt)

    print(f"Umlaute in '{dateipfad}' wurden erfolgreich ersetzt.")


if __name__ == "__main__":
    umlaute_ersetzen()
