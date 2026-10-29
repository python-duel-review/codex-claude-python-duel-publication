# AI CODING DUEL – 5. KROG

Napiši funkcijo `decode_message(text)` v Pythonu.

Funkcija dekodira stisnjena sporočila.

**Pravila:**
1. `3[ab]` pomeni `ababab`.
2. Skupine so lahko gnezdene: `2[a3[b]]` pomeni `abbbabbb`.
3. Navadne črke `a–z` ostanejo nespremenjene.
4. Števke 1–9 so dovoljene samo neposredno pred `[`. Večmestna števila niso dovoljena.
5. Prazne skupine, npr. `3[]`, so dovoljene.
6. Prazen niz `""` je veljaven in vrne `""`.
7. Pri napačnih oklepajih, neveljavnih znakih ali napačni sintaksi sproži `ValueError`.
8. Vhod mora biti niz `str`, dolg največ 60 znakov.
9. Dekodirani rezultat ne sme presegati 120 znakov; sicer sproži `ValueError`.
10. Originalnega vhoda ne spreminjaj.

**Primeri:**
```python
decode_message("3[ab]c")
# "abababc"

decode_message("2[a3[b]]")
# "abbbabbb"

decode_message("2[a]3[b]")
# "aabbb"
```

**Omejitve:**
- Največ 80 vrstic kode, vključno s tremi kratkimi testi.
- Samo standardni Python.
- Brez zunanjih orodij, ustvarjanja datotek ali izvajanja ukazov.
- Vrni samo kodo s tremi testi.
