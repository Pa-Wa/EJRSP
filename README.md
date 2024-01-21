# Ergonomic Job Rotation Scheduling Problem

Autor: Pascal Wagener

Business Analytics Seminar Wintersemester 2023/2024

Business Analytics, Universität Siegen

---

#### Inhalt:
* EJRSP - Instanzgenerierung (gemäß A.Otto, A. Scholl: Reducing ergonomic risks by job rotation scheduling (2012))
* Implementierung verschiedener Methoden zum Lösen des EJRSP (gemäß A.Otto, A. Scholl: Reducing ergonomic risks by job rotation scheduling (2012))
* Erstellung von Tabu-Suche Varianten und Analyse dieser

---

#### Doku:
* Main.py: Ausführung der einzelnen Methoden um die EJRSP-Instanzen zu lösen
* data_gen.py: Generierung der EJRSP-Instanzen
* methods:
    * ncp.py: Naive Konstruktionsheuristik
    * sh.py: Smoothing Heuristik
    * ts.py: Tabu-Suche
    * re_opt.py: Re-Optimierung (wird für die TS genutzt)
    * milp_relax.py: LP-Relaxierung (wird für die TS genutzt)
    * milp.py: MILP (Solver: Gurobi)
* data_main.pk1: Beispielhafter Datensatz
