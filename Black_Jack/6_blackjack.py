import random
import time #User experience perspective, put some sleeping time between computer's hands

hearts = chr(9829)
diamonds = chr(9830)
spades = chr(9824)
clubs = chr(9827)
#this will create actual card suits characters for better game experience
cards ={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}
pattern = (hearts, diamonds, spades, clubs )

def get_card():
    global card_deck # by adding clear function after user judge loop, we can reuse this array for computer one. delete another function
    r_number = random.randint(1, 13)
    r_pattern = random.choice(pattern)
    r_card = cards[r_number] + " " + r_pattern
    if r_card in card_deck:
        card_deck.remove(r_card)
        current_values.append(r_number)
    else:
        return get_card() # if card is not in card_deck. repick random card from deck
    return r_card

def add_a(total): # take only one argument and bring global variable a_count
    global user_qualified, a_count
    # print("I have this much a_count in my pocket:", a_count)
    while a_count:
        if not user_qualified:
            if total + 10 < 22:
                total += 10
            
        elif user_qualified:
            if int(total) + 10 >= 16 and int(total) + 10 < 22: #A, 2, K, A, 3y
                total += 10
            elif int(total) < 6: # if A 3 A 2 4 5 5 -> over 16  <- A 3 A 2= 17
                break
        a_count -= 1
    # print("I should be 0 right?", a_count)
    return total
#by adding another argument in here. I could conduct check_total for both user and computer.
def check_total(num):
    global a_count
    if num == 11: 
        num = 10.1 
    elif num == 12: 
        num = 10.2
    elif num == 13: 
        num = 10.3
    elif num == 1: 
        a_count += 1
    return num

def game_over():
    global running
    time.sleep(1)
    print("===========================")
    play = input("\nDo you want to play again? Insert coin now.\nPress \"Enter\" to continue\nPress \"N\" to end\n").lower()
    if play == "n":
        running = False
        print("\n\nThank you for playing DK-BLACKJACK")
        print("Hope you have a great rest of your day! :)")
        print("       ==========DK==========       ")
    else:
        print("================================================================================")
        print("==================New Game is being assembled===================================")
        print("================================================================================")
        time.sleep(2)
#######################################################################################################################
 
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
    a_count = 0
    first_card = get_card()
    second_card = get_card()
    current_own += first_card +" , " + second_card  
    print("Welcome to the blackjack game")
    print("****************************************")
    print(f"Your first card is {first_card}")
    print(f"Your second card is {second_card}")
    print("****************************************")

    while True:   #if under 22, not 21 -> just true
        #adding game rule that if user total over 21, it immediately end game, instead of giving choices to get more card or not
        for x in current_values:
            user_total += check_total(x)
        current_values.clear() # clean up array for next calculation
        if int(user_total) > 22:
            print("===========================")
            print("You busted!")
            print(f"Your total is {int(user_total)}") #In user experience perspective, seeing fraction is not pleasant.
            print("Sorry, Computer won :(".upper()) #finish all end sentence with capitals
            game_over()
            break

        print(f"Your current cards: {current_own}\n")
        print("Would you like to get another card?") #Hit or stand -professional terminology
        response = input("Enter \"Y\" for yes\nEnter \"N\" for no\n").lower()
        if response == "y":
            new_card = get_card() #only one return value required
            print(f"You got {new_card}")
            current_own += " , " + new_card
        elif response == "n":
            if a_count:
                user_total = add_a(user_total)
            if int(user_total) == 21: #when user get 21
                print("\n *******BLACK JACK*******")
                print("Congratulations! You won against computer, YAY!".upper())
                game_over()
                break
            user_qualified = True # if user_total is <= 21, proceed
            break #we bring user_total calculation above. No need to double calculating the user_total
    if user_qualified:
        input("\nComputer's turn, press \"Enter\" to continue")
        current_values.clear() #clear out current_value so that we can reuse this empty array for computer
        #let computer get a card if total is less than 16
        comp_total = 0
        comp_first_card = get_card()
        comp_second_card = get_card()
        print(f"\nComputer's first card is : {comp_first_card}")
        print(f"Computer's second card is : {comp_second_card}")
        time.sleep(2) # second base

        for i in current_values:
            comp_total += check_total(i)
        if a_count:
            comp_total = add_a(comp_total)
        current_values.clear()
        while int(comp_total) < 16:
        #int(comp_total) <= 16.7: # case of (10 and six) -> cause comp to get one more card even though it's int value is already16
        #current_value part no needed anymore beacuse user while loop clear current_value everytime it loops
            comp_new_card = get_card()
            print(f"Computer got one more card : {comp_new_card}")
            comp_total += check_total(current_values[0])
            current_values.clear() # if computer gets more than 3 cards in total. we need to clear this. otherwise computer computes with the third card forever.
            if a_count:
                comp_total = add_a(comp_total)
        if comp_total >= 22:
            print("===========================")
            print("Computer busted!")
            print(f"Computer total is {int(comp_total)}") #In user experience perspective, seeing fraction is not pleasant.
            print("Congratulations! You won against computer, YAY!".upper())
            game_over()
        elif int(comp_total) == 21:  #when computer got 21
            print("*******Computer got BLACK JACK *******")
            print("Sorry, Computer won :(".upper())
            game_over()
            break
        else:
            computer_qualified = True  #if computer number is > 21 proceed
    if computer_qualified:
    #judging part
        time.sleep(1) #0.5sec
        if int(user_total) == int(comp_total):
            print(f"\nYou got {int(user_total)} and Computer got {int(comp_total)}")
            print("It's a draw".upper())
        elif  user_total > comp_total:
            print(f"\nYou got {int(user_total)} and Computer got {int(comp_total)}")
            print("Congratulations! You won against computer, YAY!".upper())
        elif comp_total > user_total:
            print(f"\nYou got {int(user_total)} and Computer got {int(comp_total)}")
            print("Sorry, Computer won :(".upper())
        game_over()
    if len(card_deck) < 20: # if card deck has less than 15 cards left. replenish with a new
        card_deck = deck[:] #without using copy() built in method
    # print("Left in the deck:", len(card_deck)) #checking deck gets refreshed if certain condition met

# Your second card is 10 ♥
# ****************************************
# Your current cards: Q ♠ , 10 ♥

# Would you like to get another card?
# Enter "Y" for yes
# Enter "N" for no
# n

# Computer's turn, press "Enter" to continue

# Computer's first card is : 3 ♦
# Computer's second card is : 5 ♥
# Computer got one more card : 2 ♠
# Computer got one more card : 10 ♣

# You got 20 and Computer got 20

# CONGRATULATIONS! YOU WON AGAINST COMPUTER, YAY!

#----> fixed look line 160