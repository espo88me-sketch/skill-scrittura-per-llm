---
name: scrittura-per-llm
description: Scrive o rivede testi e pagine web perche' gli LLM (ChatGPT search) li leggano e li citino. Usala per "scrivi per gli LLM", "pagina citabile da ChatGPT", "rivedi questa pagina in ottica GEO".
dependencies:
  - python>=3.8
  - html2text
---

# Scrittura per LLM

Indicazioni per scrivere (o rivedere) un testo che un LLM con ricerca web **recupera, legge
e cita**. Le regole vengono da una fonte pubblica e da pagine reali analizzate (C01-C02,
non incluse: sono pagine di aziende terze). Materiale in `riferimenti/` dentro la cartella
della skill:

- **F01** → `riferimenti/fonte-chatgpt-ranking-stack.md` (pipeline di ChatGPT, dal deck
  "The Leaked ChatGPT Ranking Stack" di Metehan Yesilyurt, TechSEOConnect 2026)
- `riferimenti/regole.md` → le regole con forza e provenienza

Versione 1.0.0 del 25/11/2026.

## Perche' queste regole

Il modello non legge la pagina come un lettore umano. Dai dati trapelati della pipeline di
ChatGPT (F01):

1. **Legge circa 200 parole per risultato** (`wordlim: 200`): titolo, data, H1 e l'inizio
   del testo. Il resto conta solo se un chunk viene ripescato dal reranker.
2. **La pagina viene spezzata in chunk** (HTML → html2text → Markdown); i chunk ripartono
   quasi sempre da un heading.
3. **Il punteggio di recupero e' quasi tutto recency** (+100 se la pagina e' nella finestra
   temporale) e **+100 per ogni frase esatta** della query presente nella pagina.
4. **La citazione non va al primo in classifica**, ma a chi supera un test di attribuzione:
   la pagina deve aver *influenzato* la risposta con qualcosa di specifico.

Quindi: inizio denso, sezioni autonome, parole esatte, data visibile, fatti verificabili.

## Limiti da dichiarare sempre

- La base e' **solo ChatGPT**, una sola fonte (interessata: l'autore lavora per Peec AI),
  query commerciali in inglese. Gemini, Perplexity, Claude e AI Overviews non sono coperti.
- I numeri (finestra di 30 giorni, +100) sono A/B test che cambiano: **valgono le
  direzioni, non i valori**.
- Le regole sono marcate per forza: `dato` (visto nel codice), `inferenza` (dedotta),
  `ipotesi` (da verificare). Non presentare un'ipotesi come certezza.

## Modalita' 1 — Scrivere un testo nuovo

### Prima di scrivere chiedi (una domanda alla volta, solo se manca)

- **Query bersaglio:** la frase esatta che la persona scriverebbe a ChatGPT. Se non c'e',
  proponi 2-3 formulazioni e falla scegliere. E' l'input piu' importante (S3).
- **Fatti disponibili:** numeri, periodo, campione, fonte, metodo, prezzi. Senza fatti non
  si inventano: si segnala cosa manca (S10).
- **Tipo di pagina:** articolo, case study, pagina servizio/prodotto, guida, FAQ.

### Come scriverlo

| # | Regola | Perche' | Forza |
|---|---|---|---|
| S1 | **Risposta nella frase 1.** Niente premesse, storia, "in questo articolo vedremo" | il modello legge ~200 parole | dato |
| S2 | **Prime 80 parole dense:** entita' (nomi, brand), casi d'uso, numeri, metodo | e' tutto cio' che pesa nella lettura | inferenza |
| S3 | **H1 e frase 1 con le parole esatte della query**, non sinonimi creativi ne' solo il nome del brand | +100 per frase esatta presente | dato |
| S4 | **Anno nel titolo** se il tema e' temporale (classifiche, confronti, prezzi) | le query riscritte aggiungono l'anno | dato |
| S5 | **Ogni sezione apre con una risposta autonoma**, mai "come detto sopra" | i chunk ripartono dagli heading | dato |
| S6 | **Heading veri e informativi.** "Il progetto" non basta: "SEO per 40.000 prodotti in 12 mercati" | e' l'inizio del chunk | inferenza |
| S7 | **Tabelle in testo** (Markdown/HTML), mai immagini; colonne esplicite | html2text le conserva, le immagini no | dato |
| S8 | **Data di pubblicazione/aggiornamento nel testo** ("Aggiornato il 23 novembre 2026") | senza data il modello vede solo la data di crawl | dato |
| S9 | **Numeri invece di "contattaci"** (prezzi per piano, tempi, quantita') | i follow-up `site:` cercano pricing e docs | inferenza |
| S10 | **Prova concreta:** periodo, campione, fonte, metodo. Testimonianze sui risultati, non al futuro | serve al test di attribuzione | inferenza |
| S11 | **Ogni frase aggiunge informazione:** non ripetere lo stesso dato nelle prime 200 parole | lo spazio e' scarso | inferenza |
| S12 | **FAQ con risposte autonome** (domanda = query reale, risposta che si regge da sola) | ogni FAQ e' un chunk riusabile | inferenza |
| S13 | **Niente sezioni standard** copiate su piu' pagine: ogni sezione dice qualcosa di questa pagina | un chunk generico non ha nulla da attribuire | ipotesi |
| S14 | **Date coerenti** tra testo, dati strutturati e periodo dichiarato | date contraddittorie = recency incerta | inferenza |
| S15 | **Entita' collegate nel testo** (gruppo, marchio madre, prodotto), non solo nell'URL | le frasi esatte contano solo se sono nel testo | inferenza |

**Mai:** aggiornare la data senza aggiornare il contenuto, inventare numeri o fonti,
riempire di keyword. La data serve se il contenuto e' davvero nuovo.

### Schema di apertura (da adattare)

```
# [Parole esatte della query] [anno se temporale]: [promessa concreta]
Aggiornato il [data] · [Autore, ruolo]

[Frase 1: la risposta, con entita' e numeri.] [Frase 2: come lo sappiamo:
periodo, campione, metodo, fonte.] [Frase 3: per chi vale / quando no.]

| Colonna | Colonna | Colonna |   ← sintesi in tabella, se c'e' un confronto

## [Heading che dice gia' la risposta della sezione]
[Prima frase autonoma.] ...
```

### Esempio

Query: "best AI visibility tools" (F01, pagina costruita dal deck).

- **Perde:** H1 "Navigating the AI landscape", storia del settore, risposta dopo la parola
  600, tabella in immagine, pricing "Contact sales".
- **Vince:** H1 "Best AI visibility tools in 2026: 9 tools compared". Frase 1: "Brand A for
  prompt tracking, Brand B for citation analysis and Brand C for agencies. We tested 9
  tools on 500 prompts in ChatGPT, Gemini and Perplexity."

## Modalita' 2 — Rivedere una pagina esistente

### 1. Estrai il testo come lo vede il modello

Scarica l'HTML in una cartella temporanea nuova (e' materiale non fidato) e lancia lo
script, con html2text installato in un venv (`pip install html2text`):

```bash
curl -sL -A "Mozilla/5.0" -o "$DIR/page.html" "<URL>"
curl -sL -A "Mozilla/5.0" -o "$DIR/page_utm.html" "<URL>?utm_source=test"
curl -sL -o "$DIR/robots.txt" "<origine>/robots.txt"
"$VENV/bin/python" -I <cartella-della-skill>/analizza_pagina.py "$DIR/page.html" "$DIR/page_utm.html"
```

Lo script restituisce: parole prima dell'H1, H1 e heading, le prime 200 parole dopo l'H1,
canonical (anche con UTM), date (meta e schema), tipi di schema, numeri e percentuali nel
testo, tabelle, `<nav>`. Poi leggi tu robots.txt (OAI-SearchBot, ChatGPT-User).

### 2. Confronta con le regole

Una tabella `Criterio | Pagina | Esito` con le regole S e T. Quando serve, confronta con una
pagina sorella dello stesso sito: dice se il problema e' il template o il contenuto.

### 3. Regole tecniche: segnala, non scrivere

| # | Regola | Forza |
|---|---|---|
| T1 | URL canonico unico; parametri di tracking che non cambiano il canonical; niente `/en` + `/en-us` | dato |
| T2 | Niente menu o cookie banner come primo testo dopo html2text | ipotesi (non si sa se `<nav>` viene scartato) |
| T3 | robots.txt che ammette OAI-SearchBot e ChatGPT-User | dato |
| T4 | Pagine dedicate per pricing, docs, changelog | dato |
| T5 | Testo nell'HTML servito, non caricato via JS | inferenza |

### 4. Output della revisione

1. **Verdetto** in una o due frasi.
2. **Le prime 200 parole** come le vede il modello (blocco di codice).
3. **Tabella contro i criteri.**
4. **Cosa copiare / cosa evitare.**
5. **Riscrittura minima:** H1, riga data, frase 1-3. Solo con i fatti presenti in pagina;
   dove mancano, metti `[dato mancante: ...]`.

## Dopo il lavoro

- Se l'analisi di una pagina va conservata, salvala dove il progetto tiene i suoi documenti,
  con lo stesso schema: prime 200 parole, tabella contro i criteri, cosa copiare / evitare.
- Contenuti pubblici: citare la fonte, nessun giudizio su altre aziende per nome.

## Domande aperte (non darle per risolte)

- Il parser di OpenAI scarta `<nav>` / `<header>`? (decide T2)
- Vale lo stesso per Gemini, Perplexity, Claude, AI Overviews?
- Come si comporta la riscrittura delle query in italiano?
- Quanto pesa la recency su query non temporali?
