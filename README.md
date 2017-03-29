# Chat-palvelin

Chat-palvelin tietoliikennekurssin työksi.

## Versiot
* Python 3.5
sekä Python-kirjastot
* socket (latest)
* threading (latest)

## Suunnitelma

Projektin tavoite on tehdä palvelin-asiakas-keskusteluohjelma, joka tukee viestien lähettämistä, palvelimelle yhdistämistä ja sieltä poistumista.

## Protokolla

Ohjelmalle on suunniteltu TCP:n päälle viestintäprotokolla.

### Palvelimelta asiakkaalle

#### BROADCAST
Välittää asiakkaan lähettämän viestin muille asiakkaille.

```
BROADCAST\n
user_name\n
message content\n
\0
```

### Asiakkaalta palvelimelle

#### CONNECT
Ilmoittaa yhdistäneen asiakkaan käyttäjänimen.

```
CONNECT\n
user_name\n
\0
```

#### DISCONNECT
Ilmoittaa asiakkaan katkaisevan yhteyden.

```
DISCONNECT\n
user_name\n
\0
```

#### MESSAGE
Lähettää viestin palvelimelle välitettäväksi muille asiakkaille BROADCASTilla.

```
MESSAGE\n
user_name\n
message content\n
\0
```

#### KEEPALIVE
Ylläpitää yhteyttä palvelimeen, jos käyttäjä ei ole aktiivinen. Lähetetään tasaisin väliajoin.

```
KEEPALIVE\n
user_name\n
\0
```

## Tekijät

Jan Tuomi ja Toni Miilunpalo
