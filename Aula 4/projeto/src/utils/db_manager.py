import duckdb


class DBManager:
    def __init__(self):
        self.con = duckdb.connect(database=":memory:", read_only=False)

    def setup_tables(self):
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS operational_metrics (
                id INTEGER PRIMARY KEY,
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
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                rmse FLOAT,
                mae FLOAT
            )
        """
        )

    def insert_operational_metric(
        self, timestamp, method, url, response_status, latency
    ):
        self.con.execute(
            "INSERT INTO operational_metrics (timestamp, method, url, response_status, latency) VALUES (?, ?, ?, ?, ?)",
            (timestamp, method, url, response_status, latency),
        )

    def insert_ml_metric(self, timestamp, rmse, mae):
        self.con.execute(
            "INSERT INTO ml_metrics (timestamp, rmse, mae) VALUES (?, ?, ?)",
            (timestamp, rmse, mae),
        )

    def fetch_operational_metrics(self):
        return self.con.execute("SELECT * FROM operational_metrics").fetchall()

    def fetch_ml_metrics(self):
        return self.con.execute("SELECT * FROM ml_metrics").fetchall()

    def close(self):
        self.con.close()
