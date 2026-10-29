# AI CODING DUEL – 3. KROG

Napiši funkcijo `escape_maze(maze)` v Pythonu.

Labirint je mreža, kjer:
- `0` pomeni prosto polje.
- `1` pomeni zid.
- Začetek je zgoraj levo `(0, 0)`.
- Cilj je spodaj desno.
- Premikaš se lahko gor, dol, levo ali desno, nikoli diagonalno.

**Pravila:**
1. Mreža mora biti neprazen seznam seznamov, pravokotne oblike, z največ 5 vrsticami in 5 stolpci ter najmanj eno vrstico in enim stolpcem.
2. Dovoljeni sta samo celoštevilski vrednosti 0 in 1; `bool` ni dovoljen.
3. Pri neveljavnem vhodu sproži `ValueError`.
4. Vrni najkrajšo pot kot seznam koordinat `(vrstica, stolpec)`, vključno z začetkom in ciljem.
5. Če najkrajših poti obstaja več, vrni leksikografsko najmanjšo celotno pot.
6. Če pot ne obstaja ali je začetno oziroma končno polje zid, vrni `None`.
7. Originalne mreže ne spreminjaj.

**Primer:**
```python
maze = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]
```
Pričakovani rezultat:
```python
[(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
```

**Omejitve:**
- Največ 80 vrstic kode, vključno s tremi kratkimi testi.
- Samo standardni Python.
- Brez zunanjih orodij, ustvarjanja datotek ali izvajanja ukazov.
- Vrni samo kodo s tremi testi.
