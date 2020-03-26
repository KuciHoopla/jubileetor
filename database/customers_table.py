
from database.database_connection import DatabaseConnection

database = '/Users/jankucera/PycharmProjects/jubileetor/jubileetor.db'


def get_all_database_customers():
    try:
        with DatabaseConnection(database) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM customers')
            customers = [{'id_customer': row[0],
                          'name': row[1],
                          'surname': row[2],
                          'email': row[3],
                          'password': row[4]
                          } for row in cursor.fetchall()]

        return customers
    except:
        print("can not get customers")


def get_customer_email_password(email):
    try:
        with DatabaseConnection(database) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT password FROM customers WHERE email = "{email}"')
            customer_password = cursor.fetchone()
            customer_password = customer_password[0]
            cursor.execute(f'SELECT email FROM customers WHERE email = "{email}"')
            customer_email = cursor.fetchone()
            customer_email = customer_email[0]
            cursor.execute(f'SELECT id_customer FROM customers WHERE email = "{email}"')
            id_customer = cursor.fetchone()
            id_customer = id_customer[0]
        return customer_email, customer_password, id_customer
    except:
        print("can not get customers")


def insert_customer(first_name, last_name, email, password, birthday):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO customers VALUES(?,?,?,?,?,?)',
                       (None, first_name, last_name, email, password, birthday))


def insert_gift(id_customer, photo, link, description):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO gifts VALUES(?,?,?,?,?)',
                       (None, id_customer, photo, link, description))


def update_password_manually(new_password, id_customer):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE customers SET password=? WHERE id_customer=?',
                       (new_password, id_customer))


def delete_customer(id_customer):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM customers WHERE id_customer=?', (id_customer,))


def get_customer_data(id_customer):
    try:
        with DatabaseConnection(database) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM customers WHERE id_customer = "{id_customer}"')
            customer = [{'id_customer': row[0],
                         'name': row[1],
                         'surname': row[2],
                         'birthday': row[5]
                         } for row in cursor.fetchall()]
            cursor.execute(f'SELECT * FROM gifts WHERE id_customer = "{id_customer}" ORDER BY id_gift DESC')
            gifts = [{'id_gift': row[1],
                      'photo': row[2],
                      'link': row[3],
                      'description': row[4],
                      } for row in cursor.fetchall()]
            name = customer[0]["name"]
            surname = customer[0]["surname"]
            birthday = customer[0]["birthday"]
        return name, surname, gifts, birthday
    except:
        print("can not get customers")


def get_customer_name_and_last_gift():
    try:
        with DatabaseConnection(database) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT first_name, gifts.photo, customers.id_customer  FROM gifts '
                           'INNER  JOIN customers ON customers.id_customer = gifts.id_customer '
                           'ORDER BY gifts.id_gift DESC')
            data = cursor.fetchall()
        return data
    except:
        print("can not get customers")








