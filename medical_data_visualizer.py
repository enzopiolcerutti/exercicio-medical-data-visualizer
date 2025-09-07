# Importando as bibliotecas necessárias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
# Nessa linha o arquivo csv está sendo carregado
# A função pd.read_csv lê o arquivo e cria uma estrutura de dados (dataframe)
df = pd.read_csv('medical_examination.csv')

# 2
# Aqui tem o calculo para realizar se a pessoa está classificada como acima do peso ou não
# O IMC é calculado dividindo o peso pela altura ao quadrado "metros"
# Se o IMC for maior que 25, a pessoa é considerada acima do peso 
# A função astype(int) converte os valores booleanos (True/False) para inteiros (1/0)
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# 3
# Aqui os valores de colesterol e glicose estão sendo normalizados para 0 e 1, 0 normal e 1 acima do normal
# Se o valor for 1, ele é alterado para 0, caso contrário, é alterado para 1
df['cholesterol'] = (df['cholesterol'] > 1) * 1
df['gluc'] = (df['gluc'] > 1) * 1

# 4
# Nessa parte existe a função que irá criar o gráfico de barras
def draw_cat_plot():
    # 5
    # Aqui é passado os valores que irão compor as barras do gráfico com a presença ou não de doenças
    #  A função pd.melt transforma a estrutura de dados de um formato largo para um formato longo
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
 
    # 6
    # Nesse trecho os dados vão ser agrupados para a criação do gráfico
    # A função groupby agrupa os dados tendo em vista as colunas especificadas
    # A função size conta o número de atividades em cada grupo
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name= 'total')
    
    # 7
    # Aqui estão sendo passados os parâmetros para o gráfico de barras que vai ser criado
    # A função catplot cria o gráfico de barras
    fig = sns.catplot(x = 'variable', y = 'total', hue = 'value', col = 'cardio', data =df_cat , kind = 'bar')

    # 8
    # Nessa linha o gráfico é convertido para um objeto do matplotlib
    # A propriedade figure retorna a figura associada ao objeto seaborn
    fig = fig.figure

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    # Aqui é feito um filtro para remover valores inconsistentes
    # A cópia do DataFrame original é criada para evitar alterações indesejadas
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12
    # Aqui é calculada a correlação entre as variáveis da estrutura de dados
    # A função corr calcula a correlação entre as colunas numéricas da estrutura de dados
    corr = df_heat.corr()

    # 13
    # Nessa linha é criado uma máscara para ocultar a metade superior da matriz de correlação que é aquela que não é necessária
    # A função np.triu cria uma matriz triangular superior com valores True acima da diagonal principal e False abaixo dela
    # A função np.ones_like cria uma matriz de uns com a mesma forma que a matriz de correlação 
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    # Aqui são definidos os parâmetros para o gráfico de calor
    # A função subplots cria uma figura e um conjunto de subplots
    fig, ax = plt.subplots(figsize=(12, 8)) 

    # 15
    # Nessa linha o gráfico de calor é criado
    # A função heatmap cria o gráfico de calor
    # O parâmetro data recebe a matriz de correlação
    # O parâmetro mask aplica a máscara para ocultar a metade superior da matriz
    # O parâmetro annot=True mostra os valores de correlação em cada célula do gráfico
    # O parâmetro fmt escolhe o formato dos valores exibidos
    # O parâmetro center mostra o valor central da escala de cores
    # O parâmetro ax mostra em qual eixo o gráfico será desenhado
    sns.heatmap(data = corr, mask = mask, annot = True, fmt = '.1f', center = 0, ax = ax)

    # 16
    fig.savefig('heatmap.png')
    return fig