# POS System for Best Buy Retail Store

# Product catalog
products = {
    "Rice": {"price": 1200, "stock": 20},
    "Flour": {"price": 800, "stock": 15},
    "Milk": {"price": 300, "stock": 25},
    "Bread": {"price": 250, "stock": 30},
    "Eggs": {"price": 500, "stock": 10},
    "Sugar": {"price": 600, "stock": 12},
    "Cooking Oil": {"price": 1500, "stock": 8},
    "Soap": {"price": 200, "stock": 18},
    "Toothpaste": {"price": 350, "stock": 14},
    "Juice": {"price": 400, "stock": 22},
}
# Declare Constants
TAX_RATE = 0.10
DISCOUNT_RATE = 0.05
DISCOUNT_THRESHOLD = 5000

# display products - Names, price and amount in stock
def display_products():
    print("\nAvailable Products:")
    print("-" * 40)
    for item, details in products.items():
        print(f"{item:<15} | Price: ${details['price']:>5} | Stock: {details['stock']}")
    print("-" * 40)

#Add item to cart
def add_to_cart(cart):
    try:
        item = input("Enter product name: ").title()
        # Check if product exists
        if item not in products:
            print("Product not found.")
            return

        quantity = int(input("Enter quantity: "))
        #Validate quantity
        if quantity <= 0:
            print("Invalid quantity.")
            return

        if quantity > products[item]["stock"]:
            print("Not enough stock available.")
            return

        # Add to cart and update stock
        if item in cart:
            cart[item] += quantity
        else:
            cart[item] = quantity

        #Reduce stock after adding to cart
        products[item]["stock"] -= quantity
        print(f"Added {quantity} {item} to cart.")

#Handle invalid input (non integer)
    except ValueError:
        print("Invalid input. Please enter numeric values.")

#Remove item from cart
def remove_from_cart(cart):
    item = input("Enter product name to remove: ").title()

    #Check if item is in cart
    if item not in cart:
        print("Item not in cart.")
        return

    try:
        quantity = int(input(f"Enter quantity to remove (Current: {cart[item]}): "))
        #Validate quantity
        if quantity <= 0:
            print("Invalid quantity.")
            return

        if quantity >= cart[item]:
            products[item]["stock"] += cart[item]
            del cart[item]
            print(f"All {item} removed from cart.")
        else:
            cart[item] -= quantity
            products[item]["stock"] += quantity
            print(f"Updated {item} quantity.")
    except ValueError:
        print("Invalid input.")

#View items in cart
def view_cart(cart):
    #Check if cart is empty
    if not cart:
        print("\nCart is empty.")
        return

    print("\nShopping Cart:")
    print("-" * 40)
    subtotal = 0
   #Loop through cart items
    for item, qty in cart.items():
        price = products[item]["price"]
        item_total = price * qty
        subtotal += item_total
        print(f"{item:<12} | Qty: {qty:>2} | Unit: ${price:>4} | Total: ${item_total:>5}")
    
    print("-" * 40)
    print(f"Subtotal: ${subtotal:.2f}") #print subtotal as currency with 2 decimal places

# generate the receipt based on items in the cart
def generate_receipt(cart, subtotal, discount, tax, total, payment, change):
    print("\n" + "=" * 40)
    print("      BEST BUY RETAIL STORE")
    print("-" * 40)
    for item, qty in cart.items():
        price = products[item]["price"]
        print(f"{item:<15} x{qty:<2} @ ${price*qty:>7.2f}")
    
    print("-" * 40)
    print(f"Subtotal:         ${subtotal:>10.2f}")
    print(f"Discount:        -${discount:>10.2f}")
    print(f"Tax (10%):        ${tax:>10.2f}")
    print(f"TOTAL:            ${total:>10.2f}")
    print(f"Paid:             ${payment:>10.2f}")
    print(f"Change:           ${change:>10.2f}")
    print("-" * 40)
    print("      Thank you for Shopping!")
    print("=" * 40)

def checkout(cart):
    if not cart:
        print("Cart is empty.")
        return

    #Calculate subtotal using generator expression
    subtotal = sum(products[item]["price"] * qty for item, qty in cart.items())
    
    discount = 0
    #Apply discount
    if subtotal > DISCOUNT_THRESHOLD:
        discount = subtotal * DISCOUNT_RATE # Corrected formula: rate is a percentage

    taxed_amount = (subtotal - discount) * TAX_RATE
    #Apply tax after discount
    total = subtotal - discount + taxed_amount

    #Display checkout summary
    print(f"\n--- Checkout Summary ---")
    print(f"Total Due: ${total:.2f}")

    #Payment loop to ensure valid payment
    while True:
        try:
            payment = float(input("Enter payment amount: "))
            #Validate sufficient payment
            if payment < total:
                print(f"Insufficient payment. You still owe ${total - payment:.2f}")
            else:
                change = payment - total
                #Generate receipt
                generate_receipt(cart, subtotal, discount, taxed_amount, total, payment, change)
                #Clear cart after successful transaction
                cart.clear()
                low_stock_alert()
                break
        except ValueError:
            print("Invalid input.")

#Display low stock warning
def low_stock_alert():
    alerts = [item for item, details in products.items() if details["stock"] < 5]
    if alerts:
        print("\n[!] LOW STOCK ALERT:")
        for item in alerts:
            print(f" - {item}: {products[item]['stock']} remaining")

def main():
    #Loop to keep the system running until user enter the number 7
    while True:
        cart = {} 
        while True:
            print("\n===== POS MENU =====")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. New Transaction (Clear Cart)")
            print("7. Exit")

            choice = input("Enter choice: ")

            #Menu selection handling
            if choice == "1":
                display_products() # Call the Display product function
            elif choice == "2":
                add_to_cart(cart) # Call the Add to Cart function
            elif choice == "3":
                remove_from_cart(cart)# Call the Remove from cart function
            elif choice == "4":
                view_cart(cart)# Call the View Cart function
            elif choice == "5":
                if not cart:
                    print("Cart is empty.")
                else:
                    checkout(cart)# Call the Checkout function
                    break # End transaction after checkout
            elif choice == "6":
                print("Starting new transaction...")
                break
            elif choice == "7":
                print("Exiting System...")
                return
            else:
                print("Invalid choice.")

# Call the main Function at the start of the program
main()
