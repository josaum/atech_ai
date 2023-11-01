import duckdb
import configparser
import os

# Determine the location of the config.ini relative to the project root
config_path = os.path.join("src", "data", "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

# Extract configuration details
DATABASE_PATH = config["DEFAULT"]["DATABASE_PATH"]
READ_ONLY = config.getboolean("DEFAULT", "READ_ONLY")
INPUT_PATH = os.path.abspath(os.path.join("data", config["DEFAULT"]["INPUT_PATH"]))
OUTPUT_PATH = os.path.abspath(os.path.join("data", config["DEFAULT"]["OUTPUT_PATH"]))
DROP_COLUMNS = config["DEFAULT"]["DROP_COLUMNS"].split(",")
NUMERIC_COLUMNS = config["DEFAULT"]["NUMERIC_COLUMNS"].split(",")
DATE_COLUMNS = config["DEFAULT"]["DATE_COLUMNS"].split(",")
DATE_FORMAT = config["DEFAULT"]["DATE_FORMAT"]
NEW_DATE_COLUMN = config["DEFAULT"]["NEW_DATE_COLUMN"]
DATE_CONCAT_FORMAT = config["DEFAULT"]["DATE_CONCAT_FORMAT"]
REPLACE_COMMA_WITH_DOT_COLUMNS = config["DEFAULT"][
    "REPLACE_COMMA_WITH_DOT_COLUMNS"
].split(",")
SET_EMPTY_TO_NULL_COLUMNS = config["DEFAULT"]["SET_EMPTY_TO_NULL_COLUMNS"].split(",")


def connect_to_db():
    """Connect to DuckDB and return the connection."""
    return duckdb.connect(database=DATABASE_PATH, read_only=READ_ONLY)


def load_data_into_db(con, table_name, file_path):
    """Load data from a Parquet file into a DuckDB table."""
    con.execute(
        f"CREATE TABLE {table_name} AS SELECT * FROM parquet_scan('{file_path}')"
    )


def process_data(con):
    """Process data with the required transformations."""
    for column in DROP_COLUMNS:
        con.execute(f"ALTER TABLE raw_dataset DROP COLUMN {column}")

    # Replace comma with a decimal point for specified columns
    for column in REPLACE_COMMA_WITH_DOT_COLUMNS:
        con.execute(f"UPDATE raw_dataset SET {column} = REPLACE({column}, ',', '.')")

    # Set empty strings to NULL for specified columns
    for column in SET_EMPTY_TO_NULL_COLUMNS:
        con.execute(
            f"UPDATE raw_dataset SET {column} = NULL WHERE LENGTH(TRIM({column})) = 0"
        )

    for column in NUMERIC_COLUMNS:
        # Use TRY_CAST to attempt conversion, ignoring nulls
        con.execute(
            f"UPDATE raw_dataset SET {column} = TRY_CAST({column} AS REAL) WHERE {column} IS NOT NULL"
        )

    # Convert specified columns and create a new date column
    con.execute(f"ALTER TABLE raw_dataset ADD COLUMN {NEW_DATE_COLUMN} DATE")
    for column in DATE_COLUMNS:
        con.execute(f"UPDATE raw_dataset SET {column} = CAST({column} AS VARCHAR)")
    con.execute(
        f"UPDATE raw_dataset SET {NEW_DATE_COLUMN} = CAST({DATE_COLUMNS[0]} || '-' || LPAD({DATE_COLUMNS[1]}, 2, '0') || '{DATE_CONCAT_FORMAT}' AS DATE)"
    )


def save_processed_data(con, table_name, output_path):
    """Save the processed data to a Parquet file."""
    con.execute(f"COPY {table_name} TO '{output_path}' WITH (FORMAT 'PARQUET')")


def main():
    """Main function to handle data processing."""
    con = connect_to_db()
    load_data_into_db(con, "raw_dataset", INPUT_PATH)  # E/L
    process_data(con)  # T
    save_processed_data(con, "raw_dataset", OUTPUT_PATH)
    con.close()


if __name__ == "__main__":
    main()
