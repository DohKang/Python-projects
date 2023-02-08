import random


cards ={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}
pattern = ("Heart", "Diamond", "Spade", "Clover")
card_deck = ["AHeart","2Heart","3Heart","4Heart","5Heart","6Heart","7Heart","8Heart","9Heart","10Heart","JHeart","QHeart","KHeart",\
                "ADiamond","2Diamond","3Diamond","4Diamond","5Diamond","6Diamond","7Diamond","8Diamond","9Diamond","10Diamond","JDiamond","QDiamond","KDiamond",\
                "ASpade","2Spade","3Spade","4Spade","5Spade","6Spade","7Spade","8Spade","9Spade","10Spade","JSpade","QSpade","KSpade",\
                "AClover","2Clover","3Clover","4Clover","5Clover","6Clover","7Clover","8Clover","9Clover","10Clover","JClover","QClover","KClover"]



def user_get_card():
    global current_values, card_deck
    r_number = random.randint(1, 13)
    r_pattern = random.choice(pattern)
    r_card = cards[r_number] + r_pattern
    if r_card in card_deck:
        card_deck.remove(r_card)
        current_values.append(r_number)
    return r_number, r_pattern



def comp_get_card():
    global card_deck, comp_values
    r_number = random.randint(1, 13)
    r_pattern = random.choice(pattern)
    r_card = cards[r_number] + r_pattern
    if r_card in card_deck:
        card_deck.remove(r_card)
        comp_values.append(r_number)
        return r_card
    else:
        comp_get_card()

def check_total(num, total):
    if num == 11 or num == 12 or num == 13:
        num = 10
    elif num == 1 and (total + 11) <= 21:
        num = 11
    return num

#because of user_total global variable, i had to make seperate function for computer




running = True
while running:
    user_total = 0
    current_own = ""
    current_values = []
    f_number, f_pattern = user_get_card()
    s_number, s_pattern = user_get_card()
    first_card = cards[f_number] + f_pattern
    second_card = cards[s_number] + s_pattern
    current_own += first_card +" " + second_card  
    print("Welcome to the blackjack game")
    print("****************************************")
    print(f"Your firstcard is : {first_card}")
    print(f"Your secondcard is : {second_card}")
    print("****************************************")

    
    while user_total < 21:
        response = input("please type \"Y\" to get one more card, \"N\" to stop\n").lower()
        if response == "y":
            x_number, x_pattern = user_get_card()
            card = cards[x_number] + x_pattern
            print(f"You got : {card}")
            current_own += " " + card
            print(f"Your deck : {current_own}")

        elif response == "n":
            # reverse current_values so that we can calculate A last
            sorted_current_values = sorted(current_values)
            print(sorted_current_values)
            sorted_current_values.reverse()
            print(sorted_current_values)
            for x in sorted_current_values:
                user_total += check_total(x, user_total)
            print(user_total)
            break
    
     

    #let computer get a card if total is less than 16
    comp_values =[]
    comp_total = 0
    comp_first_card = comp_get_card()
    comp_second_card = comp_get_card()
    print(f"Computer's first card is : {comp_first_card}")
    print(f"Computer's second card is : {comp_second_card}")
    # comp_total += comp_check_total(comp_first_card)
    # comp_total += comp_check_total(comp_second_card)
    
    sorted_comp_values = sorted(comp_values)
    sorted_comp_values.reverse()
    for i in sorted_comp_values:
        comp_total += check_total(i, comp_total)
        
    while comp_total <= 16:
        comp_values.clear()
        comp_new_card = comp_get_card()
        comp_total += check_total(comp_values[0], comp_total)
    

    if user_total <= 21 and user_total > comp_total:
        print("\nGreat, You won against computer, YAY!")
        break
    elif comp_total <= 21 and comp_total > user_total:
        print("\nComputer win")
        break
    elif user_total >= 22 and comp_total >= 22:
        print("draw")
    elif user_total >= 22 and comp_total <= 21:
        print("\nComputer win")
    elif comp_total >= 22 and user_total <= 21:
        print("\nGreat, You won against computer, YAY!")

        
        
        
        






        
