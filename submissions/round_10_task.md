# AI CODING DUEL – 10. KROG: FINALE

Napiši funkcijo `max_product(nums)` v Pythonu.

Poišči neprazen, neprekinjen del seznama, katerega zmnožek števil je največji.

**Pravila:**
1. Vhod je seznam ali terka z 1–10 celimi števili od -5 do 5.
2. `bool` in drugi tipi niso dovoljeni.
3. Vrni `(največji_zmnožek, začetek, konec)`, pri čemer sta indeksa vključena.
4. Če ima več delov enak največji zmnožek, izberi najmanjši začetni indeks, nato najmanjši končni indeks.
5. Pri neveljavnem vhodu sproži `ValueError`.
6. Vhoda ne spreminjaj.

**Primeri:**
```python
max_product([2, -3, -2, 4])
# (48, 0, 3)

max_product([-2, 0, -1])
# (0, 0, 1)

max_product([-2, -3, -4])
# (12, 1, 2)
```

**Omejitve:**
- Največ 80 vrstic, vključno s tremi testi.
- Samo standardni Python.
- Brez orodij, datotek ali izvajanja ukazov.
- Vrni samo kodo in tri teste.

**Ocenjevanje: 100 % pravilnost.** Če sta oba pravilna, je neodločeno.
