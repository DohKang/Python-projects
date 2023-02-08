import random

cards ={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}
pattern = ("Heart", "Diamond", "Spade", "club")
# deck = ["A Heart","2 Heart","3 Heart","4 Heart","5 Heart","6 Heart","7 Heart","8 Heart","9 Heart","10 Heart","J Heart","Q Heart","K Heart",\
#                 "A Diamond","2 Diamond","3 Diamond","4 Diamond","5 Diamond","6 Diamond","7 Diamond","8 Diamond","9 Diamond","10 Diamond","J Diamond","Q Diamond","K Diamond",\
#                 "A Spade","2 Spade","3 Spade","4 Spade","5 Spade","6 Spade","7 Spade","8 Spade","9 Spade","10 Spade","J Spade","Q Spade","K Spade",\
#                 "A Clover","2 Clover","3 Clover","4 Clover","5 Clover","6 Clover","7 Clover","8 Clover","9 Clover","10 Clover","J Clover","Q Clover","K Clover"]

def get_card():
    global current_values, card_deck # by adding clear function after user judge loop, we can reuse this array for computer one. delete another function
    r_number = random.randint(1, 13)
    r_pattern = random.choice(pattern)
    r_card = cards[r_number] + " " + r_pattern
    if r_card in card_deck:
        card_deck.remove(r_card)
        current_values.append(r_number)
    else:
        return get_card() # if card is not in card_deck. repick random card from deck
    return r_card
#by adding another argument in here. I could conduct check_total for both user and computer.
def check_total(num, total):
    if num == 11: 
        num = 10.1 
    elif num == 12: 
        num = 10.2
    elif num == 13: 
        num = 10.3
    elif num == 1 and int(total + 11) <= 21: #instead of float, just use integer value to compare
        num = 11
    print("I am here checking totalTTTTTTTTTTTTTTTTTTTTTT")
    
    return num

def check_A(arr):
    temp_arr = []
    while 1 in arr:
        arr.remove(1)
        temp_arr.append(1)
    return arr + temp_arr


def game_over():
    global running
    play = input("Do you want to continue? press \"Y\" to continue, \"N\" to stop").lower()
    if play == "n":
        running = False


deck = []
for i in pattern:
    for j in cards.values():
        deck.append(j + " " + i) # found efficient way to create cards

card_deck = deck[:] #using [:] to copy the array without using built in method
running = True

while running:
    user_qualified = False
    computer_qualified = False
    user_total = 0
    current_own = ""
    current_values = []
    first_card = get_card()
    second_card = get_card()
    current_own += first_card +" " + second_card  
    print("Welcome to the blackjack game")
    print("****************************************")
    print(f"Your firstcard is : {first_card}")
    print(f"Your secondcard is : {second_card}")
    print("****************************************")

    while True:   #if under 22, not 21 -> just true
        #adding game rule that if user total over 21, it immediately end game, instead of giving choices to get more card or not
        if 1 in current_values: # to increase work efficiency, only if 1 in current_value, we are going to sort through
            current_values = check_A(current_values)
            print("I just checked AAAAAAAAAAAAAA", current_values)
        for x in current_values:
            user_total += check_total(x, user_total)
        current_values.clear() # clean up array for next calculation
        print("User total is : ", user_total)
        if user_total >= 22:
            print("============================")
            print(f"Your total is {user_total}.")
            print("++++++++++++++++COMP WIN++++++++++++++++")
            game_over()
            break
        print(f"Your current card : {current_own}")
        response = input("please type \"Y\" to get one more card, \"N\" to stop").lower()
        if response == "y":
            new_card = get_card() #only one return value required
            print(f"You got : {new_card}")
            current_own += " " + new_card
        elif response == "n":
            user_qualified = True # if user_total is <= 21, proceed
            break #we bring user_total calculation above. No need to double calculating the user_total
    if user_qualified:
        current_values.clear() #clear out current_value so that we can reuse this empty array for computer
        #let computer get a card if total is less than 16
        comp_total = 0
        comp_first_card = get_card()
        comp_second_card = get_card()
        print(f"Computer's first card is : {comp_first_card}")
        print(f"Computer's second card is : {comp_second_card}")
        # comp_total += comp_check_total(comp_first_card)
        # comp_total += comp_check_total(comp_second_card)
        if 1 in current_values:
            current_values = check_A(current_values)  #only 1 in current_values, we are conducting sort function
            print("I just checked AAAAAAAAAAAAAA", current_values)
        for i in current_values:
            comp_total += check_total(i, comp_total)
        current_values.clear()
        while int(comp_total) < 16:
        #int(comp_total) <= 16.7: # case of (10 and six) -> cause comp to get one more card even though it's int value is already16
        #current_value part no needed anymore beacuse user while loop clear current_value everytime it loops
            comp_new_card = get_card()
            print(f"Computer got one more card : {comp_new_card}")
            comp_total += check_total(current_values[0], comp_total)
            
        if comp_total >= 22:
            print("============================")
            print(f"Computer total is {comp_total}.")
            print("++++++++++++++++USER WIN++++++++++++++++")
            game_over()
        else:
            print(comp_total)
            computer_qualified = True  #if computer number is > 21 proceed
    if computer_qualified:
    #judging part
            if  user_total > comp_total:
                print("\nGreat, You won against computer, YAY!")
            elif comp_total > user_total:
                print("\nComputer win")
            elif user_total == comp_total:
                print("Draw")
            game_over()
    #put other conditions that if user or comp total value over 21.7
    if len(card_deck) < 25: # if card deck has less than 15 cards left. replenish with a new
        card_deck = deck[:] #without using copy() built in method
    print("================================================================================")
    print("================================================================================")
    print("================================================================================")
    print("Left in the deck:", len(card_deck))
            
        
""" A thing to fix
if A appears in first 2 cards,
it automatically calculate it as a 11. And cause a math problem
ex) A, 9, 8 > 21 it calculate as 28..
ex2) 9, A, 4 > 21 it calculates as 24 
"""