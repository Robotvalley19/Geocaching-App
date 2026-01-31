# 🗺️ Geocaching Web App -- Offline-First Flask Application

Eine **offlinefähige Full-Stack Geocaching-Webanwendung** auf Basis von
Flask, Leaflet und MySQL.\
Konzipiert für den privaten Einsatz im lokalen Netzwerk (z. B. Raspberry
Pi) mit Tablet-Frontend.

Die Anwendung ermöglicht das Erfassen, Verwalten und Anzeigen von
Geocaches inklusive Bild-Upload, Filterfunktionen und
Offline-Kartenmaterial auf Basis von OpenStreetMap.

------------------------------------------------------------------------

# 🎯 Projektziel

Dieses Projekt demonstriert:

-   Full-Stack Webentwicklung (Backend + Frontend)
-   REST-API Design
-   Datenbankintegration (MySQL)
-   Datei-Uploads mit Sicherheitsprüfung
-   Offline-First Architektur
-   Nebenläufigkeit (Multi-Threading)
-   Deployment im lokalen Netzwerk

Die Anwendung wurde eigenständig konzipiert und umgesetzt.

------------------------------------------------------------------------

# 🚀 Features

## 🗺️ Kartenfunktion (Leaflet)

-   Klick auf Karte → Cache anlegen
-   Marker mit Popup-Informationen
-   Offline Tile-Unterstützung (OpenStreetMap)
-   Umschaltbare Kartenlayer
-   Marker-Highlight & Sidebar-Synchronisierung

## 🗃️ Cache-Verwaltung

-   Name (Pflichtfeld)
-   Funddatum
-   Ort
-   Hinweis
-   Bemerkung
-   Bild-Upload (Validierung via Pillow)
-   Speicherung in MySQL

## 🔎 Filterfunktionen

-   Filter nach Name
-   Volltextsuche (Hinweis, Bemerkung, Ort)
-   Datumsfilter
-   Dynamische Aktualisierung

## 💾 Offline-First Ansatz

-   Offline Tile Server
-   LocalStorage-Fallback bei Serverausfall
-   Automatische Wiederverbindungsprüfung

## 🔒 Sicherheitsmechanismen

-   `secure_filename()` für sichere Dateinamen
-   10MB Upload-Limit
-   Bildvalidierung mit Pillow
-   Pfad-Normalisierung gegen Directory Traversal
-   Prepared Statements gegen SQL-Injection

## ⚙️ Multi-Thread Tile Downloader

-   Parallelisierte Tile-Downloads
-   Einstellbare Zoomlevel
-   Konfigurierbare Thread-Anzahl
-   Optionaler Delay zum Schutz des Tile-Servers

------------------------------------------------------------------------

# 🧱 Tech Stack

  Bereich         Technologie
  --------------- ---------------------------
  Backend         Flask (Python)
  Datenbank       MySQL
  Frontend        HTML5, Bootstrap 5
  Karten          Leaflet.js
  Offline Tiles   OpenStreetMap
  Bildprüfung     Pillow
  Plattform       Raspberry Pi 4 (optional)

------------------------------------------------------------------------

# 🏗️ Architektur

Client (Browser / Tablet)\
↓\
Flask Backend (REST API)\
↓\
MySQL Datenbank\
↓\
Filesystem (Uploads + Tiles)

------------------------------------------------------------------------

# ⚙️ Installation

## 1️⃣ Repository klonen

``` bash
git clone https://github.com/USERNAME/geocaching-app.git
cd geocaching-app
```

## 2️⃣ Virtuelle Umgebung erstellen

``` bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

``` bash
venv\Scripts\activate
```

## 3️⃣ Abhängigkeiten installieren

``` bash
pip install flask mysql-connector-python pillow python-dotenv tqdm requests
```

## 4️⃣ MySQL Datenbank einrichten

``` sql
CREATE DATABASE geocache;

USE geocache;

CREATE TABLE caches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lat DECIMAL(10,8) NOT NULL,
    lon DECIMAL(11,8) NOT NULL,
    found_date DATE,
    hint TEXT,
    remark TEXT,
    location VARCHAR(255),
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5️⃣ Umgebungsvariablen konfigurieren

`.env` Datei erstellen:

    DB_HOST=localhost
    DB_USER=dein_user
    DB_PASSWORD=dein_passwort
    DB_NAME=geocache

## 6️⃣ Anwendung starten

``` bash
python app.py
```

Standard:

    http://localhost:5012

------------------------------------------------------------------------

# 🗺️ Offline Tiles generieren

``` bash
python tile_downloader.py --minz 0 --maxz 8 --threads 8 --delay 0.1
```

⚠ Bitte die OpenStreetMap Tile Usage Policy beachten.

------------------------------------------------------------------------

# 📂 Projektstruktur

    geocaching-app/
    │
    ├── app.py
    ├── tile_downloader.py
    ├── .env
    ├── static/
    │   ├── uploads/
    │   └── tiles/
    ├── templates/
    │   ├── base.html
    │   └── index.html
    └── README.md

------------------------------------------------------------------------

# 🧠 Technische Highlights

-   REST-API Architektur
-   Sauberes File-Handling mit Sicherheitschecks
-   Client-seitiger Fallback-Mechanismus
-   Offline-First Design
-   Multi-Threading (ThreadPoolExecutor)
-   Path Traversal Protection
-   Strukturierte Projektarchitektur
-   Netzwerkfähiger Betrieb (Raspberry Pi)

------------------------------------------------------------------------

# 🔮 Mögliche Erweiterungen

-   Benutzer-Authentifizierung (JWT)
-   Rollen- & Rechtesystem
-   GPX-Import
-   Docker-Deployment
-   Reverse Proxy (NGINX)
-   Unit-Tests & CI/CD Pipeline

------------------------------------------------------------------------

# 👨‍💻 Autor

**Robotvalley19**\
Full-Stack Entwickler (Backend + Frontend + Offline-Architektur)

Eigenständiges Projekt zur Demonstration moderner Webentwicklung mit
Fokus auf Offline-Fähigkeit, Sicherheit und sauberer Architektur.
