import asyncio

from unisql.asyncio import connect

from const import POSTGRESQL


def test_async_sqlite():

    async def main():

        db = await connect.sqlite(":memory:")

        query = """
            CREATE TABLE "user" (
                "id"	INTEGER,
                "name"	TEXT,
                "age"	INTEGER,
                PRIMARY KEY("id")
            );
        """
        await db.execute(query)

        query = """
            INSERT OR IGNORE INTO
                user (id, name, age)
            VALUES
                (?, ?, ?)
            ;
        """
        value = [
            (1, "John", 53),
            (2, "Mark", 23),
            (3, "Luke", 25)
        ]
        await db.execute(query, value)

        value = (4, "Jude", 45)
        await db.execute(query, value)

        query = "SELECT * FROM user;"
        users = await db.fetch(query)

        assert len(users) == 4

        query = "SELECT * FROM user WHERE id = ?;"
        value = (3,)
        user = await db.fetch(query, value, multiple=False)

        assert user["name"] == "Luke"
        assert user["age"] == 25

        await db.close()

    asyncio.run(main())


def test_async_postgresql():

    async def main():

        db = await connect.postgresql(**POSTGRESQL)

        query = """
            CREATE TABLE public."user" (
                id integer NOT NULL,
                name character varying(255),
                age integer
            );
        """
        await db.execute(query)

        query = """
            INSERT INTO
                public."user" (id, name, age)
            VALUES
                (?, ?, ?)
            ON CONFLICT DO NOTHING
            ;
        """
        value = [
            (1, "John", 53),
            (2, "Mark", 23),
            (3, "Luke", 25)
        ]
        await db.execute(query, value)

        value = (4, "Jude", 45)
        await db.execute(query, value)

        query = "SELECT * FROM public.user;"
        users = await db.fetch(query)

        assert len(users) == 4

        query = "SELECT * FROM public.user WHERE id = ?;"
        value = (3,)
        user = await db.fetch(query, value, multiple=False)

        assert user["name"] == "Luke"
        assert user["age"] == 25

        query = """
            DROP TABLE public."user";
        """
        await db.execute(query)

        await db.close()

    asyncio.run(main())
