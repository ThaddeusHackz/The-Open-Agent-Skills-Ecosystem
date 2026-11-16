---
name: letterxpress
description: >
  Erzeugt DIN 5008-konforme Geschaeftsbriefe als PDF. Optional: Versand ueber
  die LetterXpress Print-and-Mail API (Testmodus).

  TRIGGERS - Use this skill when user says:
  - "Brief schreiben" / "Geschaeftsbrief" / "DIN 5008"
  - "write a letter" / "create a letter" / "draft a letter"
  - "business letter" / "formal letter" / "official letter"
  - "Fensterbrief" / "Brief nach DIN 5008"
  - "Brief versenden" / "send a letter" / "mail a letter"
  - "LetterXpress" / "Briefversand" / "postal mail"
  - Any German correspondence request that needs formal formatting
---

# Geschaeftsbrief Skill (DIN 5008 + optionaler LetterXpress-Versand)

Dieses Skill erzeugt DIN 5008-konforme Geschaeftsbriefe als PDF.
Optional koennen Briefe ueber die LetterXpress API versendet werden
(im **Testmodus**, d.h. keine Kosten, keine echten Briefe).

## Umgebung einrichten

Bevor die eigentlichen Scripts ausfuehrbar sind, muss eine virtuelle Umgebung
mit allen Abhaengigkeiten eingerichtet werden. Dafuer nutzt der Skill `uv` --
einen schnellen Python-Paketmanager. Das Setup-Script erledigt alles automatisch:

```bash
python3 SKILL_DIR/scripts/setup_env.py
```

Das erstellt eine `.venv` im Skill-Verzeichnis und installiert `reportlab` und
alle weiteren Abhaengigkeiten aus `requirements.txt`. Danach werden alle Scripts
mit dem Python aus der venv aufgerufen:

```bash
SKILL_DIR/.venv/bin/python3 SKILL_DIR/scripts/create_din5008_letter.py ...
```

Falls `uv` noch nicht installiert ist, installiere es zuerst:

```bash
pip install uv --break-system-packages
```

Das Setup muss nur einmal pro Umgebung laufen. Falls die `.venv` bereits
existiert, prueft das Script ob alles aktuell ist und ueberspringt die Erstellung.

## Ablauf

Der Workflow besteht aus vier Schritten:

1. **Briefdaten sammeln** -- Absender, Empfaenger, Betreff, Inhalt
2. **Quality-Gate: Pre-Validation** -- Daten pruefen bevor das PDF erzeugt wird
3. **DIN 5008 PDF erzeugen** -- mit dem Script `scripts/create_din5008_letter.py`
4. **User fragen: Versand gewuenscht?** -- Falls ja: Post-Validation + LetterXpress-Versand

Nach der PDF-Erstellung ist der Brief fertig. Frage den Benutzer explizit:
"Soll der Brief ueber LetterXpress versendet werden?" Nur wenn der Benutzer
zustimmt, fahre mit Schritt 4 (Validation + Versand) fort. Andernfalls ist
der Workflow nach Schritt 3 abgeschlossen.

Das Quality-Gate (`scripts/validate_letter.py`) ist ein automatischer Test, der
sicherstellt, dass Absender und Empfaenger korrekt im Sichtfenster eines
DIN-Fensterbriefumschlags positioniert sind. Kein Brief wird versendet, bevor
das Quality-Gate bestanden ist.

## Schritt 1: Briefdaten sammeln

Frage den Benutzer nach folgenden Informationen (soweit nicht bereits bekannt):

**Absender:**
- Name / Firma
- Strasse und Hausnummer
- PLZ und Ort
- Optional: Telefon, E-Mail, Website

**Empfaenger:**
- Name / Firma
- Optional: Zusatzzeile (z.B. "z.Hd. Frau Mueller")
- Strasse und Hausnummer
- PLZ und Ort
- Land (falls nicht Deutschland)

**Brief:**
- Betreff (kurz und praegnant)
- Brieftext (der eigentliche Inhalt)
- Ort und Datum (Standard: heute)
- Grussformel (Standard: "Mit freundlichen Gruessen")
- Unterschrift-Name

Wenn der Benutzer nur sagt "schreibe einen Brief an X wegen Y", formuliere den
Brieftext selbst in einem professionellen, hoeflichen Geschaeftsdeutsch. Zeige
dem Benutzer den entworfenen Text und frage, ob er passt, bevor du das PDF
erzeugst.

## Schritt 2: Quality-Gate Pre-Validation

Bevor das PDF erzeugt wird, pruefe die Briefdaten mit dem Validierungsscript.
Das verhindert, dass ein fehlerhaftes PDF erzeugt und versendet wird.

```bash
python3 SKILL_DIR/scripts/validate_letter.py --letter /path/to/brief.md --strict
```

Das Script prueft:
- Alle Pflichtfelder vorhanden (Absender: Name, Strasse, PLZ, Ort; Empfaenger ebenso)
- PLZ-Format korrekt (5 Ziffern fuer deutsche Adressen)
- Ruecksendeangabe passt in die Breite des Briefumschlag-Fensters (max. 90 Zeichen)
- Empfaengeranschrift hat maximal 6 Zeilen (DIN 5008 Vorgabe)
- Einzelne Adresszeilen passen in die Fensterbreite (max. ~55 Zeichen bei 11pt)
- Betreff und Brieftext vorhanden
- Anrede beginnt mit "Sehr geehrt..." oder "Liebe..."
- Grussformel vorhanden

**Wichtig:** Nur wenn das Script Exit-Code 0 liefert (alle Pruefungen bestanden),
darf mit der PDF-Erstellung fortgefahren werden. Bei Fehlern muessen die Daten
korrigiert werden.

## Schritt 3: DIN 5008 PDF erzeugen

Lies die DIN 5008 Spezifikation in `references/din5008_spec.md` fuer Details
zu den exakten Massen. Das Script `scripts/create_din5008_letter.py` setzt
diese Spezifikation vollstaendig um (Form B).

Erstelle eine Markdown-Datei mit YAML-Frontmatter:

```markdown
---
sender_name: Max Mustermann GmbH
sender_street: Musterstrasse 1
sender_zip: "80331"
sender_city: Muenchen
sender_phone: "+49 89 123456"
sender_email: info@mustermann.de
sender_website: www.mustermann.de
recipient_name: Erika Beispiel AG
recipient_additional: z.Hd. Frau Mueller
recipient_street: Beispielweg 42
recipient_zip: "10115"
recipient_city: Berlin
recipient_country: ""
subject: Angebot Nr. 2024-001
date: 16. Februar 2026
location: Muenchen
closing: Mit freundlichen Gruessen
signature_name: Max Mustermann
briefpapier: /pfad/zum/briefpapier.pdf
---

Sehr geehrte Frau Mueller,

hiermit uebersenden wir Ihnen...

Der Brieftext folgt hier nach dem Frontmatter.
```

Dann rufe das Script auf:

```bash
SKILL_DIR/.venv/bin/python3 SKILL_DIR/scripts/create_din5008_letter.py \
  --output /path/to/brief.pdf \
  --letter /path/to/brief.md
```

Ersetze `SKILL_DIR` durch den tatsaechlichen Pfad zum Skill-Verzeichnis.

## Schritt 4 (optional): Post-Validation und LetterXpress-Versand

Dieser Schritt wird nur ausgefuehrt, wenn der Benutzer den Versand wuenscht.

### 4a: PDF validieren (Quality-Gate)

Nach der PDF-Erstellung wird das PDF nochmals geprueft. Falls `pdfminer.six`
oder `PyMuPDF` installiert ist, werden die tatsaechlichen Textpositionen im
PDF analysiert. Andernfalls reicht die Pre-Validation aus Schritt 2.

```bash
python3 SKILL_DIR/scripts/validate_letter.py \
  --letter /path/to/brief.md \
  --pdf /path/to/brief.pdf \
  --strict
```

Nur bei Exit-Code 0 darf versendet werden.

### 4b: An LetterXpress senden

Nutze `scripts/send_letterxpress.py`. Es arbeitet immer im **Testmodus**.

**Credentials:** Das Script liest Credentials automatisch aus der macOS Keychain
(Services: `letterxpress-username` und `letterxpress-apikey`). Falls nicht in
der Keychain vorhanden, frage den Benutzer und speichere sie:

```bash
security add-generic-password -s "letterxpress-username" -a "USER" -w "BENUTZERNAME" -U
security add-generic-password -s "letterxpress-apikey" -a "USER" -w "API_KEY" -U
```

Versand (Credentials werden aus Keychain gelesen):

```bash
python3 SKILL_DIR/scripts/send_letterxpress.py \
  --pdf /path/to/brief.pdf
```

Alternativ koennen Credentials auch direkt uebergeben werden:

```bash
python3 SKILL_DIR/scripts/send_letterxpress.py \
  --pdf /path/to/brief.pdf \
  --username "BENUTZERNAME" \
  --apikey "API_KEY"
```

### Versand-Optionen

| Parameter     | Standard       | Beschreibung                          |
|---------------|---------------|---------------------------------------|
| `--pdf`       | (erforderlich) | Pfad zur PDF-Datei                   |
| `--username`  | (erforderlich) | LetterXpress Benutzername            |
| `--apikey`    | (erforderlich) | LetterXpress API-Key                 |
| `--color`     | `1`            | 1 = schwarz/weiss, 4 = Farbe        |
| `--mode`      | `duplex`       | simplex oder duplex                  |
| `--shipping`  | `national`     | national oder international          |

Das Script gibt die Job-ID und den Status zurueck.

## Fehlerbehandlung

- Bei Quality-Gate-Fehlern: zeige die fehlgeschlagenen Pruefungen und schlage Korrekturen vor
- Bei API-Fehlern: zeige die Fehlermeldung und schlage Loesungen vor
- Bei Netzwerkproblemen: schlage vor, es erneut zu versuchen
- Bei fehlenden Credentials: frage den Benutzer erneut
- Wenn das PDF zu gross ist (max. 50 Seiten): informiere den Benutzer

## Briefpapier (optionales Overlay)

Im Frontmatter kann eine PDF-Datei als Briefpapier angegeben werden:

```yaml
briefpapier: /pfad/zum/briefpapier.pdf
```

Das Briefpapier wird als Hintergrund-Layer unter den Brief gelegt:
- **Seite 1** des Briefpapiers -> unter Seite 1 des Briefs
- **Seite 2** des Briefpapiers (falls vorhanden) -> unter alle Folgeseiten
- Hat das Briefpapier nur 1 Seite, wird diese fuer alle Seiten verwendet

Das Briefpapier-PDF muss DIN A4 Hochformat sein. Typisch enthaelt es Logo,
Kopfzeile, Fusszeile und Gestaltungselemente. Der Briefinhalt wird transparent
darueber gelegt -- das Briefpapier darf keine Inhalte in den Textbereichen haben.

**Hinweis:** Bei Verwendung von Briefpapier werden Absender-Header und
Falzmarken trotzdem gezeichnet. Falls das Briefpapier diese bereits enthaelt,
sollten die entsprechenden Felder im Frontmatter leer gelassen oder das
Briefpapier entsprechend gestaltet werden.

## Wichtige Hinweise

- **Testmodus ist immer aktiv** -- keine echten Briefe, keine Kosten
- **Quality-Gate ist Pflicht** -- kein Versand ohne bestandene Validierung
- Das PDF muss DIN A4 Hochformat sein
- Falzmarken und Lochmarke werden automatisch gesetzt
- Die Absenderzeile im Anschriftfeld ist in kleiner Schrift (6pt, unterstrichen)
- Der Brieftext nutzt 11pt Helvetica
- Das Briefumschlag-Sichtfenster liegt bei X: 20-110mm, Y: 45-90mm vom oberen Rand
- Empfaengeradresse beginnt bei 66mm vom oberen Rand (nicht 62.7mm), damit der
  LetterXpress Einschreiben-Banner (17mm hoch) immer Platz hat -- auch bei
  nachtraeglicher Entscheidung fuer Einschreiben-Versand
