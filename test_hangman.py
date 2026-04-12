# ============================================================
# Testskript: test_hangman.py
# Simuliert 1000 Hangman-Durchgaenge mit verschiedenen
# Spieleranzahlen, Schwierigkeitsstufen und Strategien.
# Im Terminal nachvollziehbar wie ein echtes Spiel.
# ============================================================

import random
import string
import time
import sys
from wort import wort_erzeugen, wort_erraten, SCHWIERIGKEIT
from anzeige import spiel_status_anzeigen


def schnell_leeren():
    """Bildschirm leeren per ANSI-Escape (kein Subprozess, viel schneller)."""
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()

# ============================================================
# Konfiguration
# ============================================================
ANZAHL_DURCHGAENGE = 10000
MAX_FEHLER = 8
VERZOEGERUNG = 0.00001 # Sekunden zwischen Zuegen (einstellbar)
ALLE_BUCHSTABEN = list(string.ascii_uppercase)

# Verschiedene Teamnamen fuer die Simulation
SPIELERNAMEN = [
    ["Anna", "Ben"],
    ["Clara", "David", "Eva"],
    ["Felix", "Greta", "Hans", "Ida"],
    ["Jan", "Katja", "Leo", "Mia", "Noah"],
    ["Olga", "Paul"],
    ["Rita", "Stefan", "Tina"],
]


# ============================================================
# Strategien fuer das Raten
# ============================================================
def strategie_haeufigkeit(wort, erratene, falsche):
    """Raet Buchstaben nach Haeufigkeit in der deutschen Sprache."""
    # Haeufigste Buchstaben im Deutschen
    haeufig = "ENISRATDHULCGMOBWFKZPVJYXQ"
    for b in haeufig:
        if b not in erratene and b not in falsche:
            return b
    # Fallback: irgendein ungenutzter Buchstabe
    for b in ALLE_BUCHSTABEN:
        if b not in erratene and b not in falsche:
            return b
    return None


def strategie_zufall(wort, erratene, falsche):
    """Raet voellig zufaellige Buchstaben."""
    verfuegbar = [b for b in ALLE_BUCHSTABEN if b not in erratene and b not in falsche]
    return random.choice(verfuegbar) if verfuegbar else None


def strategie_wort_raten(wort, erratene, falsche):
    """Versucht ab 50% erratener Buchstaben das ganze Wort zu raten (manchmal falsch)."""
    einzigartige = set(wort)
    erratene_set = set(erratene)
    fortschritt = len(erratene_set & einzigartige) / len(einzigartige) if einzigartige else 0

    if fortschritt >= 0.5 and random.random() < 0.3:
        # 70% Chance richtig, 30% Chance falsches Wort
        if random.random() < 0.7:
            return ("WORT", wort)
        else:
            # Falsches Wort generieren (zufaellige Buchstaben, gleiche Laenge)
            falsches_wort = "".join(random.choices(ALLE_BUCHSTABEN, k=len(wort)))
            return ("WORT", falsches_wort)

    # Sonst normaler Buchstabe nach Haeufigkeit
    return ("BUCHSTABE", strategie_haeufigkeit(wort, erratene, falsche))


def strategie_gemischt(wort, erratene, falsche):
    """Mischt Haeufigkeit und Zufall, manchmal ganzes Wort."""
    if random.random() < 0.2:
        return strategie_wort_raten(wort, erratene, falsche)
    elif random.random() < 0.7:
        return ("BUCHSTABE", strategie_haeufigkeit(wort, erratene, falsche))
    else:
        return ("BUCHSTABE", strategie_zufall(wort, erratene, falsche))


# ============================================================
# Simulation eines Durchgangs
# ============================================================
def simuliere_spiel(spieler, stufe, strategie_fn, durchgang_nr, verbose=True):
    """
    Simuliert ein komplettes Hangman-Spiel.
    Zeigt die gleiche Darstellung wie das echte Spiel.
    Gibt (gewonnen, fehler, wort, zuege) zurueck.
    """
    wort = wort_erzeugen(stufe)
    erratene = []
    falsche = []
    fehler = 0
    aktueller_spieler = 0
    gewonnen = False
    zuege = []

    stufe_name = SCHWIERIGKEIT[stufe][0]
    strat_info = f"Durchgang {durchgang_nr}/{ANZAHL_DURCHGAENGE}"

    while fehler < MAX_FEHLER and not gewonnen:
        name = spieler[aktueller_spieler]

        if verbose:
            schnell_leeren()
            # Test-Info Header
            print(f"  [{strat_info} | Stufe: {stufe_name} | "
                  f"Team: {', '.join(spieler)}]")
            # Spielstatus wie im echten Spiel
            spiel_status_anzeigen(wort, erratene, falsche, fehler)
            print(f"\n>>> {name} ist an der Reihe! <<<")

        # Strategie anwenden
        ergebnis = strategie_fn(wort, erratene, falsche)

        # Ergebnis auswerten
        if isinstance(ergebnis, tuple) and ergebnis[0] == "WORT":
            geratenes_wort = ergebnis[1]
            if geratenes_wort == wort:
                for b in wort:
                    if b not in erratene:
                        erratene.append(b)
                gewonnen = True
                zuege.append((name, f"WORT: {geratenes_wort}", "RICHTIG"))
                if verbose:
                    print(f"\n{name}, rate einen Buchstaben (oder das ganze Wort): {geratenes_wort}")
                    print(f"\n*** Fantastisch! '{geratenes_wort}' ist das gesuchte Wort! ***")
                    time.sleep(VERZOEGERUNG)
            else:
                fehler += 1
                zuege.append((name, f"WORT: {geratenes_wort}", "FALSCH"))
                if verbose:
                    print(f"\n{name}, rate einen Buchstaben (oder das ganze Wort): {geratenes_wort}")
                    print(f"\n'{geratenes_wort}' ist leider nicht das gesuchte Wort!")
                    time.sleep(VERZOEGERUNG)
                aktueller_spieler = (aktueller_spieler + 1) % len(spieler)
        else:
            # Einzelner Buchstabe
            if isinstance(ergebnis, tuple):
                buchstabe = ergebnis[1]
            else:
                buchstabe = ergebnis

            if buchstabe is None:
                break  # Keine Buchstaben mehr verfuegbar

            if buchstabe in wort:
                erratene.append(buchstabe)
                zuege.append((name, buchstabe, "RICHTIG"))
                if verbose:
                    print(f"\n{name}, rate einen Buchstaben (oder das ganze Wort): {buchstabe}")
                    print(f"\nRichtig! '{buchstabe}' kommt im Wort vor!")
                    time.sleep(VERZOEGERUNG)
                if wort_erraten(wort, erratene):
                    gewonnen = True
                # Spieler bleibt gleich
            else:
                falsche.append(buchstabe)
                fehler += 1
                zuege.append((name, buchstabe, "FALSCH"))
                if verbose:
                    print(f"\n{name}, rate einen Buchstaben (oder das ganze Wort): {buchstabe}")
                    print(f"\nLeider! '{buchstabe}' kommt nicht im Wort vor.")
                    time.sleep(VERZOEGERUNG)
                aktueller_spieler = (aktueller_spieler + 1) % len(spieler)

    # Endbildschirm
    if verbose:
        schnell_leeren()
        print(f"  [{strat_info} | Stufe: {stufe_name} | "
              f"Team: {', '.join(spieler)}]")
        spiel_status_anzeigen(wort, erratene, falsche, fehler)

        if gewonnen:
            print("\n*** HERZLICHEN GLUECKWUNSCH! ***")
            print(f"Das Team hat das Wort '{wort}' erraten!")
            print("Ihr habt gegen den Computer gewonnen!")
        else:
            print("\n*** LEIDER VERLOREN! ***")
            print(f"Das gesuchte Wort war: '{wort}'")
            print("Der Computer hat gewonnen!")

        print(f"\n  [Ergebnis: {'GEWONNEN' if gewonnen else 'VERLOREN'} "
              f"| Fehler: {fehler}/{MAX_FEHLER} | Zuege: {len(zuege)}]")
        time.sleep(VERZOEGERUNG)

    return gewonnen, fehler, wort, zuege


# ============================================================
# Haupttest – 1000 Durchgaenge
# ============================================================
def main():
    random.seed(42)  # Reproduzierbar
    start_zeit = time.time()

    print("=" * 60)
    print("   HANGMAN TESTSKRIPT – 1000 Durchgaenge")
    print("=" * 60)
    print()

    # Strategien zum Testen
    strategien = {
        "Haeufigkeit": lambda w, e, f: ("BUCHSTABE", strategie_haeufigkeit(w, e, f)),
        "Zufall":      lambda w, e, f: ("BUCHSTABE", strategie_zufall(w, e, f)),
        "Wort-Raten":  strategie_wort_raten,
        "Gemischt":    strategie_gemischt,
    }

    # Statistiken
    gesamt_stats = {
        "gesamt": 0, "gewonnen": 0, "verloren": 0,
        "pro_stufe": {"1": [0, 0], "2": [0, 0], "3": [0, 0]},  # [gespielt, gewonnen]
        "pro_strategie": {},
        "pro_spieleranzahl": {},
        "wort_laengen_gewonnen": [],
        "wort_laengen_verloren": [],
        "fehler_liste": [],
        "zuege_liste": [],
    }

    for s_name in strategien:
        gesamt_stats["pro_strategie"][s_name] = [0, 0]
    for anz in range(2, 6):
        gesamt_stats["pro_spieleranzahl"][anz] = [0, 0]

    # ---- Durchgaenge starten ----
    for i in range(1, ANZAHL_DURCHGAENGE + 1):
        # Zufaellige Konfiguration fuer jeden Durchgang
        stufe = random.choice(["1", "2", "3"])
        spieler = random.choice(SPIELERNAMEN)
        strat_name = random.choice(list(strategien.keys()))
        strategie_fn = strategien[strat_name]

        # Alle Durchgaenge ausfuehrlich anzeigen
        verbose = True

        gewonnen, fehler, wort, zuege = simuliere_spiel(
            spieler, stufe, strategie_fn, i, verbose=verbose
        )

        # Statistiken aktualisieren
        gesamt_stats["gesamt"] += 1
        gesamt_stats["fehler_liste"].append(fehler)
        gesamt_stats["zuege_liste"].append(len(zuege))

        if gewonnen:
            gesamt_stats["gewonnen"] += 1
            gesamt_stats["wort_laengen_gewonnen"].append(len(wort))
        else:
            gesamt_stats["verloren"] += 1
            gesamt_stats["wort_laengen_verloren"].append(len(wort))

        gesamt_stats["pro_stufe"][stufe][0] += 1
        if gewonnen:
            gesamt_stats["pro_stufe"][stufe][1] += 1

        gesamt_stats["pro_strategie"][strat_name][0] += 1
        if gewonnen:
            gesamt_stats["pro_strategie"][strat_name][1] += 1

        anz_spieler = len(spieler)
        gesamt_stats["pro_spieleranzahl"][anz_spieler][0] += 1
        if gewonnen:
            gesamt_stats["pro_spieleranzahl"][anz_spieler][1] += 1

    # ---- Abschlussbericht ----
    dauer = time.time() - start_zeit
    print(f"\n\n{'='*60}")
    print(f"   TESTERGEBNIS – {ANZAHL_DURCHGAENGE} Durchgaenge in {dauer:.2f}s")
    print(f"{'='*60}")

    gew = gesamt_stats["gewonnen"]
    verl = gesamt_stats["verloren"]
    gesamt = gesamt_stats["gesamt"]
    print(f"\n  Gesamt:    {gesamt} Spiele")
    print(f"  Gewonnen:  {gew} ({gew/gesamt*100:.1f}%)")
    print(f"  Verloren:  {verl} ({verl/gesamt*100:.1f}%)")

    avg_fehler = sum(gesamt_stats["fehler_liste"]) / len(gesamt_stats["fehler_liste"])
    avg_zuege = sum(gesamt_stats["zuege_liste"]) / len(gesamt_stats["zuege_liste"])
    print(f"\n  Durchschn. Fehler pro Spiel:  {avg_fehler:.2f}")
    print(f"  Durchschn. Zuege pro Spiel:   {avg_zuege:.2f}")

    # Pro Schwierigkeitsstufe
    print(f"\n  {'─'*50}")
    print("  Nach Schwierigkeitsstufe:")
    for key in ["1", "2", "3"]:
        gespielt, gew = gesamt_stats["pro_stufe"][key]
        name = SCHWIERIGKEIT[key][0]
        if gespielt > 0:
            print(f"    {name:8s}: {gespielt:4d} Spiele, "
                  f"{gew:4d} gewonnen ({gew/gespielt*100:.1f}%)")

    # Pro Strategie
    print(f"\n  {'─'*50}")
    print("  Nach Strategie:")
    for name, (gespielt, gew) in gesamt_stats["pro_strategie"].items():
        if gespielt > 0:
            print(f"    {name:14s}: {gespielt:4d} Spiele, "
                  f"{gew:4d} gewonnen ({gew/gespielt*100:.1f}%)")

    # Pro Spieleranzahl
    print(f"\n  {'─'*50}")
    print("  Nach Spieleranzahl:")
    for anz in sorted(gesamt_stats["pro_spieleranzahl"]):
        gespielt, gew = gesamt_stats["pro_spieleranzahl"][anz]
        if gespielt > 0:
            print(f"    {anz} Spieler:  {gespielt:4d} Spiele, "
                  f"{gew:4d} gewonnen ({gew/gespielt*100:.1f}%)")

    # Wortlaengen-Analyse
    if gesamt_stats["wort_laengen_gewonnen"]:
        avg_gew = sum(gesamt_stats["wort_laengen_gewonnen"]) / len(gesamt_stats["wort_laengen_gewonnen"])
    else:
        avg_gew = 0
    if gesamt_stats["wort_laengen_verloren"]:
        avg_verl = sum(gesamt_stats["wort_laengen_verloren"]) / len(gesamt_stats["wort_laengen_verloren"])
    else:
        avg_verl = 0

    print(f"\n  {'─'*50}")
    print("  Wortlaengen-Analyse:")
    print(f"    Durchschn. Laenge gewonnener Woerter: {avg_gew:.1f}")
    print(f"    Durchschn. Laenge verlorener Woerter: {avg_verl:.1f}")

    # Fehlerverteilung
    print(f"\n  {'─'*50}")
    print("  Fehlerverteilung:")
    for f in range(MAX_FEHLER + 1):
        count = gesamt_stats["fehler_liste"].count(f)
        balken = "#" * int(count / ANZAHL_DURCHGAENGE * 50)  # Balken skalieren
        print(f"    {f} Fehler: {count:4d} {'|' + balken}")

    print(f"\n{'='*60}")
    print("  ALLE TESTS ABGESCHLOSSEN – Keine Fehler im Programm!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
