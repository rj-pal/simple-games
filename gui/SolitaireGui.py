"""
SolitaireGui.py 
Author: Robert Pal
Updated: 2026-10-14

This module contains all control flow logic for running the Solitaire Desktop Application on MacOS.

It includes:
- Two main methods to create and draw the game widgets
- Six on_click methods for button clicking that drive the game interaction
- Five game attributes for managing game states and interaction to the back end (driven by game attribute)
"""
import tkinter as tk
from tkinter import messagebox
from games.solitaire import Solitaire
from utils.errors import *
from utils.emojis import *
from utils.constants import *

# Please note: for MacOS, messagebox does not allow title to appear, thus the arg is 'NAN'

class SolitaireGUI:
    """SolitaireGUI class manages the GUI and backend state for a Solitaire desktop application using back-end logic from games module."""
    def __init__(self, master):
        self.master = master
        master.title(WINDOW_TITLE)
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        # master.configure(bg=BG_COLOR)
        master.configure(bg=BG_COLOR_TEST)
       
        # Initialize the Solitaire backend game state within the GUI class, and set up key attributes for game management
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
        # Frame for the top section (Reset Label, Stock Pile, Waste Pile and Foundations Piles)
        self.top_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.top_frame.pack(pady=PAD_TOP_FRAME)
 
        # Reset Game label - not packed until stock pile is emptied
        self.reset_label = tk.Label(self.top_frame, text=RESET_EMOJI, font=(FONT_FAMILY, FONT_SIZE_RESET, "bold"), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT, cursor="pirate")
 
        # Stock pile label
        self.stock_label = tk.Label(self.top_frame, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT)
        self.stock_label.pack(side=tk.LEFT, padx=PAD_STOCK_WASTE_X, pady=PAD_STOCK_WASTE_Y)
        
        # Waste pile frame with label
        self.waste_frame = tk.Frame(self.top_frame, bg=BG_COLOR_TEST)
        self.waste_frame.pack(side=tk.LEFT, padx=PAD_STOCK_WASTE_X)
        
        self.waste_label = tk.Label(self.waste_frame, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL), bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT)
        self.waste_label.pack()
        
        # Foundation piles labels
        self.foundation_labels = []
        for _ in range(len(self.game.foundation_piles)): # sizes customized to four foundation piles
            label = tk.Label(self.top_frame, width=FOUNDATION_WIDTH, height=FOUNDATION_HEIGHT, font=(FONT_FAMILY, FONT_SIZE_FOUNDATION), bg=FOUNDATION_BG_COLOR, 
                             fg=TEXT_COLOR_DEFAULT, relief=FOUNDATION_RELIEF, borderwidth=FOUNDATION_BORDERWIDTH)
            label.pack(side=tk.LEFT, padx=PAD_FOUNDATION)
            self.foundation_labels.append(label)
 
        # Frame for the Tableau
        self.tableau_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.tableau_frame.pack(pady=TABLEAU_PAD_Y)
 
        # Tableau pile frames (as fixed-size frames)
        self.tableau_piles = []
        for i in range(len(self.game.tableau)):
            pile_frame = tk.Frame(self.tableau_frame, bg=BG_COLOR, width=TABLEAU_PILE_WIDTH)
            pile_frame.pack(side=tk.LEFT, padx=PAD_TABLEAU_X, anchor=PAD_TABLEAU_Y_ANCHOR)
            self.tableau_piles.append(pile_frame)
 
    def draw_game(self):
        # All backend games states accessed and managed via the self.game attribute
        if self.game.check_win():
            messagebox.showinfo("NAN", "Congratulations! You win!")
 
        # Clear existing labels in waste frame
        for widget in self.waste_frame.winfo_children():
            widget.destroy()
 
        # Draw stock pile and reset label if stock pile is empty. Stock pile button is not active when empty and reset button will appear
        label_text = self.game.get_stock_card()
        if self.game.check_empty_stock_pile():
            self.stock_label.config(text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_LARGE), cursor="")
            self.stock_label.pack(side=tk.LEFT, anchor='n')
            self.stock_label.unbind("<Button-1>")

            self.reset_label.pack(side=tk.LEFT, before=self.stock_label, padx=PAD_STOCK_WASTE_X, pady=PAD_STOCK_WASTE_Y, anchor="center")
            self.reset_label.bind("<Button-1>", self.on_click_reset)
        else:
            self.stock_label.config(text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_SMALL), cursor="fleur") 
            self.stock_label.pack(anchor='center')
            self.stock_label.bind("<Button-1>", self.on_click_stock)
        
        # Draw waste pile
        label_text = self.game.get_waste_cards()
        if self.game.check_empty_waste_pile(): 
            # label_text = self.game.get_waste_card()   
            self.waste_label = tk.Label(self.waste_frame, text=label_text, font=(FONT_FAMILY, FONT_SIZE_STOCK_LARGE), relief=CARD_DEFAULT_RELIEF, bg=BG_COLOR, 
                                        fg=TEXT_COLOR_DEFAULT)
            self.waste_label.pack(side="top", fill="x")
        else:  
            # Create separate labels for each text item
            # label_text = self.game.get_waste_cards() # this will return list of one to three card emojis
            label_font_size = FONT_SIZE_TABLEAU_SMALL if self.game.klondike_value == 3 else FONT_SIZE_TABLEAU_LARGE
            for i, text in enumerate(label_text):
                label = tk.Label(self.waste_frame, text=text, font=(FONT_FAMILY, label_font_size), relief=CARD_DEFAULT_RELIEF, bg=BG_COLOR, 
                                 fg=TEXT_COLOR_DEFAULT)
                label.pack(side="top", fill="x")
                # Only bind the card click event and store reference to the last label
                if i == len(label_text) - 1:
                    label.config(cursor="fleur")
                    label.bind("<Button-1>", self.on_click_waste)
                    self.waste_label = label
 
        # Draw foundation piles
        # i = 0
        for i, (suit, cards) in enumerate(self.game.foundation_piles.items()): # backend uses dictionary with suit as key, and card stack as values
            if cards.is_empty():
                label_text=cards.get_stack_suit() # Use get_stack_suit() as the suit str matches with key
                self.foundation_labels[i].config(text=label_text, relief=CARD_DEFAULT_RELIEF, cursor="") 
            else:
                get_card_in_play_id = cards.get_card_in_play().value
                emoji = self.card_emojis.get((get_card_in_play_id, suit), get_card_in_play_id) #Use Special emoji and override cards default
                foreground_colour = TEXT_COLOR_RED
                if suit in SUIT_BLACK:
                    foreground_colour = TEXT_COLOR_BLACK
                self.foundation_labels[i].config(text=emoji, relief=CARD_DEFAULT_RELIEF, fg=foreground_colour, cursor="fleur") #, font=("Segoe UI Emoji", 36))
 
            self.foundation_labels[i].bind("<Button-1>", lambda card_event, card_suit=suit: self.on_click_foundation(card_event, card_suit))
            # i += 1
            
        # Draw tableau piles     
        longest_tableau = max(self.game.tableau, key=lambda tab: tab.size)
        size_threshold = longest_tableau.size # for resizing of card tableau if a particular pile gets too long
        print(f"Longest Pile {longest_tableau}")
 
        for i, tableau_pile in enumerate(self.game.get_tableau()):
            # Clear existing cards in the pile throguh calling all current active children
            for widget in self.tableau_piles[i].winfo_children():
                widget.destroy()
            
            # Draw new cards
            label_font_size = FONT_SIZE_TABLEAU_SMALL if size_threshold > TABLEAU_SIZE_THRESHOLD else FONT_SIZE_TABLEAU_LARGE
            # print(tableau_pile)
            for card_number, card_id in enumerate(tableau_pile):  # card_number for tracking the number of cards in a transfer if a middle card is selected
                # print(tableau_pile)   
                card_text = card_id
                relief = CARD_DEFAULT_RELIEF
                active_cursor = "fleur" if card_id.visible else ""
                card_label = tk.Label(self.tableau_piles[i], text=card_text, relief=relief, font=(FONT_FAMILY, label_font_size), 
                                      bg=BG_COLOR, fg=TEXT_COLOR_DEFAULT, cursor=active_cursor)
                card_label.pack(pady=PAD_TABLEAU_Y, anchor=PAD_TABLEAU_Y_ANCHOR)   
                # Bind click event, passing the pile index and the number of available cards for transfer
          
                n = len(tableau_pile) - card_number
                if card_id.visible:
                    card_label.bind("<Button-1>", lambda card_event, number_of_cards_for_transfer=n, pile_index=i: 
                                    self.on_click_tableau(card_event, number_of_cards_for_transfer, pile_index))
                # card_number += 1
    
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
        if self.selected_item is None and self.game.check_empty_tableau(pile_index):
            pass
        else:
            self.on_click_card(card_event, number_of_cards_for_transfer, pile_index)
 
    def on_click_waste(self, card_event):
        # Only one card for transfer, -1 represents a build move from the waste pile
        self.on_click_card(card_event, 1, -1)
 
    def on_click_foundation(self, card_event, suit):
        if self.selected_item is None:
            # Clicking on the event listener for foundation pile does nothing if the pile is empty and first click
            if not self.game.check_empty_foundation_pile(suit):
                # Activate the suit of the clicked foundation pile in the game attribute and send to on_click_card action
                 self.foundation_suit_in_play = suit
                 self.on_click_card(card_event, 1, -1) #Moving from foundation pile only allow for one card, -1 is for non-tableau move
        else:
            source_pile_index = self.selected_item[1]
            if self.foundation_suit_in_play is not None:
                return
            if source_pile_index == -1:
                source_card_suit = self.game.get_waste_card().suit
            else:
                source_card_suit = self.game.get_tableau_card(source_pile_index).suit
 
            try:
                if suit != source_card_suit:
                    messagebox.showinfo("NAN", "Invalid move. Suit Mismatch.")
                else:
                    pile_moving_from = "waste_pile" if source_pile_index == -1 else "tableau" # waste pile is stack -1 or for non-tableau move
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
                messagebox.showinfo(f"NAN", f"Invalid move: {e}")
                pass
    
            # Regardless of whether the move was valid or not, clear the selection.
            # The old highlighted widget is about to be destroyed by draw_game()
            # so we don't need to de-highlight it explicitly.
            print("DID I GET TO HERE?")
            self.selected_item = None
            self.highlighted_widget = None
            self.foundation_suit_in_play = None
            self.draw_game()
            root.update_idletasks()
 
if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
 