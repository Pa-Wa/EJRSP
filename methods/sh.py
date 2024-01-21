import numpy as np
from methods.ncp import NCP


def SH(jobs, periods, e_trans, e_trans_sorted):
    """
    Führt die beschriebene Smoothing Heuristik durch
    :param jobs: Anzahl der Jobs
    :param periods: Anzahl der Perioden
    :param e_trans: EP-Matrix
    :param e_trans_sorted: bereits aufsteigend (je Periode) sortierte EP-Matrix
    :return schedule_best: Bestes Schedule nach Anwendung der Heuristik
    :return E_best: Zielfunktionswert des besten Schedule nach Anwendung der Heuristik
    :return PEP_best: PEP der verschiedenen Arbeiter des besten Schedule nach Anwendung der Heuristik
    """
    schedule, E, PEP = NCP(jobs, periods, e_trans, e_trans_sorted) # Erzeuge Startlösung
    stop_counter = 0 # Abbruchkriterium
    schedule_best = np.copy(schedule)
    E_best = np.max(PEP)
    PEP_best = np.copy(PEP)
    iteration = 1 # Iterationszähler
    while stop_counter < 10:
        other_schedule = False # 2. Abbruchkriterium: kein anderes Schedule nach einer Iteration
        for t in range(periods): # Gleiches Vorgehen wie in NCP, außer das PEP mit angepasst werden muss
            for i in range(jobs):
                PEP[i] -= schedule[t][i][1]
            worker_pep_sort = np.argsort(-PEP)
            period_e_sort = e_trans_sorted[t]
            for i in range(jobs):
                assign_worker, assign_station, assign_ep = worker_pep_sort[i], period_e_sort[i], e_trans[t][period_e_sort[i]]
                PEP[assign_worker] += assign_ep
                if other_schedule == False:
                    if schedule[t][assign_worker][0] != assign_station: # Überprüfe, ob Änderung am Schedule
                        other_schedule = True
                schedule[t][assign_worker] = [assign_station, assign_ep]
        PEP = np.round(PEP, 4) # Python-Rundungsfehler vermeiden
        E_new = np.max(PEP)
        if other_schedule == False: # Abbruch, falls kein neues Schedule zu vorheriger Iteration
            break
        if E_new < E_best: # Falls bessere Lösung gefunden, dann aktualisiere
            stop_counter = 0
            E_best = np.max(PEP)
            schedule_best = np.copy(schedule)
            PEP_best = np.copy(PEP)
        else:
            stop_counter += 1
        iteration += 1
    return schedule_best, E_best, PEP_best