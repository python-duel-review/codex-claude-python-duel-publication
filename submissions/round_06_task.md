# AI CODING DUEL – 6. KROG

Napiši funkcijo `min_cover(text, required)` v Pythonu.

Poišči **najkrajši neprekinjeni del besedila**, ki vsebuje vse zahtevane črke, vključno s ponovitvami.

**Pravila:**
1. Vhoda sta niza `str`, sestavljena samo iz malih črk `a–z`.
2. `text` ima največ 40 znakov, `required` največ 10.
3. Vsaka črka iz `required` mora biti prisotna vsaj tolikokrat, kot se pojavi v `required`.
4. Če obstaja več najkrajših rešitev, izberi tisto z najzgodnejšim začetkom.
5. Če rešitve ni, vrni `None`.
6. Če je `required` prazen, vrni `""`.
7. Neveljaven vhod mora sprožiti `ValueError`.

**Primeri:**
```python
min_cover("adobecodebanc", "abc")
# "banc"

min_cover("aaabc", "aabc")
# "aabc"

min_cover("abc", "aabb")
# None
```

**Omejitve:**
- Največ 80 vrstic, vključno s tremi testi.
- Samo standardni Python.
- Brez orodij, datotek ali izvajanja ukazov.
- Vrni samo kodo in tri teste.
