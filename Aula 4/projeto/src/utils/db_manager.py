import duckdb
import datetime
from ..monitoring.monitor import calculate_rmse, calculate_mae
import logging


class DBManager:
    def __init__(self):
        """
        Inicializa o gerenciador do banco de dados.
        """
        logging.info("Initializing DBManager")
        self.con = duckdb.connect(database="db", read_only=False)
        logging.info("DBManager initialized successfully")

    def setup_tables(self):
        """
        Configura as tabelas no banco de dados, criando sequências e tabelas se não existirem.
        """
        logging.info("Setting up tables")
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

    logging.info("Tables set up successfully")

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
        logging.info("Operational metric inserted successfully")

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
        logging.info("ML metric inserted successfully")

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
        logging.info("Prediction inserted successfully")

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
        logging.info("Prediction updated successfully")

        # Após atualizar o valor real, dispare o cálculo das métricas
        self.calculate_and_store_metrics()

    def calculate_and_store_metrics(self):
        """
        Calcula as métricas com base nas previsões e nos valores reais e armazena no banco de dados.
        """
        # Recuperar todas as previsões que possuem valores reais e previstos
        predictions_data = self.con.execute(
            "SELECT predicted_value, actual_value FROM predictions WHERE actual_value IS NOT NULL"
        ).fetchall()

        true_values = [row[1] for row in predictions_data]
        predicted_values = [row[0] for row in predictions_data]

        # Calcular RMSE e MAE
        rmse = calculate_rmse(true_values, predicted_values)
        mae = calculate_mae(true_values, predicted_values)

        # Armazenar as métricas calculadas no banco de dados
        timestamp = datetime.datetime.now()
        self.insert_ml_metric(timestamp, rmse, mae)
        logging.info("Metrics calculated and stored successfully")

    def fetch_operational_metrics(self):
        """
        Busca todas as métricas operacionais do banco de dados.

        Returns:
        - List[Dict]: Uma lista de dicionários contendo as métricas operacionais.
        """
        metrics = self.con.execute("SELECT * FROM operational_metrics").fetchall()
        metrics_dicts = [
            dict(
                zip(
                    ("id", "timestamp", "method", "url", "response_status", "latency"),
                    metric,
                )
            )
            for metric in metrics
        ]
        logging.info("Operational metrics fetched successfully")
        return metrics_dicts

    def fetch_ml_metrics(self):
        """
        Busca todas as métricas de aprendizado de máquina do banco de dados.

        Returns:
        - List[Dict]: Uma lista de dicionários contendo as métricas de aprendizado de máquina.
        """
        metrics = self.con.execute("SELECT * FROM ml_metrics").fetchall()
        metrics_dicts = [
            dict(zip(("id", "timestamp", "rmse", "mae"), metric)) for metric in metrics
        ]
        logging.info("ML metrics fetched successfully")
        return metrics_dicts

    def fetch_predictions(self):
        """
        Busca todas as previsões do banco de dados.

        Returns:
        - List[Dict]: Uma lista de dicionários contendo as previsões.
        """
        predictions = self.con.execute("SELECT * FROM predictions").fetchall()
        predictions_dicts = [
            dict(
                zip(
                    (
                        "id",
                        "timestamp",
                        "model_type",
                        "input_data",
                        "predicted_value",
                        "actual_value",
                    ),
                    prediction,
                )
            )
            for prediction in predictions
        ]
        logging.info("Predictions fetched successfully")
        return predictions_dicts

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.con.close()
