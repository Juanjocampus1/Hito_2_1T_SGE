import mysql

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="curso",
        database="encuestas_DB"
    )