from postgres import *
import pandas as pd
import json

# Fazendo a conexão com o banco
conn = get_connection()

# Obtendo lista de rubricas
rubricas = consultar_db(conn, "SELECT rubrica, desambiguacao_micro, desambiguacao_macro FROM rubricas")
rubricas = pd.DataFrame(rubricas, columns=["rubrica", "desambiguacao_micro", "desambiguacao_macro"])

# Agrupando as rubricas por desambiguação micro
resultado_micro = dict(zip(rubricas['rubrica'], rubricas['desambiguacao_micro']))

# Cria arquivo .json com a lista de desambiguação micro
with open("desambiguacao_micro.json", "w") as json_file:
    json.dump(resultado_micro, json_file, indent=4)
   
# Agrupando as rubricas por desambiguação macro 
resultado_macro = dict(zip(rubricas['rubrica'], rubricas['desambiguacao_macro']))

# Cria arquivo .json com a lista de desambiguação macro
with open("desambiguacao_macro.json", "w") as json_file:
    json.dump(resultado_macro, json_file, indent=4)