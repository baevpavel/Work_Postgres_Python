import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        
        CREATE TABLE IF NOT EXISTS Clients (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(30) NOT NULL
        );	
        CREATE TABLE IF NOT EXISTS Phones (
            id INTEGER NOT NULL REFERENCES Clients ON DELETE CASCADE,
            phone INTEGER NOT NULL UNIQUE,
            #CONSTRAINT ch PRIMARY KEY (id, phone)
        );
#    conn.commit()  # фиксируем в БД
#conn.close()        
                """)

def add_client(conn, first_name, last_name, email, phone=None):
    pass

def add_phone(conn, client_id, phone):
    pass

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

def drop_table()
    DROP TABLE IF NOT EXISTS Phones ON DELETE CASCADE;
    DROP TABLE IF NOT EXISTS Clients;

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    drop_table(conn)# удаляем таблицы
    create_db(conn)  # вызывайте функции здесь
