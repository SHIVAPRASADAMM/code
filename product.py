import mysql.connector


class Product:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()

    def generate_product_id(self):
        try:
            self.cursor.execute("SELECT product_id FROM products ORDER BY product_id DESC LIMIT 1")
            result = self.cursor.fetchone()
            if result and result[0]:
                last_id = int(result[0][3:])  # Extract numeric part after 'PRD'
                new_id = f"PRD{last_id + 1:03d}"  # Format with leading zeros
            else:
                new_id = "PRD001"
            return new_id
        except mysql.connector.Error as err:
            print("Error generating product ID:", err)
            return None

    def add_product(self, name, category, price, quantity):
        try:
            product_id = self.generate_product_id()
            if not product_id:
                print("Failed to generate product ID.")
                return
            sql = "INSERT INTO products (product_id, name, category, price, quantity) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (product_id, name, category, price, quantity))
            self.db.commit()
            print(f"Product '{name}' added with ID: {product_id}")
        except mysql.connector.Error as err:
            print("Error adding product:", err)

    def view_products(self):
        try:
            query = "SELECT * FROM products"
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            if len(products)==0:
                print("No products found")
            else:
                print("\n--- Product List ---")
                for product in products:
                    print(
                        f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: {product[3]}, Quantity: {product[4]}")
        except mysql.connector.Error as err:
            print("Error viewing products:", err)

    def update_product(self, product_id, name=None, category=None, price=None, quantity=None):
        try:
            updates = []
            values = []
            if name:
                updates.append("name=%s")
                values.append(name)
            if category:
                updates.append("category=%s")
                values.append(category)
            if price is not None:
                updates.append("price=%s")
                values.append(price)
            if quantity is not None:
                updates.append("quantity=%s")
                values.append(quantity)

            values.append(product_id)
            sql = f"UPDATE products SET {', '.join(updates)} WHERE product_id = %s"
            self.cursor.execute(sql, tuple(values))
            self.db.commit()
            print("Product updated successfully.")
        except mysql.connector.Error as err:
            print("Error updating product:", err)

    def delete_product(self, product_id):
        try:
            query = "DELETE FROM products WHERE product_id = %s"
            self.cursor.execute(query, (product_id,))
            self.db.commit()
            if self.cursor.rowcount>0:
                print("Product deleted successfully.")
            else:
                print("No product found.")
        except mysql.connector.Error as err:
            print("Error deleting product:", err)

    def search_products(self, product_id):
        try:
            query = "SELECT * FROM products WHERE product_id = %s"
            self.cursor.execute(query, (product_id,))
            product = self.cursor.fetchone()
            return product
        except mysql.connector.Error as err:
            print("Error searching products:", err)