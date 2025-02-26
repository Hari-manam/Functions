#calculate total price in a shopping cart
def calculate_total(cart):
    total = sum(item["price"]*item["quantity"] for item in cart)
    return total

cart = [
    {"name":"laptop", "price":800, "quantity":1},
        {"name":"mouse", "price":50, "quantity":2 }]

print(f"total price: ${calculate_total(cart)}")

#2(banking and payment section)
def validate_transaction(balance, withdrawal_amount):
    if withdrawal_amount > balance:
        print("insufficient funds")
    else:
        print("transaction succesful")
print(validate_transaction(100,50))

