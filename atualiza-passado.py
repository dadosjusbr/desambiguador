from postgres import *
import json
import pandas as pd
from tqdm import tqdm

conn = get_connection()

# Lendo o json e pegando a última rubrica desambiguada 
with open("rubricas.json", encoding='utf-8') as meu_json:
    rubricas = json.load(meu_json)
    key = list(rubricas.keys())[-1]
    values = tuple(rubricas[key])

# A modificação inicial deve utilizar essa query, visto que também criará o campo 'outras'
# Após isso, deverá ser utilizada a segunda query, calculando apenas o valor agregado da nova rubrica.
# O campo 'outras' não considera o valor de rubricas da categoria "descontos" - tipo = 'D'
query = f"SELECT orgao, mes, ano, SUM(CASE WHEN item_sanitizado IN {values} THEN valor ELSE 0 END) AS valor_rubrica, sum(CASE WHEN tipo != 'D' THEN valor ELSE 0 END) as valor_total from remuneracoes r where orgao = 'cnj' and mes = 1 and ano = 2018 group by (orgao, mes, ano)"
# query = f"SELECT orgao, mes, ano, SUM(CASE WHEN item_sanitizado IN {values} THEN valor ELSE 0 END) AS valor_rubrica from remuneracoes r where orgao = 'cnj' and mes = 1 and ano = 2018 group by (orgao, mes, ano)"

# Pegando os valores agregados por rubrica para cada órgão, mês e ano.
valor_rubrica = consultar_db(conn, query)
valor_rubrica = pd.DataFrame(valor_rubrica, columns=['orgao', 'mes', 'ano', 'valor_rubrica', 'valor_total'])

# Atualizando o campo resumo com o valor agregado da nova rubrica
for orgao, mes, ano, valor_rubrica, valor_total in tqdm(valor_rubrica.to_numpy()):
    valor_total -= valor_rubrica

    # A modificação inicial deve utilizar essa query, criando também o campo 'outras'
    # Após isso, deverá ser utilizada a segunda query, apenas atualizando o valor deste campo.
    query = f'''UPDATE coletas SET resumo = jsonb_set(resumo, '{{{key}}}', '{valor_rubrica}', TRUE) || jsonb_set(resumo, '{{outras}}', '{valor_total}', TRUE) WHERE id_orgao = '{orgao}' and mes = {mes} and ano = {ano} and atual = true'''
    # query = f'''UPDATE coletas SET resumo = jsonb_set(resumo, '{{{key}}}', '{valor_rubrica}', TRUE) || jsonb_set(resumo, '{{outras}}', to_jsonb((resumo->>'outras')::numeric - {valor_rubrica}), FALSE) WHERE id_orgao = '{orgao}' and mes = {mes} and ano = {ano} and atual = true'''

    run_db(conn, query)

