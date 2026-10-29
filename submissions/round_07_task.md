# AI CODING DUEL – 7. KROG

Napiši funkcijo `task_order(tasks, dependencies)` v Pythonu.

Naloga: določi vrstni red opravljanja nalog, pri čemer morajo biti njihove odvisnosti upoštevane.

**Pravila:**
1. `tasks` je seznam ali terka z 1–7 različnimi malimi črkami `a–z`.
2. `dependencies` je seznam ali terka z največ 12 pari `(a, b)`, kar pomeni, da mora biti naloga `a` opravljena pred `b`.
3. Vse naloge v odvisnostih morajo obstajati v `tasks`.
4. Podvojene odvisnosti so dovoljene in štejejo samo enkrat.
5. Če obstaja več veljavnih vrstnih redov, vrni **leksikografsko najmanjšega**.
6. Če odvisnosti tvorijo cikel, vrni `None`.
7. Pri neveljavnem vhodu sproži `ValueError`.
8. Vhodnih podatkov ne spreminjaj.

**Primeri:**
```python
task_order(["a", "b", "c"], [("b", "a")])
# ["b", "a", "c"]

task_order(["c", "a", "b"], [])
# ["a", "b", "c"]

task_order(["a", "b"], [("a", "b"), ("b", "a")])
# None
```

**Omejitve:**
- Največ 80 vrstic kode, vključno s tremi testi.
- Samo standardni Python.
- Brez zunanjih orodij, datotek in izvajanja ukazov.
- Vrni samo kodo in tri teste.

**Ocenjevanje:** pravilnost 70, varnost vhodov 15, kakovost kode 10, lastni testi 5 točk.
