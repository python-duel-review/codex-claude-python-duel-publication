# AI CODING DUEL – MINI IZZIV

Napiši funkcijo `free_slots(bookings, start, end)` v Pythonu.

Funkcija prejme zasedene časovne intervale in vrne vse proste intervale.

**Primer:**
```python
bookings = [(10, 20), (18, 30), (40, 50)]
free_slots(bookings, 0, 60)
# Rezultat: [(0, 10), (30, 40), (50, 60)]
```

**Pravila:**
- Intervali so lahko neurejeni in se prekrivajo.
- Stikajoče se intervale obravnavaj kot neprekinjeno zasedenost.
- Začetek je vključen, konec izključen.
- Vsi časi morajo biti cela števila od 0 do 1440 (ne `bool`).
- Veljati mora `start < end`.
- Vsak zasedeni interval mora imeti začetek manjši od konca in ležati znotraj `start` in `end`.
- `bookings` je seznam ali terka z največ 20 intervali.
- Pri neveljavnem vhodu sproži `ValueError`.
- Rezultat naj bo urejen seznam terk prostih intervalov.

**Omejitve:**
- Samo standardni Python.
- Največ 80 vrstic kode, vključno s tremi kratkimi testi.
- Ne ustvarjaj datotek in ne izvajaj ukazov.
- Ne uporabljaj zunanjih orodij.
- Vrni samo rešitev v klepetu.
