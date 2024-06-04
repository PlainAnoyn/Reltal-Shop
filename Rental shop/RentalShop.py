from tabulate import tabulate
from datetime import datetime, timedelta
# Function to display the welcome screen
def display_welcome_screen():
    
    print("""
          
+--------------------------------------------------------------------------------------------------------------------------------+
|    __          __  _                               _            _____            _        _        _____ _                     |
|    \ \        / / | |                             | |          |  __ \          | |      | |      / ____| |                    |
|     \ \  /\  / ___| | ___ ___  _ __ ___   ___     | |_ ___     | |__) |___ _ __ | |_ __ _| |     | (___ | |__   ___  _ __      |
|      \ \/  \/ / _ | |/ __/ _ \| '_ ` _ \ / _ \    | __/ _ \    |  _  // _ | '_ \| __/ _` | |      \___ \| '_ \ / _ \| '_ \     |
|       \  /\  |  __| | (_| (_) | | | | | |  __/    | || (_) |   | | \ |  __| | | | || (_| | |      ____) | | | | (_) | |_) |    |
|        \/  \/ \___|_|\___\___/|_| |_| |_|\___|     \__\___/    |_|  \_\___|_| |_|\__\__,_|_|     |_____/|_| |_|\___/| .__/     |
|                                                                                                                     | |        |
|                                                                                                                     |_|        |
+--------------------------------------------------------------------------------------------------------------------------------+
          """)
    print("Options:")
    print("Press '1' To Rent an item")
    print("Press '2' To Return an item")
    print("Press 'Q' To Quit")

# Function to print a bill for the customer's order and save order data
def print_bill(customer_name, customer_contact, ordered_items, total_cost):
    print("Rental Shop - Order Bill")
    print(f"Customer Name: {customer_name}")
    print(f"Contact Information: {customer_contact}")
    print("\nOrdered Items:")
    
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(f"{customer_name}_order.txt", "w") as order_file:
        order_file.write(f"Customer Name: {customer_name}\n")
        order_file.write(f"Contact Information: {customer_contact}\n")
        order_file.write(f"Order Date: {order_date}\n\n")
        order_file.write("Ordered Items:\n")
        
        for item in ordered_items:
            order_file.write(f"{item['quantity']} {item['name']}(s) - {item['days']} days: ${item['cost']:.2f}\n")
    
        order_file.write("\nTotal Cost: ${:.2f}".format(total_cost))
    
    print("Bill printed and order data saved. Thank you for using the Rental Shop!")

# Function to handle renting an item
def rent_item(items, item_num, quantity, days, customer_name, customer_contact, ordered_items, total_cost):
    selected_item = items[item_num - 1]

    # Check if enough stock is available
    if selected_item["stock"] < quantity:
        print("Not enough stock. Please order fewer items.")
        return ordered_items, total_cost

    # Update stock and calculate total cost
    selected_item["stock"] -= quantity
    item_cost = selected_item["price"] * quantity * days
    total_cost += item_cost

    ordered_items.append({
        "name": selected_item["name"],
        "quantity": quantity,
        "days": days,
        "cost": item_cost
    })

    # Write updated inventory data back to file
    with open("inventory.txt", "w") as file:
        for item in items:
            file.write(f"{item['name']},{item['brand']},{item['price']},{item['stock']}\n")

    print(f"Added {quantity} {selected_item['name']}(s) to your order.")
    print(f"Total cost for rented items so far: ${total_cost:.2f}")

    return ordered_items, total_cost

# Function to handle returning an item
def return_item(items, item_num, quantity, ordered_items, total_cost):
    selected_item = items[item_num - 1]
    
    late_return_days = int(input("Enter the number of days the item is being returned late: "))
    late_return_charge = 0

    if late_return_days > 0:
        late_return_charge = selected_item["price"] * quantity * late_return_days
        print(f"Late return charge: ${late_return_charge:.2f}")

    # Update stock and calculate total cost
    selected_item["stock"] += quantity

    # Write updated inventory data back to file
    with open("inventory.txt", "w") as file:
        for item in items:
            file.write(f"{item['name']},{item['brand']},{item['price']},{item['stock']}\n")

    print(f"Returned {quantity} {selected_item['name']}(s). Thank you for returning the item.")

    total_cost += late_return_charge
    return ordered_items, total_cost

# Function to display the inventory
def display_inventory(items):
    items_list = [[i + 1, item["name"], item["brand"], f"${item['price']}", item["stock"]] for i, item in enumerate(items)]
    headers = ["Item Num", "Name", "Brand", "Price", "Quantity Available"]
    
    print(tabulate(items_list, headers=headers, tablefmt="grid"))

# Main program function
def main():
    display_welcome_screen()
    customer_name = input("Enter your name: ")
    customer_contact = input("Enter your contact information: ")
    ordered_items = []
    total_cost = 0
    items = []

    # Read inventory data from file
    with open("inventory.txt", "r") as file:
        for line in file:
            name, brand, price, stock = line.strip().split(",")
            items.append({"name": name, "brand": brand, "price": float(price), "stock": int(stock)})

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                display_inventory(items)  # Show inventory before renting
                item_num = int(input("Enter the item number you want to rent: "))
                quantity = int(input("Enter the quantity: "))
                days = int(input("Enter the number of days to rent: "))
                ordered_items, total_cost = rent_item(items, item_num, quantity, days, customer_name, customer_contact, ordered_items, total_cost)

                continue_choice = input("Press 'Y' to continue shopping or 'N' to proceed to checkout: ")
                if continue_choice.lower() == "n":
                    print_bill(customer_name, customer_contact, ordered_items, total_cost)
                    print("Thank you for using the Rental Shop. Goodbye!")
                    break
        elif choice == "2":
            while True:
                display_inventory(items)  # Show inventory before returning
                item_num = int(input("Enter the item number you want to return: "))
                quantity = int(input("Enter the quantity to return: "))
                return_item(items, item_num, quantity, ordered_items, total_cost)
                
                continue_choice = input("Press 'Y' to continue returning or 'N' to exit returning: ")
                if continue_choice.lower() == "n":
                    break
        elif choice.lower() == "q":
            print("Thank you for using the Rental Shop. Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()