import numpy as np

def ReOpt(jobs, periods, e_trans, schedule, PEP, e_trans_sorted):
    """
    Führt die beschriebene Re-Optimierung durch, grundsätzlich das gleiche wie in SH nur ohne Funktionsaufruf NCP
    :param jobs: Anzahl der Jobs
    :param periods: Anzahl der Perioden
    :param e_trans: EP-Matrix
    :param schedule: Schedule nach Anwendung von TS-Iteration
    :param PEP: PEP der verschiedenen Arbeiter des Schedule
    :return schedule_best: Bestes Schedule nach Anwendung der Re-Optimierung
    :return E_best: Zielfunktionswert des besten Schedule nach Anwendung der Re-Optimierung
    :return PEP_best: PEP der verschiedenen Arbeiter des besten Schedule nach Anwendung der Re-Optimierung
    """
    stop_counter = 0
    schedule_best = np.copy(schedule) # kann bei passiver Methode auskommentiert werden
    PEP_best = np.copy(PEP) # kann bei passiver Methode auskommentiert werden
    E_best = np.max(PEP)
    iteration = 1 
    while stop_counter < 10:
        other_schedule = False
        for t in range(periods):
            for i in range(jobs):
                PEP[i] -= schedule[t][i][1]
            worker_pep_sort = np.argsort(-PEP)
            period_e_sort = e_trans_sorted[t]
            for i in range(jobs):
                assign_worker, assign_station, assign_ep = worker_pep_sort[i], period_e_sort[i], e_trans[t][period_e_sort[i]]
                PEP[assign_worker] += assign_ep
                if other_schedule == False:
                    if schedule[t][assign_worker][0] != assign_station:
                        other_schedule = True
                schedule[t][assign_worker] = [assign_station, assign_ep]
        PEP = np.round(PEP, 4)
        E_new = np.max(PEP)
        if other_schedule == False:
            break
        if E_new < E_best:  
            stop_counter = 0 
            E_best = np.max(PEP) 
            schedule_best = np.copy(schedule) # kann bei passiver Methode auskommentiert werden
            PEP_best = np.copy(PEP) # kann bei passiver Methode auskommentiert werden
        else: 
            stop_counter += 1 
        iteration += 1 
    return schedule_best, E_best, PEP_best #bei passiver Methode: schedule_best und PEP-best entfernen