import gurobipy as gp
from gurobipy import GRB
import numpy as np

def MILP_Relax(jobs, periods, e):
    """
    Berechnet die Optimallösung des LP-Relaxierten Problems
    :param jobs: Anzahl der Jobs
    :param periods: Anzahl der Perioden
    :param e: EP-Matrix (nicht wie vorher transponiert)
    :return obj_val: Optimaler Zielfunktionswert der LP-Relaxation 
    """
    # Modell definieren:
    model = gp.Model("EJRSP_Relax")
    # Variablen:
    x = {}
    for i in range(0, jobs):
        for j in range(0, jobs):
            for t in range(0, periods):
                x[i, j, t] = model.addVar(vtype = GRB.CONTINUOUS, name = f"x[{i}][{j}][{t}]")
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
    # Optimierung:
    model.optimize()
    # Ausgabe:
    if model.status == GRB.OPTIMAL:
        obj_val = model.objVal
    else: # Kann nicht eintreten
        obj_val = np.inf
    return np.ceil(obj_val*10000)/10000