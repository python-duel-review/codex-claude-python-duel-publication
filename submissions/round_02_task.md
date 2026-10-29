# AI CODING DUEL – 2. KROG

Napiši funkcijo `solve_sudoku(board)` v Pythonu.

Naloga: reši Sudoku 4 × 4, v katerem:
- Uporabljamo številke od 1 do 4.
- 0 pomeni prazno polje.
- Vsaka vrstica, stolpec in kvadrat 2 × 2 mora vsebovati številke 1–4 brez ponavljanja.

**Pravila:**
1. Vhod mora biti seznam štirih seznamov s po štirimi vrednostmi.
2. Dovoljena so samo cela števila 0–4; `bool` ni dovoljen.
3. Pri neveljavnem vhodu ali podvojenih začetnih številkah sproži `ValueError`.
4. Če rešitve ni, vrni `None`.
5. Če rešitev obstaja, vrni novo rešeno mrežo. Originala ne spreminjaj.
6. Če obstaja več rešitev, vrni leksikografsko najmanjšo (vrstice primerjaj od zgoraj navzdol).
7. Največ 80 vrstic kode, vključno s tremi kratkimi testi.

**Primer:**
```python
board = [
    [1, 0, 3, 4],
    [3, 4, 1, 0],
    [0, 1, 4, 3],
    [4, 3, 0, 1]
]
```
Pričakovani rezultat:
```python
[
    [1, 2, 3, 4],
    [3, 4, 1, 2],
    [2, 1, 4, 3],
    [4, 3, 2, 1]
]
```

Uporabi samo standardni Python. Brez zunanjih orodij, zaganjanja ukazov ali ustvarjanja datotek. Vrni samo kodo s tremi testi.
