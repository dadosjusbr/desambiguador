# Desambiguador

## Função

Um problema encontrado nos dados de remunerações é a ambiguidade entre as rubricas/itens nos contracheques, isto é, um mesmo item descrito de diferentes formas.

O intuito desse desambiguador é agrupar esses itens semelhantes a um termo comum e exportá-los em um arquivo json, possibilitando o uso da informação agregada pelos demais estágios e algoritmos do DadosJusBr.

Vale ressaltar que o desambiguador ainda não está pronto para ser utilizado sem avaliação humana. Um primeiro teste foi realizado com a rubrica "auxilio-alimentação" e essa rubrica foi desambiguada manualmente antes para fins de comparação. O desambiguador encontrou 12 de 17 rubricas semelhantes a `auxilio-alimentacao` (acurácia de 70,58%).

## Desambiguando uma nova rubrica

Para isso, faz-se necessário editar a lista de rubricas `lista_rubricas`, adicionando a nova rubrica a ser desambiguada no final do arquivo.

- Caso seja necessário mais de um termo para desambiguar uma determinada rubrica, basta adicionar os termos semelhantes na mesma linha separados por ponto e vírgula. Ex.:
  
```
licenca-premio;indenizacao-licenca-premio
```

- Caso encontre um problema de repetição de rubrica, basta adicionar **%** até a quantidade de repetições necessárias. Ex.:

```
aux-saude-magis-exerc-anterior%%
output: "aux saude magis exerc anterior aux saude magis exerc anterior aux saude magis exerc anterior"
```

A nova rubrica será adicionada ao arquivo `rubricas.json` com uma lista de rubricas semelhantes após execução do script.
