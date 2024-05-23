# Projektbeschreibung: Fahrkartenautomat (Ticket Vending Machine)

## Übersicht
Das Fahrkartenautomat-Projekt ist eine Desktop-Anwendung, die mit Python und der `customtkinter`-Bibliothek für die grafische Benutzeroberfläche (GUI) erstellt wurde. Diese Anwendung simuliert einen Fahrkartenautomaten, der es den Benutzern ermöglicht, Tickets auszuwählen, die Preise basierend auf der Entfernung zwischen Städten anzuzeigen und den Zahlungsprozess abzuschließen. Das Projekt integriert mehrere Seiten für eine reibungslose Benutzererfahrung.

## Funktionen
- **Startseite**: Begrüßt die Benutzer und bietet eine Option zum Auswählen eines Tickets.
- **Ticket Suchen Seite**: Benutzer können ihren Start- und Zielort eingeben, um verfügbare Tickets zu suchen. Die Entfernung zwischen den Städten wird mit der Geopy-Bibliothek berechnet und der Ticketpreis entsprechend festgelegt.
- **Ticket Hinzufügen Seite**: Zeigt die ausgewählten Ticketdetails und ermöglicht den Benutzern, ihre Auswahl zu bestätigen und mit der Zahlung fortzufahren.
- **Zahlungsmethode Seite**: Benutzer können zwischen verschiedenen Zahlungsmethoden wählen (EC-Karte oder Bargeld).
- **EC-Karte Seite**: Simuliert den Prozess der Zahlung mit einer EC-Karte.
- **Bargeld Seite**: Simuliert den Prozess der Zahlung mit Bargeld, einschließlich der Berechnung des Wechselgeldes.
- **Ticket Drucken Seite**: Bestätigt den Ticketkauf und simuliert das Drucken des Tickets.

## Klassen und Funktionen
1. **App Klasse**:
    - Initialisiert das Hauptfenster der Anwendung.
    - Verwaltet die Navigation zwischen verschiedenen Seiten.
    - Speichert ausgewählte Ticketinformationen (Start, Ziel und Preis).

2. **Page Klasse**:
    - Basisklasse für alle Seiten, von anderen Seitenklassen geerbt.

3. **MainPage Klasse**:
    - Zeigt eine Willkommensnachricht und eine Schaltfläche, um zur Seite "Ticket Suchen" zu navigieren.

4. **FindTicket Klasse**:
    - Ermöglicht Benutzern die Eingabe von Start- und Zielstädten.
    - Lädt Stadtinformationen aus einer JSON-Datei.
    - Berechnet die Entfernung und den Preis des Tickets.
    - Überprüft die Benutzereingaben und zeigt bei Bedarf Fehler an.

5. **AddTicketPage Klasse**:
    - Zeigt die ausgewählten Ticketdetails und den Preis.
    - Bietet eine Schaltfläche, um zur Auswahl der Zahlungsmethode zu gelangen.

6. **PaymentMethod Klasse**:
    - Zeigt verfügbare Zahlungsmethoden (EC-Karte oder Bargeld) an.
    - Navigiert zu den jeweiligen Zahlungsseiten.

7. **EcCard Klasse**:
    - Behandelt den Zahlungsvorgang mit der EC-Karte.
    - Simuliert das Scannen und die Validierung der Karte.

8. **Cash Klasse**:
    - Verwalte den Zahlungsvorgang mit Bargeld.
    - Berechnet den verbleibenden Betrag und das Rückgeld.
    - Ermöglicht dem Benutzer, fortzufahren, sobald der genaue Betrag bezahlt oder ausreichend Wechselgeld bereitgestellt wurde.

9. **PrintTicket Klasse**:
    - Simuliert den Druckvorgang des Tickets.
    - Zeigt einen Countdown-Timer an, bis das Ticket gedruckt wird.

## Datenverarbeitung
- **Stadtdaten**: Werden aus einer `germany.json`-Datei geladen, die Stadtnamen und Koordinaten zur Berechnung der Entfernung enthält.
- **Entfernungsberechnung**: Nutzt das `geopy.distance`-Modul zur Berechnung der Entfernungen zwischen Städten.

## Installation und Einrichtung
1. **Erforderliche Bibliotheken installieren**:
    ```sh
    pip install customtkinter geopy
    ```
2. **Die Anwendung starten**:
    ```sh
    python main.py
    ```

## Benutzerinteraktionsablauf
1. **Startseite**: Der Benutzer startet hier und klickt auf "Ticket auswählen".
2. **Ticket Suchen Seite**: Der Benutzer gibt Start- und Zielstädte ein und klickt auf "Suchen".
3. **Ticket Hinzufügen Seite**: Der Benutzer überprüft die Ticketdetails und klickt auf "Bestätigen".
4. **Zahlungsmethode Seite**: Der Benutzer wählt eine Zahlungsmethode (EC-Karte oder Bargeld).
5. **Zahlungsseiten**: Der Benutzer schließt die Zahlung ab.
6. **Ticket Drucken Seite**: Der Benutzer wartet, bis das Ticket gedruckt wird, dann ist der Prozess abgeschlossen.

Dieses Projekt zielt darauf ab, eine einfache und interaktive Erfahrung für Benutzer zu bieten, um den Kauf von Fahrkarten an einem Automaten zu simulieren. Das modulare Design stellt sicher, dass jeder Teil des Prozesses separat behandelt wird, was die Wartung und Erweiterung erleichtert.
