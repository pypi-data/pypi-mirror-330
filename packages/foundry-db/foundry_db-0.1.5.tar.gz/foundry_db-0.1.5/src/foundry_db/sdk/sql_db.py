import logging
from tqdm import tqdm
import psycopg2
from psycopg2.extras import execute_values
import numpy as np 

from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
from pathlib import Path

# Configure logging as needed (this is just a basic config)
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class SQLDatabase:

    @staticmethod
    def get_db_credentials():
        """
        Fetch PostgreSQL database credentials from the configuration file of the kedro project.
        Uses `OmegaConfigLoader` to load credentials stored under `credentials.postgres`.
        Returns:
            dict: A dictionary with the database connection details (e.g., host, port, user, password, dbname).
        """
        conf_path = str(Path(settings.CONF_SOURCE))
        conf_loader = OmegaConfigLoader(conf_source=conf_path)
        db_credentials = conf_loader["credentials"]["postgres"]
        return db_credentials

    @staticmethod
    def clean_rows(rows):
        rows = [
            tuple(int(x) if isinstance(x, np.integer) else x for x in row[:4])
            for row in rows
        ]
        return rows

    def __init__(self, autocommit=True):
        self._credentials = self.get_db_credentials()["con"]
        self.connection = None
        self.autocommit = autocommit

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(self._credentials)
            self.connection.autocommit = self.autocommit

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        elif not self.autocommit:
            self.connection.commit()
        self.close()

    def execute_query(self, query: str, params: tuple = None, fetchall: bool = False, fetchone: bool = False, commit: bool = False):
        if fetchall and fetchone:
            raise ValueError("Both fetchall and fetchone cannot be True")
        if not self.connection:
            self.connect()
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall() if fetchall else cur.fetchone() if fetchone else None
            if commit and self.autocommit:
                self.connection.commit()
            return result
        except Exception as e:
            error_msg = f"Error executing query: {query}. Parameters: {params}. Exception: {e}"
            logging.error(error_msg)
            raise Exception(error_msg) from e

    def execute_multiple_queries(self, queries: list | str, params: list = None, fetchrows: bool = False, commit: bool = False):
        params = self.clean_rows(params)
        if not self.connection:
            self.connect()
        results = []
        try:
            with self.connection.cursor() as cur:
                if fetchrows:
                    if isinstance(queries, str):
                        queries = [queries] * len(params)
                    for query, par in tqdm(zip(queries, params), total=len(params), desc="Executing queries"):
                        cur.execute(query, par)
                        results.append(cur.fetchone())
                else:
                    if not isinstance(queries, str):
                        raise ValueError("For batch execution use a single query with multiple params (set fetchrows=True otherwise)")
                    cur.executemany(queries, tqdm(params, desc="Executing batch queries"))
            if commit and self.autocommit:
                self.connection.commit()
            return results if fetchrows else None
        except Exception as e:
            query_info = queries if isinstance(queries, str) else "Multiple queries"
            error_msg = f"Error executing multiple queries. Query: {query_info}. Parameters: {params}. Exception: {e}"
            logging.error(error_msg)
            raise Exception(error_msg) from e

    def fetch_ids_bulk(self, table_name: str, id_column, column_names: list, rows: list[tuple]) -> list:
        """
        Retrieve IDs in one bulk query using the VALUES construct.
        'id_column' can be a string or a list/tuple of column names.
        """
        if not rows:
            return []
        
        rows = self.clean_rows(rows)
        columns_str = ", ".join(column_names)
        join_clause = " AND ".join([f"t.{col} = v.{col}" for col in column_names])
        
        # Build the SELECT part based on whether id_column is a single column or multiple.
        if isinstance(id_column, (list, tuple)):
            id_columns_str = ", ".join([f"t.{col}" for col in id_column])
        else:
            id_columns_str = f"t.{id_column}"
            
        query = f"""
            SELECT {id_columns_str}
            FROM {table_name} t
            JOIN (
                VALUES %s
            ) AS v({columns_str})
            ON {join_clause}
        """
        all_ids = []
        chunk_size = 100
        if not self.connection:
            self.connect()
        try:
            with self.connection.cursor() as cur:
                for i in tqdm(range(0, len(rows), chunk_size), desc="Fetching IDs", unit="chunk"):
                    chunk = rows[i:i + chunk_size]
                    execute_values(cur, query, chunk, page_size=len(chunk))
                    results = cur.fetchall()
                    if isinstance(id_column, (list, tuple)):
                        for row in results:
                            all_ids.append(tuple(int(x) for x in row))
                    else:
                        all_ids.extend(int(row[0]) for row in results)
            return all_ids
        except Exception as e:
            error_msg = f"Error fetching IDs in bulk. Query: {query}. Last chunk processed: {chunk}. Exception: {e}"
            logging.error(error_msg)
            raise Exception(error_msg) from e
