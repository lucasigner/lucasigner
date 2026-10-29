"""Gespeicherte Aktivitäten aus daten/ wochenweise auswerten (nur lokal, keine Anfrage an Garmin).

Aufruf: python3 auswerten.py daten/aktivitaeten_VON_BIS.json
Woche 0 = die letzten 7 Tage vor dem Enddatum der Datei, Woche 1 = die 7 Tage davor usw.
"""

import json
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

LAUF = {"running", "trail_running", "treadmill_running", "track_running"}


def ohne_doppelte(aktivitaeten):
    # Zweites Gerät: Start weniger als 60 s auseinander -> nur den Eintrag mit mehr Daten behalten.
    sortiert = sorted(aktivitaeten, key=lambda a: a["startTimeLocal"])
    ergebnis = []
    for a in sortiert:
        start = datetime.fromisoformat(a["startTimeLocal"])
        if ergebnis and abs((start - datetime.fromisoformat(ergebnis[-1]["startTimeLocal"])).total_seconds()) < 60:
            if sum(v is not None for v in a.values()) > sum(v is not None for v in ergebnis[-1].values()):
                ergebnis[-1] = a
            continue
        ergebnis.append(a)
    return ergebnis, len(sortiert) - len(ergebnis)


def main():
    datei = Path(sys.argv[1])
    bis = date.fromisoformat(datei.stem.split("_")[-1])
    aktivitaeten, doppelt = ohne_doppelte(json.loads(datei.read_text(encoding="utf-8")))
    print(f"{len(aktivitaeten)} Aktivitäten ({doppelt} doppelte entfernt), Woche 0 endet am {bis}\n")

    wochen = defaultdict(list)
    for a in aktivitaeten:
        tag = datetime.fromisoformat(a["startTimeLocal"]).date()
        wochen[max(0, ((bis - tag).days - 1) // 7)].append(a)

    for nr in sorted(wochen):
        liste = wochen[nr]
        stunden = sum(a.get("duration") or 0 for a in liste) / 3600
        sportarten = defaultdict(float)
        for a in liste:
            sportarten[(a.get("activityType") or {}).get("typeKey", "?")] += (a.get("duration") or 0) / 60
        zonen = [sum(a.get(f"hrTimeInZone_{z}") or 0 for a in liste) / 60 for z in range(1, 6)]
        mittel = sum(a.get("moderateIntensityMinutes") or 0 for a in liste)
        hoch = sum(a.get("vigorousIntensityMinutes") or 0 for a in liste)
        last = sum(a.get("activityTrainingLoad") or 0 for a in liste)
        ohne_puls = sum(1 for a in liste if a.get("averageHR") is None)

        print(f"Woche {nr}: {len(liste)} Einheiten, {stunden:.1f} h, Trainingslast {last:.0f}")
        print("  Sportarten (min): " + ", ".join(f"{k} {v:.0f}" for k, v in sorted(sportarten.items(), key=lambda x: -x[1])))
        print("  Pulszonen 1-5 (min): " + " / ".join(f"{z:.0f}" for z in zonen) + (f"  ({ohne_puls} ohne Puls)" if ohne_puls else ""))
        print(f"  Intensitätsminuten: {mittel} mittel, {hoch} hoch")
        for a in liste:
            if (a.get("activityType") or {}).get("typeKey") in LAUF and a.get("averageSpeed") and a.get("averageHR"):
                minuten, sekunden = divmod(round(1000 / a["averageSpeed"]), 60)
                meter_pro_schlag = a["averageSpeed"] * 60 / a["averageHR"]
                print(f"  Lauf {a['startTimeLocal'][:10]}: {a['distance'] / 1000:.2f} km, Pace {minuten}:{sekunden:02d} min/km, "
                      f"Ø HF {a['averageHR']:.0f}, {meter_pro_schlag:.2f} m pro Herzschlag")
        print()


if __name__ == "__main__":
    main()
