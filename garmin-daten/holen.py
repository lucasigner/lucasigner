"""Aktivitäten (Standard: letzte 7 Tage) über die Garmin Personal API holen und unter daten/ speichern.

Aufruf: python3 holen.py [tage] [vor]  – z. B. "7 30" = 7 Tage, die vor 30 Tagen enden.

Basis-Adresse, Token-Pfad und Endpunkt stammen aus Garmins Beispiel-Client
github.com/garmin/connect-personal-api-python (constants.py, auth.py, client.py).
Der Schlüssel kommt nur aus der Umgebungsvariable GARMIN_API_KEY und wird nie ausgegeben.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

BASIS = "https://personal.connectapi.garmin.com"
TOKEN_PFAD = "/personalapitoken-service/personal-api/personal-api-key/token"
AKTIVITAETEN_PFAD = "/activitylist-service/activities/search/activities"
TIMEOUT = 30

FEHLER = {
    401: "401: Schlüssel oder Token ungültig bzw. abgelaufen – in Garmin Connect einen neuen erstellen.",
    403: "403: Zugriff verweigert – der Schlüssel hat für diese Daten keine Berechtigung.",
    429: "429: Zu viele Anfragen – bitte eine Weile warten und dann einmal neu starten.",
}


def anfrage(methode, pfad, kopfzeilen, parameter=None):
    url = BASIS + pfad
    if parameter:
        url += "?" + urllib.parse.urlencode(parameter)
    req = urllib.request.Request(url, method=methode, headers=kopfzeilen)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as antwort:
            return antwort.read()
    except urllib.error.HTTPError as fehler:
        print(FEHLER.get(fehler.code, f"HTTP {fehler.code} bei {methode} {pfad}"), file=sys.stderr)
        if fehler.code == 429 and fehler.headers.get("Retry-After"):
            print(f"Garmin bittet um {fehler.headers['Retry-After']} Sekunden Pause.", file=sys.stderr)
        sys.exit(1)


def main():
    schluessel = os.environ.get("GARMIN_API_KEY", "").strip()
    if not schluessel:
        sys.exit("GARMIN_API_KEY ist nicht gesetzt.")

    # Schlüssel gegen ein Bearer-Token tauschen (nur im Speicher, keine Datei).
    token = anfrage("POST", TOKEN_PFAD, {"Accept": "*/*", "Authorization": f"ApiKey {schluessel}"})
    token = token.decode().strip()

    # Optional: Anzahl Tage und wie viele Tage zurück das Fenster endet, z. B. "holen.py 7 30".
    tage = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    vor = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    bis = date.today() - timedelta(days=vor)
    von = bis - timedelta(days=tage)
    daten = anfrage(
        "GET",
        AKTIVITAETEN_PFAD,
        {"Accept": "application/json", "Authorization": f"Bearer {token}"},
        {"start": 0, "limit": 100, "startDate": von.isoformat(), "endDate": bis.isoformat()},
    )

    aktivitaeten = json.loads(daten) if daten else []
    ordner = Path(__file__).parent / "daten"
    ordner.mkdir(exist_ok=True)
    ziel = ordner / f"aktivitaeten_{von}_{bis}.json"
    ziel.write_text(json.dumps(aktivitaeten, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(aktivitaeten)} Aktivitäten von {von} bis {bis} gespeichert in {ziel.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
