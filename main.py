from queries import *
from db import cursor, conn, print_all_tables, insert_data, create_tables


def main():
    while True:
        print("Оберіть запит:")
        print("1. Продажі, оплачені готівкою:")
        print("2. Продажі з доставкою")
        print("3. Сума зі знижкою для кожного клієнта:")
        print("4. Продажі конкретного клієнта:")
        print("5. Кількість покупок кожного клієнта:")
        print("6. Сума за готівковий/безготівковий розрахунок:")
        print("0. Вийти.")

        choice = input("Ваш вибір: ")
        if choice == "1":
            query_1()
        elif choice == "2":
            query_2()
        elif choice == "3":
            query_3()
        elif choice == "4":
            source = input("Введіть клієнта: ")
            query_4(source)
        elif choice == "5":
            query_5()
        elif choice == "6":
            query_6()
        elif choice == "0":
            break
        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    create_tables()
    insert_data()
    print_all_tables()
    main()
    cursor.close()
    conn.close()
