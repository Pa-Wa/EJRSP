import numpy as np
from methods.sh import SH
from methods.re_opt import ReOpt
from methods.milp_relax import MILP_Relax


def TS(jobs, periods, e_trans, e_not_trans, e_trans_sorted):
    """
    Führt die beschriebene Tabu Suche durch
    :param jobs: Anzahl der Jobs
    :param periods: Anzahl der Perioden
    :param e_trans: EP-Matrix
    :param e_not_trans: EP-Matrix (nicht transponiert)
    :param e_trans_sorted: bereits aufsteigend (je Periode) sortierte EP-Matrix
    :return E_best: Zielfunktionswert des besten Schedule nach Anwendung der Heuristik
    """
    schedule, E, PEP = SH(jobs, periods, e_trans, e_trans_sorted)
    #schedule_best = np.copy(schedule_dic)
    E_best = np.max(PEP)
    E_MILP_Relax = MILP_Relax(jobs, periods, e_not_trans)
    TL = [] # Erstelle leere Tabu-Liste
    it_count = 1 # Iterationszähler
    while it_count <= 12000:
        max_positions = [i for i, x in enumerate(PEP) if x == max(PEP)] # Finde größten (mehrere möglich) PEP-Eintrag um Nachbarschaf zu erzeugen 
        neighboorhood = []
        for i in max_positions: # Iteriere über Arbeiter mit max. PEP
            for j in range(jobs): # Diese können mit allen anderen Arbeitern kombiniert werden für die Nachbarschaft
                if i != j:
                    if i > j:
                        if (j,i) not in neighboorhood: # Duplikate verhindern
                            neighboorhood.append((j,i)) # immer so hinzufügen, dass vorne die kleinere Zahl steht
                    if j > i:
                        if (i,j) not in neighboorhood: # Duplikate verhindern
                            neighboorhood.append((i,j)) # immer so hinzufügen, dass vorne die kleinere Zahl steht
        first_swap = True # 1. Swap je TS Iteration 
        no_possible_swap = False # Falls es keinen möglichen Nachbarn gibt
        for t in range(periods):  
            for swap in neighboorhood:
                if (t,swap[0],swap[1]) not in TL: # Nur wenn nicht durch TL verhindert
                    if first_swap:
                        E_best_swap = np.inf
                        no_possible_swap = True
                        first_swap = False
                    PEP_f_i_after = PEP[swap[0]] + schedule[t][swap[1]][1] - schedule[t][swap[0]][1] # Aktualisiere PEP nach Swap
                    PEP_s_i_after = PEP[swap[1]] + schedule[t][swap[0]][1] - schedule[t][swap[1]][1]
                    positions_to_ignore = [swap[0],swap[1]]
                    filtered_list = [value for i, value in enumerate(PEP) if i not in positions_to_ignore] # Liste ohne Arbeiter des Swaps
                    filtered_list.append(PEP_f_i_after) # Füge aktualisierte PEP hinzu
                    filtered_list.append(PEP_s_i_after)
                    E_after_swap = max(filtered_list) # Berechne E aus neuen PEP
                    if E_after_swap < E_best_swap: # Falls besser, dann aktualisiere
                        E_best_swap = E_after_swap
                        best_swap = (t, swap)
                        std_dev_best = np.std(filtered_list) # Kriterium bei gleicher Lösungsqualität
                    elif E_after_swap == E_best_swap: # Falls gleichgut, dann entscheide nach Standartabweichungs-Kriterium
                        if np.std(filtered_list) < std_dev_best:
                            E_best_swap = E_after_swap
                            best_swap = (t, swap)
                            std_dev_best = np.std(filtered_list)
        if no_possible_swap == False: # Beende TS falls keine Nachbarschaft möglich
            break
        TL.append((best_swap[0], best_swap[1][0], best_swap[1][1])) # Aktualisiere Tabu-Liste
        workstation_e_first = np.copy(schedule[best_swap[0]][best_swap[1][0]]) # Speichere Job und dessen EP ab
        workstation_e_second = schedule[best_swap[0]][best_swap[1][1]]
        dif = workstation_e_first[1] - workstation_e_second[1] # Differenz der EP
        schedule[best_swap[0]][best_swap[1][0]] = workstation_e_second # Tausche Zuweisung
        schedule[best_swap[0]][best_swap[1][1]] = workstation_e_first
        PEP[best_swap[1][0]] -= dif # Aktualisiere PEP
        PEP[best_swap[1][1]] += dif
        PEP = np.round(PEP, 4) # Python Rundungsfehler vermeiden
        E_best_swap = np.max(PEP)
        if E_best_swap == E_MILP_Relax: # Falls Lösung der LP_Relax entspricht, dann Abbruch der TS da opt. Lösung gefunden
            #schedule_best = np.copy(schedule)
            E_best = np.max(PEP)
            break
        schedule, E_best_swap, PEP = ReOpt(jobs, periods, e_trans, np.copy(schedule), np.copy(PEP), e_trans_sorted) # bei Variante ohne Re-Opt einfach auskommentieren und zusätzlich nächste If-Abfrage
        # bei passiver Variante nur Output ändern -> schedule und PEP vor dem "=" entfernen, Anpassung in Re-Opt Datei notwendig
        # bei Variante mit nur jede 2. Iteration etc. einfach eine If Anweisung mit "it_count % 2 == 0:" vor Funktionsaufruf 
        if E_best_swap == E_MILP_Relax:
            #schedule_best = np.copy(schedule)
            E_best = np.max(PEP)
            break
        if E_best_swap < E_best: # Falls Lösung der LP_Relax entspricht, dann Abbruch der TS da opt. Lösung gefunden
            #schedule_best = np.copy(schedule)
            E_best = np.max(PEP)
        if len(TL) > 0.5 * (jobs - 1):
            TL.pop(0)
        it_count += 1
    return E_best #,schedule_dic_best
