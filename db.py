import psycopg2
from psycopg2.extras import execute_values
from prettytable import PrettyTable

# Параметри підключення
conn = psycopg2.connect(
    dbname="db", user="user", password="password", host="localhost", port="5432"
)

cursor = conn.cursor()


# Створення таблиць
def create_tables():
    cursor.execute(
        """
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS clients;
        DROP TABLE IF EXISTS products;

        CREATE TABLE clients (
            client_id SERIAL PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            client_type VARCHAR(100) CHECK (client_type IN ('Юридична', 'Фізична')) NOT NULL,
            address TEXT,
            phone CHAR(30),
            contact_person VARCHAR(100),
            account_number CHAR(50) UNIQUE
        );

        -- Таблиця товарів

        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
            quantity INT NOT NULL CHECK (quantity >= 0)
        );


        -- Таблиця продажів
        CREATE TABLE sales (
            sale_id SERIAL PRIMARY KEY,
            sale_date DATE NOT NULL DEFAULT CURRENT_DATE,
            client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
            product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
            quantity INT NOT NULL CHECK (quantity > 0),
            discount NUMERIC(5, 2) NOT NULL CHECK (discount BETWEEN 3 AND 20),
            payment_method VARCHAR(50) CHECK (payment_method IN ('Готівковий', 'Безготівковий')) NOT NULL,
            delivery_needed BOOLEAN NOT NULL,
            delivery_cost NUMERIC(10, 2) CHECK (delivery_cost >= 0)
        );
                        """
    )
    conn.commit()
    print("Таблиці створено")


def insert_data():
    clients = [
        (
            "Фірма А",
            "Юридична",
            "Київ, вул. Хрещатик, 1",
            "0671234567",
            "Петренко І.",
            "UA12345678901234567890",
        ),
        (
            "Фірма Б",
            "Фізична",
            "Львів, вул. Шевченка, 10",
            "0509876543",
            "Іваненко О.",
            "UA09876543210987654321",
        ),
        (
            "Фірма В",
            "Юридична",
            "Одеса, вул. Дерибасівська, 5",
            "0931122334",
            "Сидоренко М.",
            "UA34567890123456789012",
        ),
        (
            "Фірма Г",
            "Фізична",
            "Дніпро, вул. Гагаріна, 20",
            "0679988776",
            "Коваленко Т.",
            "UA56789012345678901234",
        ),
    ]

    products = [
        ("Товар 1", 100.50, 10),
        ("Товар 2", 200.00, 5),
        ("Товар 3", 300.75, 20),
        ("Товар 4", 50.25, 50),
        ("Товар 5", 80.10, 30),
        ("Товар 6", 150.00, 15),
        ("Товар 7", 90.75, 40),
        ("Товар 8", 60.50, 25),
        ("Товар 9", 120.90, 35),
        ("Товар 10", 250.00, 8),
    ]

    sales = [
        (1, 1, 2, 5, "Готівковий", True, 50.00),
        (2, 2, 1, 3, "Безготівковий", False, 0.00),
        # Додайте ще 17 продажів відповідно до завдання
    ]

    # Вставка даних
    cursor.executemany(
        "INSERT INTO clients (company_name, client_type, address, phone, contact_person, account_number) VALUES (%s, %s, %s, %s, %s, %s)",
        clients,
    )

    cursor.executemany(
        "INSERT INTO products (product_name, price, quantity) VALUES (%s, %s, %s)",
        products,
    )

    execute_values(
        cursor,
        "INSERT INTO sales (client_id, product_id, quantity, discount, payment_method, delivery_needed, delivery_cost) VALUES %s",
        sales,
    )
    conn.commit()


def print_table(description, rows):
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]
    for row in rows:
        table.add_row(row)
    print(table)


def print_all_tables():
    tables = ["clients", "products", "sales"]

    for i in tables:
        cursor.execute(f"""SELECT * FROM {i}""")
        print(f"Таблиця {i}")
        print(print_table(cursor.description, cursor.fetchall()))
