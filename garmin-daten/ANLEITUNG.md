# Garmin Personal API – Einrichtung (Cloud-Variante)

Ziel: Eigene Garmin-Daten über die Garmin Personal API auslesen und auswerten. Nur lesend.

## Rahmen

- Umgebung: Claude Code in der Cloud (claude.ai), Nutzer arbeitet unter Windows.
- Der API-Schlüssel steht **nicht** in einer Datei und **nie** im Chat. Er ist in den
  Einstellungen der Cloud-Umgebung als Umgebungsvariable `GARMIN_API_KEY` hinterlegt.
- Den Schlüssel nie ausgeben, weder im Terminal noch in einer Datei. Prüfen nur über die Länge.
- `.env` und `daten/` bleiben per `.gitignore` aus dem Repository.
- Keine Endpunkte oder Adressen erfinden: nur aus Garmins Dokumentation, die der Nutzer einfügt.
- Code vor dem Ausführen zeigen und in zwei Sätzen erklären, dann erst ausführen.
- Nur Python-Standardbibliothek, keine zusätzlichen Pakete ohne Rückfrage.
- Nur im Ordner `garmin-daten/` arbeiten.
- Immer nur ein Schritt, danach fragen, ob es geklappt hat.

## Stand

- [x] Schritt 1: Python 3 vorhanden, Ordner und `.gitignore` angelegt.
- [x] Schritt 2: Schlüssel in Garmin Connect erstellt.
- [ ] Schritt 3: Schlüssel als `GARMIN_API_KEY` in den Umgebungs-Einstellungen hinterlegen,
      neue Sitzung starten, prüfen, ob die Variable gesetzt ist (Länge > 0, Wert nie anzeigen).
- [ ] Schritt 4: Nutzer kopiert Garmins Doku (Basis-Adresse, Authentifizierung,
      Beispiel-Request) in den Chat. Daraus `holen.py` schreiben: Aktivitäten der letzten
      7 Tage, Antwort unter `daten/` speichern. Danach berichten: Anzahl, Felder, ob Schlaf,
      Puls und HRV dabei sind; testen, ob Zeiträume vor 30 und vor 180 Tagen abrufbar sind.
      Bei 401, 403 oder 429 in einem Satz erklären; bei 429 warten statt in einer Schleife.
      Falls die Netzwerk-Richtlinie den Garmin-Host blockt: Host in den Umgebungs-Einstellungen
      unter „Allowed domains“ freigeben.
- [ ] Schritt 5: Auswerten. Drei Starts anbieten:
      (a) letzte Woche: Umfang, Intensität, Pace im Verhältnis zur Herzfrequenz;
      (b) Trainingsplan für zwei Wochen (vorher Ziel, Renndatum und freie Tage erfragen);
      (c) was ein guter Trainer zu diesen Daten sagen würde.
      Mit echten Zahlen und Einheiten rechnen und sagen, wenn die Datenlage zu dünn ist.
      Auf die Uhr schicken geht mit der Personal API nicht.

## Sicherheit

- Läuft der Schlüssel ab oder war er sichtbar: In Garmin Connect einen neuen erstellen,
  den alten löschen und `GARMIN_API_KEY` in den Umgebungs-Einstellungen ersetzen.
