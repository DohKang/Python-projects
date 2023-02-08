import random
import time

hearts = chr(9829)
diamonds = chr(9830)
spades = chr(9824)
clubs = chr(9827)
#this will create actual card suits characters for better game experience
cards ={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10", 11:"J", 12:"Q", 13:"K"}
pattern = (hearts, diamonds, spades, clubs )
deck = []
for i in pattern:
    for j in cards.values():
        deck.append(j + " " + i) # found efficient way to create cards
card_deck = deck[:] #using [:] to copy the array without using built in method



class Blackjack():
    def __init__(self):
        self.user_qualified = False
        self.computer_qualified = False
        self.current_values = []
        self.user_total = 0
        self.a_count = 0
        self.user_first_card = self.get_card()
        self.user_second_card = self.get_card()
        self.user_current_own = self.user_first_card + " , " + self.user_second_card
        self.intro = self.get_intro()
        self.ask_user = self.go_ask_user()
        self.computer_total = 0
        self.computer_turn = self.get_computer_turn()
        self.judge = self.get_judged()
        self.refil_deck = self.refill_card_deck()

    def get_card(self):
        global card_deck
     # by adding clear function after user judge loop, we can reuse this array for computer one. delete another function
        r_number = random.randint(1, 13)
        r_pattern = random.choice(pattern)
        r_card = cards[r_number] + " " + r_pattern
        if r_card in card_deck:
            card_deck.remove(r_card)
            self.current_values.append(r_number)
        else:
            return self.get_card() # if card is not in card_deck. repick random card from deck
        return r_card

    def lets_check_total(self, total):
        for x in self.current_values:
            if x == 11: 
                x = 10.1 
            elif x == 12: 
                x = 10.2
            elif x == 13: 
                x = 10.3
            elif x == 1: 
                self.a_count += 1
            total += x
        self.current_values.clear()
        return total
        
    def lets_add_a(self, total): # take only one argument and bring global variable a_count
        # print("I have this much a_count in my pocket:", a_count)
        while self.a_count:
            if not self.user_qualified:
                if total + 10 < 22:
                    total += 10
                
            elif self.user_qualified:
                if int(total) + 10 >= 16 and int(total) + 10 < 22: #A, 2, K, A, 3y
                    total += 10
                elif int(total) < 6: # if A 3 A 2 4 5 5 -> over 16  <- A 3 A 2= 17
                    break
            self.a_count -= 1
        return total
        # print("I should be 0 right?", a_count)
        # return total    
    
    def go_ask_user(self):
        while True:
            self.user_total = self.lets_check_total(self.user_total)
            if self.user_total >= 22:
                print("===========================")
                print("You busted!")
                print(f"Your total is {int(self.user_total)}") #In user experience perspective, seeing fraction is not pleasant.
                print("Sorry, Computer won :(".upper()) #finish all end sentence with capitals
                self.game_over()
                break
            print(f"Your current cards: {self.user_current_own}\n")
            print("Would you like to get another card?") #Hit or stand -professional terminology
            response = input("Enter \"Y\" for yes\nEnter \"N\" for no\n").lower()
            if response == "y":
                new_card = self.get_card() #only one return value required
                print(f"You got {new_card}")
                self.user_current_own += " , " + new_card
            elif response == "n":
                if self.a_count:
                    self.user_total = self.lets_add_a(self.user_total)
                if int(self.user_total) == 21: #when user get 21
                    print("\n *******BLACK JACK*******")
                    print("Congratulations! You won against computer, YAY!".upper())
                    self.game_over()
                    break
                self.user_qualified = True
                break

                

    def get_intro(self):
        print("Welcome to the blackjack game")
        print("****************************************")
        print(f"Your first card is {self.user_first_card}")
        print(f"Your second card is {self.user_second_card}")
        print("****************************************")

    def get_computer_turn(self):
        if self.user_qualified:
            input("\nComputer's turn, press \"Enter\" to continue")
            #let computer get a card if total is less than 16
            comp_first_card = self.get_card()
            comp_second_card = self.get_card()
            print(f"\nComputer's first card is : {comp_first_card}")
            print(f"Computer's second card is : {comp_second_card}")
            time.sleep(2) # second base
            self.computer_total = self.lets_check_total(self.computer_total)
            self.computer_total = self.lets_add_a(self.computer_total)
            while int(self.computer_total) < 16:
            #int(comp_total) <= 16.7: # case of (10 and six) -> cause comp to get one more card even though it's int value is already16
            #current_value part no needed anymore beacuse user while loop clear current_value everytime it loops
                comp_new_card = self.get_card()
                print(f"Computer got one more card : {comp_new_card}")
                self.computer_total = self.lets_check_total(self.computer_total)
                self.computer_total = self.lets_add_a(self.computer_total)
            if self.computer_total >= 22:
                print("===========================")
                print("Computer busted!")
                print(f"Computer total is {int(self.computer_total)}") #In user experience perspective, seeing fraction is not pleasant.
                print("Congratulations! You won against computer, YAY!".upper())
                self.game_over()
            elif int(self.computer_total) == 21:  #when computer got 21
                print("*******Computer got BLACK JACK *******")
                print("Sorry, Computer won :(".upper())
                self.game_over()
            else:
                self.computer_qualified = True  #if computer number is > 21 proceed
    def get_judged(self):
        if self.computer_qualified:
    #judging part
            time.sleep(1) #0.5sec
            if int(self.user_total) == int(self.computer_total):
                print(f"\nYou got {int(self.user_total)} and Computer got {int(self.computer_total)}")
                print("It's a draw".upper())
            elif  self.user_total > self.computer_total:
                print(f"\nYou got {int(self.user_total)} and Computer got {int(self.computer_total)}")
                print("Congratulations! You won against computer, YAY!".upper())
            elif self.computer_total > self.user_total:
                print(f"\nYou got {int(self.user_total)} and Computer got {int(self.computer_total)}")
                print("Sorry, Computer won :(".upper())
            self.game_over()

    def game_over(self):
        global running
        self.refill_card_deck()
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
    def refill_card_deck(self):
        global card_deck
        if len(card_deck) < 20:
            card_deck = deck[:]




if __name__ == "__main__":
    running = True
    while running:
        Blackjack()