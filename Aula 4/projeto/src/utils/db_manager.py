import duckdb


class DBManager:
    def __init__(self):
        """
        Inicializa o gerenciador do banco de dados.
        """
        self.con = duckdb.connect(database="db", read_only=False)

    def setup_tables(self):
        """
        Configura as tabelas no banco de dados, criando sequências e tabelas se não existirem.
        """
        self.con.execute(
            "CREATE SEQUENCE IF NOT EXISTS seq_operational_metrics_id START 1"
        )
        self.con.execute("CREATE SEQUENCE IF NOT EXISTS seq_ml_metrics_id START 1")
        self.con.execute("CREATE SEQUENCE IF NOT EXISTS seq_predictions_id START 1")

        # Criar tabelas
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS operational_metrics (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_operational_metrics_id'),
                timestamp TIMESTAMP,
                method TEXT,
                url TEXT,
                response_status INTEGER,
                latency FLOAT
            )
        """
        )
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS ml_metrics (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_ml_metrics_id'),
                timestamp TIMESTAMP,
                rmse FLOAT,
                mae FLOAT
            )
        """
        )
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_predictions_id'),
                timestamp TIMESTAMP,
                model_type TEXT,
                input_data TEXT,
                predicted_value FLOAT,
                actual_value FLOAT
            )
        """
        )

    def insert_operational_metric(
        self, timestamp, method, url, response_status, latency
    ):
        """
        Insere uma métrica operacional na tabela correspondente.

        Args:
        - timestamp (TIMESTAMP): O timestamp da métrica.
        - method (str): O método HTTP utilizado.
        - url (str): A URL acessada.
        - response_status (int): O status da resposta.
        - latency (float): A latência da requisição.
        """
        self.con.execute(
            "INSERT INTO operational_metrics (timestamp, method, url, response_status, latency) VALUES (?, ?, ?, ?, ?)",
            (timestamp, method, url, response_status, latency),
        )

    def insert_ml_metric(self, timestamp, rmse, mae):
        """
        Insere uma métrica de aprendizado de máquina na tabela correspondente.

        Args:
        - timestamp (TIMESTAMP): O timestamp da métrica.
        - rmse (float): O valor do RMSE.
        - mae (float): O valor do MAE.
        """
        self.con.execute(
            "INSERT INTO ml_metrics (timestamp, rmse, mae) VALUES (?, ?, ?)",
            (timestamp, rmse, mae),
        )

    def insert_prediction(
        self, timestamp, model_type, input_data, predicted_value, actual_value=None
    ):
        """
        Insere uma previsão na tabela de previsões.

        Args:
        - timestamp (TIMESTAMP): O timestamp da previsão.
        - model_type (str): O tipo do modelo utilizado.
        - input_data (str): Os dados de entrada usados para a previsão.
        - predicted_value (float): O valor previsto.
        - actual_value (float, opcional): O valor real. Default é None.
        """
        self.con.execute(
            "INSERT INTO predictions (timestamp, model_type, input_data, predicted_value, actual_value) VALUES (?, ?, ?, ?, ?)",
            (timestamp, model_type, input_data, predicted_value, actual_value),
        )

    def update_actual_value_by_id(self, prediction_id, actual_value):
        """
        Atualiza o valor real para uma previsão específica no banco de dados usando seu ID.

        Args:
        - prediction_id (int): O ID da previsão a ser atualizada.
        - actual_value (float): O valor real a ser atualizado.
        """
        self.con.execute(
            "UPDATE predictions SET actual_value = ? WHERE id = ?",
            (actual_value, prediction_id),
        )

    def fetch_operational_metrics(self):
        """
        Busca todas as métricas operacionais do banco de dados.

        Returns:
        - List[Dict]: Uma lista de dicionários contendo as métricas operacionais.
        """
        return self.con.execute("SELECT * FROM operational_metrics").fetchall()

    def fetch_ml_metrics(self):
        """
        Busca todas as métricas de aprendizado de máquina do banco de dados.

        Returns:
        - List[Dict]: Uma lista de dicionários contendo as métricas de aprendizado de máquina.
        """
        return self.con.execute("SELECT * FROM ml_metrics").fetchall()

    def fetch_predictions(self):
        """
        Busca todas as previsões do banco de dados.

        Returns:
        - List[Dict]: Uma lista de dicionários contendo as previsões.
        """
        return self.con.execute("SELECT * FROM predictions").fetchall()

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.con.close()