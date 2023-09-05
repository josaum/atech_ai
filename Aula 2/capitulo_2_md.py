# %% [markdown]
#
# ---
#
# ### Diferença entre Métricas e Losses
#
# - **Loss (Função de Perda)**: É uma função que mede o quão bem o modelo está se saindo em relação aos dados de treinamento. Durante o treinamento, o objetivo é minimizar essa função. A função de perda é usada pelo algoritmo de otimização para atualizar os parâmetros do modelo.
#
# - **Métrica**: É uma função que mede a qualidade do modelo em relação a uma tarefa específica (por exemplo, classificação, regressão). Ao contrário das funções de perda, as métricas são usadas para interpretar e avaliar o desempenho do modelo, mas não são usadas diretamente no processo de treinamento.
#
# ---
#
# ### Métricas e Funções de Perda para Regressão:
#
# #### 1. Erro Quadrático Médio (MSE - Mean Squared Error)
#
# - **Definição Matemática**:
#
# \[
# \text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
# \]
#
# - **Premissas**:
#   - Assume que os erros são distribuídos normalmente.
#
# - **Pontos Fortes**:
#   - Penaliza outliers fortemente devido ao quadrado.
#
# - **Pontos Fracos**:
#   - Pode ser sensível a outliers.
#
# - **Código Python**:
#
# ```python
# def mse(y_true, y_pred):
#     return np.mean((y_true - y_pred)**2)
# ```
#
# #### 2. Erro Absoluto Médio (MAE - Mean Absolute Error)
#
# - **Definição Matemática**:
#
# \[
# \text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|
# \]
#
# - **Premissas**:
#   - Não assume uma distribuição específica dos erros.
#
# - **Pontos Fortes**:
#   - Menos sensível a outliers do que o MSE.
#
# - **Pontos Fracos**:
#   - Não penaliza erros grandes tanto quanto o MSE.
#
# - **Código Python**:
#
# ```python
# def mae(y_true, y_pred):
#     return np.mean(np.abs(y_true - y_pred))
# ```
#
# #### 3. Raiz do Erro Quadrático Médio (RMSE - Root Mean Squared Error)
#
# - **Definição Matemática**:
#
# \[
# \text{RMSE} = \sqrt{\text{MSE}}
# \]
#
# - **Premissas**:
#   - Assume que os erros são distribuídos normalmente.
#
# - **Pontos Fortes**:
#   - É uma das métricas mais usadas, e sua escala é a mesma que a variável de resposta.
#
# - **Pontos Fracos**:
#   - Sensível a outliers.
#
# - **Código Python**:
#
# ```python
# def rmse(y_true, y_pred):
#     return np.sqrt(mse(y_true, y_pred))
# ```
#
# #### 4. Erro Percentual Absoluto Médio (MAPE - Mean Absolute Percentage Error)
#
# - **Definição Matemática**:
#
# \[
# \text{MAPE} = \frac{1}{n} \sum_{i=1}^{n} \left|\frac{y_i - \hat{y}_i}{y_i}\right|
# \]
#
# - **Premissas**:
#   - Os verdadeiros valores não devem ser zero, pois divide por \(y_i\).
#
# - **Pontos Fortes**:
#   - Escala independente, fácil interpretação em termos percentuais.
#
# - **Pontos Fracos**:
#   - Infinito ou indefinido se o verdadeiro valor for zero para qualquer observação. Pode fornecer erros muito grandes se os valores verdadeiros estiverem próximos de zero.
#
# - **Código Python**:
#
# ```python
# def mape(y_true, y_pred):
#     return np.mean(np.abs((y_true - y_pred) / y_true))
# ```
#
# #### 5. R-Squared (Coeficiente de Determinação)
#
# - **Definição Matemática**:
#
# \[
# R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}
# \]
#
# - **Premissas**:
#   - Assume que os erros são distribuídos normalmente.
#
# - **Pontos Fortes**:
#   - Mede a proporção da variância total explicada pelo modelo. Valores mais próximos de 1 indicam um bom ajuste.
#
# - **Pontos Fracos**:
#   - Pode ser um indicador enganoso do ajuste do modelo se o modelo não for ajustado ao intercepto. Além disso, sempre aumenta à medida que mais variáveis são adicionadas, independentemente de sua utilidade.
#
# - **Código Python**:
#
# ```python
# def r_squared(y_true, y_pred):
#     ss_res = np.sum((y_true - y_pred)**2)
#     ss_tot = np.sum((y_true - np.mean(y_true))**2)
#     return 1 - (ss_res / ss_tot)
# ```
#
# #### 6. Quantile Loss
#
# - **Definição Matemática**:
#
# \[
# QL_{\tau}(y, \hat{y}) = \frac{1}{n} \sum_{i=1}^{n} \left[ \tau \cdot \max(y_i - \hat{y}_i, 0) + (1-\tau) \cdot \max(\hat{y}_i - y_i, 0) \right]
# \]
#
# - **Premissas**:
#   - Não assume uma distribuição específica para os erros.
#
# - **Pontos Fortes**:
#   - Penaliza erros acima ou abaixo do quantil de interesse de forma diferenciada, permitindo modelar a incerteza de maneira mais flexível.
#
# - **Pontos Fracos**:
#   - Para cada quantil desejado, é necessário treinar um modelo diferente.
#
# - **Código Python**:
#
# ```python
# def quantile_loss(y_true, y_pred, tau=0.5):
#     return np.mean(np.where(y_true >= y_pred, tau * (y_true - y_pred), (1 - tau) * (y_pred - y_true)))
# ```
#
# #### 7. MASE (Mean Absolute Scaled Error)
#
# - **Definição Matemática**:
#
# \[
# \text{MASE} = \frac{\text{MAE}}{\frac{1}{n-1} \sum_{i=2}^{n} |y_i - y_{i-1}|}
# \]
#
# - **Premissas**:
#   - Assume que o método de referência é a
#
#  previsão "naive", que apenas considera o último valor observado.
#
# - **Pontos Fortes**:
#   - Escala independente, fácil interpretação. Útil quando se deseja comparar o desempenho do modelo em relação a um método simples de referência.
#
# - **Pontos Fracos**:
#   - O denominador, baseado na previsão "naive", pode não ser adequado para todos os casos, especialmente para séries temporais não estacionárias.
#
# - **Código Python**:
#
# ```python
# def mase(y_true, y_pred):
#     n = len(y_true)
#     naive_forecast = y_true[:-1]
#     y_t_minus_one = y_true[1:]
#     mae_naive = np.mean(np.abs(y_t_minus_one - naive_forecast))
#     mae_model = mae(y_true[1:], y_pred[1:])
#     return mae_model / mae_naive
# ```
#
# ---
