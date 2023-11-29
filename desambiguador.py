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
    rubrica = rubrica.rstrip("\n")
    grupos_rubricas[rubrica] = get_close_matches(rubrica, rubricas, n=len(rubricas), cutoff=0.7)

# Cria arquivo .json com a lista de rubricas desambiguadas
with open("rubricas.json", "w") as json_file:
    json.dump(grupos_rubricas, json_file, indent=4) 