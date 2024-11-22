from db import print_table, cursor


def query_1():
    cursor.execute(
        """SELECT s.*, c.company_name
FROM sales s
JOIN clients c ON s.client_id = c.client_id
WHERE s.payment_method = 'Готівковий'
ORDER BY c.company_name;
"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_2():
    cursor.execute(
        """SELECT * FROM sales WHERE delivery_needed = TRUE;
"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_3():
    cursor.execute(
        """

SELECT
    c.company_name,
    SUM(s.quantity * p.price) AS total,
    SUM(s.quantity * p.price * (1 - s.discount / 100)) AS total_with_discount
FROM sales s
JOIN clients c ON s.client_id = c.client_id
JOIN products p ON s.product_id = p.product_id
GROUP BY c.company_name;

                   """
    )
    print_table(cursor.description, cursor.fetchall())


def query_4(company: str):
    cursor.execute(
        f"""
    SELECT *
FROM sales
WHERE client_id = (SELECT client_id FROM clients WHERE company_name = '{company}');

"""
    )

    print_table(cursor.description, cursor.fetchall())


def query_5():
    cursor.execute(
        """
SELECT c.company_name, COUNT(*) AS purchase_count
FROM sales s
JOIN clients c ON s.client_id = c.client_id
GROUP BY c.company_name;

"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_6():
    cursor.execute(
        """
    SELECT
    c.company_name,
    s.payment_method,
    SUM(s.quantity * p.price * (1 - s.discount / 100)) AS total
FROM sales s
JOIN clients c ON s.client_id = c.client_id
JOIN products p ON s.product_id = p.product_id
GROUP BY c.company_name, s.payment_method;

"""
    )

    print_table(cursor.description, cursor.fetchall())
