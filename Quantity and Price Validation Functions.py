def validate_quantity():
   quantity = ""
   while True:
      try:
         quantity = input("Enter the quantity: ")
         int(quantity)
         while float(quantity) < 0:
            print("enter a value bigger than 0")
            quantity = input("Enter the quantity: ")
         break
      except ValueError:
         print("You entered a string or a float.")
   if '.' in quantity:
      quantity = float(quantity)
   else:
      quantity = int(quantity)
   return quantity

def validate_price():
   price = ""
   while True:
      try:
         price = input("Enter the price: ")
         float(price)
         while float(price) < 0:
            print("enter a value bigger than 0")
            price = input("Enter the price: ")
         break
      except ValueError:
         print("You entered a string")
   if '.' in price:
      price = float(price)
   else:
      price = int(price)
   return price
if __name__ == "__main__":
   print(f"The price is {validate_price()}$.")
   print(f"There are {validate_quantity()} available.")
