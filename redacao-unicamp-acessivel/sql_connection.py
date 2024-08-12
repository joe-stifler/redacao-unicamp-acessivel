import streamlit as st  # Importa o módulo Streamlit para a interface web
from streamlit.connections import ExperimentalBaseConnection  # Importa a classe base para conexões personalizadas do Streamlit
import sqlite3  # Importa o módulo SQLite3 para interagir com bancos de dados SQLite
import pandas as pd  # Importa o módulo Pandas para trabalhar com DataFrames

# Define a classe SQLiteConnection para interagir com bancos de dados SQLite
class SQLiteConnection(ExperimentalBaseConnection[sqlite3.Connection]):
    """
    Classe de conexão personalizada do Streamlit para interagir com bancos de dados SQLite3.

    Esta classe estende a classe ExperimentalBaseConnection do Streamlit e fornece métodos para
    conectar a um banco de dados SQLite3, executar consultas SQL e recuperar resultados como
    DataFrames do Pandas. Ela não depende de segredos para conexões com bancos de dados locais.
    """

    def __init__(self, database: str, **kwargs) -> None:
        """
        Inicializa a classe SQLiteConnection.

        Args:
            database (str): Caminho para o arquivo do banco de dados SQLite3.
            **kwargs: Argumentos adicionais para a conexão.
        """
        self.database = database  # Armazena o caminho do banco de dados
        super().__init__(**kwargs)  # Chama o construtor da classe base

    def _connect(self, **kwargs) -> sqlite3.Connection:
        """
        Conecta ao banco de dados SQLite3.

        Args:
            **kwargs: Argumentos adicionais para a conexão.

        Returns:
            sqlite3.Connection: Objeto de conexão SQLite3.
        """
        # Conecta ao banco de dados SQLite3 usando o caminho do arquivo e os argumentos adicionais
        return sqlite3.connect(database=self.database, **kwargs)

    def cursor(self) -> sqlite3.Cursor:
        """
        Retorna um cursor para a conexão.

        Returns:
            sqlite3.Cursor: Objeto de cursor SQLite3.
        """
        return self._instance.cursor()  # Retorna o cursor da instância da conexão

    def execute(self, query: str, *args) -> None:
        """
        Executa uma consulta SQL no banco de dados.

        Args:
            query (str): Consulta SQL a ser executada.
            *args: Parâmetros para a consulta.
        """
        cursor = self.cursor()  # Obtem um cursor para a conexão

        cursor.execute(query, *args)  # Executa a consulta com os parâmetros fornecidos
        self._instance.commit()  # Confirma a transação no banco de dados

    def query(self, query: str, ttl: int = 3600) -> pd.DataFrame:
        """
        Executa uma consulta SQL no banco de dados e retorna os resultados como um DataFrame do Pandas.

        Args:
            query (str): Consulta SQL a ser executada.
            ttl (int, optional): Tempo de vida do cache (em segundos). Padrão: 3600 (1 hora).
            **kwargs: Argumentos adicionais para a consulta.

        Returns:
            pd.DataFrame: DataFrame do Pandas com os resultados da consulta.
        """

        # Função interna para executar a consulta e retornar os resultados
        def _query(query: str) -> pd.DataFrame:
            cursor = self.cursor()  # Obtem um cursor para a conexão
            query_result = cursor.execute(query)  # Executa a consulta
            return query_result.fetchall()  # Retorna os resultados como uma lista de tuplas

        # Retorna os resultados da consulta como um DataFrame do Pandas
        return _query(query)

# Define uma função para obter a sessão do banco de dados, usando o cache do Streamlit
@st.cache_resource
def get_database_session():
    """
    Obtem a sessão do banco de dados SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexão SQLite3.
    """
    # Cria a conexão com o banco de dados
    conn = st.connection(
        "sqlite",  # Nome da conexão
        type=SQLiteConnection,  # Classe de conexão personalizada
        # Passa o caminho para o banco de dados diretamente
        database="chat_history.db",
        check_same_thread=False,  # Desabilita a verificação de thread para conexões locais
    )

    # Retorna a conexão com o banco de dados
    return conn
