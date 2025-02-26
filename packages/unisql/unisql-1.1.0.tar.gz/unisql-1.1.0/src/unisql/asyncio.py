import aiosqlite
import asyncpg
import re
import typing as t

from .functions import contains_nested_sequence


class connect:
    """
    A class to manage connections and operations with SQLite and PostgreSQL databases.

    Attributes
    ----------
    connection
        The database connection object.

    cursor
        The database cursor object (for SQLite).

    engine
        A string indicating the type of the database engine ("sqlite" or "postgresql").

    Methods
    -------
    sqlite
        Asynchronously establishes a connection to an SQLite database.

    postgresql
        Asynchronously establishes a connection to a PostgreSQL database.

    fetch
        Asynchronously fetches data from the database.

    execute
        Asynchronously executes a query in the database.

    close
        Asynchronously closes the database connection.
    """

    def __init__(self, connection, cursor, engine):
        """
        Initializes the connect class with the given database connection, cursor, and engine type.

        Parameters
        ----------
        connection : object
            The database connection object.

        cursor : object
            The database cursor object (for SQLite).

        engine : str
            A string indicating the type of the database engine ("sqlite" or "postgresql").
        """
        self.connection = connection
        self.cursor = cursor
        self.engine = engine

    @classmethod
    async def sqlite(cls, filename: str) -> "connect":
        """
        Asynchronously establishes a connection to an SQLite database.

        Parameters
        ----------
        filename : str
            The name of the SQLite database file.

        Returns
        -------
        connect
            An instance of the connect class configured for SQLite.
        """
        connection = await aiosqlite.connect(filename)
        connection.row_factory = aiosqlite.Row
        cursor = await connection.cursor()
        return cls(connection, cursor, "sqlite")

    @classmethod
    async def postgresql(
        cls,
        database: str,
        host: str,
        user: str,
        password: str,
        port: int
    ) -> "connect":
        """
        Asynchronously establishes a connection to a PostgreSQL database.

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
        connection = await asyncpg.connect(
            database=database,
            host=host,
            user=user,
            password=password,
            port=port,
        )
        return cls(connection, None, "postgresql")

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
        if self.engine == "postgresql":
            placeholder = ",".join(["${}".format(i+1) for i in range(s.count("?"))])
            s = re.sub(r"\?", "{}", s).format(*placeholder.split(","))
        return s

    async def fetch(
        self,
        query: str,
        value: t.Optional[t.Union[t.Iterable[t.Any], t.Iterable[t.Iterable[t.Any]]]] = None,
        multiple: t.Optional[bool] = True
    ) -> t.Union[t.List[t.Dict], t.Dict, None]:
        """
        Asynchronously fetches data from the database.

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
        if self.engine == "sqlite":
            await self.cursor.execute(query, value)
            if multiple:
                res = await self.cursor.fetchall()
                if res:
                    return [dict(r) for r in res]
            else:
                res = await self.cursor.fetchone()
                if res:
                    return dict(res)
        elif self.engine == "postgresql":
            if multiple:
                if value:
                    res = await self.connection.fetch(query, *value)
                else:
                    res = await self.connection.fetch(query)
                return [dict(r) for r in res]
            else:
                if value:
                    res = await self.connection.fetchrow(query, *value)
                else:
                    res = await self.connection.fetchrow(query)
                return dict(res)

    async def execute(
        self,
        query: str,
        value: t.Union[t.Iterable[t.Any], t.Iterable[t.Iterable[t.Any]]] = None
    ) -> None:
        """
        Asynchronously executes a query in the database.

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
        if self.engine == "sqlite":
            if value:
                if contains_nested_sequence(value):
                    await self.cursor.executemany(query, value)
                else:
                    await self.cursor.execute(query, value)
            else:
                await self.cursor.execute(query)
            await self.connection.commit()
        elif self.engine == "postgresql":
            if value:
                if contains_nested_sequence(value):
                    await self.connection.executemany(query, value)
                else:
                    await self.connection.execute(query, *value)
            else:
                await self.connection.execute(query)

    async def close(self) -> None:
        """
        Asynchronously closes the database connection.

        Returns
        -------
        None
        """
        await self.connection.close()
