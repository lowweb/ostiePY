from mysql.connector import MySQLConnection, Error
from db_config import read_db_config

def sql_request (query):
    """
    input: query - запрос
    output: result - возвращеает информацию по запросу с ключем по названию поля в таблице
    """
    result=[]
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
    except Error as e:

        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

