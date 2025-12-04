import psycopg2
import re

conn = psycopg2.connect(
    dbname="phone",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

table_name = "contacts"
num = input("Введите команду (all_pattern, create, create2,create3,delete): ")

def check_number_exists(conn, table_name, name, phone_number):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM {table_name} WHERE name = %s AND phone_number = %s", (name, phone_number))
        result = cur.fetchone()
        cur.close()
        return result 
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return False

def all_pattern():
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()

def add_new_user(conn, table_name, user_name, phone_number):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO contacts (name, phone_number)
            VALUES (%s, %s);
        """, (user_name, phone_number))
        conn.commit()
        print("New user added.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def update_num(conn, number, user_name):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE contacts
            SET phone_number = %s
            WHERE name = %s;
        """, (number, user_name))
        conn.commit()
        print("Update was successfull.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def insert_users(conn, name, phone):
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone_number) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()

def is_valid_phone(phone):
    x = re.search(r'^87\d{9}', phone)
    y = re.search(r'^\+77\d{9}', phone)
    z = re.search(r'^7\d{9}', phone)

    if x is not None and phone == x.group():
        return True
    elif y is not None and phone == y.group():
        return True
    elif z is not None and phone == z.group():
        return True
    else:
        return False

def query_with_pagination(conn,table_name, limit, offset):
    # Connect to the database
    cur = conn.cursor()

    # Query the data with pagination
    cur.execute(f"SELECT * FROM {table_name} ORDER BY id ASC LIMIT {limit} OFFSET {offset};")
    rows = cur.fetchall()

    # Close the database connection
    cur.close()

    return rows

def delete_user_by_username_or_phone(conn,name=None, number=None):
    # Connect to the database
    cur = conn.cursor()

    # Delete the user(s) by name or phone
    if name is not None:
        cur.execute(f"DELETE FROM contacts WHERE name = '{name}';")
    elif number is not None:
        cur.execute(f"DELETE FROM contacts WHERE number = '{number}';")
    else:
        raise ValueError("Either name or phone must be provided for deletion")

    # Commit the changes and close the database connection
    conn.commit()
    cur.close()

# 1
if num == 'all_pattern':
    all_pattern()

# 2
elif num == "create":
    user_name = input("Name: ")
    phone_number = input("Phone number: ")

    if not check_number_exists(conn, table_name, user_name, phone_number):
        add_new_user(conn, table_name, user_name, phone_number)
    else:
        number = input("New number: ")
        update_num(conn, number, user_name)

# 3
elif num == "create2":
    Phone_numbers = {
        "Nurik": "+77087214957",
        "Ramazan": "123456"
    }
    incorrect = []

    for d, z in Phone_numbers.items():
        if not is_valid_phone(z):
            incorrect.append((d, z))
        else:
            insert_users(conn, d, z)

    if incorrect:
        print("Incorrect numbers:")
        for name, number in incorrect:
            print(f"{name}: {number}")

#4
if num == "create3":
    limit = int(input())
    offset = int(input())
    rows = query_with_pagination(conn, table_name, limit, offset)

    for row in rows:
        print(row)

#5
if num == "delete":
    name = input()
    number = input()
    delete_user_by_username_or_phone(conn,name, number)



conn.close()