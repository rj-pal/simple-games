import tkinter as tk
from tkinter import messagebox
from games.solitaire import Solitare
from utils.errors import *
from utils.emojis import *
class SolitaireGUI:
    """SolitaireGUI class manages the GUI and backend state for a Solitaire desktop application."""
    def __init__(self, master):
        self.master = master
        master.title("Solitaire - Emoji Edition")
        master.geometry("1200x1000")
        master.configure(bg="#006400") # Dark green felt color
        # master.configure(bg="#640032") # Test color

       
        # Initialize the Solitaire backend game state within the GUI class
        self.game = Solitare(klondike_value=3)
        self.selected_item = None
        self.highlighted_widget = None
        self.foundation_suit_in_play = None
        self.reset = False
        
        # Define the emoji card characters from utilities
        self.card_back_emoji = FACE_DOWN_EMOJI
        self.card_back_empty_pile = EMPTYPILEEMOJI
        self.card_emojis = EMOJIDICTIONARY

        self.create_widgets()
        self.draw_game()

    def create_widgets(self):
        # Frame for the top section
        self.top_frame = tk.Frame(self.master, bg="#006400")
        self.top_frame.pack(pady=(20, 0))

        # Reset Game label
        ### N.B. -  Arial 20 here, others are 40 ###
        self.reset_label = tk.Label(self.top_frame, text="↩️", font=("Arial", 22, "bold"), bg="#006400", fg="white",
            cursor="pirate"
        )

        # Stock pile
        label_text=self.game.get_stock_pile().get_card_in_play()
        self.stock_label = tk.Label(self.top_frame, text=label_text, font=("Arial", 22), bg="#006400", fg="white", cursor="fleur")
        # self.stock_label = tk.Label(self.top_frame, text=self.card_back_emoji, font=("Arial", 22), bg="#006400", fg="white", cursor="fleur")
        self.stock_label.pack(side=tk.LEFT, padx=10)
        
        # Waste pile
        label_text=self.game.get_waste_pile().get_card_in_play()
        self.waste_label = tk.Label(self.top_frame, text=label_text, font=("Arial", 22), bg="#006400", fg="white")
        # self.waste_label = tk.Label(self.top_frame, text=self.card_back_empty_pile, font=("Arial", 22), bg="#006400", fg="white")
        self.waste_label.pack(side=tk.LEFT, padx=10)

        # Foundation piles
        self.foundation_labels = []
        for i in range(4):
            label = tk.Label(self.top_frame, width=3, height=2, font=("Arial", 22), bg="#004d00", fg="white", relief="groove", borderwidth=2)
            label.pack(side=tk.LEFT, padx=10)
            self.foundation_labels.append(label)

        # Frame for the tableau
        self.tableau_frame = tk.Frame(self.master, bg="#006400")
        self.tableau_frame.pack(pady=20)

        # Tableau piles as fixed-size frames
        self.tableau_piles = []
        for i in range(7):
            pile_frame = tk.Frame(self.tableau_frame, bg="#006400", width=140)
            pile_frame.pack(side=tk.LEFT, padx=10, anchor='n')
            self.tableau_piles.append(pile_frame)
            # pile_frame.pack_propagate(False) # Prevents the frame from shrinking

    def draw_game(self):
        # The game state is directly accessible via self.game
        if self.game.check_win():
            messagebox.showinfo("NAN", "You win!")

        # Draw stock pile and reset label if stock pile is empty
        label_text = self.game.get_stock_pile().get_card_in_play()
        if self.game.check_empty_stock_pile():
            self.stock_label.config(text=label_text, relief="flat")
            # Stock pile button is not active when empty and reset button will appear
            self.reset_label.pack(side=tk.LEFT, padx=10, before=self.stock_label)
            self.reset_label.bind("<Button-1>", self.on_click_reset)
        else:
            self.stock_label.config(text=label_text, relief="flat")
            self.stock_label.bind("<Button-1>", self.on_click_stock)

            # self.reset_label.pack_forget()
        
        # Draw waste pile
        
        if self.game.check_empty_waste_pile():
            label_text = self.game.get_waste_pile().get_card_in_play()
            self.waste_label.config(text=label_text, relief="flat")
        else:  
            label_text=self.game.get_waste_pile_for_print()
            self.waste_label.config(text="\n".join(label_text), relief="flat")
            # default one card transfer and index -1 as only one card available for transfer 
            self.waste_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=1, pile_index=-1: 
                                  self.on_click_card(card_event, number_of_cards_for_transfer, pile_index)) 
        
        # Draw foundation piles
        i = 0
        for suit, cards in self.game.foundation_piles.items(): # backend uses dictionary with suit as key, and card stack as values
            if cards.is_empty():
                label_text=cards.get_stack_suit() # Use get_stack_suit() as the suit str matches with key
                self.foundation_labels[i].config(text=label_text, relief="flat") 
            else:
                get_card_in_play_id = cards.get_card_in_play().value
                emoji = self.card_emojis.get((get_card_in_play_id, suit), get_card_in_play_id) #Use Special emoji and override cards default
                foreground_colour = "red"
                if suit in {"S", "C"}:
                    foreground_colour = "black"
                self.foundation_labels[i].config(text=emoji, relief="flat", fg=foreground_colour) #, font=("Segoe UI Emoji", 36))
                print("FOUNDATION PILE INFO")
                print("CARD")
                print(get_card_in_play_id)
                print("EMOJI")
                print(emoji)
            
            self.foundation_labels[i].bind("<Button-1>", lambda e, s=suit: self.on_click_foundation(e, s))
            i += 1
            

        # Draw tableau piles
        for i, pile in enumerate(self.game.tableau):
            # Clear existing cards in the pile throguh calling all current active children
            for widget in self.tableau_piles[i].winfo_children():
                widget.destroy()
            
            # Draw new cards
            # print(f"LENGHTH of PILE {i} is {pile.size}")
            card_number = 0
            card_list = []
            if pile.size == 0:
                card_list.append(pile.get_card_in_play())
            for j in range(pile.size - 1, -1, -1):
                card_list.append(pile.look_at(j))
            
            for card_id in card_list:     
                card_text = card_id
                relief ="flat"
                card_label = tk.Label(self.tableau_piles[i], text=card_text, relief=relief, font=("Arial", 22), 
                                      bg="#006400", fg='white')
                card_label.pack(pady=0, anchor='n')   
                # Bind click event, passing the pile index
                n = pile.size - card_number
                # print(f"Transfer number Test {n}")
                card_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=n, pile_index=i: 
                                self.on_click_card(card_event, number_of_cards_for_transfer, pile_index))
                card_number += 1


    
    def on_click_stock(self, event):
        if self.selected_item is None:
            try:
                self.game.draw()
                # if self.game.check_stock_pile():
                #     self.reset = True
            except GameError:
                print("Pile is empty.")
                pass
            self.draw_game()

    def on_click_reset(self, event):
        self.game.reset_pile()
        self.reset = False
        self.reset_label.pack_forget()
        self.draw_game()

    def on_click_waste(self, event):
        self.game.draw()
        self.draw_game()

    def on_click_foundation(self, card_event, suit):
        if self.selected_item is None:
            if not self.game.foundation_piles[suit].is_empty():
                #  self.highlighted_widget = card_event.widget
                #  self.highlighted_widget.config(relief="sunken", borderwidth=2)
                 self.foundation_suit_in_play = suit
                 self.on_click_card(card_event, 1, -1)

        else:
            source_pile_index = self.selected_item[1]
            if self.foundation_suit_in_play is not None:
                return
            if source_pile_index == -1:
                source_card_suit = self.game.waste_pile.get_card_in_play().suit
            else:
                source_card_suit = self.game.get_tableau_card(source_pile_index).suit
            print(f"Selected Card suit is {source_card_suit}")
            print(f"My Foundation suit is {suit}")
            try:
                if suit != source_card_suit:
                    messagebox.showinfo("NAN", "Invalid move. Suit Mismatch.")
                else:
                    pile_moving_from = "waste_pile" if source_pile_index == -1 else "tableau" # waste pile is stack -1 or not from the tableau
                    self.game.move_to_foundation(from_pile=pile_moving_from, stack_number=source_pile_index)
                    self.draw_game()
            except GameError:
                messagebox.showinfo("NAN", "Invalid move. Cannot move this card.")
                pass
            print("HERE IN CLICK ON FOUNDATION")
            self.selected_item = None
            self.highlighted_widget = None
            self.foundation_suit_in_play = None
            self.draw_game()

    def on_click_card(self, card_event, number_of_cards_for_transfer, pile_index):
    # Step 1: Check if a card is already selected
    
        if self.selected_item is None:
            # No card selected, so this is the first click.
            # Store the card data and the widget reference for highlighting.
            self.selected_item = (number_of_cards_for_transfer, pile_index) # Stores key information for first selected item
            if self.game.tableau[pile_index].is_empty():
                print("Cannot Select an empty tableau pile in the first move")
                self.selected_item = None
                pass
                
            else:
                self.highlighted_widget = card_event.widget
                self.highlighted_widget.config(relief="sunken", borderwidth=2)
                test_number=self.selected_item
                print("HERE IN SELECT ITEM IS NONE")
                print(test_number)

        else:
            # A card is already selected, so this is the second click (a move).
            source_number_of_cards_for_transfer, source_pile_index = self.selected_item
            # destination_card_id = card_id
            destination_pile_index = pile_index
            print(f"SECOND CLICK INDEX {destination_pile_index}")
            print(number_of_cards_for_transfer)
            # print(source_card_id)
            # print(destination_card_id)
            # source_card = self.game.tableau[source_pile_index].get_card_in_play()
            # destination_card = self.game.tableau[destination_pile_index].get_card_in_play()

            try:
                if self.foundation_suit_in_play is not None:
                    print("FOUNDATION MOVE")
                    self.game.move_from_foundation(self.foundation_suit_in_play, destination_pile_index)
                    self.draw_game()
                elif source_pile_index == -1:
                    print("Build Move")
                    self.game.build(destination_pile_index)
                    self.draw_game()
                else:
                    print("TRANSFER Move")
                    self.game.transfer(source_pile_index, destination_pile_index, source_number_of_cards_for_transfer)
                    self.draw_game()
            except GameError as e:
                # message = str(e)
                messagebox.showinfo(f"NAN", f"Invalid move {e}")
                pass
                        
            # else:
            #     print("COULD NOT MOVE")
                
            # Regardless of whether the move was valid or not, clear the selection.
            # The old highlighted widget is about to be destroyed by draw_game()
            # so we don't need to de-highlight it explicitly.
            self.selected_item = None
            self.highlighted_widget = None
            self.foundation_suit_in_play = None
            print(f"Currently Selected Foundation Suit {self.foundation_suit_in_play}")
            self.draw_game()
