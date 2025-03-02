import random
import time

def blackjack():
    print("♠️♥️♦️♣️ Welcome to Blackjack! ♠️♥️♦️♣️")
    time.sleep(2)

    while True:
        start = input("\nDo you want to start the game? (y/n) ").strip().lower()
        
        if start == "y":
            cards = {"A": 11, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, 
                     "8": 8, "9": 9, "10": 10, "K": 10, "Q": 10, "J": 10}

            def deal_card():
                return random.choice(list(cards.keys()))

            def calculate_hand(hand):
                total = sum(cards[card] for card in hand)
                num_aces = hand.count("A")
                while total > 21 and num_aces > 0:
                    total -= 10
                    num_aces -= 1
                return total

            player_hand = [deal_card(), deal_card()]
            dealer_hand = [deal_card(), deal_card()]
            
            time.sleep(2)
            print(f"\nYour cards: {player_hand}, Total: {calculate_hand(player_hand)}")
            time.sleep(2)
            print(f"\nDealer's first card: {dealer_hand[0]}")
            time.sleep(2)

            while calculate_hand(player_hand) < 21:
                action = input("\nDo you want to 'hit' or 'stand'? ").strip().lower()
                if action == "hit":
                    player_hand.append(deal_card())
                    time.sleep(2)
                    print(f"\nYour cards: {player_hand}, Total: {calculate_hand(player_hand)}")
                else:
                    break

            player_total = calculate_hand(player_hand)
            time.sleep(2)

            if player_total > 21:
                print(f"\n💀 Busted! Your total is {player_total}. Try again, loser! 😈")
            else:
                print("\nDealer's turn... 🃏")
                time.sleep(2)

                while calculate_hand(dealer_hand) < 17:
                    dealer_hand.append(deal_card())
                    time.sleep(2)
                    print(f"\nDealer draws a card... {dealer_hand[-1]}")

                dealer_total = calculate_hand(dealer_hand)
                time.sleep(2)
                print(f"\nDealer's final hand: {dealer_hand}, Total: {dealer_total}")

                if dealer_total > 21 or player_total > dealer_total:
                    print(f"\n🎉 You win! {player_hand} ({player_total}) beats {dealer_hand} ({dealer_total})!")
                    print("Was it luck or skill? Prove it and play again! 😏")
                elif player_total < dealer_total:
                    print(f"\n😈 You lost! {player_hand} ({player_total}) vs. {dealer_hand} ({dealer_total})")
                    print("Try again, but you still won’t beat me... 🤡")
                else:
                    print("\n🤝 It's a tie! But are you really that lucky? Play again!")

            time.sleep(2)
            play_again = input("\nDo you want to play again? (y/n) ").strip().lower()
            if play_again != "y":
                print("\nCoward... Come back when you're ready to lose again. 😆")
                break
        elif start == "n":
            print("\n🐔 Scared, huh? Maybe next time...")
            break
        else:
            print("\nBruh, type 'y' or 'n'. Even a monkey could do that. 🐵")
