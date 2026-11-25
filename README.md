# Skill "scrittura per LLM" per Claude

Una skill per Claude (Claude Code o Claude.ai) che **scrive o rivede pagine web perché ChatGPT
con ricerca web le recuperi, le legga e le citi**. Versione 1.0.0 del 25 novembre 2026.

Le regole vengono dall'analisi dei dati di debug della pipeline di ricerca di ChatGPT presentata
nel deck "The Leaked ChatGPT Ranking Stack" di Metehan Yesilyurt (TechSEOConnect 2026), più
alcune pagine reali analizzate. Ogni regola è marcata per forza: `dato`, `inferenza`, `ipotesi`.

## Cosa fa

| Modalità | Input | Output |
|---|---|---|
| 1 · Scrivere | query bersaglio, fatti disponibili, tipo di pagina | testo con H1, data, risposta nelle prime 3 frasi, sezioni autonome, tabelle, FAQ |
| 2 · Rivedere | URL di una pagina | le prime 200 parole come le vede il modello, tabella contro i criteri, riscrittura minima |

## Le regole in breve

1. Risposta nella prima frase: il modello legge circa 200 parole per risultato.
2. Prime 80 parole dense: nomi, numeri, metodo.
3. H1 e prima frase con le parole esatte della query.
4. Anno nel titolo se il tema è temporale.
5. Data di aggiornamento scritta nel testo.
6. Ogni sezione apre con una risposta autonoma, sotto un heading informativo.
7. Tabelle in HTML, mai in immagine.
8. Numeri e prove al posto di "contattaci".
9. Tecnico: URL canonico unico, robots.txt che ammette `OAI-SearchBot`.

L'elenco completo (S1-S15, T1-T5) è in [`scrittura-per-llm/SKILL.md`](scrittura-per-llm/SKILL.md).

## Installazione

**Claude Code** (tutti i progetti):
```bash
git clone <url-di-questo-repo> /tmp/skill-llm
cp -r /tmp/skill-llm/scrittura-per-llm ~/.claude/skills/
```
Solo per un progetto: copia la cartella in `.claude/skills/` del progetto.

**Claude.ai**: comprimi la cartella `scrittura-per-llm` in uno zip e caricala da
Impostazioni → Funzionalità → Skill.

La revisione di pagine (modalità 2) usa `analizza_pagina.py`, che richiede Python 3.8+ e
`html2text` (`pip install html2text`, meglio in un virtualenv).

## Come si usa

- "Scrivi per gli LLM una pagina su *come scegliere un ombrellone da spiaggia*"
- "Rivedi questa pagina in ottica GEO: https://..."

## Limiti

- La base è **solo ChatGPT**: Gemini, Perplexity, Claude e AI Overviews non sono coperti.
- I numeri (finestra di recency, +100 punti) vengono da A/B test che cambiano:
  **valgono le direzioni, non i valori**.
- La fonte è di parte (l'autore lavora per un'azienda di tracciamento della visibilità AI)
  e le query analizzate sono commerciali e in inglese.
- Mai aggiornare la data senza aggiornare il contenuto.

## Fonti

- Metehan Yesilyurt, "The Leaked ChatGPT Ranking Stack", TechSEOConnect 2026:
  https://speakerdeck.com/metehanyesilyurt/techseoconnect-the-leaked-chatgpt-ranking-stack
- OpenAI, crawler e user agent: https://platform.openai.com/docs/bots

## Licenza

MIT. Autore: Michele Esposto.
