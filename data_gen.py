import numpy as np
import random
import pickle

"""
Datei zur Generierung der EJRSP-Instanzen
Methodik wie bei Otto und Scholl (Reducing ergonomic risks by job rotation scheduling, 2012) beschrieben
Rundung auf 4 Dezimalstellen
"""

number_jobs = [10, 15, 20] # Job-Perioden Kombinationen
number_periods = [4, 8, 16]
instance_counter = 0
data = {}
for i in number_jobs:
    for t in number_periods:
        for inst in range(5): # Erstelle je Kombination 5 Instanzen
            mean = 30/t # Definiere Parameter für die Normalverteilung
            std_dev = 20/t
            lb = 2/t
            ub = 100/t
            ep_one_period=[]
            for point in range(i):
                point = np.random.normal(loc = mean, scale = std_dev) # Normalverteilung
                point = max(lb, min(ub, point)) # Punkte nach unten und oben abschneiden 
                ep_one_period.append(round(point, 4))
            ep_t_period = [ep_one_period.copy() for t_period in range(t)] # auf t Perioden multiplizieren
            e_trans_data = np.array(ep_t_period).transpose() # Matrix transponieren für später
            number_change_jobs = round(1/3 * i)
            random_jobs = random.sample(range(i), number_change_jobs) # Zufällig Jobs wählen, deren Einträge verändert werden
            for random_job in random_jobs:
                for element in range(t):
                    modification = random.uniform(-0.25, 0.25)
                    e_trans_data[random_job][element] = round(e_trans_data[random_job][element] * (1 + modification), 4) # Eintrag verändern
            list_for_dictonary = [i, t, e_trans_data]
            data[instance_counter] = list_for_dictonary # Instanz ins Dic einfügen
            instance_counter += 1

with open("data_main.pk1", "wb") as ejrsp_data: # Abspeichern
    pickle.dump(data, ejrsp_data)



            
