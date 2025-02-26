# UniSQL: SQL Database Wrapper

UniSQL is a software package that offers a unified interface for connecting to and interacting with various database engines, including SQLite, MySQL, and PostgreSQL. This package simplifies database management by abstracting the underlying complexities of each database engine, providing a consistent and user-friendly API for developers.

## Installation

```
Dependencies:

- Python 3.8, 3.9, 3.11, 3.12, 3.13

Installation:

$ pip install unisql
```

## Synchronous Connections

For synchronous connections, use the following code:

```python
from unisql import connect

# SQLite
db = connect.sqlite("database.db")

# MySQL
db = connect.mysql(database="mydatabase", host="localhost", user="myuser", password="mypassword", port=3306)

# PostgreSQL
db = connect.postgresql(database="mydatabase", host="localhost", user="myuser", password="mypassword", port=5432)
```

## Asynchronous Connections (with asyncio)

For asynchronous connections using asyncio, use the following code:

```python
from unisql.asyncio import connect

# SQLite
db = await connect.sqlite("database.db")

# PostgreSQL
db = await connect.postgresql(database="mydatabase", host="localhost", user="myuser", password="mypassword", port=5432)
```

> [!IMPORTANT]
> Asynchronous connections are currently not supported for MySQL in this package.

## Executing Queries

After establishing a connection, you can execute queries using the query and value properties, and then call the fetch or execute methods.

```python
# Set the query and values
query = "SELECT * FROM users WHERE name = ? AND email = ?;"
value = ("John Doe", "john@example.com")

# Fetch a single row
result = db.fetch(query, value, multiple=False)

# Fetch all rows
results = db.fetch(query, value, multiple=True)

# Execute an INSERT or UPDATE query at once
query = "INSERT INTO users (name, email) VALUES (?, ?);"
value = ("John Doe", "john@example.com")
db.execute(query, value)

# Execute an INSERT or UPDATE query at many
value = [("Sam Smith", "sam@example.com"), ("Adam Page", "adam@example.com")]
db.execute(query, value)
```

To close the connection:

```python
db.close()
```
