from db_config import create_connection
from product import Product
from customer import Customer
from sales import Sale
from billing import Billing

def product_menu(product_manager):
    while True:
        print("\n=== Product Management Menu ===")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter quantity: "))
            product_manager.add_product(name, category, price, quantity)

        elif choice == "2":
            product_manager.view_products()

        elif choice == "3":
            pid = input("Enter product ID to update: ")
            name = input("New name (or press Enter to skip): ")
            category = input("New category (or press Enter to skip): ")
            price = input("New price (or press Enter to skip): ")
            quantity = input("New quantity (or press Enter to skip): ")
            product_manager.update_product(
                pid,
                name=name,
                category=category,
                price=float(price) if price else None,
                quantity=int(quantity) if quantity else None
            )

        elif choice == "4":
            pid = input("Enter product ID to delete: ")
            product_manager.delete_product(pid)

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def customer_menu(customer_manager):
    while True:
        print("\n=== Customer Management Menu ===")
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter Customer Name: ")
            phone = input("Enter phone: ")
            customer_manager.add_customer(name, phone)

        elif choice == "2":
            customer_manager.get_all_customers()

        elif choice == "3":
            cid = input("Enter customer ID to update: ")
            name = input("New name (or press Enter to skip): ")
            phone = input("New phone (or press Enter to skip): ")
            customer_manager.update_customer(cid, name, phone)

        elif choice == "4":
            cid = input("Enter customer ID to delete: ")
            customer_manager.delete_customer(cid)

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def sales_menu(sales_manager):
    while True:
        print("\n=== Sales Menu ===")
        print("1. Record a Sale")
        print("2. View All Sales")
        print("3. Show Daily Sales Summary")
        print("4. Show Monthly Sales Summary")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_id = input("Enter customer ID: ")
            product_id = input("Enter product ID: ")
            quantity = int(input("Enter quantity sold: "))
            sale_date=input("Enter the date: ")
            sales_manager.record_sale(customer_id, product_id, quantity,sale_date)

        elif choice == "2":
            sales_manager.get_all_sales()

        elif choice == "3":
            sales_manager.show_daily_sales_summary()
        elif choice == '4':
            sales_manager.show_monthly_sales_summary()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def billing_menu(billing_manager):
    while True:
        print("\n=== Billing Menu ===")
        print("1. Generate Bill by Customer ID")
        print("2. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_id = input("Enter customer ID: ")
            billing_manager.generate_bill_by_customer(customer_id)

        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    conn = create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    product_manager = Product(conn)
    customer_manager = Customer(conn)
    sales_manager = Sale(conn)
    billing_manager = Billing(conn)

    while True:
        print("\n=== Inventory and Sales System ===")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Process Sales")
        print("4. Generate Bills")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_menu(product_manager)
        elif choice == "2":
            customer_menu(customer_manager)
        elif choice == "3":
            sales_menu(sales_manager)
        elif choice == "4":
            billing_menu(billing_manager)
        elif choice == "5":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()


if __name__ == "__main__":
    main()