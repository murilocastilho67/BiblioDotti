import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="db_biblioteca_dotti"
    )