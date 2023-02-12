
#========Class==========
class Shoe:
    '''Defines a class for shoe objects with attributes country, code, product, cost and quantity'''
    def __init__(self, country, code, product, cost, quantity):
        self.country = country 
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
       
    def get_cost(self):
        ''' Returns the cost of the shoe object.'''
        return self.cost
        
    def get_quantity(self):
        ''' Returns  the quantity assigned to the shoe object.'''
        return self.quantity
        
    def __str__(self):
        ''' Defines a string that is returned when the shoe object is printed.'''
        return (f"Country: {self.country}, Code: {self.code}, Product: {self.product}, Cost: R{self.cost}, Quantity: {self.quantity}")
     

#=============Shoe list===========

''' The list will be Tused to store a list of shoe objects'''
shoe_list = []

#==========Functions outside the class==============
def read_shoes_data():
    '''
    Opens the inventory file and reads the data, processes it and creates a Shoe object from each line.
    Adds the object to the shoe_list.

    Returns:
    shoe_list

    Raises:
    FileNotFoundError if file not found
    Exception message if file contents not able to be processed correctly
    '''
    
    try:
        # Opens and reads file to stock_data list
        with open("inventory.txt","r") as f:
            stock_data = f.readlines()
            # Splits each item at the , and adds the split lines to split_data list
            split_data = [i.split(",") for i in stock_data]
            
            # Removes the header data
            del split_data[0]  

            # Loops through the split data, creating a Shoe object for each line and adding it to shoe_list
            for i in split_data:
                shoe_obj = Shoe(i[0],i[1],i[2],i[3],i[4].strip("\n"))
                shoe_list.append(shoe_obj)
            
            return shoe_list

    # If the inventory file is not in the folder, prints an error message and exits function
    except FileNotFoundError:
        print("The file you are trying to read does not exist in this location.")
        return

    # If there are any other problems with the inventory file, prints an error message and exits function
    except Exception:
        print("There was a problem with the file contents.")
        return
  
def capture_shoes():
    ''' Creates a shoe object from country, code, product, cost and quantity inputs and adds the new object to the shoe_list'''
    # Gets input of all arguments from user
    country = input("Enter the country:\n")
    code = input("Enter a unique product code:\n")
    product = input("Enter the name of the shoe style:\n")
    cost = input("Enter the price per pair in South African Rand:\n")
    quantity = input("Enter the number of pairs in stock:\n")
    
    # Feeds arguments to Shoe class to create new object, appends it to the shoe_list and prints confirmation message
    new_shoe_obj = Shoe(country,code,product,cost,quantity)
    shoe_list.append(new_shoe_obj)

    # Opens the inventory file and writes the updated shoe_list plus column headers back into the file (overwriting existing data)
    with open('inventory.txt','w+') as f: 
        f.write('Country,Code,Product,Cost,Quantity')  
        for shoe in shoe_list:
            f.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}") 

    print(f"\nThe following product has been added to the system:\n\n\t{new_shoe_obj}")
    
def view_all():
    '''Iterates over the shoe_list and prints the details of the shoes returned from the __str__ function. '''
    print("\n-------------------------------SHOE STOCK DATA--------------------------------\n")
    
    for shoe in shoe_list:
        print(shoe)

    print("--------------------------------------------------------------------------------\n")
    
def re_stock():
    ''' Finds shoe with lowest quantity, asks for a restock number and updates file with new total '''
    # Sets a nominal starting max stock number, then iterates through list comparing each object's quantity to it and 
    # assigning the lowest value to the variable. 
    lowest_stock = 1000
    for shoe in shoe_list:
        if int(shoe.quantity) < lowest_stock:
            lowest_stock = int(shoe.quantity)
            # Pulls out the shoe object with the lowest stock and assigns it to this variable
            lowest_stock_shoe = shoe

    # Gets input of quantity to add to the existing stock (restock figure)        
    top_up = int(input(f'''\nThe item with the lowest stock is:

    {lowest_stock_shoe}
    
How many would you like to add to the quantity? '''))
    
    # Sets the quantity of that object to the original quantity plus the restock quantity
    lowest_stock_shoe.quantity = lowest_stock + top_up 

    print(f"\nThank you. The new stock quantity is: {lowest_stock_shoe.quantity}")

    # Iterates through the list, finding the shoe object by code and assigning the total new quantity to the object in the list
    for shoe in shoe_list:
        if shoe.code == lowest_stock_shoe.code:
            shoe.quantity = lowest_stock_shoe.quantity

    # Opens the inventory file and writes the updated shoe_list plus column headers back into the file (overwriting existing data)
    with open('inventory2.txt','w+') as f:   
        f.write('Country,Code,Product,Cost,Quantity')
        for shoe in shoe_list:
            f.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}") 

   
def highest_qty():
    ''' Finds the shoe with the highest stock quantity and allows the user to calculate a discount sale price. '''
    # Sets a checking variable to 0, then iterates through list comparing each object's quantity to it and assigning the lowest value to the variable. 
    highest_stock = 0
    for shoe in shoe_list:
        if int(shoe.quantity) > highest_stock:
            highest_stock = int(shoe.quantity)
            highest_stock_shoe = shoe

    # Prints the string for the shoe with the highest stock quantity, asks user to choose whether to apply a discount, and calculates the price based on the discount
    while True:       
        # Displays highest stock item and user inputs choice of whether to put shoe on sale
        on_sale = input(f'''
The item with the highest stock quantity is:

    {highest_stock_shoe}
        
Do you want to put this shoe on sale (recommended)? Enter Y or N: ''').lower()

        # If user chooses to put shoe on sale, this validates the input and asked to choose a discount %
        if on_sale == "y":
            while True:
                try:
                    discount = int(input("\nWhat percentage discount will you offer (5-70%)? "))

                    # Returns to start of loop if input is outside boundaries
                    if discount > 70 or discount < 5:
                        print("\nYou must enter a discount between 5% and 70%")
                        continue
                    
                    # Calculates the new sale price
                    sale_price = int(highest_stock_shoe.cost)*((100-discount)/100)
            
                    # Prints the discount requested and the sale price rounded to nearest 10
                    print(f"\nThe sale price at a {discount}% discount is R{int(round(sale_price,-1))}, rounded to the nearest 10.")
                    return

                # Returns an error message if the discount input cannot be cast to int
                except ValueError:
                    print("\nSorry, the input must be a number. Try again.")
                    continue

        # Exits function if user doesn't want to discount shoe price
        elif on_sale == "n":
            return

        else: 
            print("Sorry, that's not a valid input. Try again.")
            continue
    
def search_shoe():
    ''' Searches for a shoe from the list using the code and returns the object. '''
    code = input("\nEnter the product code of the shoe you want to find: ")
    search_result = ""
    shoe_found = False
    for shoe in shoe_list:
        if shoe.code == code:
            search_result = shoe
            shoe_found = True
    if shoe_found == False:
        search_result = "\nSorry, there are no products with that code."
    return search_result

def value_per_item():
    ''' Calculates the total value for each item (cost * quantity) and prints this information for all the shoes. '''
    print(f"\nThe total value of the stock for each item is:\n\n")
    
    # Iterates through shoe_list and prints the code, shoe name and total value of stock for each
    for shoe in shoe_list:
        print(f"{shoe.code}, {shoe.product}: R{int(shoe.cost)*int(shoe.quantity)}")
    

#==========Main Menu=============
''' A menu that executes each function above. '''

print("\n Welcome to the product database.")

# Main menu listing
while True:

    user_choice = int(input('''
------------------------------MAIN MENU-----------------------------
1 - View all products in the database
2 - Enter a new product
3 - Find a product using the product code
4 - Find and add stock to the item with the smallest stock quantity
5 - Find the item with the highest stock quantity and put on sale 
6 - Calculate the value of all stock
7 - Exit the programme
--------------------------------------------------------------------

Input your selection here: '''))

    # If user chooses 1, this reads all the items from the file into the object list and then prints all the data 
    if user_choice == 1:
        read_shoes_data()
        view_all()

    # If user chooses 2, this gets input from user of all the attributes of the object, creates an object and adds it to the list and the file
    elif user_choice == 2:
        read_shoes_data()
        capture_shoes()

    # If user chooses 3, this reads all the items from the file into the object list, gets input of a code from the user and finds and returns the object corresponding
    elif user_choice == 3:
        read_shoes_data()
        print(f"\n{search_shoe()}")

    # If user chooses, 4, this reads all the items from the file into the object list, finds the lowest stock object, takes input of a restock figure and writes new total back to the file
    elif user_choice == 4:
        read_shoes_data()
        re_stock()
        
    elif user_choice == 5:
        read_shoes_data()
        highest_qty()

    elif user_choice == 6:
        read_shoes_data()
        value_per_item()

    elif user_choice == 7:
        print("Thank you. Closing the programme now.")
        exit()

    elif user_choice > 7 or user_choice >1:
        print("That's not a valid option. Try again.")
        continue

    else: 
        print("That's not a valid option. Try again.")
        continue


    
  