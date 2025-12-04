import psycopg2
import csv

# Function to connect to the database
def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="Pg_sql_2025_pp2",
        host="localhost",
        port="5432"
    )

# Loading data from a CSV file into the phonebook table
def insert_from_csv():
    conn = connect()
    cur = conn.cursor()
    with open(r'/Users/hatefchalak/Desktop/Lab 11/phonebook.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
                (row[0], row[1])
            )
    conn.commit()
    print("Data from CSV successfully added.")
    cur.close()
    conn.close()

# Manual data input and adding into the table
def insert_from_input():
    conn = connect()
    cur = conn.cursor()
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    cur.execute(
        "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Data successfully added manually.")
    cur.close()
    conn.close()

# Updating name or phone in the phonebook table
def update_data():
    conn = connect()
    cur = conn.cursor()
    print("Choose what you want to update:")
    print("1 — Update name")
    print("2 — Update phone number")
    choice = input("Your choice: ")

    if choice == "1":
        old_name = input("Enter old name: ")
        new_name = input("Enter new name: ")
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
            (new_name, old_name)
        )
        print(f"User name {old_name} updated to {new_name}.")
    
    elif choice == "2":
        name = input("Enter user name: ")
        new_phone = input("Enter new phone number: ")
        cur.execute(
            "UPDATE phonebook SET phone_number = %s WHERE first_name = %s",
            (new_phone, name)
        )
        print(f"Phone number for {name} updated to {new_phone}.")
    
    else:
        print("Invalid choice!")

    conn.commit()
    cur.close()
    conn.close()

# Function for adding multiple users with phone validation
def insert_multiple_users():
    conn = connect()
    cur = conn.cursor()

    # Example list of users and phone numbers
    users = ['John Doe', 'Jane Smith', 'Alice Johnson']
    phones = ['1234567890', '987654321', '5551234567']

    try:
        # Calling stored procedure to insert users
        cur.execute("CALL insert_users_from_list(%s, %s)", (users, phones))
        conn.commit()
        print("Data successfully added or incorrect data displayed.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# Searching data by name or phone (with filters)
def query_data():
    conn = connect()
    cur = conn.cursor()
    print("Choose a filter for search:")
    print("1 — Show all users")
    print("2 — Search by name")
    print("3 — Search by phone number")
    print("4 — Search by part of name")

    choice = input("Your choice: ")

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
        results = cur.fetchall()
    elif choice == "2":
        name = input("Enter name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        results = cur.fetchall()
    elif choice == "3":
        phone = input("Enter phone number to search: ")
        cur.execute("SELECT * FROM phonebook WHERE phone_number = %s", (phone,))
        results = cur.fetchall()
    elif choice == "4":
        part = input("Enter part of the name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + part + '%',))
        results = cur.fetchall()
    else:
        print("Invalid choice!")
        return

    if results:
        print("Search results:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("Nothing found.")
    cur.close()
    conn.close()

# Deleting data by name or phone number
def delete_data():
    conn = connect()
    cur = conn.cursor()
    print("Choose delete method:")
    print("1 — Delete by name")
    print("2 — Delete by phone number")

    choice = input("Your choice: ")
    if choice == "1":
        name = input("Enter user name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
        print(f"User(s) with name '{name}' deleted.")
    
    elif choice == "2":
        phone = input("Enter phone number to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
        print(f"User with phone number '{phone}' deleted.")
    
    else:
        print("Invalid choice!")

    conn.commit()
    cur.close()
    conn.close()

# Search by pattern: name, part of name, or number (uses SQL function search_by_pattern)
def search_by_pattern():
    pattern = input("Enter search pattern (e.g., part of name or number): ")

    conn = connect()
    cur = conn.cursor()

    # Calling SQL function defined in DB
    cur.execute("SELECT * FROM search_by_pattern(%s);", (pattern,))
    results = cur.fetchall()

    if results:
        print("Search results:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("Nothing found.")

    cur.close()
    conn.close()

# Function to add a new user or update phone if name already exists
def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
        conn.commit()
        print("User successfully added or updated.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# Function for adding multiple users manually
# Calls insert_users_from_list, which returns invalid data
def insert_multiple_users():
    conn = connect()
    cur = conn.cursor()

    count = int(input("How many users do you want to add? "))

    users = []
    phones = []

    for i in range(count):
        name = input(f"Enter name for user #{i + 1}: ")
        phone = input(f"Enter phone number for {name}: ")
        users.append(name)
        phones.append(phone)

    try:
        cur.execute(
            "SELECT * FROM insert_users_from_list(%s, %s);",
            (users, phones)
        )
        invalids = cur.fetchall()
        conn.commit()

        if invalids:
            print("Invalid data found:")
            for name, phone in invalids:
                print(f"Name: {name}, Phone: {phone}")
        else:
            print("All users successfully added.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# Pagination: getting data using limit and offset
def query_data_with_pagination():
    conn = connect()
    cur = conn.cursor()
    
    while True:
        try:
            print("Enter page number (starting from 1):")
            page = int(input())
            if page < 1:
                print("Page number must be positive.")
                continue
            break
        except ValueError:
            print("Enter a valid page number.")

    while True:
        try:
            print("Enter number of records per page:")
            limit = int(input())
            if limit < 1:
                print("Records per page must be positive.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")
    
    offset = (page - 1) * limit
    
    cur.execute("SELECT * FROM phonebook LIMIT %s OFFSET %s", (limit, offset))
    results = cur.fetchall()
    
    if results:
        print(f"Results for page {page}:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("Nothing found.")
    
    cur.close()
    conn.close()

# Call pagination function
query_data_with_pagination()

# Main menu
print("Choose an action:")
print("1 - Load from CSV")
print("2 - Enter manually")
print("3 - Update data")
print("4 - Search data")
print("5 - Delete data")
print("6 - Search by pattern (DB function)")
print("7 - Add/update user")
print("8 - Bulk add users with validation")

choice = input("Your choice: ")

if choice == "1":
    insert_from_csv()
elif choice == "2":
    insert_from_input()
elif choice == "3":
    update_data()
elif choice == "4":
    query_data()
elif choice == "5":
    delete_data()
elif choice == "6":
    search_by_pattern()
elif choice == "7":
    insert_or_update_user()
elif choice == "8":
    insert_multiple_users()
else:
    print("Invalid choice!")