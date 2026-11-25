# The Leaked ChatGPT Ranking Stack (Metehan Yesilyurt)

> Nota di studio dal deck "TechSEOConnect - The Leaked ChatGPT Ranking Stack: How OpenAI
> Scores Every Webpage" di Metehan Yesilyurt (GEO Researcher, Peec AI), 39 slide,
> TechSEOConnect, Durham NC, 09/11/2026.
> Fonte: https://speakerdeck.com/metehanyesilyurt/techseoconnect-the-leaked-chatgpt-ranking-stack
> Analisi del 19/11/2026 dalla trascrizione Speaker Deck.
>
> Nota di studio alla base della skill. Le sezioni 1-5 riportano il deck.
> La sezione 6 traduce i dati in regole di scrittura: e' una mia lettura, segnata **[mia]**.

---

## 1. Da dove vengono i dati

- A settembre 2026 ogni risposta di ChatGPT con ricerca web portava nello stream SSE un
  **payload di debug nascosto**: query, punteggi, blocchi del prompt, A/B test.
- Studiato set-ott 2026 su centinaia di dump (USA, Europa, Asia). OpenAI ha chiuso la falla
  circa un mese dopo.
- I numeri nelle slide vengono da **un solo dump per modello** (GPT-5.6 il 25/09, GPT-6 il
  12/10). I pattern vengono dalle centinaia. ChatGPT fa moltissimi A/B test: i valori
  cambiavano da un dump all'altro.

## 2. La pipeline, in 10 passi

| # | Passo | Cosa succede | Campo nel dump |
|---|---|---|---|
| 1 | Prompt | il messaggio dell'utente | — |
| 2 | Query rewrite | il modello riscrive la domanda | `system2_search_query` |
| 3 | Fan-out | piu' query su 10 motori | Labrador |
| 4 | Retrieval score | recency + frasi + ann + bm25 | `@retrieval_score` |
| 5 | Fusion | fusione dei ranking | `@rrf`, halflife 12 |
| 6 | Chunk rerank | ogni pezzo di pagina ha un punteggio | `sonic-re-fh-chunk-ev3` |
| 7 | Dedup | i quasi-duplicati vengono fusi | `minhash_dedup` |
| 8 | Prompt heap | cosa entra nel prompt | `wordlim: 200` |
| 9 | Il modello scrive | — | `gpt4o-sonic-1p-ev3` |
| 10 | Attribution | chi riceve la citazione | 50 campioni, soglia 0,45 |

- **L'84% del tempo di una risposta e' retrieval** (fan-out, scoring, rerank). Il modello
  principale e il render del prompt sono il 13%.
- **Un solo indice, molte porte:** 65 motori configurati, 10 attivi, tutti varianti di
  **Labrador** (indice proprietario OpenAI): web, reddit, pdf, wiki, arxiv, youtube, 4
  finestre news. Bing, SerpApi e Oxylabs sono nella config ma non sono partiti.

## 3. Query fan-out: il prompt non e' la query

- "what are the best ai visibility tools" → 3 query riscritte, con **nomi di brand mai
  scritti dall'utente** e **l'anno "2026" in 3 query su 3**.
- Differenze tra modelli (stesso stack, diverso "scrittore di query"):

| Segnale | GPT-5.6 | GPT-6 |
|---|---|---|
| Query al turno 0 | 4 | 3 |
| "Frasi tra virgolette" al turno 0 | 4 su 4 | 0 su 3 |
| Finestra di recency | 3.650 giorni | **30 giorni** |
| Anno "2026" nella query | 1 su 23 | 14 su 25 |
| Query `site:` su domini di brand | 15 su 23 | 20 su 25 |
| Parole medie per query | 7,2 | 7,4 |

- **Piu' approfondisci, piu' si allarga:** fino a 15 query e 172 risultati in un turno.
  GPT-6 ha risposto ai turni 4-7 senza nuova ricerca.
- **Tetto di 12 risultati per motore per query** (`topn: 12`, esatto).
- **Dopo il turno 0 va dritto sul tuo dominio:** query tipo `site:dominio.com pricing`.
  Il turno 0 ti trova, il turno 1 ti verifica. Pricing, docs e changelog vengono cercati
  per nome.

## 4. La formula di scoring

**`@retrieval_score` e' una somma semplice**, verificata su 62/62 risultati (GPT-6) e 77/77
(GPT-5.6):

```
recency (100) + required_phrases (0) + ann (12,41) + bm25 (1,44) + log_in_search_result (0,03) = 113,88
```

| Feature | Cosa misura | Peso osservato |
|---|---|---|
| `recency` | 100 se la pagina sta nella finestra temporale, altrimenti 0 | **88% del punteggio** |
| `ann` | match semantico (embedding) | ~11% (range 11,6-13,0) |
| `bm25` | match per parole chiave | ~1% (range 1,3-2,0) |
| `required_phrases` | **+100 per ogni frase tra virgolette** della query presente nella pagina | fino a 2,75x |

- **La recency vale solo per il motore web.** Reddit, PDF, wiki, arXiv: 0 punti recency.
- **Frasi esatte:** con 2 frasi quotate matchate il punteggio passa da 113 a 313. GPT-5.6
  le usava in tutte le query del turno 0, GPT-6 no (ma e' un A/B, puo' tornare).
- **Dentro la finestra i punteggi quasi non separano:** ann e bm25 hanno range strettissimi,
  nessuna soglia di punteggio.
- **Fusion (RRF)** schiaccia tutto intorno a 7,0. Tutti i 24 posti nel prompt vengono da
  questa zona piatta; dopo il rank 36 nulla entra. Dei 12 esclusi, 3 erano duplicati, 9
  erano piu' in basso dopo la fusione.

### Chunking

- Pipeline: **HTML → html2text (parser ibrido) → Markdown → chunk** (`#` titoli, liste,
  tabelle). ~178 parole e ~1.074 caratteri per chunk mediano.
- **Il primo chunk prende 1,0 nel 64% delle pagine.** 210 chunk su 326 successivi
  **iniziano da un heading**.
- 61 pagine → 214 chunk, ciascuno coppia [testo, punteggio]. Mediana 0,9992: il reranker
  e' quasi sempre sicuro, **la differenza sta negli ultimi decimali**.
- Il parser cambia spesso. "HTML pulito che diventa Markdown pulito sopravvive a ogni
  versione."

### Dedup

- Una pagina con 4 URL (parametri `?gad=`, `?tp=`, `?authuser=`, app) = 4 documenti.
  `minhash_dedup` 0,74 / 0,46 / 0,46 / 0,38: **due varianti hanno comunque preso posti nel
  prompt**, due sono state scartate. Stesso caso con `/en` e `/en-us`.
- 1 = unico, piu' basso = quasi duplicato.

## 5. Dal risultato al prompt, e alla citazione

- **Funnel GPT-6 turno 0:** 62 risultati → 61 pagine → 39 domini → **24 blocchi nel prompt**.
  GPT-5.6: 77 → 77 → 56 → 22.
- **Reddit recuperato 24 volte, 0 posti nel prompt.** Tutti i posti del turno 0 sono andati a
  `system2-web`. Reddit, PDF, wiki, arXiv, news: recuperati, valutati, esclusi.
- **Cosa legge il modello per ogni risultato:**
  ```
  Titolo | Sito (URL) 【turn0search0】 [wordlim: 200]
  Published: 3 months ago; Crawled: 2 weeks ago;
  # H1 ... primo testo della pagina ...
  ```
- **`wordlim: 200` = il modello legge circa il 5-6% della pagina** (~88 token su ~1.500).
- **La data in parole:** "Published: last week". Su 24 blocchi, 11 avevano solo
  "Crawled: ...". **Senza data in pagina, la tua eta' e' la data di crawl.** Sopra ogni
  risultato c'e' la data di oggi e la posizione dell'utente.
- GPT-6 aggiunge `WebRef[title, timestamp, domain, url]` come oggetto tipizzato.
- **La citazione non viene dal rank ma da un test di attribuzione:** 50 campioni,
  soglia di probabilita' 0,45, baseline 0,02, temperatura 0,2, metodo "koo". Per il
  ragionamento si costruisce una lista ordinata dei domini (top 80%). Essere letti non
  basta: bisogna **influenzare la risposta** abbastanza da superare la soglia.
- A/B test attivi: redirect Google su Labrador, **`filter_serp_by_robots`** (robots.txt
  controllato), `budget_trimmed`, test shopping e immagini.

## 6. Le sei mosse del deck

| # | Mossa | Motivo nel codice |
|---|---|---|
| 1 | **Mostra una data reale** | dentro la finestra = +100 recency; senza data compare solo "Crawled" |
| 2 | **Carica le prime 200 parole** | il modello vede ~88 token su 1.500 (`wordlim 200`) |
| 3 | **Sii una pagina web, non un thread** | Reddit: 24 recuperi, 0 posti nel prompt |
| 4 | **Un URL per pagina** | le varianti vengono fuse da minhash; canonical e parametri puliti vincono |
| 5 | **Rendi il sito degno di una query `site:`** | 20 follow-up su 25 puntano a un solo dominio |
| 6 | **Usa le parole esatte che la gente cita** | +100 per ogni frase quotata matchata |

### L'esempio del deck (pagina inventata, costruita dalle regole)

| Passo | Pagina che perde | Pagina che vince |
|---|---|---|
| Recency | nessuna data, solo "Crawled" | "Published last week", +100 |
| Frase | dice "AI landscape", mai "ai visibility" | "AI visibility tools" nell'H1 e nella frase 1 |
| Dedup | stessa pagina su 4 URL con tracking | un URL canonico |
| Parse e chunk | chunk 0 = cookie banner e menu; tabella come immagine | chunk 0 = H1, risposta e tabella Markdown |
| Prime 200 parole | storia della ricerca, risposta dopo la parola 600 | nomi, casi d'uso e prezzi nelle prime 80 parole |
| Follow-up | pricing "Contact sales", la `site:` non trova nulla | pricing con un numero per ogni piano |
| Citazione | letta, poi lasciata fuori | supera il test, citata |

Titolo vincente: "Best AI visibility tools in 2026: 9 tools compared". Frase 1: "Brand A
for prompt tracking, Brand B for citation analysis and Brand C for agencies. We tested 9
tools on 500 prompts in ChatGPT, Gemini and Perplexity."

---

## 7. Regole di scrittura che ne derivo [mia]

Il materiale grezzo per la skill. Divise tra cio' che dipende da chi scrive e cio' che
dipende dal sito.

**Scrittura (cosa fa la skill):**

1. **Risposta nella frase 1.** Le prime 200 parole sono tutto quello che il modello legge.
   Niente premesse, storia, "in questo articolo vedremo".
2. **Densita' nelle prime 80 parole:** entita' (nomi, brand), casi d'uso, numeri (prezzi,
   quantita', metodo del test).
3. **H1 = la frase che la gente scrive.** Le parole esatte della query nell'H1 e nella
   frase 1, non un sinonimo creativo ("landscape" perde contro "visibility tools").
4. **Anno nel titolo quando il tema e' temporale.** Le query riscritte aggiungono l'anno.
5. **Ogni sezione si regge da sola.** I chunk ripartono dagli heading: ogni H2 deve aprire
   con una risposta autonoma, non con "come detto sopra".
6. **Tabelle vere in Markdown/HTML, mai immagini.** Confronti con colonne esplicite
   (Strumento | Per chi | Prezzo).
7. **Data di pubblicazione e aggiornamento visibili nel testo.**
8. **Numeri invece di "contattaci":** pagina prezzi con un numero per piano.
9. **Prova concreta:** "abbiamo testato 9 tool su 500 prompt" e' cio' che serve al test
   di attribuzione per scegliere te.

**Tecnico (fuori dalla scrittura, da segnalare):**

- URL canonico unico, parametri di tracking puliti, niente doppioni `/en` `/en-us`.
- Nessun cookie banner o menu come primo testo dopo html2text.
- robots.txt che non blocca il crawler OpenAI.
- Pagine dedicate per pricing, docs, changelog: sono i bersagli delle `site:`.

## 8. Limiti da tenere presenti [mia]

- **Fonte interessata:** l'autore lavora per Peec AI, che vende tracking di visibilita'
  AI. Nell'esempio Peec AI compare nelle query riscritte.
- **Un dump per modello** per i numeri esatti. I valori (finestra 30 vs 3.650 giorni,
  virgolette si'/no) sono A/B test e cambiano. Le **direzioni** sono piu' solide dei
  numeri.
- **Solo ChatGPT.** Nulla su Gemini, Perplexity, Claude, AI Overviews.
- Un solo tipo di query (commerciale, "best X tools"). Su query informative o locali il
  comportamento puo' cambiare.
- Prompt in inglese; non sappiamo come si comporta la riscrittura su query in italiano.
- **Dato da verificare prima di trasformarlo in regola:** la recency vale +100 ma premia
  solo le pagine *dentro* la finestra; non dice se "aggiornare la data" senza cambiare il
  contenuto funzioni (e sarebbe una pratica scorretta).
