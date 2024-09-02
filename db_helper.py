from decimal import Decimal
import mysql.connector
from mysql.connector import Error

# Global connection variable
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chef_for_you_chatbot_db"
)

def get_order_status(order_id: int):
    with cnx.cursor() as cursor:
        query = "SELECT status FROM order_tracking WHERE order_id=%s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()

    return result[0] if result else None

def get_next_order_id():
    with cnx.cursor() as cursor:
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()[0]

    return 1 if result is None else result + 1

def insert_order_item(food_item: str, quantity: int, order_id: int):
    try:
        with cnx.cursor() as cursor:
            query = "SELECT item_id, price FROM food_items WHERE name=%s"
            cursor.execute(query, (food_item,))
            item = cursor.fetchone()

            if item is None:
                print("Food item not found.")
                return -1

            item_id, price = item
            total_price = price * Decimal(quantity)

            query = "INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (order_id, item_id, quantity, total_price))
            cnx.commit()
            print("Order item inserted successfully")
            return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        cnx.rollback()
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

def get_total_order_price(order_id: int):
    with cnx.cursor() as cursor:
        query = "SELECT SUM(total_price) FROM orders WHERE order_id=%s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()

    return result[0] if result else 0

def insert_order_tracking(order_id: int, statement: str):
    with cnx.cursor() as cursor:
        query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(query, (order_id, statement))
        cnx.commit()


