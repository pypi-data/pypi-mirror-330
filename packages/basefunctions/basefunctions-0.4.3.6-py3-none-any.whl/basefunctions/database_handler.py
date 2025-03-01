"""
=============================================================================

  Licensed Materials, Property of Ralph Vogl, Munich

  Project : backtraderfunctions

  Copyright (c) by Ralph Vogl

  All rights reserved.

  Description:

  a simple database abstraction layer for SQLite, MySQL, and PostgreSQL

=============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import sqlite3
import psycopg2
import mysql.connector
from sqlalchemy import create_engine

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
class DataBaseHandler:
    """
    Abstract base class for all databases.

    Methods
    -------
    connect(parameters: dict):
        Establishes a connection to the database using a dictionary of parameters.

    close():
        Closes the connection to the database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.

    is_connected() -> bool:
        Checks if the connection to the database is active.

    check_if_table_exists(table_name: str) -> bool:
        Checks if the specified table exists in the database.

    create_database_handler(db_type: str) -> DataBaseHandler:
        Factory method that returns an instance of a specific database handler.
    """

    def connect(self, parameters: dict):
        """Establishes a connection to the database using a dictionary of parameters."""
        raise NotImplementedError

    def close(self):
        """Closes the connection to the database."""
        raise NotImplementedError

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        raise NotImplementedError

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        raise NotImplementedError

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        raise NotImplementedError

    def get_connection(self):
        """Returns the connection object for use with pandas."""
        raise NotImplementedError

    def begin_transaction(self):
        """Begins a transaction."""
        raise NotImplementedError

    def commit(self):
        """Commits the current transaction."""
        raise NotImplementedError

    def rollback(self):
        """Rolls back the current transaction."""
        raise NotImplementedError

    def is_connected(self) -> bool:
        """Checks if the connection to the database is active."""
        raise NotImplementedError

    def check_if_table_exists(self, table_name: str) -> bool:
        """Checks if the specified table exists in the database."""
        raise NotImplementedError

    def replace_sql_statement(self, sql_statement: str) -> str:
        """replace DDL specific instructions in sql statement"""
        # Definition des Primärschlüssels für verschiedene Datenbanksysteme
        primary_key_map = {
            "sqlite": "INTEGER PRIMARY KEY AUTOINCREMENT",  # SQLite
            "mysql": "SERIAL AUTO_INCREMENT PRIMARY KEY",  # MySQL
            "postgresql": "BIGSERIAL PRIMARY KEY",  # PostgreSQL
        }
        replacement = sql_statement.replace(
            "<PRIMARYKEY>", primary_key_map.get(self.db_type, "BIGSERIAL PRIMARY KEY")
        )
        return replacement

    @staticmethod
    def create_database_handler(db_type: str) -> "DataBaseHandler":
        """Factory method that returns an instance of a specific database handler."""
        if db_type.lower() == "sqlite3":
            return SQLiteDataBaseHandler()
        elif db_type.lower() == "mysql":
            return MySQLDataBaseHandler()
        elif db_type.lower() == "postgresql":
            return PostgreSQLDataBaseHandler()
        else:
            raise ValueError(
                f"Unsupported database type: {db_type}, "
                f"please choose from sqlite3, mysql or postgresql."
            )


class SQLiteDataBaseHandler(DataBaseHandler):
    """
    Implementation of the Database abstraction for SQLite.

    Methods
    -------
    connect(connection_string: str):
        Establishes a connection to the SQLite database.

    close():
        Closes the connection to the SQLite database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.

    is_connected() -> bool:
        Checks if the connection to the database is active.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.last_query_string = None
        self.db_type = "sqlite3"

    def connect(self, parameters: dict):
        """Establishes a connection to the SQLite database using a dictionary of parameters."""
        if "database" not in parameters:
            raise ValueError("Missing 'database' parameter.")
        self.connection = sqlite3.connect(parameters["database"])
        self.cursor = self.connection.cursor()

    def close(self):
        """Closes the connection to the SQLite database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.cursor = None
        self.connection = None

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        self.cursor.execute(self.replace_sql_statement(query), parameters)
        self.connection.commit()

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        if new_query or (query != self.last_query_string):
            self.cursor.execute(query, parameters)
            self.last_query_string = query
        columns = [desc[0] for desc in self.cursor.description]
        result = self.cursor.fetchone()
        return dict(zip(columns, result)) if result else None

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        self.cursor.execute(query, parameters)
        columns = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]

    def get_connection(self):
        """Returns the connection object for use with pandas."""
        return self.connection

    def begin_transaction(self):
        """Begins a transaction."""
        self.connection.execute("BEGIN")

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()

    def is_connected(self) -> bool:
        """Checks if the connection to the SQLite database is active."""
        return self.connection is not None

    def check_if_table_exists(self, table_name: str) -> bool:
        """Checks if the specified table exists in the SQLite database."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        self.cursor.execute(query, (table_name,))
        return self.cursor.fetchone() is not None


class MySQLDataBaseHandler(DataBaseHandler):
    """
    Implementation of the Database abstraction for MySQL.

    Methods
    -------
    connect(connection_string: dict):
        Establishes a connection to the MySQL database.

    close():
        Closes the connection to the MySQL database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.

    is_connected() -> bool:
        Checks if the connection to the database is active.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.last_query_string = None
        self.db_type = "mysql"

    def connect(self, parameters: dict):
        """Establishes a connection to the MySQL database using a dictionary of parameters."""
        mandatory_keys = ["user", "password", "host", "database"]
        for key in mandatory_keys:
            if key not in parameters:
                raise ValueError(f"Missing '{key}' parameter.")

        self.connection = mysql.connector.connect(
            user=parameters["user"],
            password=parameters["password"],
            host=parameters["host"],
            port=parameters.get("port", 3306),  # Default port is 3306
            database=parameters["database"],
        )
        self.cursor = self.connection.cursor()

    def close(self):
        """Closes the connection to the MySQL database."""
        if self.cursor:
            self.cursor.close()  # Cursor schließen
        if self.connection:
            self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        self.cursor.execute(self.replace_sql_statement(query), parameters)
        self.connection.commit()

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        if new_query or (query != self.last_query_string):
            self.cursor.execute(query, parameters)
            self.last_query_string = query
        return self.cursor.fetchone()

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def get_connection(self):
        """Returns the connection object for use with pandas."""
        return self.connection

    def begin_transaction(self):
        """Begins a transaction."""
        self.connection.start_transaction()

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()

    def is_connected(self) -> bool:
        """Checks if the connection to the MySQL database is active."""
        return self.connection is not None and self.connection.is_connected()

    def check_if_table_exists(self, table_name: str) -> bool:
        """Checks if the specified table exists in the MySQL database."""
        query = "SHOW TABLES LIKE %s;"
        self.cursor.execute(query, (table_name,))
        return self.cursor.fetchone() is not None


class PostgreSQLDataBaseHandler(DataBaseHandler):
    """
    Implementation of the Database abstraction for PostgreSQL.

    Methods
    -------
    connect(connection_string: str):
        Establishes a connection to the PostgreSQL database.

    close():
        Closes the connection to the PostgreSQL database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.

    is_connected() -> bool:
        Checks if the connection to the database is active.
    """

    def __init__(self):
        self.connection = None
        self.engine = None  # Add an engine variable
        self.cursor = None
        self.last_query_string = None
        self.db_type = "postgresql"

    def connect(self, parameters: dict):
        """Establishes a connection to the PostgreSQL database using a dictionary of parameters.

        It also creates a SQLAlchemy engine for additional usage.
        """
        mandatory_keys = ["user", "password", "host", "database"]
        for key in mandatory_keys:
            if key not in parameters:
                raise ValueError(f"Missing '{key}' parameter.")

        # Create a connection string for psycopg2
        self.connection = psycopg2.connect(
            user=parameters["user"],
            password=parameters["password"],
            host=parameters["host"],
            port=parameters.get("port", 5432),  # Default port is 5432
            database=parameters["database"],
        )
        self.cursor = self.connection.cursor()

        # Create SQLAlchemy engine
        connection_url = (
            f"postgresql+psycopg2://{parameters['user']}:"
            f"{parameters['password']}@"
            f"{parameters['host']}:{parameters.get('port', 5432)}/"
            f"{parameters['database']}"
        )
        self.engine = create_engine(connection_url)

    def close(self):
        """Closes the connection to the PostgreSQL database."""
        if self.cursor:
            self.cursor.close()  # Cursor schließen
        if self.connection:
            self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        self.cursor.execute(self.replace_sql_statement(query), parameters)
        self.connection.commit()

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        if new_query or (query != self.last_query_string):
            self.cursor.execute(query, parameters)
            self.last_query_string = query
        columns = [desc[0] for desc in self.cursor.description]
        result = self.cursor.fetchone()
        return dict(zip(columns, result)) if result else None

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        self.cursor.execute(query, parameters)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_connection(self):
        """Returns the SQLAlchemy engine for use with pandas."""
        return self.engine

    def begin_transaction(self):
        """Begins a transaction."""
        self.connection.autocommit = False

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()

    def is_connected(self) -> bool:
        """Checks if the connection to the PostgreSQL database is active."""
        return self.connection is not None and self.cursor is not None

    def check_if_table_exists(self, table_name: str) -> bool:
        """Checks if the specified table exists in the PostgreSQL database."""
        query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name=%s);"
        self.cursor.execute(query, (table_name,))
        return self.cursor.fetchone()[0]
