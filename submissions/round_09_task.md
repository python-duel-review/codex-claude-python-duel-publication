# AI CODING DUEL – 9. KROG

Napiši funkcijo `repair_brackets(text)` v Pythonu.

**Naloga:** Popravi nepravilno postavljene oklepaje tako, da odstraniš najmanjše možno število oklepajev.

**Pravila:**
1. Besedilo vsebuje samo male črke `a–z` ter oklepaja `(` in `)`.
2. Odstranjuješ lahko samo oklepaje, nikoli črk.
3. Oklepaji morajo biti pravilno uravnoteženi in gnezdeni.
4. Med rešitvami z najmanj odstranitvami vrni **leksikografsko najmanjšo**.
5. Prazen niz je dovoljen.
6. Vhod mora biti tipa `str`, dolg največ 14 znakov.
7. Neveljaven vhod sproži `ValueError`.

**Primeri:**
```python
repair_brackets("a)b(c)d")
# "ab(c)d"

repair_brackets("())(")
# "()"

repair_brackets("()())()")
# "(())()"

repair_brackets("abc")
# "abc"
```

**Omejitve:**
- Največ 80 vrstic kode, vključno s tremi kratkimi testi.
- Samo standardni Python.
- Brez orodij, datotek ali izvajanja ukazov.
- Vrni samo kodo in tri teste.

**OCENJEVANJE:** 100 % pravilnost programa, vključno z robnimi primeri. Lastni testi in slog ne prinašajo dodatnih točk. Če sta obe rešitvi pravilni, je rezultat neodločen.
