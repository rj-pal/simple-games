import tkinter as tk
import random # Used for shuffling in the placeholder backend
from games.solitaire import Solitare

# --- Backend Class (for illustration) ---
class SolitaireBackend:
    def __init__(self):
        self.suits = ['♠', '♥', '♦', '♣']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        # self.deck = [f"{rank}{suit}" for suit in self.suits for rank in self.ranks]
        # random.shuffle(self.deck)
        self.game = Solitare()

        
        self.stock = self.game.draw_pile
        self.tableau = self.game.tableau
        self.foundation = self.game.foundation_piles
        self.waste = self.game.waste_pile
        self.selected_card = None

    def get_game_state(self):
        return {
            'stock': self.stock,
            'waste': self.waste,
            'foundation': self.foundation,
            'tableau': self.tableau
        }
    
    def move_card(self, source, destination, card_id):
        print(f"Moving card {card_id} from {source} to {destination}")
        return True # Placeholder for your actual game logic

# --- GUI Class with Emojis ---
class SolitaireGUI(tk.Tk):
    def __init__(self, backend):
        super().__init__()
        self.title("Solitaire - Emoji Edition")
        self.geometry("1000x800")
        self.configure(bg="#006400") # Dark green felt color
        self.backend = backend
        
        self.selected_item = None
        
        # Define the emoji card characters
        self.card_emojis = {
            'A♠': '🂡', '2♠': '🂢', '3♠': '🂣', '4♠': '🂤', '5♠': '🂥', '6♠': '🂦', '7♠': '🂧',
            '8♠': '🂨', '9♠': '🂩', 'T♠': '🂪', 'J♠': '🂫', 'Q♠': '🂭', 'K♠': '🂮',
            'A♥': '🂱', '2♥': '🂲', '3♥': '🂳', '4♥': '🂴', '5♥': '🂵', '6♥': '🂶', '7♥': '🂷',
            '8♥': '🂸', '9♥': '🂹', 'T♥': '🂺', 'J♥': '🂻', 'Q♥': '🂽', 'K♥': '🂾',
            'A♦': '🃁', '2♦': '🃂', '3♦': '🃃', '4♦': '🃄', '5♦': '🃅', '6♦': '🃆', '7♦': '🃇',
            '8♦': '🃈', '9♦': '🃉', 'T♦': '🃊', 'J♦': '🃋', 'Q♦': '🃍', 'K♦': '🃎',
            'A♣': '🃑', '2♣': '🃒', '3♣': '🃓', '4♣': '🃔', '5♣': '🃕', '6♣': '🃖', '7♣': '🃗',
            '8♣': '🃘', '9♣': '🃙', 'T♣': '🃚', 'J♣': '🃛', 'Q♣': '🃝', 'K♣': '🃞'
        }
        self.card_back_emoji = "🎴" # '🃏'  Joker or generic back
        
        self.create_widgets()
        self.draw_game()

    def create_widgets(self):
        # Frame for the top section
        self.top_frame = tk.Frame(self, bg="#006400")
        self.top_frame.pack(pady=20)

        # Stock pile
        self.stock_label = tk.Label(self.top_frame, text=self.card_back_emoji, font=("Arial", 40), bg="#006400", fg="white")
        self.stock_label.pack(side=tk.LEFT, padx=10)
        self.stock_label.bind("<Button-1>", self.on_click_stock)

        # Waste pile
        self.waste_label = tk.Label(self.top_frame, font=("Arial", 40), bg="#006400", fg="white")
        self.waste_label.pack(side=tk.LEFT, padx=10)

        # Foundation piles
        self.foundation_labels = []
        for i in range(4):
            label = tk.Label(self.top_frame, width=3, height=2, font=("Arial", 40), bg="#004d00", fg="white", relief="groove", borderwidth=2)
            label.pack(side=tk.LEFT, padx=10)
            self.foundation_labels.append(label)

        # Frame for the tableau
        self.tableau_frame = tk.Frame(self, bg="#006400")
        self.tableau_frame.pack(pady=20)

        # Tableau labels
        self.tableau_piles = []
        for i in range(7):
            pile_frame = tk.Frame(self.tableau_frame, bg="#006400")
            pile_frame.pack(side=tk.LEFT, padx=10, anchor='n')
            self.tableau_piles.append(pile_frame)

    def draw_game(self):
        game_state = self.backend.get_game_state()

        # Draw stock pile
        self.stock_label.config(text=self.card_back_emoji if game_state['stock'] else "", relief="flat")
        
        # Draw waste pile
        if game_state['waste'].top_card():
            last_card_id = game_state['waste'].top_card().face
            emoji = self.card_emojis.get(last_card_id, last_card_id)
            self.waste_label.config(text=emoji)
        else:
            self.waste_label.config(text="")
        
        # Draw foundation piles
        i = 0
        for suit, cards in game_state['foundation'].items(): # backend uses dictionary with suit as key
            if cards.top_card():
                top_card_id = pile.top_card().face
                emoji = self.card_emojis.get(top_card_id, top_card_id)
                self.foundation_labels[i].config(text=emoji)
            else:
                VALID_SUITS = {"S": "♠️", "H": "❤️", "D": "♦️", "C": "♣️"}
                self.foundation_labels[i].config(text=VALID_SUITS[suit])
            i += 1

        # Draw tableau piles
        for i, pile in enumerate(game_state['tableau']):
            # Clear existing cards in the pile
            for widget in self.tableau_piles[i].winfo_children():
                widget.destroy()
            
            # Draw new cards
            for card_id in pile.to_list()[::-1]:
                # Determine if the card is face up
                is_face_up = True # Placeholder logic
                
                card_text = self.card_emojis.get(card_id, card_id) if is_face_up else self.card_back_emoji
                # bg_color = 'white' if any(suit in card_id for suit in ['♥', '♦']) else 'black'
                
                card_label = tk.Label(self.tableau_piles[i], text=card_text, font=("Arial", 40), 
                                      bg="#006400", fg='white')
                card_label.pack(pady=0, anchor='n')
                
                # Bind click event, passing the pile index
                card_label.bind("<Button-1>", lambda e, c=card_id, p=i: self.on_click_card(e, c, p))

    def on_click_stock(self, event):
        print("Stock pile clicked.")
        # Your backend call to deal from stock
        self.backend.game.draw()
        self.draw_game()

    # --- Modified on_click_card method ---
    def on_click_card(self, event, card_id, pile_index):
        print(f"Card {card_id} clicked in pile {pile_index}.")

        if self.selected_item is None:
            # First click: select a card
            self.selected_item = (card_id, pile_index, event.widget)
            event.widget.config(relief="sunken", borderwidth=2)
            print(f"Selected card: {card_id} from pile {pile_index}")
        else:
            # Second click: attempt to move the selected card
            source_card_id, source_pile_index, source_widget = self.selected_item
            destination_card_id = card_id
            destination_pile_index = pile_index
            
            # Call your backend's move function with the pile indices
            # The backend will handle the move validation and execution
            # The third parameter is the destination card, which might be the pile itself
            # depending on your backend's design.

            game_state = self.backend.get_game_state()
            tableau = game_state['tableau']
            if self.backend.game.move_card(tableau[source_pile_index], tableau[destination_pile_index]):
                self.draw_game()
            
            # Reset selection highlight
            source_widget.config(relief="flat", borderwidth=0)
            self.selected_item = None

    # def on_click_card(self, event, card_id):
    #     print(f"Card {card_id} clicked.")

    #     if self.selected_item is None:
    #         # First click: select a card
    #         self.selected_item = (card_id, event.widget)
    #         event.widget.config(relief="sunken", borderwidth=2)
    #         print(f"Selected card: {card_id}")
    #     else:
    #         # Second click: attempt to move the selected card
    #         source_card_id, source_widget = self.selected_item
    #         destination_card_id = card_id

    #         if self.backend.game.move_card(source_card_id, destination_card_id, 'pile_info'):
    #             self.draw_game()
            
    #         source_widget.config(relief="flat", borderwidth=0)
    #         self.selected_item = None

# --- Main application loop ---
if __name__ == "__main__":
    backend = SolitaireBackend()
    app = SolitaireGUI(backend)
    app.mainloop()