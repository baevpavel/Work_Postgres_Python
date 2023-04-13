import psycopg2

def drop_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS Phones CASCADE;
        DROP TABLE IF EXISTS Clients;
            """)

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(30) NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS Phones (
            id INTEGER NOT NULL REFERENCES Clients ON DELETE CASCADE,
            phone VARCHAR(11) UNIQUE
        );
                """)

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        if find_client(conn, first_name, last_name, email):
            return "Client not unique!"
        if phone != None:
            if find_client(conn, phone=phone):
                return "Phone not unique!"
        cur.execute("""
        INSERT INTO Clients VALUES
        (DEFAULT, %s, %s, %s) RETURNING client_id;
        """, (first_name, last_name, email))
        if phone != None:
            add_phone(conn, cur.fetchone(), phone)

        return (first_name, last_name, email, phone)

def add_phone(conn, client_id, phone):
    if find_client(conn, phone=phone):
        return "Phone not unique"
    with conn.cursor() as cur:
        cur.execute("""
        SELECT client_id FROM Clients
        WHERE client_id=%s;
        """,(client_id,))
        if not cur.fetchone():
            return "The client does not exist"
        cur.execute("""
        INSERT INTO Phones VALUES
        (%s, %s) RETURNING phone;
                """, (client_id, phone))
        return (cur.fetchone()[0])


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as curs:
        curs.execute(
            """
            SELECT client_id, first_name, last_name, email FROM Clients #--Из таблицы клиентов получаем имя, фамилию почту и id клиента. Такой порядок важен, т.к. легче будет передавать данные далее в запрос
            WHERE client_id = %s; --Где id клиента равно %s
            """,
            (client_id,) #Передаем id клиента
        )
        client_data = curs.fetchone() #Получаем данные пользователя в виде кортежа из запроса и сохраняем в переменную
        if not client_data: #Если селект данные не вернул, то проваливаемся в блок
            return "Еhe client does not exist" #Сообщаем, что такого пользователя нет
        if client_data[0]: #Если имя пустое, то проваливаемся в блок
            first_name = client_data[0] #Изменяем имя клиента на значение из кортежа, который вернулся из запроса
        if client_data[1]: #Если фамилия пустая, то проваливаемся в блок
            first_name = client_data[1] #Изменяем фамилию клиента на значение из кортежа, который вернулся из запроса
        if client_data[2]: #Если почта пустая, то проваливаемся в блок
            email = client_data[2] #Изменяем почту клиента на значение из кортежа, который вернулся из запроса
        curs.execute(
            """
            UPDATE Clients /* Обновляем таблицу клиентов */
            SET first_name = %s, last_name = %s, email = %s /* Где для имени, фамилии и почты устанавливаем новые значения */
            WHERE client_id = %s; /* Где id клиента равно передаваемому значению */
            """,
            (client_id, first_name, last_name, email) #Передаем имя, фамилию, почту и айди клиента
        )
        conn.commit()
    return "Пользователь успешно изменен"

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as curs:
        if first_name is None:
            first_name = '%'
        if last_name is None:
            last_name = '%'
        if email is None:
            email = '%'
        list_atr = [first_name, last_name, email]
        new_str = ''
        if phone != None:
            new_str = ' AND phone = %s'
            list_atr.append(phone)
        sel_str = f"""
            SELECT email, first_name, last_name,
                CASE
                    WHEN ARRAY_AGG(phone) = '{{Null}}' THEN '{{}}'
                    ELSE ARRAY_AGG(phone)
                END phones
            FROM Clients c
            LEFT JOIN Phones p ON c.client_id = p.id
            WHERE first_name ILIKE %s AND last_name ILIKE %s AND email ILIKE %s{new_str}
	    GROUP BY email, first_name, last_name
	    """
        curs.execute(
            sel_str,
            list_atr
        )
        return curs.fetchall()
with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    pass
    # drop_db(conn)
    # create_db(conn)
    print(add_client(conn,'name08','name078','08@kkt1.ru', '89000000002'))
    # print(find_client(conn,'name05','name05','05@kkt1.ru'))
    # print(find_client(conn, phone='79242345679'))
    # print("Add client", add_client(conn,'name1','name2','13@kkt.ru', '79125487543'))
    # print("Add phone:", add_phone(conn, 1, '89000000003'))
    # print("Result find: ", find_client(conn,'name1'))
    # print("Result find: ", find_client(conn,'name1', 'name2'))
    # print("Result find: ", find_client(conn, email ='6@kkt1.ru'))
    # print("Result find: ", find_client(conn, phone='71234567890'))
    # print("Result find: ", find_client(conn, phone='89000000000'))



