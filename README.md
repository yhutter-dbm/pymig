# Pymig

## Ausgangslage / Motivation

Ich möchte eine Webapplikation entwickeln, welche es einem erlaubt, auf einfach Art und Weise Bildergallerien zu erstellen. Meine Motivation dahinter ist es eine Ordnung im "Bilderchaos" von Personen zu schaffen. Auch soll mit Hilfe von Metainformationen wie Tags und Titel die erstellten Gallerien durchsucht werden können.

## Funktion / Projektidee

- Gallerien erstellen
- Gallerien editieren
- Gallerien löschen
- Gallerien anschauen (Bildervorschau)
- Gallerie liken
- Nach Gallerien mit Hilfe von Metainformationen wie Titel und Tags suchen

## Workflow

- Zu Beginn erstellt der Benutzer Gallerien. Hierzu gibt er der zu erstellenden Gallerie einen Tilte, Bilder sowie Metainformationen (Tags, Like Status)
- Der Benutzer kann die erstellten Gallerien in einer Übersicht ansehen.
- Der Benutzer kann die erstellten Gallerien jederzeit editieren oder löschen
- Der Benutzer kann jederzeit die Bilder, welche zu einer spezifischen Gallerie gehören anschauen
- Nach Gallerien kann mit einer Suchfunktion gesucht werden

### Dateneingabe

Eine Gallerie hat folgende Informationen, welche vom Benutzer angegeben werden müssen:

- Titel
- Bilder welche zur Gallerie gehören
- Tags um eine Gallerie einfach suchen zu können
- Like-Status (Favoriten)

### Datenverarbeitung / Speicherung

Als Datenspeicherung wird eine JSON Datei verwendet, diese weisst folgende Struktur auf

```json
[
  {
    "title": "my awesome gallery 1",
    "tags": ["awesome", "omg"],
    "liked": true,
    "images": [
      {
        "path": "c:\\awesome-image.png"
      },
      {
        "path": "c:\\awesome-image.png"
      }
    ]
  },
  {
    "title": "my awesome gallery 2",
    "tags": ["omg"],
    "liked": false,
    "images": [
      {
        "path": "c:\\awesome-image.png"
      },
      {
        "path": "c:\\awesome-image.png"
      }
    ]
  }
]
```

### Datenausgabe

Wie bereits erwähnt wird die Datenstruktur als JSON Datei abgespeichert, siehe Kapitel **Datenverarbeitung / Speicherung**.

### Mockups

![Überblick Gallerien](/mockups/1-My-Galleries.png)
Dies ist die Ansicht welche der Benutzer beim Öffnen der Webapplikation sieht. Hier erhält er einen Überblick über all seine Gallerien

![Gallerie löschen](/mockups/2-Delete-a-Gallery.png)
Beim Löschen einer Gallery wird ein Dialog eingeblendet, welche den Benutzer zur Bestätigung auffordert.

![Ein Blick in eine Gallery](/mockups/3-Look-at-It.png)
Der Benutzer kann über jederzeit die Bilder, welche einer bestimmten Gallerie zugeordnet sind anschauen. Hierzu klickt er einfach auf "Look at it". Anschliessend werden die Bilder der Gallerie dargestellt.

![Neue Gallerie erstellen](/mockups/4-Create-a-new-Gallery.png)
Auf dieser Ansicht muss der Benutzer alle notwendigen Informationen angeben. Hierzu gehört der Name der Gallery sowie die Tags und der Like Status. Zudem hat der Benutzer die Möglichkeit über ein "Drop-Target" verschiedene Bilder hochzuladen.

![Bestehende Gallerie editieren](/mockups/5-Edit-Gallery.png)
Natürlich hat der Benutzer auch die Möglichkeit eine Gallerie zu editieren.

![Suchfunktion](/mockups/6-Search.png)
Mit Hilfe der Suchfunktion ist es sehr einfach möglich eine gewünschte Gallerie zu finden. Es kann mit Hilfe der hinterlegten Tags gesucht werden. Die Suchresultate können zudem noch nach "Like-Status" gefiltert werden.

### Seitennavigation / Szenarios
Das untenstehende Ablaufdiagramm soll veranschaulichen, wohin der Benutzer bei bestimmten Interaktionen mit der Webseite gelangt.
![Szenarios](/scenarios/scenarios.png)