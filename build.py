#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera index.html per il sito «I gravellonesi della Seconda guerra mondiale».

Sorgente: caduti.json (30 record, da Colli 1960 pp. 105-106 + Banca dati
Caduti e Dispersi 2.a GM del Ministero della Difesa).
Uso: python3 build.py
"""

import html
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).parent
ROWS = json.loads((ROOT / "caduti.json").read_text(encoding="utf-8"))
EMAIL = "archivio-festadellarte@outlook.it"
AGGIORNATO = "5 novembre 2026"


def anno_di(s):
    """Estrae il primo anno 19xx dalla stringa data."""
    m = re.search(r"\b(19\d\d)\b", s)
    return int(m.group(1)) if m else None


def parti_data(s):
    """Da 'DD/MM/YYYY' a (y, m, d), o None se non completa."""
    corpo = s.split(",")[0].strip()
    m = re.match(r"(\d\d)/(\d\d)/(\d\d\d\d)$", corpo)
    if m:
        d, mo, y = (int(x) for x in m.groups())
        return (y, mo, d)
    return None


def eta(r):
    b, d = parti_data(r["nato"]), parti_data(r["morte"])
    if not b or not d:
        return None
    return d[0] - b[0] - ((d[1], d[2]) < (b[1], b[2]))


def teatro(r):
    l = r["morte"].lower()
    if "ucraina" in l or "russia" in l:
        return "Russia/Ucraina"
    if "germania" in l:
        return "Germania"
    if "albania" in l or "grecia" in l:
        return "Albania/Grecia"
    if "italia" in l:
        return "Italia"
    return "Non documentato"


def num(x):
    """26.6 -> 26,6"""
    return f"{x:.1f}".replace(".", ",")


def pct(a, b):
    return int(100 * a / b + 0.5) if b else 0


N = len(ROWS)

ESITI = {
    "morto": sum(r["esito"] == "morto" for r in ROWS),
    "disperso": sum(r["esito"] == "disperso" for r in ROWS),
    "deportata": sum(r["esito"] == "deportata" for r in ROWS),
}

ETAS = sorted(e for e in (eta(r) for r in ROWS) if e is not None)
ETA_MEDIA = statistics.mean(ETAS)
ETA_MEDIANA = statistics.median(ETAS)

TEATRI = {}
for r in ROWS:
    t = teatro(r)
    TEATRI[t] = TEATRI.get(t, 0) + 1
TEATRI_ORDINE = ["Russia/Ucraina", "Albania/Grecia", "Germania", "Italia", "Non documentato"]

ANNI = {}
for r in ROWS:
    y = anno_di(r["morte"])
    ANNI[y] = ANNI.get(y, 0) + 1
ANNI_ORDINE = [1940, 1941, 1942, 1943, 1944, 1945]
NON_DATATI = ANNI.get(None, 0)

IN_COLLI = [r for r in ROWS if r["in_colli"]]
FUORI = [r for r in ROWS if not r["in_colli"]]
NCOLA, NFUO = len(IN_COLLI), len(FUORI)
DOC_COLLI = sum(r["stato"] == "documentato" for r in IN_COLLI)
DA_CONFERMARE = sum(r["stato"] == "da confermare" for r in ROWS)
NDB = sum(
    1 for r in ROWS if r.get("difesa_ids") and "Gravellona Toce" not in r["nato"]
)

def riga_tabella(label, n, totale):
    return (
        f"<tr><td>{html.escape(label)}</td>"
        f'<td class="n">{n}</td><td class="n">{pct(n, totale)}%</td></tr>'
    )


def li(r):
    badges = []
    if r.get("badge"):
        badges.append(f'<span class="badge badge-fuori">{html.escape(r["badge"])}</span>')
    if r.get("in_lapide") is False:
        badges.append('<span class="badge badge-fuori">non nella lapide</span>')
    if r["stato"] == "da confermare":
        badges.append('<span class="badge badge-verifica">senza riscontro nella Banca dati Difesa</span>')
    if not r["in_colli"]:
        badges.append('<span class="badge badge-fuori">non nella lista di Colli</span>')
    badge_html = (" " + " ".join(badges)) if badges else ""
    cerca = html.escape(
        " ".join([r["nome"], r["paternita"], r["nato"], r["morte"], r["esito"], r["note"]]),
        quote=True,
    )
    nota = f'<span class="caduto-nota">{html.escape(r["note"])}</span>' if r["note"] else ""
    nato = html.escape(r["nato"]) if r["nato"] else "notizie anagrafiche non raccolte"
    morte = html.escape(r["morte"]) if r["morte"] else "morte documentata solo dall'elenco locale, senza data"
    return (
        f'<li data-stato="{html.escape(r["stato"], quote=True)}" data-cerca="{cerca}">'
        f'<strong>{html.escape(r["nome"])}</strong>{badge_html}'
        f'<span class="caduto-dettagli">nato: {nato} · {html.escape(r["esito"])}: {morte}</span>'
        f"{nota}</li>"
    )


elenco = "\n".join(li(r) for r in ROWS)
anni_rows = "\n".join(riga_tabella(str(y), ANNI.get(y, 0), N) for y in ANNI_ORDINE)
anno_non_datati_row = riga_tabella("non precisato", NON_DATATI, N)
teatri_rows = "\n".join(riga_tabella(t, TEATRI.get(t, 0), N) for t in TEATRI_ORDINE if TEATRI.get(t))
fuori_rows = "\n".join(
    riga_tabella(t, sum(teatro(r) == t for r in FUORI), NFUO)
    for t in TEATRI_ORDINE
    if sum(teatro(r) == t for r in FUORI)
)

HTML = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>I gravellonesi della Seconda guerra mondiale</title>
<meta name="description" content="{N} nominativi tra la lista di Colli 1960 e la Banca dati Difesa della 2.a guerra mondiale: statistiche, teatri di morte e schede.">
<link rel="canonical" href="https://racconti-di-gravellona.github.io/caduti-seconda-guerra-gravellona/">
<meta property="og:type" content="website">
<meta property="og:title" content="I gravellonesi della Seconda guerra mondiale">
<meta property="og:description" content="{N} nominativi tra Colli 1960 e Banca dati Difesa: teatri di morte, dispersi, deportata.">
<meta property="og:url" content="https://racconti-di-gravellona.github.io/caduti-seconda-guerra-gravellona/">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./">Caduti di Gravellona</a>
    <p class="motto">1940-1945 · Colli 1960 e Banca dati della Difesa</p>
  </div>
</header>

<main class="wrap">
  <h1>I gravellonesi della Seconda guerra mondiale</h1>
  <p class="lead">Ernesto Colli chiude il capitolo «I Caduti per la Patria» con la lista «1940-1945 (2.a guerra mondiale)»: <strong>{NCOLA} nominativi</strong> (13 caduti, 6 dispersi e una deportata civile). La <strong>Banca dati dei Caduti e Dispersi della 2.a guerra mondiale</strong> del Ministero della Difesa permette oggi di incrociarla: aggiunge paternità, date e teatri di morte, e riporta alla luce <strong>{NFUO} uomini nati a Gravellona</strong> che la lista locale non aveva. In tutto <strong>{N} gravellonesi</strong>: {ESITI["morto"]} morti, {ESITI["disperso"]} dispersi, {ESITI["deportata"]} deportata.</p>

  <h2 id="numeri">I numeri</h2>
  <p><strong>Età media alla morte: {num(ETA_MEDIA)} anni</strong> (mediana {ETA_MEDIANA if isinstance(ETA_MEDIANA, int) else num(ETA_MEDIANA)}; il più giovane {min(ETAS)}, il più anziano {max(ETAS)}), calcolata sui {len(ETAS)} nominativi con nascita e morte databili. Dopo l'armistizio dell'8 settembre 1943 muoiono in Germania — per internamento militare o deportazione — tre uomini; una donna viene deportata come civile.</p>

  <table>
    <thead><tr><th>anno di morte</th><th class="n">n.</th><th class="n">%</th></tr></thead>
    <tbody>
{anni_rows}
{anno_non_datati_row}
    </tbody>
  </table>

  <p class="nota-metodo">«Non precisato» raccoglie i nominativi documentati solo dalla lista locale di Colli, senza data; sono i {DA_CONFERMARE} nominativi segnati «senza riscontro» nell'elenco.</p>

  <table>
    <thead><tr><th>teatro, su tutti e {N}</th><th class="n">n.</th><th class="n">%</th></tr></thead>
    <tbody>
{teatri_rows}
    </tbody>
  </table>

  <p class="nota-metodo">Le doppie schede Difesa di Baratto, Dellupi, Romè, Carnevale Mario, Galletti e Maffei (una con la data e senza luogo, una con nazione «Russia» e senza data) indicano un <strong>disperso del fronte russo la cui morte fu riconosciuta con data convenzionale</strong> (il 1.o del mese: 01/12/1942, 01/01/1943). La data non è quella del decesso: se fu prigionia o morte nella ritirata lo dice solo il fascicolo matricolare.</p>

  <p><strong>La Russia/Ucraina è il teatro maggiore</strong> ({TEATRI.get("Russia/Ucraina", 0)} su {N}): il fronte russo pesa quanto tutti gli altri teatri noti messi insieme. Seguono Albania/Grecia ({TEATRI.get("Albania/Grecia", 0)}) e Germania ({TEATRI.get("Germania", 0)}); {TEATRI.get("Italia", 0)} muore in Italia nel 1944, in circostanze ancora da ricostruire.</p>

  <h2 id="elenco">L'elenco</h2>
  <div class="cerca-caduti">
    <div class="cerca-riga">
      <label for="cerca-caduti">Cerca fra i {N} nominativi</label>
      <input type="search" id="cerca-caduti" name="q" autocomplete="off" placeholder="es. Carnevale, Russia, 1943, disperso">
      <label for="filtro-stato">Stato</label>
      <select id="filtro-stato">
        <option value="">tutti</option>
        <option value="documentato">documentati</option>
        <option value="da confermare">senza riscontro</option>
      </select>
    </div>
    <p class="cerca-esito" id="cerca-esito" role="status" aria-live="polite">{N} nominativi</p>
    <ul id="elenco-caduti" class="elenco-caduti">
{elenco}
    </ul>
    <p id="nessun-caduto" hidden>Nessun risultato.</p>
  </div>

  <p class="legenda"><strong>documentato</strong>: dati incrociati tra Colli 1960, lapide 1940-45 e Banca dati della Difesa. <strong>senza riscontro</strong>: il nome è nella lista di Colli ma non è stato trovato (per ora) nella Banca dati Difesa: la lista locale registra i <em>residenti</em>, la banca dati i <em>nati</em> a Gravellona, quindi i due elenchi non vengono a coincidere per costruzione. <strong>non nella lista di Colli</strong>: uomo nato a Gravellona presente nella Banca dati Difesa ma assente dall'elenco locale. <strong>non nella lapide</strong>: assente dalla lastra 1940-45 del monumento (ha una targa propria, come Clotilde, oppure è noto da altre fonti).</p>

  <p>La <strong>lapide del 1940-45</strong> (lastra laterale del monumento di piazza Delucca, fotografata e trascritta da Pietre della Memoria) elenca <strong>17 nomi</strong>: 13 caduti e 4 dispersi (Romè, Milanesi, Bossi, Piccolini). Rispetto a essa, la lista di Colli aggiunge <strong>Dellupi, Baratti e Giannini Clotilde</strong> (quest'ultima con una targa a sé, datata 24-12-1903 – 27-7-1945); la Banca dati Difesa aggiunge i {NFUO} nati a Gravellona. La lapide riporta anche le <strong>classi di nascita</strong>, che colmano in parte i vuoti anagrafici dei senza riscontro.</p>

  <h2 id="colli">Perché i due elenchi non coincidono</h2>
  <p>Colli conta {NCOLA} nominativi (13 «caduti», 6 dispersi, 1 deportata); la Banca dati Difesa registra {NDB} persone nate a Gravellona. Il confronto completa {DOC_COLLI} nominativi colliani con paternità, date e teatro, e porta in luce <strong>{NFUO} nomi in più</strong> — Ambrosini, Baratto, Bellazzi, Carnevale Mario, Demarchi, Galletti, Maffei, Massolino, Moro Guido, Truffa — assenti dalla lista locale. Come per la Grande Guerra, la spiegazione più semplice è la <strong><em>residenza</em></strong>: la lista colliana sembra elencare chi abitava a Gravellona al momento del censimento dei caduti, la banca dati chi vi era <em>nato</em>; con il tempo le due nozioni potevano non coincidere più, per emigrazione della famiglia.</p>
  <p>Gli altri {NCOLA - DOC_COLLI} nominativi colliani restano senza riscontro nella banca dati: essa copre i caduti e i dispersi riconosciuti dalle forze armate italiane, non tutti i dispersi di Gravellona ricordati dalla memoria locale.</p>

  <h2 id="correzioni">Correzioni e avvertenze</h2>
  <ul>
    <li><strong>Dellupi</strong> (Banca dati Difesa), non «Deluppi»; <strong>Baratti</strong> Primo (lettura diretta sull'immagine della pagina), non «Baralti».</li>
    <li><strong>Pavesi Cesare</strong>: la lapide lo dà classe 1910, la Banca dati Difesa nato il 3/4/1913; prevale la data anagrafica.</li>
    <li><strong>Giannini Clotilde</strong> (in Colli «Clotilde Giovannina in Biscaldi»): nata a Tornaco nel 1903, deportata civile dopo lo sciopero del calzificio Giudice di Cilavegna, morta a Bergen-Belsen; pietra d'inciampo a Gravellona nel 2019. La targa a lei dedicata — verificata sulla fotografia, non è un errore di trascrizione — porta il cognome inciso <strong>«GIANINI»</strong> (una sola n) e le date <strong>24-12-1903 – 27-7-1945</strong>; la scheda ANED/ITS dà invece <strong>24/4/1945</strong>, nove giorni dopo la liberazione del campo. Si citano entrambe le date: quella documentaria (24/4) e quella della targa (27/7). Non è una caduta in guerra: si tiene a parte, mai sotto «caduti in combattimento». Scheda: <a href="https://www.deportatipavesi.it/giannini-clotilde/">deportatipavesi.it/giannini-clotilde</a>.</li>
    <li><strong>Travaglino Gaudenzio</strong>: l'Albo Caduti RSI lo registra come alpino della Divisione Littorio, 4° Reggimento alpini «Sennelager», morto il 25/7/1944 a Paderborn (Bassa Sassonia) per incidente — stessa data e luogo della Banca dati Difesa, che però lo fa nato a Gravellona Toce. Il cognome è comune a Gravellona Lomellina: l'iscrizione colliana si spiega con la residenza, da confermare sulla matricola.</li>
    <li><strong>Carnevale Mario</strong>: le schede Difesa parallele divergono sul giorno di nascita (29/10 vs 29/11) e sulla data di morte (31/01 vs 03/03/1943).</li>
    <li><strong>Ambrosini</strong> compare anche grafato «Ambrosioni».</li>
  </ul>

  <h2 id="fonti">Fonti</h2>
  <ul>
    <li>Ernesto Colli, <em>Gravellona Lomellina nella sua storia</em>, Novara 1960, cap. «I Caduti per la Patria», p. 105 (lista «1940-1945 (2.a guerra mondiale)» e dispersi; letture fatte direttamente sull'immagine della pagina) e p. 106 (salme rimpatriate nel 1955).</li>
    <li>Ministero della Difesa, Banca dati dei Caduti e Dispersi 2.a guerra mondiale (SICAD): <a href="https://www.difesa.it/il-ministro/cadutiinguerra/secondaguerra/secondaguerra.html">difesa.it/il-ministro/cadutiinguerra/secondaguerra</a> (ricerca per luogo di nascita «Gravellona Lomellina», accesso novembre 2026). Trascrizione grezza in <a href="https://github.com/racconti-di-gravellona/caduti-seconda-guerra-gravellona/blob/main/difesa_grezzo.json">difesa_grezzo.json</a>.</li>
    <li>Pietre della Memoria, scheda 185250 «Monumento ai Caduti di Gravellona Lomellina» (foto e trascrizione delle iscrizioni, a cura di ISIS Omodeo Mortara, 2021): <a href="https://www.pietredellamemoria.it/pietre/monumento-ai-caduti-di-gravellona-lomellina/">pietredellamemoria.it</a> (accesso novembre 2026). Da questa trascrizione vengono le classi di nascita dei nominativi senza data.</li>
    <li>Fondazione RSI, <em>Albo dei Caduti e Dispersi della RSI</em>, ed. 2019 (PDF): <a href="https://www.fondazionersi.org/caduti/AlboCaduti2019.pdf">fondazionersi.org</a> — voce Travaglino Gaudenzio.</li>
    <li>ANED Sez. Pavia / Istituto storico della Resistenza Pavia, scheda «Giannini Clotilde»: <a href="https://www.deportatipavesi.it/giannini-clotilde/">deportatipavesi.it/giannini-clotilde</a> (accesso novembre 2026); bibliografia e documenti in scheda (San Vittore, ISTORECO PV fondi ANED, CICR, ITS Bad Arolsen).</li>
  </ul>

  <h2 id="contatti">Correzioni e contatti</h2>
  <p>Questo è un elenco di lavoro, non un albo definitivo. I dieci nominativi «senza riscontro» aspettano le matricole e l'incrocio con le lapidi del monumento (fotografabile a piazza Delucca); altri potrebbero mancare. Se trovi un errore o un nome da aggiungere, scrivi a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <p class="ultimo-aggiornamento">Ultimo aggiornamento: {AGGIORNATO}.</p>
</main>

<footer class="site-footer">
  <div class="wrap">
    <p>Dati: Colli 1960; Ministero della Difesa (Banca dati Caduti e Dispersi 2.a GM). Testi originali <a href="https://creativecommons.org/licenses/by/4.0/deed.it">CC BY 4.0</a>, salvo diversa indicazione.</p>
    <p>Nessun cookie, nessun tracking. <a href="privacy.html">Privacy e correzioni</a>.</p>
  </div>
</footer>

<script src="cerca.js" defer></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print(f"index.html: {N} record, {len(HTML)} byte")
print("esiti:", ESITI)
print("teatri:", TEATRI)
print("anni:", ANNI)
print("eta:", len(ETAS), round(ETA_MEDIA, 1), ETA_MEDIANA, min(ETAS), max(ETAS))
print("in_colli:", len(IN_COLLI), "documentati:", DOC_COLLI, "| fuori da Colli:", NFUO, "| da confermare:", DA_CONFERMARE)
