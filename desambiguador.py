import difflib  
from difflib import get_close_matches
from postgres import *
import pandas as pd
import json
from tqdm import tqdm

# Fazendo a conexão com o banco
conn = get_connection()

# Obtendo lista de rubricas sanitizadas e distintas
rubricas = consultar_db(conn, "SELECT DISTINCT item_sanitizado FROM remuneracoes WHERE inconsistente = false")
rubricas = pd.DataFrame(rubricas, columns=["item"]).item.values

# Lista de rubricas a serem agrupadas
# Esse arquivo deverá ser editada ao desambiguar uma nova rubrica
lista_rubricas = open("lista_rubricas.txt", "r").readlines()
grupos_rubricas = {}

# Usando o método get_close_matches para desambiguar as rubricas, com precisão de 70%
for rubrica in tqdm(lista_rubricas):
    # Caso seja necessário mais de um termo para desambiguar uma rubrica, esperamos esses termos separados por ";"
    rubrica = rubrica.rstrip("\n").split(";")

    # Desambiguamos cada termo e adicionamos a sua respectiva rubrica, isto é, o primeiro termo.
    for r in rubrica:
        lista_desambiguada = get_close_matches(r, rubricas, n=len(rubricas), cutoff=0.7)
        
        if rubrica[0] in grupos_rubricas:
            grupos_rubricas[rubrica[0]].extend(lista_desambiguada)
        else:
            grupos_rubricas[rubrica[0]] = lista_desambiguada

    # Limpando a lista desambiguada da rubrica e mantendo apenas itens distintos.
    grupos_rubricas[rubrica[0]] = list(set(grupos_rubricas[rubrica[0]]))
    grupos_rubricas[rubrica[0]].sort()

# Cria arquivo .json com a lista de rubricas desambiguadas
with open("rubricas.json", "w") as json_file:
    json.dump(grupos_rubricas, json_file, indent=4)