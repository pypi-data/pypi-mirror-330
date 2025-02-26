from unisql import connect

from const import POSTGRESQL


def test_sqlite():

    db = connect.sqlite(":memory:")

    query = """
        CREATE TABLE "user" (
            "id"	INTEGER,
            "name"	TEXT,
            "age"	INTEGER,
            PRIMARY KEY("id")
        );
    """
    db.execute(query)

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
    db.execute(query, value)

    value = (4, "Jude", 45)
    db.execute(query, value)

    query = "SELECT * FROM user;"
    users = db.fetch(query)

    assert len(users) == 4

    query = "SELECT * FROM user WHERE id = ?;"
    value = (3,)
    user = db.fetch(query, value, multiple=False)

    assert user["name"] == "Luke"
    assert user["age"] == 25

    db.close()


def test_postgresql():

    db = connect.postgresql(**POSTGRESQL)

    query = """
        CREATE TABLE public."user" (
            id integer NOT NULL,
            name character varying(255),
            age integer
        );
    """
    db.execute(query)

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
    db.execute(query, value)

    value = (4, "Jude", 45)
    db.execute(query, value)

    query = "SELECT * FROM public.user;"
    users = db.fetch(query)

    assert len(users) == 4

    query = "SELECT * FROM public.user WHERE id = ?;"
    value = (3,)
    user = db.fetch(query, value, multiple=False)

    assert user["name"] == "Luke"
    assert user["age"] == 25

    query = """
        DROP TABLE public."user";
    """
    db.execute(query)

    db.close()
