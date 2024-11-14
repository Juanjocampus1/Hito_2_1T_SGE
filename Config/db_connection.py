import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="curso",
        database="encuestas_DB"
    )