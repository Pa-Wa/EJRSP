import numpy as np


def NCP(jobs, periods, e_trans, e_trans_sorted):
    """
    Führt die beschriebene Naive Konstruktionsheuristik durch
    :param jobs: Anzahl der Jobs
    :param periods: Anzahl der Perioden
    :param e_trans: EP-Matrix
    :param e_trans_sorted: bereits aufsteigend (je Periode) sortierte EP-Matrix
    :return schedule: Schedule nach Anwendung der Heuristik
    :return E: Zielfunktionswert des Schedules
    :return PEP: Persönliche EP der verschiedenen Arbeiter
    """
    PEP = np.zeros(jobs) # Persönliche ergonomische Punkte
    schedule = np.zeros((periods, jobs, 2)) # Schedule: Pro Periode eine Liste, in jeder Liste ist ein Tupel für die Arbeitsstation und deren EP angegeben, 1. Eintrag einer Liste steht für den 1. Arbeiter usw.
    for t in range(periods):
        worker_pep_sort = np.argsort(-PEP) # Sortiere PEP absteigend
        period_e_sort = e_trans_sorted[t] # Nutze jeweilige aufsteigend sortierte EP
        for i in range(jobs):
            assign_worker, assign_station, assign_ep = worker_pep_sort[i], period_e_sort[i], e_trans[t][period_e_sort[i]]
            schedule[t][assign_worker] = [assign_station, assign_ep] # Aktualisiere Schedule
            PEP[assign_worker] += assign_ep # Aktualisiere PEP
    E = np.max(PEP)
    return schedule, E, PEP