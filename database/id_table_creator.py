from database.database_connection import DatabaseConnection
from datetime import datetime, timezone

database = '/Users/jankucera/PycharmProjects/jubileetor/jubileetor.db'


def create_table_personalised(id_customer):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        id_customer = str(id_customer)
        cursor.execute(f'CREATE TABLE IF NOT EXISTS "{id_customer}"('
                       'id_gift integer primary key autoincrement,'
                       'date text,'
                       'gift text)')


def get_all_gift_by_id(id_customer):
    try:
        with DatabaseConnection(database) as connection:
            cursor = connection.cursor()
            id_customer = str(id_customer)
            cursor.execute(f'SELECT date, gift FROM "{id_customer}"')
            gifts_of_customer = [{'date': row[0],
                                 'gift': row[1]} for row in cursor.fetchall()]
            return gifts_of_customer
    except:
        create_table_personalised(id_customer)
        return 0


def get_last_gift_by_id(id_customer):
    try:
        gift_of_customer = get_all_gift_by_id(id_customer)[-1]["gift"]
        return gift_of_customer
    except:
        return None


def insert_gift_to_customer(id_customer, gift):
    try:
        with DatabaseConnection(database) as connection:
            date = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H-%M-%S')
            cursor = connection.cursor()
            id_customer = str(id_customer)
            cursor.execute(f'INSERT INTO "{id_customer}" VALUES(?,?,?)', (None, date, gift))

    except:
        print("except")
        create_table_personalised(id_customer)


def input_photo_to_customer(id_customer, photo):
    try:
        with DatabaseConnection(database) as connection:
            binary_photo = photo.read()
            print(binary_photo)
            id_customer = str(id_customer)
            cursor = connection.cursor()
            cursor.execute("UPDATE customers SET photo = (?) WHERE id_customer = (?)", (binary_photo, id_customer))
    except:
        print("can not input photo to customer")


