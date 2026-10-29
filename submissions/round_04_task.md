# AI CODING DUEL – 4. KROG

Napiši funkcijo `best_change(coins, amount)` v Pythonu.

Naloga: iz razpoložljivih vrednosti kovancev sestavi znesek z najmanjšim možnim številom kovancev.

**Pravila:**
1. `coins` je seznam ali terka z 1–8 različnimi pozitivnimi celimi števili od 1 do 20.
2. Vsako vrsto kovanca lahko uporabiš neomejenokrat.
3. `amount` je celo število od 0 do 60.
4. Dovoljen je samo tip `int` (ne `bool` in ne druge vrste).
5. Pri neveljavnem vhodu sproži `ValueError`.
6. Vrni seznam izbranih kovancev, urejen padajoče.
7. Če obstaja več rešitev z najmanjšim številom kovancev, vrni leksikografsko največji padajoče urejeni seznam.
8. Če zneska ni mogoče sestaviti, vrni `None`.
9. Za znesek 0 vrni prazen seznam `[]`.
10. Vhodnih podatkov ne spreminjaj.

**Primeri:**
```python
best_change([1, 3, 4], 6)
# [3, 3] in ne [4, 1, 1]

best_change([2, 3, 4], 6)
# [4, 2] in ne [3, 3]

best_change([4, 6], 5)
# None
```

**Omejitve:**
- Največ 80 vrstic kode, vključno s tremi kratkimi testi.
- Samo standardni Python.
- Brez zunanjih orodij, ustvarjanja datotek ali izvajanja ukazov.
- Vrni samo kodo s tremi testi.
