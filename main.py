# -*- coding: cp1251 -*-
import psycopg2

def create_table(cur):
    cur.execute("""
        DROP TABLE IF EXISTS phone_num;
        DROP TABLE IF EXISTS client;
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) UNIQUE,
            last_name VARCHAR(40) UNIQUE,
            email VARCHAR(40) UNIQUE
            );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_num(
            id SERIAL PRIMARY KEY,
            number VARCHAR(40),
            client_id INTEGER NOT NULL REFERENCES client(id)
        );
        """)
    conn.commit()


def add_client(cur, first_name, last_name, email, number=None):
    cur.execute("""
        INSERT INTO client(first_name, last_name, email) 
        VALUES(%s, %s, %s)
        RETURNING id;
        """, (first_name, last_name, email))
    client_id = cur.fetchone()
    if number != None:
        cur.execute("""
        INSERT INTO phone_num(client_id, number)
        VALUES(%s, %s);
        """, (client_id, number))
    conn.commit()


def add_phone(cur, id, number):
    cur.execute("""
            INSERT INTO phone_num(client_id, number)
            VALUES(%s, %s);
            """, (id, number))
    conn.commit()


def change_client(cur, id, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name != None:
        cur.execute("""
        UPDATE client SET first_name=%s WHERE id=%s;
        """, (first_name, id))
    if last_name != None:
        cur.execute("""
        UPDATE client SET last_name=%s WHERE id=%s;
        """, (last_name, id))
    if email != None:
        cur.execute("""
        UPDATE client SET email=%s WHERE id=%s;
        """, (email, id))
    if phone_number != None:
        cur.execute("""
        UPDATE phone_num SET number=%s WHERE client_id=%s;
        """, (phone_number, id))
    conn.commit()


def delete_phone(cur, id):
    cur.execute("""
            DELETE FROM phone_num WHERE client_id=%s;
        """, (id,))
    conn.commit()


def find_client(cur, first_name=None, last_name=None, email=None, number=None):
    if first_name != None:
        cur.execute("""
        SELECT id FROM client WHERE first_name=%s;
        """, (first_name,))
    if last_name != None:
        cur.execute("""
        SELECT id FROM client WHERE last_name=%s;
        """, (last_name,))
    if email != None:
        cur.execute("""
        SELECT id FROM client WHERE email=%s;
        """, (email,))
    if number != None:
        cur.execute("""
        SELECT client_id FROM phone_num WHERE number=%s;
        """, (number,))
    print(cur.fetchone()[0])


def delete_client(cur, id):
    cur.execute("""
               DELETE FROM phone_num WHERE client_id=%s;
           """, (id,))
    cur.execute("""
               DELETE FROM client WHERE id=%s;
           """, (id,))
    conn.commit()


if __name__ == '__main__':
    with psycopg2.connect(database='clients_db', user='postgres', password='postgres') as conn:
        with conn.cursor() as cur:

            # Функция, создающая структуру БД(таблицы).
            create_table(cur)

            # Функция, позволяющая добавить нового клиента.
            add_client(cur, 'Sayaka', 'Aoki', 'Aoki@gmail.com', 998907449251)
            add_client(cur, 'Philipp', 'Yakimov', 'Yakimov@gmail.com', 998907449252)
            add_client(cur, 'Lorgar', 'Avrelian', 'Avrelian@gmail.com')
            add_client(cur, 'Roboute', 'Guilliman', 'Guilliman@gmail.com', 998907449648)
            add_client(cur, 'Leman ', 'Russ', 'Russ@gmail.com', 998907449649)

            # Функция, позволяющая добавить телефон для существующего клиента.
            add_phone(cur, 1, 998907449253)
            add_phone(cur, 2, 998907449254)
            add_phone(cur, 2, 998907449255)
            add_phone(cur, 3, 998907449256)
            add_phone(cur, 3, 998907449257)

            # Функция, позволяющая изменить данные о клиенте.
            change_client(cur, 4, last_name='Khan', email='Khan@gmail.com')

            # Функция, позволяющая удалить телефон для существующего клиента.
            delete_phone(cur, 2)

            # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
            find_client(cur, first_name='Sayaka')
            find_client(cur, last_name='Yakimov')
            find_client(cur, email='Avrelian@gmail.com')
            find_client(cur, number='998907449649')

            # Функция, позволяющая удалить существующего клиента.
            delete_client(cur, 1)