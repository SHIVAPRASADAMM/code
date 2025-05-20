import mysql.connector

class Customer:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()

    def generate_customer_id(self):
        try:
            self.cursor.execute("SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1")
            result = self.cursor.fetchone()
            if result and result[0]:
                if isinstance(result[0], int):
                    last_id = result[0]
                    new_id = f"CUST{last_id + 1:03d}"
                else:
                    last_id = int(result[0][4:])  # If it's like 'CUST001'
                    new_id = f"CUST{last_id + 1:03d}"
            else:
                new_id = "CUST001"
            return new_id
        except mysql.connector.Error as err:
            print("Error generating customer ID:", err)
            return None

    def add_customer(self, name, phone):
        try:
            customer_id = self.generate_customer_id()
            if not customer_id:
                print("Customer ID generation failed.")
                return
            sql = "INSERT INTO customers (customer_id, name, phone) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (customer_id, name, phone))
            self.db.commit()
            print(f"Customer '{name}' added with ID: {customer_id}")
        except mysql.connector.Error as err:
            print("Error adding customer:", err)

    def view_customers(self):
        try:
            self.cursor.execute("SELECT * FROM customers")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Error viewing customers:", err)

    def get_all_customers(self):
        try:
            self.cursor.execute("SELECT * FROM customers")
            rows = self.cursor.fetchall()
            if rows:
                print("\n--- Customer List ---")
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]},Phone: {row[2]}")
            else:
                print("No customers found.")
        except Exception as e:
            print("Failed to retrieve customers:", e)

    def update_customer(self, customer_id, name=None, phone=None):
        try:
            updates = []
            params = []

            if name:
                updates.append("name = %s")
                params.append(name)

            if phone:
                updates.append("phone = %s")
                params.append(phone)

            if not updates:
                print("No fields to update.")
                return

            query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = %s"
            params.append(customer_id)

            self.cursor.execute(query, tuple(params))
            self.db.commit()
            print("Customer updated successfully.")
        except Exception as e:
            print("Failed to update customer:", e)

    def delete_customer(self, customer_id):
        try:
            self.cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
            self.db.commit()
            if self.cursor.rowcount > 0:
                print("Customer deleted successfully.")
            else:
                print("No customer found.")
        except Exception as e:
            print("Failed to delete customer:", e)