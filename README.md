# Bist du da?

"Bist du da?" ist ein innovatives Gesichtserkennungs- und Anwesenheitsverwaltungssystem, das entwickelt wurde, um die Anwesenheit von Personen automatisch zu erkennen und zu verfolgen. Es kombiniert moderne Gesichtserkennungstechnologie mit einer benutzerfreundlichen grafischen Oberfläche und bietet zudem eine Integration zur Analyse und Speicherung von Pausenzeiten.

## Inhaltsverzeichnis

1. [Über das Projekt](#über-das-projekt)
2. [Funktionen](#funktionen)
3. [Installation](#installation)
4. [Verwendung](#verwendung)
5. [Webseiten-Integration](#webseiten-integration)
6. [Login- und Registrierungssystem](#login--und-registrierungssystem)
7. [Technologien](#technologien)
8. [Beitragende](#beitragende)
9. [Lizenz](#lizenz)

## Über das Projekt

Das Projekt "Bist du da?" ermöglicht es, die Anwesenheit von Personen in Echtzeit zu überwachen und aufzuzeichnen. Es ist ideal für Büros, Schulen und andere Institutionen, die eine effiziente Verwaltung der Anwesenheit benötigen. Die Software verwendet OpenCV zur Gesichtserkennung und speichert die erkannten Gesichter sowie die entsprechenden Anwesenheitszeiten in einer lokalen Datenbank. Zusätzlich können Pausenzeiten erfasst und analysiert werden, um eine vollständige Übersicht über die Aktivitäten zu gewährleisten.

## Funktionen

- **Echtzeit-Gesichtserkennung**: Erfassen und Erkennen von Gesichtern mit einer integrierten Kamera.
- **Anwesenheitsprotokollierung**: Speichert Anwesenheitsdaten in einer CSV-Datei und zeigt eine visuelle Darstellung an.
- **Pausenmanagement**: Ermöglicht das Starten und Stoppen von Pausen sowie die Analyse der Pausenzeiten.
- **Benutzerfreundliche Oberfläche**: Eine intuitive grafische Benutzeroberfläche für eine einfache Bedienung.
- **Integration mit einem RESTful API**: Sendet Anwesenheits- und Pausendaten an eine externe API zur weiteren Verarbeitung.

## Installation

### Voraussetzungen

- Python 3.x
- OpenCV
- Tkinter (wird normalerweise mit Python installiert)
- Scikit-Learn
- NumPy
- Requests
- win32com.client (Für Text-to-Speech, auf Windows)
- Flask (optional, für API-Tests)

### Installationsschritte

1. **Repository klonen**:
   ```bash
   git clone https://github.com/DeinBenutzername/bist-du-da.git
   cd bist-du-da
   ```

2. **Virtuelle Umgebung erstellen**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Bei Windows: venv\Scripts\activate
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Benötigte Dateien bereitstellen**:
   Stelle sicher, dass die Datei `haarcascade_frontalface_default.xml` im Ordner `data` vorhanden ist.

### Abhängigkeiten in `requirements.txt`

Erstelle eine Datei namens `requirements.txt` mit folgendem Inhalt:

```plaintext
opencv-python
scikit-learn
numpy
requests
flask  # Optional, für API-Tests
pywin32  # Nur für Windows (win32com.client)
boto3  # Für AWS DynamoDB Interaktion
```

## Verwendung

### Gesichtserkennung starten

1. Führe das Skript `add-face.py` aus, um ein neues Gesicht hinzuzufügen.
   ```bash
   python add-face.py
   ```

2. Starte das Hauptprogramm, um die Anwesenheit zu überwachen.
   ```bash
   python main.py
   ```

3. Verwende die Schaltflächen in der Benutzeroberfläche, um Pausen zu verwalten oder die Erfassung zu beenden.

### API-Daten senden

Die Anwesenheitsdaten können am Ende der Erfassung an eine externe API gesendet werden. Dies erfolgt automatisch, wenn die Schaltfläche "Ende" gedrückt wird.

## Webseiten-Integration

Das Projekt enthält auch eine Webseite, die Daten von der DynamoDB-Datenbank über eine API abruft und die Anwesenheits- sowie Pausenzeiten in einer übersichtlichen Tabelle darstellt.

### Funktionen der Webseite:

- **Anwesenheitsanzeige**: Zeigt die Anwesenheitsdaten von Benutzern für einen bestimmten Tag an.
- **Pause-Überprüfung**: Vergleicht die Pausenzeiten der Benutzer mit einer gespeicherten Zeit und markiert Abweichungen.
- **Datenaktualisierung**: Ermöglicht das Abrufen und Anzeigen von aktuellen Anwesenheitsdaten.

### Verwendung:

1. Die Webseite ruft die Anwesenheitsdaten und Pausenzeiten von einer AWS-Lambda-Funktion ab, die in der DynamoDB gespeicherte Daten bereitstellt.
2. Die Benutzeroberfläche zeigt diese Daten an und bietet zusätzliche Interaktionen wie das Überprüfen der Pause (mit visuellem Hinweis bei Abweichungen).

### Start der Webseite:

Die Webseite befindet sich im Ordner `webseite`. Öffne einfach die `index.html`-Datei in einem Browser, um die Anwendung zu starten. 

## Login- und Registrierungssystem

Das System unterstützt ein sicheres Login- und Registrierungssystem, bei dem nur autorisierte Benutzer Zugriff haben.

### Funktionen:

- **Benutzerregistrierung**: Nur vorab autorisierte E-Mail-Adressen (z. B. Lehrer) können sich registrieren.
- **Passwort-Hashing**: Passwörter werden sicher mit SHA-256 gehasht und in der DynamoDB gespeichert.
- **Login**: Benutzer können sich mit ihrer E-Mail und ihrem Passwort anmelden.

### Implementierung:

- **DynamoDB**: Speichert Benutzerinformationen wie E-Mail und gehashtes Passwort.
- **AWS Lambda**: Handhabt die Registrierung und das Login durch Verarbeiten von HTTP-Anfragen und Interaktion mit DynamoDB.
- **API Gateway**: Dient als Schnittstelle zwischen dem Frontend (Webseite) und der AWS Lambda-Funktion.

### Code Beispiele:

- **Registrierung**:
   ```python
   # Boto3 Code zur Speicherung von Benutzerdaten in DynamoDB
   ```

- **Login**:
   ```python
   # Boto3 Code zur Authentifizierung eines Benutzers mit DynamoDB
   ```

## Technologien

- **Programmiersprache**: Python, HTML, CSS, JavaScript
- **Bibliotheken**: OpenCV, Tkinter, Scikit-Learn, Requests, NumPy, Boto3
- **API**: RESTful API mit AWS Lambda und API Gateway
- **Datenbank**: AWS DynamoDB

## Beitragende

- **Dein Name** - Entwickler und Projektleiter

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die [LICENSE](LICENSE)-Datei für Details.
```

You can copy this content directly into your README.md file. It now includes detailed information about the login and website functionalities integrated into the project, with sections dedicated to the API interactions, AWS Lambda, and DynamoDB for managing users and attendance data.
