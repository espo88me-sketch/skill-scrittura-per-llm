# Regole candidate per la skill

_Lista viva. Ogni fonte o caso nuovo conferma, smentisce o aggiunge una regola._
_Versione 1.0.0 del 2026-11-25 (fonte F01, casi C01-C02: pagine di aziende terze analizzate, non pubblicate)_

**Forza:** `dato` = osservato nel codice/dump · `inferenza` = dedotto dai dati ·
`ipotesi` = da verificare. **Fonti:** F = fonte, C = caso.

## Scrittura (cosa fa la skill)

| # | Regola | Forza | Da |
|---|---|---|---|
| S1 | Risposta nella frase 1: niente premesse, storia, "in questo articolo" | dato (`wordlim 200`) | F01 |
| S2 | Prime 80 parole dense: entita', casi d'uso, numeri, metodo | inferenza | F01, C01, C02 |
| S3 | H1 e frase 1 con le parole esatte della query, non sinonimi creativi ne' solo nomi propri | dato (`required_phrases` +100) | F01, C01, C02 |
| S4 | Anno nel titolo se il tema e' temporale | dato (anno in 14/25 query GPT-6) | F01 |
| S5 | Ogni sezione apre con una risposta autonoma (i chunk ripartono dagli heading) | dato (210/326 chunk) | F01, C01 |
| S6 | Le etichette di sezione devono essere heading veri, e gli heading devono dire qualcosa ("il progetto" non basta) | inferenza | C01, C02 |
| S7 | Tabelle in testo (Markdown/HTML), mai immagini | dato (html2text) | F01, C01 |
| S8 | Data di pubblicazione/aggiornamento visibile nel testo | dato (recency +100, "Published" nel prompt) | F01, C01, C02 |
| S9 | Numeri invece di "contattaci" (prezzi per piano) | inferenza (follow-up `site:`) | F01, C01 |
| S10 | Prova concreta: periodo, campione, fonte, metodo. Testimonianze sui risultati, non al futuro | inferenza (test di attribuzione) | F01, C01, C02 |
| S11 | Non ripetere lo stesso dato nelle prime 200 parole: ogni frase aggiunge informazione | inferenza | C01, C02 |
| S12 | FAQ con risposte autonome, riusabili come chunk | inferenza | C01 |
| S13 | Niente sezioni standard uguali su piu' pagine: ogni chunk dice qualcosa di specifico per quella pagina | ipotesi (chunk senza nulla da attribuire) | C02 |
| S14 | Date coerenti tra testo, schema e periodo dichiarato | inferenza | C02 |
| S15 | Le entita' collegate (gruppo, marchio madre) vanno nel testo, non solo nell'URL | inferenza (`required_phrases`) | C02 |

## Tecnico (la skill lo segnala, non lo scrive)

| # | Regola | Forza | Da |
|---|---|---|---|
| T1 | URL canonico unico, parametri puliti, niente `/en` + `/en-us` | dato (minhash) | F01, C01 |
| T2 | Niente menu/cookie banner come primo testo dopo html2text | ipotesi (non si sa se `<nav>` viene scartato) | F01, C01, C02 |
| T3 | robots.txt che ammette OAI-SearchBot / ChatGPT-User | dato (`filter_serp_by_robots`) | F01, C01 |
| T4 | Pagine dedicate per pricing, docs, changelog | dato (`site:` 20/25) | F01 |
| T5 | Testo nell'HTML server-side | inferenza | C01 |

## Domande aperte

- Il parser di OpenAI scarta `<nav>` / `<header>`? (decide T2)
- Vale lo stesso per Gemini, Perplexity, Claude, AI Overviews?
- Come si comporta la riscrittura delle query in italiano?
- Quanto pesa la recency su query non temporali?
