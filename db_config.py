import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # change if your host is different
            user="root",  # replace with your MySQL username
            password="root@39",  # replace with your MySQL password
            database="inventory_sales"  # replace with your database name
        )

        if connection.is_connected():
            print("Database connection successful.")
            return connection

    except Error as e:
        print("Error while connecting to database:", e)
        return None