import gurobipy as gp
from gurobipy import GRB
import numpy as np

def MILP(jobs, periods, e):
    """
    Berechnet die Optimallösung des Problems
    :param jobs: Anzahl der Jobs
    :param periods: Anzahl der Perioden
    :param e: EP-Matrix
    :return obj_val: Optimaler Zielfunktionswert
    :return optimal: Beschreibt, ob eine Optimallösung innerhalb des Zeitlimits gefunden wurde
    """
    optimal = True # Gibt an, ob innerhalb des Zeitlimits eine Lösung gefunden wurde

    # Modell definieren:
    model = gp.Model("EJRSP")
    # Variablen:
    x = {}
    for i in range(0, jobs):
        for j in range(0, jobs):
            for t in range(0, periods):
                x[i, j, t] = model.addVar(vtype = GRB.BINARY, name = f"x[{i}][{j}][{t}]")
    E = model.addVar(name = "E")                
    model.update()
    # Nebenbedingungen:
    for j in range(0, jobs):
        for t in range (0, periods):
            model.addConstr(sum(x[i, j, t] for i in range(0, jobs)) == 1)
    for i in range(0, jobs):
        for t in range (0, periods):
            model.addConstr(sum(x[i, j, t] for j in range(0, jobs)) == 1)
    for i in range(0, jobs):
        model.addConstr(sum(x[i, j, t] * e[j, t] for j in range (0, jobs) for t in range(0, periods) ) <= E)
    # Zielfunktion:
    z = E 
    model.setObjective(z, GRB.MINIMIZE)
    # Paramter:
    model.setParam(GRB.Param.TimeLimit, 900) # 900 Sekunden Time-Limit
    # Optimierung:
    model.optimize()
    # Ausgabe:
    if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
        obj_val = model.objVal
        lb = model.ObjBound
    else: # Fiktiver Fall
        obj_val = np.inf
    if model.status == GRB.TIME_LIMIT:
        optimal = False

    """ Falls Veranschaulichung der Lösung erwünscht
    if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
        print("Zielfunktionswert =", model.objVal)
        print("\nSchedule:")
        col_width = 15
        print("Station(EP)", end = "")
        for i in range(jobs):
            print(f"Arbeiter {i}".center(col_width), end = "")
        print("\n" + "-" * (col_width * jobs + 9))
        for t in range(periods):
            print(f"Periode {t} |", end = "")
            for i in range(jobs):
                for j in range(jobs):
                    if x[i, j, t].x > 0.7:
                        print(f"{j}({e[j, t]})".center(col_width), end = "")
            print()
    """
    return round(obj_val, 4), optimal