import psycopg2

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
            phone VARCHAR(11) NOT NULL UNIQUE
        );
                """)

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Clients VALUES
        (DEFAULT, %s, %s, %s) RETURNING client_id;
        """, (first_name, last_name, email))

        if phone != None:
            add_phone(conn, cur.fetchone(), phone)

        return (first_name, last_name, email, phone)

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT client_id FROM %s
        """, (client_id))

        cur.execute("""
        INSERT INTO Phones VALUES
        (%s, %s) RETURNING phone;
        """, (client_id, phone))
        return (cur.fetchone()[0])

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

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
            new_str = ' AND phone = %s::text'
            list_atr.append(phone)
        sel_str = f"""
            SELECT  
                email,
                first_name,
                last_name,
                CASE
                    WHEN ARRAY_AGG(phone) = '{{Null}}' THEN '{{}}'
                    ELSE ARRAY_AGG(phone)
                END phones 
            FROM Clients c/* Из таблицы клиентов */
            LEFT JOIN Phones p ON c.client_id = p.id
            WHERE first_name ILIKE %s AND last_name ILIKE %s AND email ILIKE %s{new_str}
	    GROUP BY email, first_name, last_name
	    """
        curs.execute(
            sel_str,
            new_str
        )
        return curs.fetchall()

def drop_table()
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS Phones CASCADE;
        DROP TABLE IF EXISTS Clients;
        """)

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    pass
    # drop_db(conn)
    # create_db(conn)
    # add_client(conn,'name1','name2','9@kkt1.ru')
    # print("Add client", add_client(conn,'name1','name2','13@kkt.ru', '79125487543'))
    # print("Add phone", add_phone(conn, 1, '79242345678'))
    # find_client(conn,'name1')
    # find_client(conn,'name1', 'name2')
    # find_client(conn, 'name2', 'name4', 'email2')
    # find_client(conn, email ='email3')
    print("Resu", find_client(conn, phone = '79024123453'))
