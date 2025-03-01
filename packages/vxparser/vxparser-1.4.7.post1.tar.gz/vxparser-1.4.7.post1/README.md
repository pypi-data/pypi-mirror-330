# vavoo-parser (für LiveTV) + xstream-addon (für VoD's & Series) ...

## Next Gen fork - (Beta!) CLI Version 1.4.7

# Update Verlauf:

<details>
<summary>Klick HIER für Content.</summary>

### Update to 1.4.7-1:
- veclist.json von michaz1988.github.io auf Mastaaa1987.github.io verschoben und download url angepasst ...
### Update to 1.4.7:
- Einen neuen Menüpunkt im Hauptmenü hinzugefügt. Dieser startet die install.py für den vxparser.service um diesen voll automatisch in ein Unix (root) System zu speichern und ggf. direkt aus zu führen.
- install.py komplett überarbeitet. Jetzt ist jeder Inhalt genauso wie beim vxparser in Deutsch oder Englisch versehen.
- Einen neuen Process hinzugefügt, da beim livetv die befüllung der Datenbank und die m3u8 Listen Erstellung aufgeteilt worden sind.
- Noch ein neuen Menüpunkt im Vavoo Untermenü hinzugefügt. Und zwar lässt sich der Process der Datenbank befüllung jetzt seperat damit anstoßen.
### Update to 1.4.6:
- epg provider tvSpielfilme plugin gefixxt, sodass wenn magenta mal wieder verbindungsprobleme hat, man einfach zu tvs wechseln kann um seine epg.xml.gz zu erstellen.
- megakino Site Plugin: hoster url aktuallisiert, nun geht megakino auch wieder ...
- Als vorerst letztes Site Plugin xcine hinzugefügt.
- Die epg Service Einstellung von Vavoo Einstellungen in Haupt Einstellungen verschoben. Jetzt können alle 3 Services in den Haupt Einstellungen eingestellt werden.
- Die Service Wartezeit einstellung von Stunden in 5 Tagen geändert.
- Die VoD & Series Übergabe automatisiert. Die Weiterleitung an den Clienten funktioniert jetzt bedeutend geschmeidiger ...
- So alle Site Plugins funktionieren momentan im Auto Modus sowie in der Globalen Suche. Solange das jetzt der Fall bleibt, war dies vorerst mein letztes Update! Muss reichen ;-) (Und natürlich gibt es Buggs die ich fixxen muss ^^)
### Update to 1.4.5:
- Fixxed api getStream link Übergabe (remove |User-Agent=.* in link). Endlich funktionieren die site plugins ordnungsgemäß.
- Site Plugins noch einmal angepasst, dokus4 removed. Jetzt funktionieren alle Site Plugins ordnungsgemäß.
### Update to 1.4.4:
- ResolveURL auf Version 5.1.145 geupdated & soweit angepasst dass jetzt alles wieder reibungslos funktioniert mit der Hoster übergabe.
- Programm Versions check eingebaut, sodass beim updaten vom vxparser alle Datenbanken geleert werden um errors innerhalb der Datenbank beim updaten zu vermeiden.
- Site Plugins noch etwas an gepasst, xcine removed, movie4k added.
### Update to 1.4.3:
- Diverse site plugins den letzten schliff gegeben, damit es weitesgehend reibungslos abläuft.
- Einen Service layer für VoD's & Serien hinzugefügt. Somit ist es jetzt möglich alle Bereiche vom vxparser voll automatisch laufen zu lassen.
- Fist start PreMenu ein gebaut. Jetzt ist es beim ersten start vom vxparser nun die Menüsprache auf Deutsch oder Englisch stellen kann.
- Danach besteht die möglichkeit alle Services zu deaktivieren, damit für den User erstmal ggf. nötige Einstellungen vorab zu tätigen. (wie z.b. Server ip zu setzen ...)
### Update to 1.4.2-1:
- Xstream Conten wieder hinzu gefügt + site plugins to aktueller version (4.1.2) updated ...
### Update to 1.4.1-1:
- OMG die install.py soll Malware detection ausgelöst haben ich kanns nicht glauben -.-
### Update to 1.4.1:
- Added LiveTV funktion um eigene m3u8 listen & gruppen zu erstellen + stream links hinzu zufügen ...
### Update to 1.4.0:
- Remove Xstream part zwecks Anti Malware detection ...
### Update v1.3.0 -> v.1.3.2:
- epg.xml.gz export bug fixx ... Jetzt läuft's wieder gut ;-)
### Update v1.3.0:
- Xtream Code Api letzte Funktion komplementiert. (get.php m3u/m3u_plus ...)
- added custom_sid: '' to return json, nun laufen alle gängigen Xtream Code App's wie IPTV Smarters, IPTV Extream, IPTV Pro usw.
### Update to v1.2.5:
- Xtream Code Api gefixxt, sodass jetzt xtream code api, livetv + serien + filme mit epg läuft ...
### Update to v1.2.1:
- HLS/TS Stream Source Settings wahl für Xtream api code Live TV ...
- Einstellung für epg Provider, Icon & Rytec ID's xml.gz generation ...
- Automatische erfassung der Internet IP für den Vavoo key, ggf automatische neu generierung dessen ...
- Vavoo Live TV hls Streams hinzugefügt, sodass via SmartIPTV auf Samsung Smart TV's gestreamt werden kann...
- Global Search, Fixxed sodass jetzt auch Filme gesucht und geaddet werden konnen ...
- Signatur Key check integriert, sodass wenn sich internet ip ändert bzw. key sigvalitUntil ausläuft, automatisch ein neuer Key angefordert wird ...
- Main Settings wurden neu gestaltet, jetzt gibts ne kleine Info zur Setting ;-)
- Xtream Code zu 100% integriert. Ab jetzt kann insofern Xtream Code api vom clienten unterstützt wird, den gesamten Kontent darüber bekommen könnt! (Info hier drunter ^^)
</details>

# Installation / Start:

<details>
<summary>Klick HIER für Content.</summary>

```shell
python3 -m pip install vxparser
```

```shell
vxparser
```

### Android AiO installer Apk (Termux):

Für jeden der den vxparser auf seinen Android Smart TV oder so installieren will, für den habe ich eine AiO Termux apk gebaut. Einfach installieren und beim erstmaligen starten von Termux läd er eine (ca. 100mb) bootstrap File herunter. Der vxparser startet dann vollautomatisch mit Termux zusammen.

[vxparser_termux_0.83.apk](https://github.com/Mastaaa1987/termux-vxparser/releases/download/v0.8.3/vxparser_termux_0.83.apk)

- Für ein Update vom vxparser muss nur die Termux App Daten gelöscht & die bootstrap erneut herunter geladen werden.

</details>

# Menü Aufbau / General Ablauf:

<details>
<summary>Klick HIER für Content.</summary>


1. Menü Information:

Allgemeine Menüpunkt Auswahl (bestätigung) via
- [ENTER]

Im Selection Menü Menüpunkt Auswahl (select) via
- [Leertaste] (an oder abwählen)
- [Rechts] (anwählen eines Menüpunktes)
- [Links] (abwählen eines Menüpunktes)

Bestätigung der getroffenen Auswahl im Selection Menü via
- [ENTER]

Falls das Menü mal nicht Sichtbar sein sollte (zwecks output etc.), bekommt man es wieder Sichtbar indem man [Hoch] oder [Runter] geht.


2. Menü Aufbau:

- Main Menü:

```shell
   Einstellungen =>                     #Submenü
   Vavoo Untermenü (LiveTV) =>          #Submenü
   Xstream Untermenü (VoDs & Series) => #Submenü
   Stop Services                        #Services einschaltbar via Settings
   Starte Services Neu                  #epg_service / m3u8_service:
   - Leere Datenbank (Einstellungen)    #Löscht aktuelle einstellungen aus der Sqlite Datenbank
   - Lösche Data Ordner                 #Löscht den aktuellen cache Ordner
   <= Herunterfahren                    #Exit Programm
```

- Main Settings:

```shell
   <= Back                              #Zurück zum Hauptmenü
   [0.0.0.0]                            #FastAPI Server IP (0.0.0.0 = listen on all ips)
   [192.168.2.67]                       #Server IP for M3U8 List Creation
   [8080]                               #Server Port
   [On]                                 #Set Automatic Network IP to Server IP Setting
   [Off]                                #LiveTV m3u8 Listen Erstellung Background Service.
   [12]                                 #Warte Zeit zwischen m3u8 Listen Erstellung in Stunden.
   [Off]                                #VoD & Series m3u8 Listen Erstellung Background Service.
   [112]                                #Warte Zeit zwischen VoD & Series Listen Erstellung in Stunden.
   [Info]                               #Log Level (1=Info,3=Error)
   [Off]                                #Search in TMDB after VoD & Series Infos
   []                                   #Username of S.to User Accound
   []                                   #Password for S.to User Accound
   [ts]                                 #Bevorzugter codec für Xtream Codes
```

- Vavoo Menü:

```shell
Einstellungen =>                        #Submenü
List|Group|Stream Untermenü =>          #Submenü
Erstelle M3U8 Listen                    #Erstellt Sky LiveTV m3u8 Lists (alle Länder...)
Hole epg.xml.gz                         #Erstellt epg.xml.gz für Germany LiveTV
- Lösche Datenbank (LiveTV)             #Löscht alle LiveTV Einträge aus der Datenbank.
<= Haupt Menu                           #Zurück zum Hauptmenü
```

- Vavoo Settings:

```shell
   <= Back
   [On]                                 #Generate HLS m3u8
   [On]                                 #Vavoo Channel Namen ersetzen
   [Magenta]                            #Provider to get EPG Infos
   [Off]                                #Start epg.xml.gz Creation for LiveTV als Service
   [5]                                  #Sleep Time for epg.xml.gz Creation Service in Tagen
   [7]                                  #Anzahl an Tagen für epg.xml.gz Erstellung
   [On]                                 #Provider IDs mit Rytec ersetzen
   [Provider]                           #Logos bevorzugen
```

- Info:
Wenn sich die Server Ip ändert 1x "Get LiveTV Lists" ausgewählen, damit die aktuelle Netzwerk IP in den LiveTV Listen ersetzt wird.
ggf. "Delete Signatur Key" falls momentaner Signatur Key noch nicht ausgelaufen ist. (neuer key wird automatisch erstellt...)

- List|Group|Stream Menü:

```shell
   <= Zurück                            #Zurück zum Vavoo Menü.
   M3U8 Listen Menü =>                  #Menü um m3u8 Listen zu erstellen, zu bearbeiten & zu löschen.
   Gruppen Menü =>                      #Menü um Gruppen zu einer m3u8 Liste hinzu zufügen, zu bearbeiten & zu löschen.
   Stream Menü =>                       #Menü um Ausgewählte Country Streams zu einer Gruppe hinzu zufügen, zu bearbeiten & zu löschen.
```

- Info:
Genereller Ablauf ist wie folgt:
1. M3U List Menu => um eine neue m3u8 Liste zu erstellen.
2. Group Menu => um eine oder mehrere Gruppen zu einer neuen m3u8 Liste hinzu zufügen.
3. Stream Menu => um Streams aus einem ausgewählten Country zu einer Gruppe hinzu zufügen.

- M3U List Menu:

```shell
   <= Zurück                            #Zurück zum List|Group|Stream Menü.
   Neue M3u8 Liste hinzufügen           #Erstellt eine neue m3u8 Liste (Die via http://<ip>:<port>/<list_name>.m3u8 ab zu rufen ist).
   Bearbeite M3u8 Liste                 #Bearbeitet den Namen einer der selbst erstellen m3u8 Liste.
   Lösche M3u8 Liste                    #Löscht eine selbst erstellte m3u8 Liste.
```

- Group Menu:

```shell
   <= Zurück                            #Zurück zum List|Group|Stream Menü.
   Neue Gruppe hinzufügen               #Erstellt eine neue Gruppe für eine selbst erstellte m3u8 Liste.
   Bearbeite eine Gruppe                #Bearbeitet den Namen einer der selbst erstellen Gruppe.
   Lösche eine Gruppe                   #Löscht eine selbst erstellte Gruppe.
```

- Stream Menu:

```shell
   <= Zurück                            #Zurück zum List|Group|Stream Menü.
   Füge Streams zu einer Gruppe hinzu   #Fügt Streams zu einer selbst erstellten Gruppe hinzu.
   Bearbeite Streams in M3u8 Liste      #Dieser Menü Punkt hat momentan noch keine funktion.
```

- Xstream Menü:

```shell
   Einstellungen =>                     #Site Einstellungen, an/abschaltung einzelner Sites für Suche/Auto Generation.
   Globale Suche                        #Site Suche um Movies und/oder Serien zur Datenbank hinzu zu fügen.
   Hole neue VoD & Serien Daten         #Automatische Suche nach Inhalten in allen Sites (Sites unter Settings ein/abschaltbar)
   Erstelle vod+series.m3u8 erneut      #Erstellt vod.m3u8 (für Filme) + series.m3u8 (für Serien) aus der Datenbank.
   - Lösche Datenbank (Streams)         #Löscht alle Stream's aus der Datenbank.
   <= Haupt Menü                        #Zurück zum Hauptmenü
```

- Info:
Genereller Ablauf ist wie folgt:
1. "Get New VoD & Series" oder "Global Search" zum befüllen der Datenbank.
2. Gefolgt von "ReCreate vod+series.m3u8" um die neuen Datenbank einträge in die Listen zu schreiben.
- ggf. Wenn sich die Server Ip ändert 1x"ReCreate vod+series.m3u8" ausgewählen, damit die aktuelle Netzwerk IP in den LiveTV Listen ersetzt wird.

- Xstream Settings:

```shell
[X] cinemathek: auto list creation?  # Aktiviert Site für die Automatische Suche (Xstream Menü: Get New VoD & Series)
[X] cinemathek: global search?       # Aktiviert SIte für die Site Suche (Xstream Menü: Global Search)
...
...
```

</details>

### Allgemeiner Ablauf:

<details>
<summary>Klick HIER für Content.</summary>

Die meisten Programm Daten leiten sich von dem Kodi Plugin Xstream (Special thanks to Xstream Team!) & resolverurl (Special thanks to gujal!) ab.

Das Autoscript durchsucht die Sites bis zu dem link "showHosters" und trägt alle Items inklusive aller relevanten Infos in die Datenbank.

Wenn dann ein Stream vom Clienten angefordert wird, holt der Server alle aktuellen Hoster zu dem Item ein und leitet den 1. Stream an den Clienten weiter. (insofern Online ...)

Fragt man den selben Item nocheinmal an, mekt sich der Server die Position in der Hoster Liste und versucht dann den 2. Stream der List an den Clienten weiter. (insofern mehr als 1 Hoster vorhanden ...)

Dabei spielt es momentan noch keine Rolle ob der vorige Stream Erfolgreich weitergeleitet wurde oder nicht. Das bedeutet will man wieder zur 1. Hoster Url muss das Item so lange angefragt werden bis der Server wieder bei der 1. Url zurück springt ... (Output Infos im Server Terminal ...)

</details>

# Xtream Codes API Readme:

<details>
<summary>Klick HIER für Content.</summary>

Xtream ist nun soweit verbaut dass die panel_api.php, player_api.php & xmltv.php zu 100% via GET+POST Callable sind ...

Wie gehabt spielt der username & password keine Rolle, aber um auch Items angezeigt zu bekommen muss zuvor (wie für die m3u8 listen) Get LiveTV Lists (für LiveTV) oder

Get New VoD & Series (für Filme & Serien) zumindest 1x ausgeführt worden sein. Genauer gesagt es sollten auch Datensätze in der Database vorhanden sein ;-)

Aber dann läuft der LiveTV teil komplett ohne das auf die Server IP in den m3u8 Listen geachtet werden muss, zwecks dynamischer Übergabe dessen (und automatischer SigKey

überprüfung, funktioniert selbst Intetnet IP change nahtlos ohne das was eingestellt werden muss! (Solange die Server API von mir local auf dem Client Gerät gestartet ist!)

Z.b. über Android -> Termux -> locale Ausführung meiner API ...

So das erstmal dazu, jetzt gibts noch ne api callable Übersicht (Beispiel Anhand GET Requests, für POST Request müssen die Parameter in body form übertragen werden ...):

(* = kann man eingeben was man will! X = int(id) ... (also eine Zahl ^^))


- GET ACCOUND Info:
```shell
panel_api.php?username=*&password=*
```
- GET VOD Stream Categories:
```shell
player_api.php?username=*&password=*&action=get_vod_categories
```
- GET VOD Streams:
```shell
player_api.php?username=*&password=*&action=get_vod_streams
player_api.php?username=*&password=*&action=get_vod_streams&category_id=X
```
- GET VOD Info:
```shell
player_api.php?username=*&password=*&action=get_vod_info&vod_id=X
```
- GET SERIES Categories:
```shell
player_api.php?username=*&password=*&action=get_series_categories
```
- GET SERIES Streams:
```shell
player_api.php?username=*&password=*&action=get_series
player_api.php?username=*&password=*&action=get_series&category_id=X
```
- GET SERIES Info:
```shell
player_api.php?username=*&password=*&action=get_series_info&series_id=X
```
- GET LIVE Categories:
```shell
player_api.php?username=*&password=*&action=get_live_categories
```
- GET LIVE Streams:
```shell
player_api.php?username=*&password=*&action=get_live_streams
player_api.php?username=*&password=*&action=get_live_streams&category_id=X
```
- GET XMLTV:
```shell
xmltv.php?username=*&password=*
```
- GET EPG:
```shell
player_api.php?username=*&password=*&action=get_simple_data_table&steam_id=X
```
- GET SHORT EPG:
```shell
player_api.php?username=*&password=*&action=get_short_epg&steam_id=X&limit=X
```
- GET m3u:
```shell
get.php?username=*&password=*&type=[m3u|m3u_plus]&output=[hls|ts|mpegts|rtmp]
```

</details>

### Verbesserungen in dieser Version:

<details>
<summary>Klick HIER für Content.</summary>

- API komplett mit Python 3 verwendbar. Alle benötigten Packages via pip installierbar. Keine zusätzlichen Binaries benötigt! (wie lighttpd, php in termux Version z.b...)
- Auf jedem System startbar. Android (via Termux ab Android version 5), Linux, Raspberry Pi, Windows ...
- Effizienz Steigerung im Allgemein verfahren durch multiprocessing bzw. async requests ...

</details>

### Erneuerungen in dieser Version:

<details>
<summary>Klick HIER für Content.</summary>

- CLI Menü
- Settings
- Service Option (LiveTV m3u8 lists & epg.xml.gz)
- Xstream Addon integration (voll automatische Kontent abfrage der aktuell beliebtesten Stream Sites für Filme und Serien ...)
Momentan verfügbare Plugins:
- cinemathek
- dokus4
- filmpalast
- hdfilme
- kinokiste
- kino
- kkiste
- megakino
- movie2k
- movie4k
- movieking
- serienstream (accound benötigt!)
- streamcloud
- streamen
- streampalace
- xcine

</details>

# Copyright 2025 @Mastaaa1987

