import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import sqlite3
import pandas as pd


class SQLiteConnection(ExperimentalBaseConnection[sqlite3.Connection]):
    """
    A custom Streamlit connection class for interacting with SQLite3 databases.

    This class extends Streamlit's ExperimentalBaseConnection and provides methods for
    connecting to a SQLite3 database, executing SQL queries, and retrieving results as
    Pandas DataFrames. It does not rely on secrets for local database connections.
    """

    def __init__(self, database: str, **kwargs) -> None:
        """
        Initializes the SQLiteConnection.

        Args:
            database: Path to the SQLite3 database file.
            **kwargs: Additional arguments for the connection.
        """
        self.database = database
        super().__init__(**kwargs)

    def _connect(self, **kwargs) -> sqlite3.Connection:
        """
        Connects to the SQLite3 database.

        Args:
            **kwargs: Additional arguments for the connection.

        Returns:
            SQLite3 connection object.
        """
        return sqlite3.connect(database=self.database, **kwargs)

    def cursor(self) -> sqlite3.Cursor:
        """
        Returns a cursor for the connection.

        Returns:
            SQLite3 cursor object.
        """
        return self._instance.cursor()

    def execute(self, query: str, *args) -> None:
        """
        Executes an SQL query on the database.

        Args:
            query: SQL query to execute.
            params: Parameters for the query.
        """
        cursor = self.cursor()

        cursor.execute(query, *args)
        self._instance.commit()

    def query(self, query: str, ttl: int = 3600) -> pd.DataFrame:
        """
        Executes an SQL query on the database.

        Args:
            query: SQL query to execute.
            ttl: Cache time-to-live (in seconds).
            **kwargs: Additional arguments for the query.

        Returns:
            Pandas DataFrame with the query results.
        """

        def _query(query: str) -> pd.DataFrame:
            cursor = self.cursor()
            query_result = cursor.execute(query)
            return query_result.fetchall()

        return _query(query)


@st.cache_resource
def get_database_session():
    # Database connection
    conn = st.connection(
        "sqlite",
        type=SQLiteConnection,
        # Pass the database path directly
        database="chat_history.db",
        check_same_thread=False,
    )

    return conn
