import psycopg2
import psycopg2.extras
import pymysql
import pymysql.cursors
import sqlite3
import typing as t

from .functions import contains_nested_sequence


class connect:
    """
    A class to manage connections and operations with SQLite, MySQL, and PostgreSQL databases.

    Attributes
    ----------
    connection
        The database connection object.

    cursor
        The database cursor object.

    engine
        A string indicating the type of the database engine ("sqlite", "mysql", or "postgresql").

    Methods
    -------
    sqlite
        Establishes a connection to an SQLite database.

    mysql
        Establishes a connection to a MySQL database.

    postgresql
        Establishes a connection to a PostgreSQL database.

    fetch
        Fetches data from the database.

    execute
        Executes a query in the database.

    close
        Closes the database connection.
    """

    def __init__(self, connection, cursor, engine):
        """
        Initializes the connect class with the given database connection, cursor, and engine type.

        Parameters
        ----------
        connection : object
            The database connection object.

        cursor : object
            The database cursor object.

        engine : str
            A string indicating the type of the database engine ("sqlite", "mysql", or "postgresql").
        """
        self.connection = connection
        self.cursor = cursor
        self.engine = engine

    @classmethod
    def sqlite(cls, database: str) -> "connect":
        """
        Establishes a connection to an SQLite database.

        Parameters
        ----------
        database : str
            The name of the SQLite database file.

        Returns
        -------
        connect
            An instance of the connect class configured for SQLite.
        """
        connection = sqlite3.connect(database)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return cls(connection, cursor, "sqlite")

    @classmethod
    def mysql(
        cls,
        database: str,
        host: str,
        user: str,
        password: str,
        port: int
    ) -> "connect":
        """
        Establishes a connection to a MySQL database.

        Parameters
        ----------
        database : str
            The name of the MySQL database.

        host : str
            The host of the MySQL server.

        user : str
            The user for the MySQL database.

        password : str
            The password for the MySQL user.

        port : int
            The port number of the MySQL server.

        Returns
        -------
        connect
            An instance of the connect class configured for MySQL.
        """
        connection = pymysql.connect(
            database=database,
            host=host,
            user=user,
            password=password,
            port=port,
            cursorclass=pymysql.cursors.DictCursor,
        )
        cursor = connection.cursor()
        return cls(connection, cursor, "mysql")

    @classmethod
    def postgresql(
        cls,
        database: str,
        host: str,
        user: str,
        password: str,
        port: int
    ) -> "connect":
        """
        Establishes a connection to a PostgreSQL database.

        Parameters
        ----------
        database : str
            The name of the PostgreSQL database.

        host : str
            The host of the PostgreSQL server.

        user : str
            The user for the PostgreSQL database.

        password : str
            The password for the PostgreSQL user.

        port : int
            The port number of the PostgreSQL server.

        Returns
        -------
        connect
            An instance of the connect class configured for PostgreSQL.
        """
        connection = psycopg2.connect(
            database=database,
            host=host,
            user=user,
            password=password,
            port=port,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        cursor = connection.cursor()
        return cls(connection, cursor, "postgresql")

    def __query(self, s: str) -> str:
        """
        Converts a query string to a database-specific format.

        Parameters
        ----------
        s : str
            The SQL query string.

        Returns
        -------
        str
            The database-specific SQL query string.
        """
        if self.engine in ("mysql", "postgresql"):
            s = s.replace("?", "%s")
        return s

    def fetch(
        self,
        query: str,
        value: t.Optional[t.Union[t.Iterable[t.Any], t.Iterable[t.Iterable[t.Any]]]] = None,
        multiple: t.Optional[bool] = True
    ) -> t.Union[t.List[t.Dict], t.Dict, None]:
        """
        Fetches data from the database.

        Parameters
        ----------
        query : str
            The SQL query string.

        value : Optional[Union[Iterable[Any], Iterable[Iterable[Any]]]], optional
            The values to substitute in the query. Defaults to None.

        multiple : Optional[bool], optional
            Whether to fetch multiple rows. Defaults to True.

        Returns
        -------
        Union[List[Dict], Dict, None]
            The fetched data in dictionary form, or None if no data is found.
        """
        query = self.__query(query)
        if value:
            self.cursor.execute(query, value)
        else:
            self.cursor.execute(query)
        if multiple:
            res = self.cursor.fetchall()
            if res:
                return [dict(r) for r in res]
        else:
            res = self.cursor.fetchone()
            if res:
                return dict(res)

    def execute(
        self,
        query: str,
        value: t.Union[t.Iterable[t.Any], t.Iterable[t.Iterable[t.Any]]] = None
    ) -> None:
        """
        Executes a query in the database.

        Parameters
        ----------
        query : str
            The SQL query string.

        value : Union[Iterable[Any], Iterable[Iterable[Any]]], optional
            The values to substitute in the query. Defaults to None.

        Returns
        -------
        None
        """
        query = self.__query(query)
        if value:
            if contains_nested_sequence(value):
                self.cursor.executemany(query, value)
            else:
                self.cursor.execute(query, value)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def close(self) -> None:
        """
        Closes the database connection.

        Returns
        -------
        None
        """
        self.connection.close()
