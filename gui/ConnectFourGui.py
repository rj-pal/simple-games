import tkinter as tk
from tkinter import messagebox
from games.connect4 import ConnectFour

class ConnectFourGame:
    def __init__(self, master):
        self.master = master
        master.title("Connect Four")
        self.master_colour = "#4682B4"  # Steel Blue
        self.master.configure(bg=self.master_colour)

        # Initialize the backend game state
        self.game = ConnectFour()
        self.player_1 = self.game.get_player(0)
        self.player_2 = self.game.get_player(1)
        self.current_player = self.player_1 
        
        self.board = [['' for _ in range(7)] for _ in range(6)]
        self.game_over = False
        self.buttons = []
        self.column_buttons = []
        self.create_game_board_gui()

    def create_game_board_gui(self):
        """Creates and places all GUI widgets for the main game board."""
        self.main_frame = tk.Frame(self.master, bg=self.master_colour)
        self.main_frame.pack(expand=True, padx=20, pady=20)
        
        # Create a frame for the column buttons
        column_button_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        column_button_frame.pack(pady=10)

        # Create 7 buttons, one for each column
        for col in range(7):
            button = tk.Button(column_button_frame, text="▼", font=("Inter", 24, "bold"), width=2,
                               bg="#3498db", fg="#ffffff", activebackground="#2980b9",
                               command=lambda c=col: self.column_click(c), relief="raised")
            button.pack(side=tk.LEFT, padx=5)
            self.column_buttons.append(button)

        # Create a frame for the game grid
        grid_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        grid_frame.pack()
        
        # Create the 6x7 grid of visual representation buttons (disabled)
        for row in range(6):
            button_row = []
            for col in range(7):
                # Using canvas to draw circles for a round appearance
                canvas = tk.Canvas(grid_frame, width=70, height=70, bg=self.master_colour, highlightthickness=0)
                canvas.grid(row=row, column=col, padx=5, pady=5)
                # Draw a white circle for empty slots
                canvas.create_oval(5, 5, 65, 65, fill="#ecf0f1", outline="#bdc3c7", width=2)
                button_row.append(canvas)
            self.buttons.append(button_row)

    def column_click(self, col):
        """Handles a click on a column button."""
        if not self.game_over: #and not self.current_player.is_ai_player:
            # Send the move to the backend Connect 4 for processing if valid
            is_valid_move = self.make_valid_move(col=col, marker=self.current_player.marker)
            
            # Updates the UI and Connect 4 Game after a valid move
            if is_valid_move:
                winner = self.game.check_winner()
                if winner:
                    messagebox.showinfo("Game Over", f"{self.current_player.name} wins the game!")
                    exit()
                if not self.game_over:
                    self.change_current_player()
                    # self.check_ai_player_turn()
        print(f"Column {col} was clicked.")

    def make_valid_move(self, col, marker):
        # Updates the UI and Connect 4 Game after valid move
        is_valid = self.game.make_move(col=col, marker=self.current_player.marker)
        if is_valid:
            row = self.game.height_list[col]
            canvas_to_update = self.buttons[row][col]
            if self.current_player.marker == 'r':
                circle_colour = "#CD5C5C" # "#B22222" <- darker red #  #"Red" 
            else:
                circle_colour = "#F0E68C" #"#DAA520" <- a bit darker #"Yellow" 
            canvas_to_update.itemconfig(canvas_to_update.find_all()[0], fill=circle_colour)
            return True

        else:
            return False
        

    def change_current_player(self):
        self.current_player = self.player_2 if self.current_player.marker == 'r' else self.player_1
        # self.status_label.config(text=f"{self.current_player.name}'s turn")
        
def main():
    root = tk.Tk()
    game = ConnectFourGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()