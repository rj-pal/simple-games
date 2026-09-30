"""
SolitaireGui.py 
Author: Robert Pal
Updated: 2026-09-13

This module contains all control flow logic for running the Solitaire Desktop Application on MacOS.

It includes:
- button_click() which acts as the main() game running function
- helper functions to manage game states and UI display
"""
import tkinter as tk
from tkinter import messagebox
from games.solitaire import Solitaire
from utils.errors import *
from utils.emojis import *
from utils.constants import *

class SolitaireGUI:
    """SolitaireGUI class manages the GUI and backend state for a Solitaire desktop application."""
    def __init__(self, master):
        self.master = master
        master.title(WINDOW_TITLE)
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        # master.configure(bg=BG_COLOR)
        master.configure(bg=BG_COLOR_TEST)
       
        # Initialize the Solitaire backend game state within the GUI class
        self.game = Solitaire(klondike_value=3)
        self.selected_item = None
        self.highlighted_widget = None
        self.foundation_suit_in_play = None
        self.reset = False
 
        # Define the emoji card characters from utilities
        self.card_back_emoji = FACE_DOWN_EMOJI
        self.card_back_empty_pile = EMPTY_PILE_EMOJI
        self.card_emojis = EMOJI_DICTIONARY
 
        self.create_widgets()
        self.draw_game()
 
    def create_widgets(self):
        # Frame for the top section
        self.top_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.top_frame.pack(pady=PAD_TOP_FRAME)
 
        # Reset Game label
        self.reset_label = tk.Label(self.top_frame, text=RESET_EMOJI, font=(FONT_FAMILY, FONT_SIZE_RESET, "bold"), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT,
            cursor="pirate")
 
        # Stock pile
        self.stock_label = tk.Label(self.top_frame, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT, cursor="fleur")
        self.stock_label.pack(side=tk.LEFT, padx=PAD_STOCK_WASTE_X, pady=PAD_STOCK_WASTE_Y)
        
        # Waste pile
        self.waste_frame = tk.Frame(self.top_frame, bg=BG_COLOR_TEST)
        self.waste_frame.pack(side=tk.LEFT, padx=PAD_STOCK_WASTE_X)
        
        label_text=self.game.get_waste_pile().get_card_in_play()
        self.waste_label = tk.Label(self.waste_frame, text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT)
        self.waste_label.pack()
        
 
        # Foundation piles
        self.foundation_labels = []
        for i in range(FOUNDATION_COUNT):
            label = tk.Label(self.top_frame, width=FOUNDATION_WIDTH, height=FOUNDATION_HEIGHT, font=(FONT_FAMILY, FONT_SIZE_FOUNDATION), bg=FOUNDATION_BG_COLOR, fg=TEXT_COLOR_DEFAULT, relief=FOUNDATION_RELIEF, borderwidth=FOUNDATION_BORDERWIDTH)
            label.pack(side=tk.LEFT, padx=PAD_FOUNDATION)
            self.foundation_labels.append(label)
 
        # Frame for the tableau
        self.tableau_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.tableau_frame.pack(pady=TABLEAU_PAD_Y)
 
        # Tableau piles as fixed-size frames
        self.tableau_piles = []
        for i in range(TABLEAU_COUNT):
            pile_frame = tk.Frame(self.tableau_frame, bg=BG_COLOR, width=TABLEAU_PILE_WIDTH)
            pile_frame.pack(side=tk.LEFT, padx=PAD_TABLEAU_X, anchor=PAD_TABLEAU_Y_ANCHOR)
            self.tableau_piles.append(pile_frame)
 
    def draw_game(self):
        # The game state is directly accessible via self.game
        if self.game.check_win():
            messagebox.showinfo("NAN", "You win!")
 
        # Clear existing labels in waste frame
        for widget in self.waste_frame.winfo_children():
            widget.destroy()
 
        # Draw stock pile and reset label if stock pile is empty
        label_text = self.game.get_stock_pile().get_card_in_play()
        if self.game.check_empty_stock_pile():
            self.stock_label.config(text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_LARGE))
            self.stock_label.pack(side=tk.LEFT, anchor='n')
            # Stock pile button is not active when empty and reset button will appear
            self.reset_label.pack(side=tk.LEFT, before=self.stock_label, padx=PAD_STOCK_WASTE_X, pady=PAD_STOCK_WASTE_Y, anchor='center')
            self.reset_label.bind("<Button-1>", self.on_click_reset)
        else:
            self.stock_label.config(text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL)) 
            self.stock_label.pack(anchor='center')
            self.stock_label.bind("<Button-1>", self.on_click_stock)


            # self.stock_label = tk.Label(self.top_frame, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT, cursor="fleur")
            # self.stock_label.pack(side=tk.LEFT, padx=PAD_STOCK_WASTE, pady=PAD_STOCK_Y)
        
        # Draw waste pile
        if self.game.check_empty_waste_pile():     
            label_text = self.game.get_waste_pile().get_card_in_play()
            self.waste_label = tk.Label(self.waste_frame, text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_LARGE), relief=CARD_DEFAULT_RELIEF, bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT)
            self.waste_label.pack(side="top", fill="x")
            # self.waste_label.unbind("<Button-1>")
        else:  
 
            label_text = self.game.get_waste_pile_for_print()
            label_font_size = FONT_SIZE_TABLEAU_SMALL if self.game.klondike_value == 3 else FONT_SIZE_TABLEAU_LARGE
 
            # # Create separate labels for each text item
            for i, text in enumerate(label_text):
                label = tk.Label(self.waste_frame, text=text, font=(FONT_FAMILY, label_font_size), relief=CARD_DEFAULT_RELIEF, bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT)
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
                self.foundation_labels[i].config(text=label_text, relief=CARD_DEFAULT_RELIEF) 
            else:
                get_card_in_play_id = cards.get_card_in_play().value
                emoji = self.card_emojis.get((get_card_in_play_id, suit), get_card_in_play_id) #Use Special emoji and override cards default
                foreground_colour = TEXT_COLOR_RED
                if suit in SUIT_BLACK:
                    foreground_colour = TEXT_COLOR_BLACK
                self.foundation_labels[i].config(text=emoji, relief=CARD_DEFAULT_RELIEF, fg=foreground_colour) #, font=("Segoe UI Emoji", 36))
 
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
            card_number = 0 # For tracking the number of cards in a transfer if a middle card is selected
            card_list = []
            if pile.size == 0:
                card_list.append(pile.get_card_in_play())
            for j in range(pile.size - 1, -1, -1):
                card_list.append(pile.look_at(j))
            label_font_size = FONT_SIZE_TABLEAU_LARGE
            if size_threshold > TABLEAU_SIZE_THRESHOLD:
                label_font_size = FONT_SIZE_TABLEAU_SMALL
            for card_id in card_list:     
                card_text = card_id
                relief = CARD_DEFAULT_RELIEF
                card_label = tk.Label(self.tableau_piles[i], text=card_text, relief=relief, font=(FONT_FAMILY, label_font_size), 
                                      bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT)
                card_label.pack(pady=PAD_TABLEAU_Y, anchor=PAD_TABLEAU_Y_ANCHOR)   
                # Bind click event, passing the pile index
                n = pile.size - card_number
                card_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=n, pile_index=i: 
                                self.on_click_tableau(card_event, number_of_cards_for_transfer, pile_index))
                card_number += 1
    
    def on_click_stock(self, event):
        if self.selected_item is None:
            try:
                self.game.draw()
            except GameError:
                print("Cannot draw empty stock pile")
            self.draw_game()
 
    def on_click_reset(self, event):
        self.game.reset_pile()
        self.reset = False
        self.reset_label.pack_forget()
       
        self.draw_game()
 
    def on_click_tableau(self, card_event, number_of_cards_for_transfer, pile_index):
        if self.selected_item is None and self.game.tableau[pile_index].is_empty():
            pass
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
            self.highlighted_widget.config(relief=CARD_SELECTED_RELIEF, borderwidth=CARD_SELECTED_BORDERWIDTH)
            test_number=self.selected_item
           
 
        else:
            # A card is already selected, so this is the second click (a move).
            # Upack the key information from the first click 
            source_number_of_cards_for_transfer, source_pile_index = self.selected_item
            destination_pile_index = pile_index
         
       
            try:
                if self.foundation_suit_in_play is not None:
                    self.game.move_from_foundation(self.foundation_suit_in_play, destination_pile_index)
                    self.draw_game()
                elif source_pile_index == -1:
                    self.game.build(destination_pile_index)
                    self.draw_game()
                else:
                    self.game.transfer(source_pile_index, destination_pile_index, source_number_of_cards_for_transfer)
                    self.draw_game()
            except GameError as e:
                messagebox.showinfo(f"NAN", f"Invalid move{e}")
                pass
    
            # Regardless of whether the move was valid or not, clear the selection.
            # The old highlighted widget is about to be destroyed by draw_game()
            # so we don't need to de-highlight it explicitly.
            self.selected_item = None
            self.highlighted_widget = None
            self.foundation_suit_in_play = None
            self.draw_game()
 
if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
 






# class SolitaireGUI:
#     """SolitaireGUI class manages the GUI and backend state for a Solitaire desktop application."""
#     def __init__(self, master):
#         self.master = master
#         master.title("Solitaire - Emoji Edition")
#         master.geometry("1200x1000")
#         master.configure(bg="#006400") # Dark green felt color
#         # master.configure(bg="#640032") # Test color
       
#         # Initialize the Solitaire backend game state within the GUI class
#         self.game = Solitaire(klondike_value=1)
#         self.selected_item = None
#         self.highlighted_widget = None
#         self.foundation_suit_in_play = None
#         self.reset = False

#         # Define the emoji card characters from utilities
#         self.card_back_emoji = FACE_DOWN_EMOJI
#         self.card_back_empty_pile = EMPTYPILEEMOJI
#         self.card_emojis = EMOJIDICTIONARY

#         self.create_widgets()
#         self.draw_game()

#     def create_widgets(self):
#         # Frame for the top section
#         self.top_frame = tk.Frame(self.master, bg="#006400")
#         self.top_frame.pack(pady=(20, 0))

#         # Reset Game label
#         ### N.B. -  Arial 20 here, others are 40 ###
#         self.reset_label = tk.Label(self.top_frame, text="🔄", font=("Arial", 22, "bold"), bg="#006400", fg="white",
#             cursor="pirate")

#         # Stock pile
#         label_text=self.game.get_stock_pile().get_card_in_play()
#         self.stock_label = tk.Label(self.top_frame, text=label_text, font=("Arial", 36), bg="#006400", fg="white", cursor="fleur")
#         self.stock_label.pack(side=tk.LEFT, padx=10, pady=(10, 0))
        
#         # Waste pile
#         self.waste_frame = tk.Frame(self.top_frame, bg="#006400")
        
#         label_text=self.game.get_waste_pile().get_card_in_play()
#         self.waste_label = tk.Label(self.waste_frame, text=label_text, font=("Arial", 48), bg="#006400", fg="white")
#         self.waste_label.pack()
#         self.waste_frame.pack(side=tk.LEFT, padx=10)

#         # Foundation piles
#         self.foundation_labels = []
#         for i in range(4):
#             label = tk.Label(self.top_frame, width=3, height=2, font=("Arial", 28), bg="#004d00", fg="white", relief="groove", borderwidth=2)
#             label.pack(side=tk.LEFT, padx=10)
#             self.foundation_labels.append(label)

#         # Frame for the tableau
#         self.tableau_frame = tk.Frame(self.master, bg="#006400")
#         self.tableau_frame.pack(pady=20)

#         # Tableau piles as fixed-size frames
#         self.tableau_piles = []
#         for i in range(7):
#             pile_frame = tk.Frame(self.tableau_frame, bg="#006400", width=140)
#             pile_frame.pack(side=tk.LEFT, padx=10, anchor='n')
#             self.tableau_piles.append(pile_frame)

#     def draw_game(self):
#         # The game state is directly accessible via self.game
#         if self.game.check_win():
#             messagebox.showinfo("NAN", "You win!")

#         # Clear existing labels
#         for widget in self.waste_frame.winfo_children():
#             widget.destroy()

#         # Draw stock pile and reset label if stock pile is empty
#         label_text = self.game.get_stock_pile().get_card_in_play()
#         if self.game.check_empty_stock_pile():
#             self.stock_label.config(text=label_text, font=("Arial", 48), relief="flat")
#             self.stock_label.pack(side=tk.LEFT, padx=10, pady=(10, 0), anchor='n')
#             # Stock pile button is not active when empty and reset button will appear
#             # self.reset_label.pack(side=tk.LEFT, padx=10, before=self.stock_label)
#             self.reset_label.bind("<Button-1>", self.on_click_reset)
#         else:
#             self.stock_label.config(text=label_text, font=("Arial", 36), relief="flat")
#             self.stock_label.bind("<Button-1>", self.on_click_stock)
        
#         # Draw waste pile
#         if self.game.check_empty_waste_pile():     
#             label_text = self.game.get_waste_pile().get_card_in_play()
#             self.waste_label = tk.Label(self.waste_frame, text=label_text, font=("Arial", 48), relief="flat", bg="#006400", fg="white")
#             self.waste_label.pack(side="top", fill="x")
#             # self.waste_label.unbind("<Button-1>")
#         else:  

#             label_text = self.game.get_waste_pile_for_print()
#             label_font_size = 22 if self.game.klondike_value == 3 else 32

#             # # Create separate labels for each text item
#             for i, text in enumerate(label_text):
#                 label = tk.Label(self.waste_frame, text=text, font=("Arial", label_font_size), relief="flat", bg="#006400", fg="white")
#                 label.pack(side="top", fill="x")
    
#             # Only bind click event and store reference to the last label
#             if i == len(label_text) - 1:
#                 label.bind("<Button-1>", lambda card_event: self.on_click_waste(card_event))
#                 self.waste_label = label

#         # Draw foundation piles3
#         i = 0
#         for suit, cards in self.game.foundation_piles.items(): # backend uses dictionary with suit as key, and card stack as values
#             if cards.is_empty():
#                 label_text=cards.get_stack_suit() # Use get_stack_suit() as the suit str matches with key
#                 self.foundation_labels[i].config(text=label_text, relief="flat") 
#             else:
#                 get_card_in_play_id = cards.get_card_in_play().value
#                 emoji = self.card_emojis.get((get_card_in_play_id, suit), get_card_in_play_id) #Use Special emoji and override cards default
#                 foreground_colour = "red"
#                 if suit in {"S", "C"}:
#                     foreground_colour = "black"
#                 self.foundation_labels[i].config(text=emoji, relief="flat", fg=foreground_colour) #, font=("Segoe UI Emoji", 36))

#             self.foundation_labels[i].bind("<Button-1>", lambda card_event, card_suit=suit: self.on_click_foundation(card_event, card_suit))
#             i += 1
            
#         # Draw tableau piles     
#         longest_tableau = max(self.game.tableau, key=lambda tab: tab.size)
#         size_threshold = longest_tableau.size # for resizing of card tableau if a particular pile gets too long

#         for i, pile in enumerate(self.game.tableau):
#             # Clear existing cards in the pile throguh calling all current active children
#             for widget in self.tableau_piles[i].winfo_children():
#                 widget.destroy()
            
#             # Draw new cards
#             card_number = 0 # For tracking the number of cards in a transfer if a middle card is selected
#             card_list = []
#             if pile.size == 0:
#                 card_list.append(pile.get_card_in_play())
#             for j in range(pile.size - 1, -1, -1):
#                 card_list.append(pile.look_at(j))
#             label_font_size = 32
#             if size_threshold > 15:
#                 label_font_size = 22
#             for card_id in card_list:     
#                 card_text = card_id
#                 relief ="flat"
#                 card_label = tk.Label(self.tableau_piles[i], text=card_text, relief=relief, font=("Arial", label_font_size), 
#                                       bg="#006400", fg='white')
#                 card_label.pack(pady=0, anchor='n')   
#                 # Bind click event, passing the pile index
#                 n = pile.size - card_number
#                 card_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=n, pile_index=i: 
#                                 self.on_click_tableau(card_event, number_of_cards_for_transfer, pile_index))
#                 card_number += 1
    
#     def on_click_stock(self, event):
#         if self.selected_item is None:
#             try:
#                 self.game.draw()
#             except GameError:
#                 pass
#             self.draw_game()

#     def on_click_reset(self, event):
#         self.game.reset_pile()
#         self.reset = False
#         self.reset_label.pack_forget()
       
#         self.draw_game()

#     def on_click_tableau(self, card_event, number_of_cards_for_transfer, pile_index):
#         if self.selected_item is None and self.game.tableau[pile_index].is_empty():
#             pass
#         else:
#             self.on_click_card(card_event, number_of_cards_for_transfer, pile_index)

#     def on_click_waste(self, card_event):
#         # Waste pile is simpler - just call core logic
#         self.on_click_card(card_event, 1, -1)

#     def on_click_foundation(self, card_event, suit):
#         if self.selected_item is None:
#             if not self.game.foundation_piles[suit].is_empty():
#                 #  self.highlighted_widget = card_event.widget
#                 #  self.highlighted_widget.config(relief="sunken", borderwidth=2)
#                  self.foundation_suit_in_play = suit
#                  self.on_click_card(card_event, 1, -1)

#         else:
#             source_pile_index = self.selected_item[1]
#             if self.foundation_suit_in_play is not None:
#                 return
#             if source_pile_index == -1:
#                 source_card_suit = self.game.waste_pile.get_card_in_play().suit
#             else:
#                 source_card_suit = self.game.get_tableau_card(source_pile_index).suit

#             try:
#                 if suit != source_card_suit:
#                     messagebox.showinfo("NAN", "Invalid move. Suit Mismatch.")
#                 else:
#                     pile_moving_from = "waste_pile" if source_pile_index == -1 else "tableau" # waste pile is stack -1 or not from the tableau
#                     self.game.move_to_foundation(from_pile=pile_moving_from, stack_number=source_pile_index)
#                     self.draw_game()
#             except GameError:
#                 messagebox.showinfo("NAN", "Invalid move. Cannot move this card.")
#                 pass
#             self.selected_item = None
#             self.highlighted_widget = None
#             self.foundation_suit_in_play = None
#             self.draw_game()

#     def on_click_card(self, card_event, number_of_cards_for_transfer, pile_index):
#         # Step 1: Check if any card has already been selected
#         if self.selected_item is None:
#             # Store the key information (number of cards for transfer and index) for solitaire move
#             self.selected_item = (number_of_cards_for_transfer, pile_index)

#             self.highlighted_widget = card_event.widget
#             self.highlighted_widget.config(relief="sunken", borderwidth=2)
#             test_number=self.selected_item
           

#         else:
#             # A card is already selected, so this is the second click (a move).
#             # Upack the key information from the first click 
#             source_number_of_cards_for_transfer, source_pile_index = self.selected_item
#             destination_pile_index = pile_index
         
       
#             try:
#                 if self.foundation_suit_in_play is not None:
#                     self.game.move_from_foundation(self.foundation_suit_in_play, destination_pile_index)
#                     self.draw_game()
#                 elif source_pile_index == -1:
#                     self.game.build(destination_pile_index)
#                     self.draw_game()
#                 else:
#                     self.game.transfer(source_pile_index, destination_pile_index, source_number_of_cards_for_transfer)
#                     self.draw_game()
#             except GameError as e:
#                 messagebox.showinfo(f"NAN", f"Invalid move{e}")
#                 pass
    
#             # Regardless of whether the move was valid or not, clear the selection.
#             # The old highlighted widget is about to be destroyed by draw_game()
#             # so we don't need to de-highlight it explicitly.
#             self.selected_item = None
#             self.highlighted_widget = None
#             self.foundation_suit_in_play = None
#             self.draw_game()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SolitaireGUI(root)
#     root.mainloop()