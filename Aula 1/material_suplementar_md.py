# %% [markdown]
# # Material Suplementar 1
#
# ### Distribuição Normal
#
# A **distribuição normal**, também conhecida como distribuição Gaussiana, é uma das distribuições estatísticas mais conhecidas e utilizadas em uma variedade de campos, desde a física até as ciências sociais. Ela é importante devido a vários motivos, principalmente pelo Teorema do Limite Central.
#
# **Fundamentos**:
# - Simétrica em torno de sua média.
# - A maioria dos dados (cerca de 68%) cai dentro de um desvio padrão da média, 95% dentro de dois desvios padrão, e 99,7% dentro de três desvios padrão.
#
# **Equação Matemática**:
# \[ f(x | \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}} \]
# Onde:
# - \( \mu \) é a média
# - \( \sigma^2 \) é a variância
# - \( e \) é a base do logaritmo natural
#
# **Código Python**:
# ```python
# import numpy as np
# import matplotlib.pyplot as plt
#
# mu, sigma = 0, 0.1
# s = np.random.normal(mu, sigma, 1000)
#
# plt.hist(s, 30, density=True)
# plt.xlabel('Valor')
# plt.ylabel('Frequência')
# plt.title('Distribuição Normal')
# plt.show()
# ```
#
# ---
#
# ### Distribuição Power Law
#
# A **distribuição Power Law** (ou Lei de potência) descreve um fenômeno onde uma pequena quantidade de ocorrências é comum, enquanto uma grande quantidade de ocorrências é rara.
#
# **Fundamentos**:
# - Frequentemente observada em sistemas complexos.
# - Exemplos incluem a distribuição de renda, frequência de palavras em idiomas, e links na web.
#
# **Equação Matemática**:
# \[ P(x) = ax^{-k} \]
# Onde:
# - \( a \) e \( k \) são constantes. \( k \) é tipicamente maior que 1.
#
# **Código Python**:
# ```python
# import powerlaw
#
# data = powerlaw.Power_Law(xmin=1, parameters=[2.5]).generate_random(10000)
# fit = powerlaw.Fit(data)
# print(fit.power_law.alpha)
# print(fit.power_law.xmin)
# ```
#
# ---
#
# ### Comparação entre Distribuição Normal e Power Law
#
# **Distribuição Normal vs Power Law**:
# - Enquanto a distribuição normal é simétrica e tem uma "cauda" finita, a power law tem uma "cauda" pesada ou uma longa cauda.
# - Em uma distribuição normal, eventos extremos são muito raros, enquanto na power law, a probabilidade de eventos extremos é maior.
# - A distribuição normal é definida por dois parâmetros (média e variância), enquanto a power law é tipicamente definida pelos parâmetros \( a \) e \( k \).
# - Em muitos sistemas naturais, as distribuições de power law surgem devido a processos multiplicativos, enquanto as distribuições normais tendem a surgir de processos aditivos.
#
# Ambas as distribuições são ferramentas valiosas na caixa de ferramentas do cientista de dados e são aplicáveis a diferentes fenômenos. Escolher a distribuição apropriada para modelar um conjunto de dados pode ter um grande impacto nas conclusões e previsões derivadas desse modelo.
#
# ---

# %% [markdown]
# ## Material Suplementar 2
#
# ### Quando Faz Sentido Tirar a Média de um Conjunto de Valores
#
# A média, ou valor esperado, é uma das estatísticas descritivas mais comuns. No entanto, não é sempre que ela é a medida mais apropriada para resumir um conjunto de valores. Para determinar se faz sentido calcular a média, deve-se considerar os seguintes pontos:
#
# **1. Dados contínuos e intervalares**: A média é mais apropriada para dados que são contínuos e intervalares, onde as diferenças entre os valores têm significado. Por exemplo, a média das temperaturas diárias durante um mês é informativa.
#
# **2. Distribuição simétrica**: Se os dados têm uma distribuição aproximadamente simétrica, a média é uma boa representação do "centro" do conjunto de dados. Em um conjunto de dados simétrico, a média, mediana e moda tendem a ser iguais ou próximas.
#
# **3. Ausência de outliers significativos**: A média é sensível a valores extremos. Se há outliers significativos no conjunto de dados, eles podem distorcer a média e torná-la menos representativa do conjunto de dados como um todo.
#
# ### Quando Não Faz Sentido Tirar a Média
#
# **1. Dados ordinais ou nominais**: Em variáveis ordinais, a ordem dos dados é importante, mas as diferenças entre os valores não têm significado consistente. Por exemplo, uma escala de satisfação de "não satisfeito", "neutro" e "muito satisfeito" é ordinal. Enquanto você pode codificar essas respostas numericamente (como 1, 2 e 3), a média desses números não forneceria um insight significativo.
#
# **2. Presença de outliers**: Como a média é sensível a outliers, se houver valores extremos no conjunto de dados, a média pode não representar adequadamente o "centro" dos seus dados.
#
# **3. Distribuições altamente assimétricas**: Em distribuições fortemente inclinadas, a média pode ser puxada na direção da cauda, tornando-a menos representativa da maioria dos valores no conjunto de dados.
#
# **4. Dados em escala de razão com zero não inerente**: Em escalas onde o zero não tem um significado inerente (como temperatura em Celsius), a média pode não ser interpretável de maneira clara.
#
# **Conclusão**:
#
# Ao considerar se deve ou não calcular a média de um conjunto de dados, é crucial compreender a natureza dos dados e o que se deseja inferir a partir da estatística. Em muitos casos, outras medidas de tendência central, como a mediana ou a moda, podem ser mais apropriadas. Ao analisar dados, sempre visualize sua distribuição e considere seu tipo e estrutura antes de decidir sobre a estatística descritiva mais adequada.
#
# ---

# %% [markdown]
# ## Divisões em Ciência de Dados
#
# ### Divisão 1: Tipos de Aprendizado
#
# **1. Aprendizado Supervisionado**:
#    - **Descrição**: Utiliza um conjunto de dados onde as saídas corretas são conhecidas para aprender o mapeamento entre entradas e saídas. É fundamentalmente utilizado para tarefas de predição.
#    - **Exemplos de algoritmos**: Regressão linear, árvores de decisão, máquinas de vetores de suporte (SVM) e redes neurais.
#    - **Complexidade de Implementação**: Moderada, mas varia com o algoritmo.
#    - **Capacidade de Geração de Valor**: Alto valor em tarefas de previsão e classificação, tais como prever vendas ou classificar emails como spam.
#
# **2. Aprendizado Não-supervisionado**:
#    - **Descrição**: Usado quando não temos um conjunto de dados rotulado. O foco está na estrutura e padrões dos dados.
#    - **Exemplos de algoritmos**: K-means, PCA (Análise de Componentes Principais) e DBSCAN.
#    - **Complexidade de Implementação**: Moderada a Alta, devido à necessidade de interpretar os resultados.
#    - **Capacidade de Geração de Valor**: Útil para segmentação de mercado, detecção de anomalias, e estruturação de dados.
#
# **3. Aprendizado Auto-supervisionado**:
#    - **Descrição**: Uma forma de aprendizado supervisionado onde as etiquetas são geradas a partir dos próprios dados.
#    - **Exemplos de algoritmos**: Autoencoders e modelos de predição de próxima palavra.
#    - **Complexidade de Implementação**: Alta, dada a natureza complexa do treinamento.
#    - **Capacidade de Geração de Valor**: Utilizado principalmente em situações com falta de dados rotulados, especialmente em tarefas de processamento de linguagem natural e visão computacional.
#
# **4. Aprendizado por Reforço**:
#    - **Descrição**: Os modelos são treinados tomando ações em um ambiente para maximizar uma recompensa cumulativa.
#    - **Exemplos de algoritmos**: Q-learning e Deep Q Networks.
#    - **Complexidade de Implementação**: Alta, devido à necessidade de simular ambientes e ajustar recompensas.
#    - **Capacidade de Geração de Valor**: Alto valor em aplicações como jogos, robótica e otimização de sistemas.
#
# ### Divisão 2: Tipos de Analytics
#
# **1. Analytics Descritivo**:
#    - **Descrição**: Responde à pergunta "O que aconteceu?". Analisa dados passados para entender como eles podem impactar futuras decisões.
#    - **Exemplos de Algoritmos**: Estatísticas descritivas, análise de tendência.
#    - **Complexidade de Implementação**: Baixa.
#    - **Capacidade de Geração de Valor**: Fundamental para qualquer empresa entender seu desempenho histórico.
#
# **2. Analytics Diagnóstico**:
#    - **Descrição**: Responde à pergunta "Por que algo aconteceu?".
#    - **Exemplos de Algoritmos**: Análise de regressão, análise de fator.
#    - **Complexidade de Implementação**: Moderada.
#    - **Capacidade de Geração de Valor**: Auxilia na identificação de causas de problemas ou oportunidades.
#
# **3. Analytics Preditivo**:
#    - **Descrição**: Responde à pergunta "O que poderia acontecer no futuro?".
#    - **Exemplos de Algoritmos**: Modelos de séries temporais, florestas aleatórias e redes neurais.
#    - **Complexidade de Implementação**: Moderada a Alta, dependendo da técnica.
#    - **Capacidade de Geração de Valor**: Potencialmente alto, pois pode ajudar as empresas a se prepararem para futuras oportunidades ou ameaças.
#
# **4. Analytics Prescritivo**:
#    - **Descrição**: Responde à pergunta "O que deveríamos fazer sobre isso?".
#    - **Exemplos de Algoritmos**: Otimização linear, pesquisa operacional.
#    - **Complexidade de Implementação**: Alta, pois muitas vezes requer simulações.
#    - **Capacidade de Geração de Valor**: Extremamente alto, pois pode orientar a ação e otimizar os resultados.
#
#
# ---

# %% [markdown]
# ## Material Suplementar 3: Quantos Dados Eu Preciso? O Mito do n=30
#
# (referência: Nassim Nicholas Taleb: https://www.edge.org/response-detail/25401)
#
# A ciência de dados, estatística e pesquisa têm uma máxima que muitas vezes é mal interpretada: a ideia de que uma amostra de tamanho \( n = 30 \) é, de alguma forma, "suficiente" para fazer inferências sobre uma população. Essa noção decorre da Central Limit Theorem (CLT), que sugere que a distribuição das médias amostrais de qualquer distribuição com variância finita irá se aproximar de uma distribuição normal, independentemente da forma da distribuição original, desde que a amostra seja grande o suficiente. Na prática, \( n = 30 \) tornou-se um ponto de referência, mas isso pode ser enganoso.
#
# Vamos desmascarar esse mito.
#
# ### Distribuições e Convergência
#
# 1. **Distribuições Normais e a Racionalidade do n=30**: Em cenários ideais, com distribuições perfeitamente normais, a média da amostra (a partir de um tamanho de amostra de cerca de 30) tende a ser uma boa estimativa da média populacional. No entanto, isso é verdade principalmente para distribuições que não têm muita assimetria ou caudas pesadas.
#
# 2. **Log-Normal, Power Law e o Problema com n=30**: Em muitos fenômenos do mundo real, particularmente em ciências sociais, economia, e redes, os dados seguem distribuições que são log-normais ou obedecem a uma lei de potência. Estas são conhecidas por suas caudas pesadas, e a regra do n=30 simplesmente não se aplica. Uma amostra de tamanho 30, ou mesmo muito maior, não garante que a média da amostra se aproxime da média da população. De fato, para algumas distribuições de lei de potência, a variância é infinita, o que significa que não há média "típica"!
#
# ### Na Prática: A Importância de Conhecer a Distribuição
#
# Para distribuições com caudas pesadas, como a lei de potência, a média amostral pode variar enormemente de uma amostra para outra, mesmo para amostras relativamente grandes. E aqui está o ponto crítico: em muitos casos, pode ser impraticável coletar uma amostra suficientemente grande para que a média amostral se estabilize.
#
# Isso nos leva a uma conclusão importante: o tamanho da amostra necessário para fazer inferências precisas depende fortemente da natureza da distribuição subjacente dos dados. Se você não sabe que tipo de distribuição seus dados seguem (e na maioria dos casos do mundo real, você não sabe), confiar cegamente na regra do n=30 pode ser perigoso.
#
# ### Conclusão
#
# Enquanto o n=30 pode funcionar para alguns cenários, é vital entender o contexto e a distribuição dos dados antes de se comprometer com qualquer número. Em muitos casos práticos, especialmente quando se trata de distribuições com caudas pesadas, a média pode não ser uma métrica confiável e o tamanho da amostra necessário pode ser impraticável. A ciência de dados é tanto sobre compreensão e intuição quanto sobre números, e abordagens simplistas podem levar a conclusões equivocadas.
