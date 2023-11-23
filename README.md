# Desambiguador

## Função

Um problema encontrado nos dados de remunerações é a ambiguidade entre as rubricas/itens nos contracheques, isto é, um mesmo item descrito de diferentes formas.

O intuito desse desambiguador é agrupar esses itens semelhantes a um termo comum e exportá-los em um arquivo json, possibilitando o uso da informação agregada pelos demais estágios e algoritmos do DadosJusBr.

## Desambiguando uma nova rubrica

Para isso, faz-se necessário editar a lista de rubricas `(desambiguador.py, linha 16)`, adicionando a nova rubrica a ser desambiguada:

```python
lista_rubricas = ["auxilio-alimentacao"]
```

A nova rubrica será adicionada ao arquivo `rubricas.json` com uma lista de rubricas semelhantes.

Após o arquivo ser atualizado, basta rodar o script `atualiza-passado.py`. O script pega a última rubrica adicionada ao arquivo json, agrega os valores por rubrica e atualiza a coluna `resumo` no banco de dados com a nova rubrica.
