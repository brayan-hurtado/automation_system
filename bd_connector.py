import pymysql
import pymysql.cursors

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='D3SK0001110100',
        database='db_automationsys'
    )