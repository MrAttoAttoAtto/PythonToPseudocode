'''Customer choose components script'''

'''Task 1 setup'''
# var for storing the estimate number, incremented to make unique
estimate_number = 0
# category list
CATEGORIES = ["processor", "RAM", "storage", "case"]
# 3D array for storing categories, choices, and prices
COMPONENTS = [[["P5", 100], ["P7", 200]], [["32GB", 75], ["64GB", 150]], [["1TB", 50], ["2TB", 100]], [["Mini Tower", 100], ["Midi Tower", 150]]]

'''Task 2 setup'''
# stock, starts at 10
STOCK_LEVELS = [[10, 10], [10, 10], [10, 10], [10, 10]]

'''Task 3 setup'''
# total for all orders
ALL_ORDER_TOTAL = 0

total = 0
estimate_number += 1
choice_list = [0, 0, 0, 0]

# 4 categories so 4 times
for i in range(4):
    valid_choice = False
    # while the user has not inputted a 1 or a 2
    while not valid_choice:
        # asks the question, formatted for that part
        choice = input("\nWhat type of " + CATEGORIES[i] + " would you like?\n1. " + COMPONENTS[i][0][0] + "\n2. " + COMPONENTS[i][1][0] + "\nEnter choice: ")
        # checks it is one of the two valid inputs
        if choice == 1 or choice == 2:
            # checks the stock is above 0 - TASK 2
            if STOCK_LEVELS[i][choice-1] > 0:
                valid_choice = True
                STOCK_LEVELS[i][choice-1] -= 1
            else:
                # asks if the user wants to cancel or choose another part - TASK 2
                alt_or_cancel = input("Sorry, that part is out of stock, would you like to cancel (c) or choose and alternative part (a): ")
                if alt_or_cancel == "a":
                    continue
                elif alt_or_cancel == "c":
                    exit()
                
        else:
            print("Invalid choice!")
            continue

    # adds the price to total (-1 because arrays start at 0)
    total += COMPONENTS[i][choice-1][1]
    # adds the choice to the choice list
    choice_list[i] = choice

# applied 20% VAT
total *= 1.2

print("\nEstimate number " + str(estimate_number) + "\nYou chose:")
for i in range(4):
    # prints the formatted parts (4 times as there are 4 parts)
    print(COMPONENTS[i][choice_list[i]-1][0] + " for " + CATEGORIES[i])

print("Total price: £" + str(total))

# until a valid option has been chosen... - TASK 2
place_choice_make = True
while place_choice_make:
    # asks if they want to place the order - TASK 2
    place_choice = input("Would you like to place the order? [y/n] ")
    if place_choice == "n":
        exit()
    elif place_choice == "y":
        place_choice_make = False

# asks the name
name = input("Enter your name: ")

# until a valid email has been entered...
email_needed = True
while email_needed:
    # asks the email
    email = input("Enter your email: ")
    # checks that the email has an @ in it
    if "@" in email:
        email_needed = False
    else:
        print("Invalid email")

# adds this order's total to the total for the day
ALL_ORDER_TOTAL += total
# displays it
print("Today's order total: " + str(ALL_ORDER_TOTAL))

# for every component type (4)
for i in range(4):
    # print the heading
    print("\n" + CATEGORIES[i].title() + " stock: ")
    # for every component choice of that type (2)
    for c in range(2):
        # print the stock
        print(COMPONENTS[i][c][0] + " stock: " + str(STOCK_LEVELS[i][c]))
