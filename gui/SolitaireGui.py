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
        self.game = Solitare(klondike_value=1)
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
        self.reset_label = tk.Label(self.top_frame, text="🔄", font=("Arial", 22, "bold"), bg="#006400", fg="white",
            cursor="pirate")

        # Stock pile
        label_text=self.game.get_stock_pile().get_card_in_play()
        self.stock_label = tk.Label(self.top_frame, text=label_text, font=("Arial", 36), bg="#006400", fg="white", cursor="fleur")
        self.stock_label.pack(side=tk.LEFT, padx=10, pady=(10, 0))
        
        # Waste pile
        self.waste_frame = tk.Frame(self.top_frame, bg="#006400")
        
        label_text=self.game.get_waste_pile().get_card_in_play()
        self.waste_label = tk.Label(self.waste_frame, text=label_text, font=("Arial", 48), bg="#006400", fg="white")
        self.waste_label.pack()
        self.waste_frame.pack(side=tk.LEFT, padx=10)

        # Foundation piles
        self.foundation_labels = []
        for i in range(4):
            label = tk.Label(self.top_frame, width=3, height=2, font=("Arial", 28), bg="#004d00", fg="white", relief="groove", borderwidth=2)
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

    def draw_game(self):
        # The game state is directly accessible via self.game
        if self.game.check_win():
            messagebox.showinfo("NAN", "You win!")

        # Clear existing labels
        for widget in self.waste_frame.winfo_children():
            widget.destroy()

        # Draw stock pile and reset label if stock pile is empty
        label_text = self.game.get_stock_pile().get_card_in_play()
        if self.game.check_empty_stock_pile():
            self.stock_label.config(text=label_text, font=("Arial", 48), relief="flat")
            self.stock_label.pack(side=tk.LEFT, padx=10, pady=(10, 0), anchor='n')
            # Stock pile button is not active when empty and reset button will appear
            # self.reset_label.pack(side=tk.LEFT, padx=10, before=self.stock_label)
            self.reset_label.bind("<Button-1>", self.on_click_reset)
        else:
            self.stock_label.config(text=label_text, font=("Arial", 36), relief="flat")
            self.stock_label.bind("<Button-1>", self.on_click_stock)
        
        # Draw waste pile
        if self.game.check_empty_waste_pile():     
            label_text = self.game.get_waste_pile().get_card_in_play()
            self.waste_label = tk.Label(self.waste_frame, text=label_text, font=("Arial", 48), relief="flat", bg="#006400", fg="white")
            self.waste_label.pack(side="top", fill="x")
            # self.waste_label.unbind("<Button-1>")
        else:  

            label_text = self.game.get_waste_pile_for_print()
            label_font_size = 22 if self.game.klondike_value == 3 else 32

            # # Create separate labels for each text item
            for i, text in enumerate(label_text):
                label = tk.Label(self.waste_frame, text=text, font=("Arial", label_font_size), relief="flat", bg="#006400", fg="white")
                label.pack(side="top", fill="x")
    
            # Only bind click event and store reference to the last label
            if i == len(label_text) - 1:
                label.bind("<Button-1>", lambda card_event: self.on_click_waste(card_event))
                self.waste_label = label

        # Draw foundation piles3
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
            
            self.foundation_labels[i].bind("<Button-1>", lambda card_event, card_suit=suit: self.on_click_foundation(card_event, card_suit))
            i += 1
            
        # Draw tableau piles     
        longest_tableau = max(self.game.tableau, key=lambda tab: tab.size)
        size_threshold = longest_tableau.size # for resizing of card tableau if a particular pile gets too long

        for i, pile in enumerate(self.game.tableau):
            # Clear existing cards in the pile throguh calling all current active children
            for widget in self.tableau_piles[i].winfo_children():
                widget.destroy()
            
            # Draw new cards
            # print(f"LENGHTH of PILE {i} is {pile.size}")
            card_number = 0 # For tracking the number of cards in a transfer if a middle card is selected
            card_list = []
            if pile.size == 0:
                card_list.append(pile.get_card_in_play())
            for j in range(pile.size - 1, -1, -1):
                card_list.append(pile.look_at(j))
            label_font_size = 32
            if size_threshold > 15:
                label_font_size = 22
            for card_id in card_list:     
                card_text = card_id
                relief ="flat"
                card_label = tk.Label(self.tableau_piles[i], text=card_text, relief=relief, font=("Arial", label_font_size), 
                                      bg="#006400", fg='white')
                card_label.pack(pady=0, anchor='n')   
                # Bind click event, passing the pile index
                n = pile.size - card_number
                # print(f"Transfer number Test {n}")
                card_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=n, pile_index=i: 
                                self.on_click_tableau(card_event, number_of_cards_for_transfer, pile_index))
                card_number += 1
    
    def on_click_stock(self, event):
        if self.selected_item is None:
            try:
                self.game.draw()
            except GameError:
                print("Pile is empty.")
                pass
            self.draw_game()

    def on_click_reset(self, event):
        self.game.reset_pile()
        self.reset = False
        self.reset_label.pack_forget()
       
        self.draw_game()

    def on_click_tableau(self, card_event, number_of_cards_for_transfer, pile_index):
        if self.selected_item is None and self.game.tableau[pile_index].is_empty():
            print("Cannot Select an empty tableau pile in the first move")         
        else:
            self.on_click_card(card_event, number_of_cards_for_transfer, pile_index)

    def on_click_waste(self, card_event):
        # Waste pile is simpler - just call core logic
        self.on_click_card(card_event, 1, -1)

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
        # Step 1: Check if any card has already been selected
        if self.selected_item is None:
            # Store the key information (number of cards for transfer and index) for solitaire move
            self.selected_item = (number_of_cards_for_transfer, pile_index)

            self.highlighted_widget = card_event.widget
            self.highlighted_widget.config(relief="sunken", borderwidth=2)
            test_number=self.selected_item
            print("HERE IN SELECT ITEM IS NONE")
            print(test_number)

        else:
            # A card is already selected, so this is the second click (a move).
            # Upack the key information from the first click 
            source_number_of_cards_for_transfer, source_pile_index = self.selected_item
            destination_pile_index = pile_index
            print(f"SECOND CLICK INDEX {destination_pile_index}")
            print(number_of_cards_for_transfer)
       
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
                messagebox.showinfo(f"NAN", f"Invalid move{e}")
                pass
    
            # Regardless of whether the move was valid or not, clear the selection.
            # The old highlighted widget is about to be destroyed by draw_game()
            # so we don't need to de-highlight it explicitly.
            self.selected_item = None
            self.highlighted_widget = None
            self.foundation_suit_in_play = None
            print(f"Currently Selected Foundation Suit {self.foundation_suit_in_play}")
            self.draw_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()