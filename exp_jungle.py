import pandas as pd
import numpy as np

df_explorateurs = pd.read_csv("parcours_explorateurs.csv")

points_de_depart = df_explorateurs[df_explorateurs["type_aretes"] == "depart"]["noeud_amont"].values
points_d_arrivee = df_explorateurs[df_explorateurs["type_aretes"] == "arrivee"]["noeud_aval"].values
liens = {ligne["noeud_amont"]: ligne["noeud_aval"] for _, ligne in df_explorateurs.iterrows()}

def tracer_parcours(depart):
    parcours = [depart]
    actuel = depart
    while actuel not in points_d_arrivee:
        suivant = liens[actuel]
        parcours.append(suivant)
        actuel = suivant
    return parcours

def montrer_parcours(nom, parcours):
    print(f"Explorateur : {nom}")
    print(f"Chemin : {parcours}")

for depart in points_de_depart:
    parcours = tracer_parcours(depart)
    montrer_parcours(depart, parcours)

graph = {}
for _, ligne in df_explorateurs.iterrows():
    graph.setdefault(ligne["noeud_amont"], []).append(ligne["noeud_aval"])

def explorer_en_profondeur(noeud, visite, trace):
    visite.add(noeud)
    trace.append(noeud)
    parcours_maximal = []
    if noeud in graph:
        for voisin in graph[noeud]:
            if voisin not in visite:
                nouveau_trace = explorer_en_profondeur(voisin, visite.copy(), trace.copy())
                if len(nouveau_trace) > len(parcours_maximal):
                    parcours_maximal = nouveau_trace
    return parcours_maximal

parcours_maximaux = {}
for depart in graph.keys():
    parcours_maximaux[depart] = explorer_en_profondeur(depart, set(), [])
