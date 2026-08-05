import tkinter as tk
from tkinter import messagebox
from games.solitaire import Solitare
from utils.errors import *
class SolitaireGUI:
    """SolitaireGUI class manages the GUI and backend state for a Solitaire desktop application."""
    def __init__(self, master):
        self.master = master
        master.title("Solitaire - Emoji Edition")
        master.geometry("1200x1000")
        master.configure(bg="#006400") # Dark green felt color
       
        # Initialize the Solitaire backend game state within the GUI class
        self.game = Solitare(klondike_value=1)
        self.selected_item = None
        self.highlighted_widget = None
        self.foundation_suit_in_play = None
        self.reset = False
        
        # Define the emoji card characters
        self.card_back_emoji = "🎴"
        self.card_back_empty_pile = "⚔️"
        self.card_emojis = {
            (1, 'S'): 'A♠',  (2, 'S'): '2♠',  (3, 'S'): '3♠',  (4, 'S'): '4♠',
            (5, 'S'): '5♠',  (6, 'S'): '6♠',  (7, 'S'): '7♠',  (8, 'S'): '8♠',
            (9, 'S'): '9♠', (10, 'S'): 'T♠', (11, 'S'): 'J♠', (12, 'S'): 'Q♠',
            (13, 'S'): 'K♠',

            (1, 'H'): 'A♥',  (2, 'H'): '2♥',  (3, 'H'): '3♥',  (4, 'H'): '4♥',
            (5, 'H'): '5♥',  (6, 'H'): '6♥',  (7, 'H'): '7♥',  (8, 'H'): '8♥',
            (9, 'H'): '9♥', (10, 'H'): 'T♥', (11, 'H'): 'J♥', (12, 'H'): 'Q♥',
            (13, 'H'): 'K♥',

            (1, 'D'): 'A♦',  (2, 'D'): '2♦',  (3, 'D'): '3♦',  (4, 'D'): '4♦',
            (5, 'D'): '5♦',  (6, 'D'): '6♦',  (7, 'D'): '7♦',  (8, 'D'): '8♦',
            (9, 'D'): '9♦', (10, 'D'): 'T♦', (11, 'D'): 'J♦', (12, 'D'): 'Q♦',
            (13, 'D'): 'K♦',

            (1, 'C'): 'A♣',  (2, 'C'): '2♣',  (3, 'C'): '3♣',  (4, 'C'): '4♣',
            (5, 'C'): '5♣',  (6, 'C'): '6♣',  (7, 'C'): '7♣',  (8, 'C'): '8♣',
            (9, 'C'): '9♣', (10, 'C'): 'T♣', (11, 'C'): 'J♣', (12, 'C'): 'Q♣',
            (13, 'C'): 'K♣'
        }

        self.create_widgets()
        self.draw_game()

    def create_widgets(self):
        # Frame for the top section
        self.top_frame = tk.Frame(self.master, bg="#006400")
        self.top_frame.pack(pady=20)

        # Reset Game label
        self.reset_label = tk.Label(self.top_frame, text="↩️", font=("Arial", 20, "bold"), bg="#006400", fg="white",
            cursor="pirate"
        )

        # Stock pile
        self.stock_label = tk.Label(self.top_frame, text=self.card_back_emoji, font=("Arial", 40), bg="#006400", fg="white", cursor="fleur")
        self.stock_label.pack(side=tk.LEFT, padx=10)
        
        # Waste pile
        self.waste_label = tk.Label(self.top_frame, text=self.card_back_empty_pile, font=("Arial", 40), bg="#006400", fg="white")
        self.waste_label.pack(side=tk.LEFT, padx=10)

        # Foundation piles
        self.foundation_labels = []
        for i in range(4):
            label = tk.Label(self.top_frame, width=3, height=2, font=("Arial", 40), bg="#004d00", fg="white", relief="groove", borderwidth=2)
            label.pack(side=tk.LEFT, padx=10)
            self.foundation_labels.append(label)

        # Frame for the tableau
        self.tableau_frame = tk.Frame(self.master, bg="#006400")
        self.tableau_frame.pack(pady=20)

        # Tableau piles as fixed-size frames
        self.tableau_piles = []
        for i in range(7):
            pile_frame = tk.Frame(self.tableau_frame, bg="#006400", width=140, height=500)
            pile_frame.pack(side=tk.LEFT, padx=10, anchor='n')
            self.tableau_piles.append(pile_frame)
            pile_frame.pack_propagate(False) # Prevents the frame from shrinking

    def draw_game(self):
        # The game state is directly accessible via self.game
        if self.game.check_win():
            messagebox.showinfo("NAN", "You win!")

        # Draw stock pile and reset label if stock pile is empty
        if self.game.check_empty_stock_pile():
            self.stock_label.config(text=self.card_back_empty_pile, relief="flat")
            # Stock pile button is not active when empty and reset button will appear
            self.reset_label.pack(side=tk.LEFT, padx=10, before=self.stock_label)
            self.reset_label.bind("<Button-1>", self.on_click_reset)
        else:
            self.stock_label.config(text=self.card_back_emoji, relief="flat")
            self.stock_label.bind("<Button-1>", self.on_click_stock)

            # self.reset_label.pack_forget()
        
        # Draw waste pile
        if self.game.check_empty_waste_pile():
            self.waste_label.config(text=self.card_back_empty_pile, relief="flat")
        else:
            last_card_id = self.game.waste_pile.top_card().face
            self.waste_label.config(text=last_card_id, relief="flat")
            # default one card transfer and index -1 as only one card available for transfer 
            self.waste_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=1, pile_index=-1: 
                                  self.on_click_card(card_event, number_of_cards_for_transfer, pile_index)) 
        
        # Draw foundation piles
        i = 0
        for suit, cards in self.game.foundation_piles.items(): # backend uses dictionary with suit as key
            if cards.is_empty():
                VALID_SUITS = {"S": "♠️", "H": "❤️", "D": "♦️", "C": "♣️"}
                self.foundation_labels[i].config(text=VALID_SUITS[suit], relief="flat")

            else:
                top_card_id = cards.top_card().value
                emoji = self.card_emojis.get((top_card_id, suit), top_card_id)
                foreground_colour = "red"
                if suit in {"S", "C"}:
                    foreground_colour = "black"
                self.foundation_labels[i].config(text=emoji, relief="flat", fg=foreground_colour) #, font=("Segoe UI Emoji", 36))
                print("FOUNDATION PILE INFO")
                print("CARD")
                print(top_card_id)
                print("EMOJI")
                print(emoji)
            
            self.foundation_labels[i].bind("<Button-1>", lambda e, s=suit: self.on_click_foundation(e, s))
            i += 1
            

        # Draw tableau piles
        for i, pile in enumerate(self.game.tableau):
            # Clear existing cards in the pile
            for widget in self.tableau_piles[i].winfo_children():
                widget.destroy()
            
            # Draw new cards
            # print(f"LENGHTH of PILE {i} is {pile.size}")
            card_number = 0
            # print(pile.to_list())
            for card_id in pile.to_list()[::-1]:
            
                # print(f"We are in Pile {i}")
                # print(card_id)
                
                # bg_color = 'white' if any(suit in card_id for suit in ['♥', '♦']) else 'black'
                card_text = card_id
                # print(card_text)
                relief ="flat"
                if card_text == ' ':
                    relief = "sunken"


                card_label = tk.Label(self.tableau_piles[i], text=card_text, relief=relief, font=("Arial", 40), 
                                      bg="#006400", fg='white')
                card_label.pack(pady=0, anchor='n')
                
                # Bind click event, passing the pile index
                # print(f"Size Test {pile.size}")
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
                source_card_suit = self.game.waste_pile.top_card().suit
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
            # source_card = self.game.tableau[source_pile_index].top_card()
            # destination_card = self.game.tableau[destination_pile_index].top_card()

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
                messagebox.showinfo("NAN", "Invalid move")
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

    # def on_click_card(self, event, card_id, pile_index):
    #     print(f"Card {card_id} clicked in pile {pile_index}.")

    #     if self.selected_item is None:
    #         # First click: select a card
    #         self.selected_item = (card_id, pile_index, event.widget)
    #         event.widget.config(relief="sunken", borderwidth=2)
    #         print(f"Selected card: {card_id} from pile {pile_index}")
    #     else:
    #         # Second click: attempt to move the selected card
    #         source_card_id, source_pile_index, source_widget = self.selected_item
    #         destination_card_id = card_id
    #         destination_pile_index = pile_index
            
    #         # Call your backend's move function with the pile indices
    #         # The backend will handle the move validation and execution
    #         # The third parameter is the destination card, which might be the pile itself
            # depending on your backend's design.

           
            # if self.game.move_card(self.game.tableau[source_pile_index], self.game.tableau[destination_pile_index]):
            #     self.draw_game()
            
            
            # Reset selection highlight
            # source_widget.config(relief="flat", borderwidth=0)
            # self.selected_item = None

        

    # def on_click_card(self, event, card, pile_index):
    #     if self.selected_item is None:
    #         # First click: select a card
    #         self.selected_item = (card, pile_index, event.widget)
    #         event.widget.config(relief="sunken", borderwidth=2)
    #     else:
    #         # Second click: attempt to move the selected card
    #         source_card, source_pile_index, source_widget = self.selected_item
            
    #         # The backend's `move_card` logic needs to handle various scenarios
    #         # For simplicity, let's assume it can move from a tableau pile to another tableau pile
    #         destination_pile = self.game.tableau[pile_index]
            
    #         if self.game.move_card(source_card, destination_pile):
    #             self.draw_game()
            
    #         # Reset selection highlight
    #         source_widget.config(relief="flat", borderwidth=0)
    #         self.selected_item = None

# --- Main application loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()

# --- Backend Class (for illustration) ---
# class SolitaireBackend:
#     def __init__(self):
#         self.suits = ['♠', '♥', '♦', '♣']
#         self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
#         # self.deck = [f"{rank}{suit}" for suit in self.suits for rank in self.ranks]
#         # random.shuffle(self.deck)
#         self.game = Solitare()

        
#         self.stock = self.game.draw_pile
#         self.tableau = self.game.tableau
#         self.foundation = self.game.foundation_piles
#         self.waste = self.game.waste_pile
#         self.selected_card = None

#     def get_game_state(self):
#         return {
#             'stock': self.stock,
#             'waste': self.waste,
#             'foundation': self.foundation,
#             'tableau': self.tableau
#         }
    
#     def move_card(self, source, destination, card_id):
#         print(f"Moving card {card_id} from {source} to {destination}")
#         return True # Placeholder for your actual game logic

# # --- GUI Class with Emojis ---
# class SolitaireGUI(tk.Tk):
#     def __init__(self, backend):
#         super().__init__()
#         self.title("Solitaire - Emoji Edition")
#         self.geometry("1000x800")
#         self.configure(bg="#006400") # Dark green felt color
#         self.backend = backend
        
#         self.selected_item = None
        
#         # Define the emoji card characters
#         self.card_emojis = {
#             'A♠': '🂡', '2♠': '🂢', '3♠': '🂣', '4♠': '🂤', '5♠': '🂥', '6♠': '🂦', '7♠': '🂧',
#             '8♠': '🂨', '9♠': '🂩', 'T♠': '🂪', 'J♠': '🂫', 'Q♠': '🂭', 'K♠': '🂮',
#             'A♥': '🂱', '2♥': '🂲', '3♥': '🂳', '4♥': '🂴', '5♥': '🂵', '6♥': '🂶', '7♥': '🂷',
#             '8♥': '🂸', '9♥': '🂹', 'T♥': '🂺', 'J♥': '🂻', 'Q♥': '🂽', 'K♥': '🂾',
#             'A♦': '🃁', '2♦': '🃂', '3♦': '🃃', '4♦': '🃄', '5♦': '🃅', '6♦': '🃆', '7♦': '🃇',
#             '8♦': '🃈', '9♦': '🃉', 'T♦': '🃊', 'J♦': '🃋', 'Q♦': '🃍', 'K♦': '🃎',
#             'A♣': '🃑', '2♣': '🃒', '3♣': '🃓', '4♣': '🃔', '5♣': '🃕', '6♣': '🃖', '7♣': '🃗',
#             '8♣': '🃘', '9♣': '🃙', 'T♣': '🃚', 'J♣': '🃛', 'Q♣': '🃝', 'K♣': '🃞'
#         }
#         self.card_back_emoji = "🎴" # '🃏'  Joker or generic back
        
#         self.create_widgets()
#         self.draw_game()

#     def create_widgets(self):
#         # Frame for the top section
#         self.top_frame = tk.Frame(self, bg="#006400")
#         self.top_frame.pack(pady=20)

#         # Stock pile
#         self.stock_label = tk.Label(self.top_frame, text=self.card_back_emoji, font=("Arial", 40), bg="#006400", fg="white")
#         self.stock_label.pack(side=tk.LEFT, padx=10)
#         self.stock_label.bind("<Button-1>", self.on_click_stock)

#         # Waste pile
#         self.waste_label = tk.Label(self.top_frame, font=("Arial", 40), bg="#006400", fg="white")
#         self.waste_label.pack(side=tk.LEFT, padx=10)

#         # Foundation piles
#         self.foundation_labels = []
#         for i in range(4):
#             label = tk.Label(self.top_frame, width=3, height=2, font=("Arial", 40), bg="#004d00", fg="white", relief="groove", borderwidth=2)
#             label.pack(side=tk.LEFT, padx=10)
#             self.foundation_labels.append(label)

#         # Frame for the tableau
#         self.tableau_frame = tk.Frame(self, bg="#006400")
#         self.tableau_frame.pack(pady=20)

#         # Tableau labels
#         self.tableau_piles = []
#         for i in range(7):
#             pile_frame = tk.Frame(self.tableau_frame, bg="#006400")
#             pile_frame.pack(side=tk.LEFT, padx=10, anchor='n')
#             self.tableau_piles.append(pile_frame)

#     def draw_game(self):
#         game_state = self.backend.get_game_state()

#         # Draw stock pile
#         self.stock_label.config(text=self.card_back_emoji if game_state['stock'] else "", relief="flat")
        
#         # Draw waste pile
#         if game_state['waste'].top_card():
#             last_card_id = game_state['waste'].top_card().face
#             emoji = self.card_emojis.get(last_card_id, last_card_id)
#             self.waste_label.config(text=emoji)
#         else:
#             self.waste_label.config(text="")
        
#        

#         
#     def on_click_stock(self, event):
#         print("Stock pile clicked.")
#         # Your backend call to deal from stock
#         self.backend.game.draw()
#         self.draw_game()

#     # --- Modified on_click_card method ---


#     # def on_click_card(self, event, card_id):
#     #     print(f"Card {card_id} clicked.")

#     #     if self.selected_item is None:
#     #         # First click: select a card
#     #         self.selected_item = (card_id, event.widget)
#     #         event.widget.config(relief="sunken", borderwidth=2)
#     #         print(f"Selected card: {card_id}")
#     #     else:
#     #         # Second click: attempt to move the selected card
#     #         source_card_id, source_widget = self.selected_item
#     #         destination_card_id = card_id

#     #         if self.backend.game.move_card(source_card_id, destination_card_id, 'pile_info'):
#     #             self.draw_game()
            
#     #         source_widget.config(relief="flat", borderwidth=0)
#     #         self.selected_item = None

# # --- Main application loop ---
# if __name__ == "__main__":
#     backend = SolitaireBackend()
#     app = SolitaireGUI(backend)
#     app.mainloop()