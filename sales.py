import mysql.connector
from datetime import date,datetime

class Sale:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()

    def record_sale(self, customer_id, product_id, quantity, sale_date):
        try:
            self.db.start_transaction()
            # Check stock
            self.cursor.execute("SELECT quantity FROM products WHERE product_id = %s", (product_id,))
            stock = self.cursor.fetchone()
            if not stock or stock[0] < quantity:
                self.db.rollback()
                raise ValueError("Insufficient stock")

            # Record sale
            #sale_date = date.today()
            query = """
                    INSERT INTO sales (customer_id, product_id, quantity,sale_date)
                    VALUES (%s, %s, %s, %s)
            """
            values = (customer_id, product_id, quantity,sale_date)
            self.cursor.execute(query, values)

            # Update stock
            self.cursor.execute(
                "UPDATE products SET quantity = quantity - %s WHERE product_id = %s",
                (quantity, product_id)
            )

            self.db.commit()
            print("Sale recorded successfully.")

        except ValueError as ve:
            print("Stock error:", ve)
        except mysql.connector.Error as err:
            self.db.rollback()
            print("Database error during sale:", err)

    def get_all_sales(self):
        try:
            query = "select * from sales"
            self.cursor.execute(query)
            sales = self.cursor.fetchall()
            print("\n--- Sales List ---")
            for sale in sales:
                sale_id = sale[0]
                customer_id = sale[1]
                product_id = sale[2]
                quantity = sale[3]
                sale_date = sale[4]
                # Format the date if needed
                if isinstance(sale_date, (date,)):
                    sale_date_str = sale_date.strftime('%Y-%m-%d')
                else:
                    sale_date_str = str(sale_date)
                print(
                    f"sale_id: {sale_id}, customer_id: {customer_id}, product_id: {product_id}, quantity: {quantity}, sale_date: {sale_date_str}")
        except mysql.connector.Error as err:
            print("Error viewing Sales:", err)

    def show_daily_sales_summary(self, target_date=None):
        """Show total quantity and value of sales per product for a given day."""
        try:
            if target_date is None:
                target_date = input("Enter date (YYYY-MM-DD): ")
            datetime.strptime(target_date, "%Y-%m-%d")

            query = """
                        SELECT DATE(s.sale_date) as sale_day,
                               SUM(s.quantity) as total_qty,
                               SUM(s.quantity * p.price) as total_amount
                        FROM sales s
                        JOIN products p ON s.product_id = p.product_id
                        WHERE DATE(s.sale_date) = %s
                        GROUP BY sale_day
                    """
            self.cursor.execute(query, (target_date,))
            result = self.cursor.fetchone()

            if result:
                print("\n📊 Daily Sales Summary")
                print(f"Date: {result[0]}")
                print(f"Total Quantity Sold: {result[1]}")
                print(f"Total Sales Amount: ₹{result[2]:.2f}")
            else:
                print("❗ No sales found for the given date.")

        except Exception as e:
            print("❌ Error:", e)

    def show_monthly_sales_summary(self, month=None):
        from datetime import datetime
        try:
            if month is None:
                month = input("Enter month (YYYY-MM): ")
            month = month.strip()
            datetime.strptime(month, "%Y-%m")
            print("DEBUG: Searching for month:", month)

            query = """
                SELECT MONTH(s.sale_date) as month_num,
                       YEAR(s.sale_date) as year_num,
                       SUM(s.quantity) as total_qty,
                       SUM(s.quantity * p.price) as total_amount
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                WHERE DATE_FORMAT(s.sale_date, '%%Y-%%m') = %s
                GROUP BY year_num, month_num
            """
            self.cursor.execute(query, (month,))
            result = self.cursor.fetchone()
            print("DEBUG: Raw DB result:", result)

            if result and result[2] is not None and result[3] is not None:
                print("\n📊 Monthly Sales Summary")
                print(f"Month: {month}")
                print(f"Total Quantity Sold: {result[2]}")
                print(f"Total Sales Amount: ₹{result[3]:.2f}")
            else:
                print("❗ No sales found for the given month.")

        except Exception as e:
            print("❌ Error:", e)