# Pymig

## Ausgangslage / Motivation
Ich will eine Web Applikation erstellen, mit welcher leicht Bilder hochgeladen, editiert und verwaltet werden können.
An Hand der Bilder sollen schlussendlich Bildergallerien erstellt werden können.

## Funktion / Projektidee
- Gallerien erstellen (ist der Hauptkernpunkt der Anwendung)
- Gallerien können ebenfalls mit Metainformationen angereichert werden (Tags etc.)
- Bilder hochladen und Gallerien zuordnen
- Bilder mit Metainformationen (Tags, Beschreibung, Ort der Bildaufnahme anreichern)
- Kommentarfunktion für die Bilder
- Bilder mit vordefinierten Filtern versehen (Gaussian-Blur, Schwarz-Weiss etc.)
- Verzeichnisstruktur von Bildern anlegen (Ordner etc.)
- Bilder "liken"
- Nach Bildern und Gallerien suchen können (an Hand des Gallerienamens und der hinterlegten Metainformationen)

## Workflow
- Benutzer muss immer zuerst eine Bildergallerie anlegen, es können keine Bilder ohne eine zuvor definierten Bildergallerie hochgeladen werden
- Wenn eine Gallerie erstellt wurde, kann der Benutzer beliebige Bilder hinzufügen
- Beim Hochladen eines Bildes wird das Bild mit Metainformationen angereichert (Name des Bildes, Tags, Ort der Aufnahme, Tags)
- Der Benutzer hat die Möglichkeit Bilder zu liken, dann erscheinen sie unter den "Favoriten"
- Über eine globale Suchfunktion kann schnell nach Gallerien und Bildern gesucht werden

### Dateneingabe
- Der Benutzer muss den Namen der Gallerie eingeben
- Zusätzlich zum Namen der Gallerie kann diese um Metainformationen angereichert werden
- Der Benutzer muss beim Hochladen der Bilder einen Namen etc. eingeben
- Der "Like" Status muss pro Bild individuell gespeichert werden.
- Über die Globale Suche kann mit Hilfe der Metainformationen in Bildgallerien und Bildern gesucht werden
- Bilder können editiert werden, hier kann der Benutzer vordefinierte Filter anwenden (Gaussian-Blur, Schwarz-Weiss etc.)

### Datenverarbeitung / Speicherung
Als Datenspeicherung wird eine JSON Datei verwendet, diese weisst folgende Struktur auf
```json
[
	"my_awesome_gallery" : {

	}
]
```

### Datenausgabe
TODO
