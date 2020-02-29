from mysql.connector import MySQLConnection, Error
from db_config import read_db_config

def insert_music(data_array):
    """
    input - множество групп/исполнителей
    Перед началом вставки чистим таблицу
    """
    query = "INSERT INTO artists(id,nconst,fullname,proffesion,titles) VALUES(%s,%s,%s,%s,%s)"
    del_query = "DELETE FROM music"
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(del_query)
        conn.commit()
        print('delete music')
        for row in data_array:
            # print(row)
            cursor.execute(query, row)
            conn.commit()
        # cursor.executemany(query, data_array)
        # conn.commit()
        print('music inserted')
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

# def main():
#     array = [{1, 'nm0000001','dasdasd','sadas/ddasda/dasd','tt001,tt321321321'},
#              {2, 'nm0000002','dasdasd','sadas/ddasda/dasd','tt0012,tt321321321'},
#              {4, 'nm0000003', 'dasdasd', 'sadas/ddasda/dasd', 'tt00121,tt321321321'},
#              {3, 'nm0000003', 'dasdasd', 'sadas/ddasda/dasd', 'tt00121,tt321321321'}]
#     insert_music(array)
#
# if __name__ == '__main__':
#     main()