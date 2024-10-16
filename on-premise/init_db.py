import psycopg2 #pip install psycopg2 psycopg-binary
from psycopg2 import sql

dbname = 'postgres'
user = 'postgres'
password = 'example'
host = 'localhost'
port = '5432'

new_dbname = 'rag-sample-onpremise'

# Connect to the PostgreSQL server
connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

connection.autocommit = True

try:
    cursor = connection.cursor()

    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [new_dbname])

    exists = cursor.fetchone()

    if not exists:
        # Create the new database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_dbname)))
        print(f"Database {new_dbname} created successfully.")
    
    connection.close()
    connection = psycopg2.connect(dbname=new_dbname, user=user, password=password, host=host, port=port)
    cursor = connection.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    print(f"Vector plugin enabled successfully on database {new_dbname}.")
finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()