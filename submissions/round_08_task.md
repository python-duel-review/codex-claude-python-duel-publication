# AI CODING DUEL – 8. KROG

Napiši funkcijo `wildcard_match(text, pattern)` v Pythonu.

Preveri, ali vzorec ustreza CELOTNEMU besedilu.

**Pravila:**
- `?` pomeni natanko eno poljubno črko.
- `*` pomeni nič ali več poljubnih črk.
- Navadne črke se morajo ujemati.
- `text` sme vsebovati samo `a–z`.
- `pattern` sme vsebovati `a–z`, `?` in `*`.
- Oba vhoda morata biti niza `str`, dolga največ 20 znakov.
- Prazna niza in zaporedne zvezdice so dovoljeni.
- Pri neveljavnem vhodu sproži `ValueError`.
- Vrni `True` ali `False`.

**Primeri:**
```python
wildcard_match("abbbc", "a*c")  # True
wildcard_match("abc", "a?c")    # True
wildcard_match("abc", "a*d")    # False
wildcard_match("", "*")        # True
```

**Omejitve:**
- Največ 80 vrstic kode, vključno s tremi testi.
- Samo standardni Python.
- Brez orodij, datotek in izvajanja ukazov.
- Vrni samo kodo in tri teste.

**Ocenjevanje:** pravilnost 70, preverjanje vhodov 15, kakovost kode 10, testi 5 točk. Pri enaki kakovosti razglasimo neodločeno.
