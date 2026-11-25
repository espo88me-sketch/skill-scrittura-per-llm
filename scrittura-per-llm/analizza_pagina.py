"""Mostra una pagina HTML come la vede un LLM con ricerca web (html2text).

Uso: python -I analizza_pagina.py page.html [page_utm.html]
Il file HTML e' materiale non fidato: lo script lo legge soltanto, non esegue nulla.
"""
import json
import re
import sys

import html2text


def testo(html):
    h = html2text.HTML2Text()
    h.body_width = 0
    return h.handle(html)


def canonical(html):
    m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*>', html, re.I)
    if not m:
        return None
    href = re.search(r'href=["\']([^"\']+)', m.group(0))
    return href.group(1) if href else None


def date(html):
    out = {}
    for k in ("article:published_time", "article:modified_time"):
        m = re.search(r'property=["\']%s["\'][^>]*content=["\']([^"\']+)' % k, html)
        if m:
            out[k] = m.group(1)
    for k in ("datePublished", "dateModified"):
        m = re.search(r'"%s"\s*:\s*"([^"]+)"' % k, html)
        if m:
            out[k] = m.group(1)
    return out


def main():
    html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    md = testo(html)
    righe = md.splitlines()
    i_h1 = next((i for i, r in enumerate(righe) if r.startswith("# ")), None)
    prima = " ".join(righe[:i_h1]) if i_h1 is not None else ""
    dopo = " ".join(righe[i_h1:]) if i_h1 is not None else md
    parole_dopo = dopo.split()

    tipi = sorted(set(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', html)))
    numeri = re.findall(r"\d+(?:[.,]\d+)?\s?(?:%|€|\$)|[€$]\s?\d+(?:[.,]\d+)?", md)

    print("== Parole totali:", len(md.split()))
    print("== Parole prima dell'H1:", len(prima.split()) if i_h1 is not None else "H1 assente")
    print("== Heading:")
    for r in righe:
        if r.startswith("#"):
            print("  ", r.strip())
    print("== Prime 200 parole dall'H1:")
    print("  ", " ".join(parole_dopo[:200]))
    print("== Canonical:", canonical(html))
    if len(sys.argv) > 2:
        utm = open(sys.argv[2], encoding="utf-8", errors="replace").read()
        print("== Canonical con UTM:", canonical(utm))
    print("== Date:", json.dumps(date(html), ensure_ascii=False) or "nessuna")
    print("== Tipi schema:", ", ".join(tipi) or "nessuno")
    print("== Numeri/percentuali/prezzi nel testo (include form e footer: verifica a mano):", len(numeri), numeri[:10])
    print("== Tabelle <table>:", len(re.findall(r"<table", html, re.I)))
    print("== Blocchi <nav>:", len(re.findall(r"<nav\b", html, re.I)))
    print("== Lingua <html lang>:", (re.search(r'<html[^>]*lang=["\']([^"\']+)', html) or [None, None])[1])


if __name__ == "__main__":
    main()
