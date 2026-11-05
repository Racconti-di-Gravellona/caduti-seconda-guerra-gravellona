# Caduti gravellonesi della Seconda guerra mondiale

Sito statico autonomo (una pagina + dati) sui morti, dispersi e deportati di
Gravellona Lomellina nella seconda guerra mondiale (1940-1945). È il terzo
della serie, dopo `guerre-indipendenza-gravellona` e `caduti-gravellona`
(Grande Guerra): stesso metodo, stessa grafica, ricerca locale senza cookie.

**URL previsto:** <https://racconti-di-gravellona.github.io/caduti-seconda-guerra-gravellona/>

## Cosa contiene

- **30 nominativi**: 20 dalla lista di Colli (13 caduti + 6 dispersi + 1
  deportata civile, pp. 105-106 di Colli 1960) + 10 uomini nati a Gravellona
  che la lista locale non aveva, dalla Banca dati Caduti e Dispersi 2.a GM
  del Ministero della Difesa.
- Statistiche: esiti, anno di morte, teatro (Russia/Ucraina, Albania/Grecia,
  Germania, Italia), età.
- Ricerca client-side (testo libero + stato), senza cookie e senza tracking.
- Il perché i due elenchi non coincidono: la lista registra i *residenti*,
  la banca dati i *nati* a Gravellona (come per la Grande Guerra).
- Correzioni note: Dellupi (non «Deluppi»), Baratti (non «Baralti»),
  Travaglino nato a Gravellona Toce nelle schede Difesa, Carnevale Mario con
  date divergenti tra le schede.

## File

| file | ruolo |
|---|---|
| `index.html` | pagina generata (non modificare a mano) |
| `build.py` | genera `index.html` da `caduti.json` |
| `caduti.json` | i 30 record (unica fonte dati curata) |
| `difesa_grezzo.json` | trascrizione grezza delle schede Difesa (27 voci, con duplicati) |
| `style.css` | stili |
| `cerca.js` | filtro locale |
| `privacy.html` | privacy, correzioni, licenza |

## Rigenerare la pagina

```sh
python3 build.py
```

## Fonti

- Ernesto Colli, *Gravellona Lomellina nella sua storia*, Novara 1960, cap.
  «I Caduti per la Patria», p. 105 (lista «1940-1945 (2.a guerra mondiale)» e
  dispersi) e p. 106 (salme rimpatriate nel 1955). Nomi letti
  direttamente sull'immagine di `pagine_originali/.../pag_107.jpg` (nel repo
  `wikipedia_storia_gravellona`): l'OCR intreccia le due colonne.
- Ministero della Difesa, Banca dati dei Caduti e Dispersi 2.a guerra
  mondiale (SICAD), <https://www.difesa.it/il-ministro/cadutiinguerra/secondaguerra/secondaguerra.html>
  — 318.740 fascicoli; interrogata a novembre 2026 per luogo di nascita
  «Gravellona Lomellina» via `sicadapi.difesa.it`.

## Limiti noti

- La banca dati Difesa copre caduti e dispersi *riconosciuti*; i dispersi
  non riconosciuti restano fuori. 10 nominativi di Colli sono
  «senza riscontro».
- L'OMI/deportazione in Germania (Carnevale Pietro, Travaglino, Moro Guido,
  Dellupi? e la deportata Clotilde in Biscaldi) va definita con Albo IMI
  (Archivio di Stato di Bolzano) e ANED.
- Il monumento ai Caduti (piazza Delucca) va fotografato e incrociato.

## Pubblicazione

GitHub Pages, branch `main`, cartella radice, come i due siti gemelli.

## Licenza

Testi originali: CC BY 4.0. I dati storici sono citati dalle fonti
indicate e non sono coperti dalla licenza.
