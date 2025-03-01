import sqlite3
import mysql.connector
from typing import Dict, Optional, Union, Any, List, Tuple


class Chimaera:
    """
    The main DbChimaera class - a database adapter that automatically handles
    syntax differences between multiple database engines.

    This class provides a unified interface for working with SQLite and MySQL,
    adapting query placeholders and parameter styles automatically.
    """

    def __init__(self, connection_details: Optional[Dict[str, Any]] = None):
        """
        Initialize a new DbChimaera instance.

        Args:
            connection_details: Optional dictionary with database connection parameters.
                                If None or empty, connects to a local SQLite database.

                                For MySQL, should contain:
                                - host: MySQL server hostname or IP
                                - user: Username for authentication
                                - password: Password for authentication
                                - database: Database name to connect to
                                - port: (optional) MySQL server port, defaults to 3306
        """
        self.connection = self._connect_to_database(connection_details)
        # Determine database type
        self.is_sqlite = isinstance(self.connection, sqlite3.Connection)
        self.is_mysql = isinstance(self.connection, mysql.connector.connection.MySQLConnection)

    def _connect_to_database(self, connection_details: Dict[str, Any] = None) -> Union[
        sqlite3.Connection, mysql.connector.connection.MySQLConnection]:
        """
        Establishes a database connection based on the provided connection details.

        Args:
            connection_details: Dictionary with database connection parameters.
                                If None or empty, connects to SQLite.

        Returns:
            Database connection object (SQLite or MySQL)

        Raises:
            Exception: If connection fails
        """
        try:
            if not connection_details:
                # Use SQLite as default local database
                print("Connecting to local SQLite database...")
                conn = sqlite3.connect("database.db")
                conn.row_factory = sqlite3.Row  # Access query results by column name
                return conn
            else:
                # Use MySQL with provided parameters
                print("Connecting to remote MySQL database...")
                conn = mysql.connector.connect(
                    host=connection_details.get("host", "localhost"),
                    user=connection_details.get("user", ""),
                    password=connection_details.get("password", ""),
                    database=connection_details.get("database", ""),
                    port=connection_details.get("port", 3306)
                )
                return conn
        except Exception as e:
            raise Exception(f"Database connection error: {str(e)}")

    def adapt_query(self, query: str) -> str:
        """
        Adapts query placeholder syntax based on the current database type.

        Args:
            query: SQL query with placeholders in %s format

        Returns:
            Query with adapted placeholder syntax for the current database
        """
        if self.is_sqlite:
            # Convert %s to ? for SQLite
            return query.replace("%s", "?")
        elif self.is_mysql:
            # Keep %s for MySQL
            return query
        else:
            raise Exception("Unsupported database type")

    def execute_query(self, query: str, params: Union[Tuple, List, Dict] = None):
        """
        Executes an SQL query on the database, automatically adapting syntax.

        Args:
            query: SQL query with placeholders
            params: Parameters to pass to the query

        Returns:
            Query execution result
        """
        adapted_query = self.adapt_query(query)
        cursor = self.connection.cursor()

        try:
            if params:
                cursor.execute(adapted_query, params)
            else:
                cursor.execute(adapted_query)

            # For SELECT queries, return results
            if adapted_query.strip().upper().startswith("SELECT"):
                if self.is_sqlite:
                    return cursor.fetchall()
                else:
                    return cursor.fetchall()

            # For modification queries, commit and return affected row count
            else:
                self.connection.commit()
                return cursor.rowcount

        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Query execution error: {str(e)}")
        finally:
            cursor.close()

    def insert_data(self, table: str, data: Dict[str, Any]):
        """
        Inserts data into a table.

        Args:
            table: Table name
            data: Dictionary with data to insert (key=column_name, value=value)

        Returns:
            ID of the last inserted record
        """
        columns = ", ".join(data.keys())

        if self.is_sqlite:
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            params = tuple(data.values())
        else:  # MySQL
            placeholders = ", ".join(["%s"] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            params = tuple(data.values())

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()

            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Data insertion error: {str(e)}")
        finally:
            cursor.close()

    def query_with_params(self, query: str, params: Union[Tuple, List, Dict] = None):
        """
        Executes a parameterized query using correct syntax for each database.
        This method is a more explicit alias for execute_query.

        Args:
            query: SQL query with appropriate placeholders.
                   Use %s for both SQLite and MySQL (will be automatically adapted).
            params: Parameters to pass to the query

        Returns:
            Query execution result
        """
        return self.execute_query(query, params)

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()