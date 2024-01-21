import numpy as np
import pickle
import time
import gurobipy as gp
import pandas as pd

from methods.ncp import NCP
from methods.sh import SH
from methods.ts import TS
from methods.milp import MILP


"""
Mit dieser Datei werden die einzelnen Verfahren auf die generierten Instanzen angewendet.
Nach Beendigung der Verfahren wird eine CSV-Datei mit den Ergebnissen erstellt.
Zur Anwendung der TS Varianten (aktive/passive Re-Optimierung bzw. keine Re-Optimierung) bitte die jeweiligen Kommentare beachten/umsetzen
"""

gp.setParam("OutputFlag", 0) # Ausgabe des Solver Outputs verhindern

with open("data_main.pk1", "rb") as datei: # Instanz-Datei öffnen
    data = pickle.load(datei)

solution_list = []
for instance in data: 
    jobs_data = data[instance][0] # Abruf der Daten
    periods_data = data[instance][1]
    e = data[instance][2] # n*T
    e_trans_data = e.transpose() # T*n
    e_trans_sorted = np.argsort(e_trans_data, axis = 1) # Sortiere EP je Periode
    print(jobs_data,periods_data)
    
    start_time = time.time() # Zeit messen
    schedule_ncp, E_ncp, PEP_ncp = NCP(jobs_data, periods_data, e_trans_data, e_trans_sorted)
    NCP_time = time.time() - start_time # Zeitmessung beendet

    start_time = time.time()
    schedule_sh, E_sh, PEP_sh = SH(jobs_data, periods_data, e_trans_data, e_trans_sorted)
    SH_time = time.time() - start_time

    start_time = time.time()
    E_ts = TS(jobs_data, periods_data, e_trans_data, e, e_trans_sorted)
    TS_time = time.time() - start_time
    
    start_time = time.time()
    E_MILP, optimality = MILP(jobs_data, periods_data, e)
    MILP_time = time.time() - start_time
    
    solution = {"ID": instance, "E NCP": E_ncp, "Time NCP": NCP_time, "E SH": E_sh, "Time SH": SH_time, "E TS": E_ts, "Time TS": TS_time, "E MILP": E_MILP, "Time": MILP_time, "Opt.?": optimality}
    solution_list.append(solution)

df_solution = pd.DataFrame(solution_list)
print(df_solution)
df_solution.to_csv("solution_main.csv", sep = ";") # Erstelle CSV-Datei mit Lösungsdaten