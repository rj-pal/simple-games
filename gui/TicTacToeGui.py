"""
TicTacToeGui.py 
Author: Robert Pal
Updated: 2025-09-03

This module contains all control flow logic for running the Tic Tac Toe Desktop Application.
It includes:
- button_click() which acts as the main() game running function
- helper functions to manage game states and UI display
"""
import tkinter as tk
from tkinter import messagebox
import games.tictactoe as tictactoe

class TicTacToeGUI:
    """
    A single class to manage the Tic Tac Toe game's GUI and state.
    This encapsulates all related data and functionality, eliminating global variables.
    """
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")
        master.configure(bg="#2c3e50") # Dark background for the window
        master.geometry("600x600")
        master.resizable(True, True)
       
        # Initialize the backend game state
        self.game = tictactoe.TicTacToe()
        self.game.update_player_name(name="Player 1", marker="x")
        self.game.update_player_name(name="Player 2", marker="o")
        self.player_1 = self.game.get_player(0)
        self.player_2 = self.game.get_player(1)

        # Game state variables
        self.current_player = self.player_1 if self.game.go_first else self.player_2
        self.buttons = []
        self.game_over = False

        # self.create_board()
        self.create_gui_elements()

    # def create_board(self):
    #     """Creates and places all GUI widgets for the Tic Tac Toe game."""
    #     # Create a 3x3 grid of buttons for the board
    #     for row in range(3):
    #         button_row = []
    #         for col in range(3):
    #             button = tk.Button(self.master, text="", font=("Helvetica", 24), width=5, height=2,
    #                                command=lambda r=row, c=col: self.button_click(r, c))
    #             button.grid(row=row, column=col, padx=5, pady=5)
    #             button_row.append(button)
    #         self.buttons.append(button_row)

    #     # Create a status label
    #     self.status_label = tk.Label(self.master, text=f"{self.current_player.name}'s turn", font=("Helvetica", 16))
    #     self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

    #     # Create a reset button
    #     self.reset_button = tk.Button(self.master, text="Reset", font=("Helvetica", 16), command=self.reset_game)
    #     self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

    #     # Create an end session button
    #     self.end_session_button = tk.Button(self.master, text="End Session", font=("Helvetica", 16), command=self.end_session)
# #####

#     def create_gui_elements(self):
#         """Creates and places all GUI widgets for the game."""

#         # Create a 3x3 grid of buttons for the board
#         button_width = 6
#         button_height = 2
#         grid_padding = 5

#         # Fixed grid size (button dimensions: 6 width, 2 height)
#         for row in range(3):
#             button_row = []  # To store buttons in the current row
#             for col in range(3):
#                 # Creating individual button for the Tic-Tac-Toe grid
#                 button = tk.Button(self.master, text="", font=("Inter", 36, "bold"), width=button_width, height=button_height,
#                                    bg="#ecf0f1", fg="#34495e", activebackground="#bdc3c7",
#                                    command=lambda r=row, c=col: self.button_click(r, c),
#                                    relief="raised")
#                 button.grid(row=row, column=col, padx=grid_padding, pady=grid_padding)  # Buttons inside grid
#                 button_row.append(button)  # Add button to row list
#             self.buttons.append(button_row)  # Add row of buttons to main button list

#         # Center the grid inside the window by configuring the grid rows and columns
#         self.master.grid_rowconfigure(0, weight=1, minsize=button_height*3 + grid_padding*2)  # Row for the buttons (game grid)
#         self.master.grid_rowconfigure(1, weight=1)  # Extra space between grid and status (if needed)
#         self.master.grid_rowconfigure(2, weight=1)  # Row for the status label and buttons

#         self.master.grid_columnconfigure(0, weight=1)  # Left side
#         self.master.grid_columnconfigure(1, weight=1)  # Center
#         self.master.grid_columnconfigure(2, weight=1)  # Right side

#         # Create a status label to show the current player's turn
#         self.status_label = tk.Label(self.master, text=f"{self.current_player.name}'s turn", 
#                                      font=("Inter", 18, "bold"), bg="#34495e", fg="#ecf0f1", 
#                                      padx=10, pady=5)
#         self.status_label.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")  # Center the label

#         # Create a reset button to restart the game
#         self.reset_button = tk.Button(self.master, text="Reset", font=("Inter", 16), command=self.reset_game,
#                                       bg="#3498db", fg="white", activebackground="#2980b9", relief="raised")
#         self.reset_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")  # Center the reset button

#         # Create an end session button to end the game session
#         self.end_session_button = tk.Button(self.master, text="End Session", font=("Inter", 16), command=self.end_session,
#                                             bg="#e74c3c", fg="white", activebackground="#c0392b", relief="raised")
#         self.end_session_button.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")  # Center the end session button

#####


    def create_gui_elements(self):
        """Creates and places all GUI widgets for the game."""
        # Use a main frame to contain all widgets for centering
        main_frame = tk.Frame(self.master, bg="#2c3e50")
        main_frame.pack(expand=True, padx=20, pady=20)
        
        
        # self.master.grid_rowconfigure(0, weight=1)  # Row for the buttons (game grid)
        # self.master.grid_rowconfigure(1, weight=1)  # Extra space between grid and status (if needed)
        # self.master.grid_rowconfigure(2, weight=1)  # Row for the status label and buttons

        # self.master.grid_columnconfigure(0, weight=1)  # Left side
        # self.master.grid_columnconfigure(1, weight=1)  # Center
        # self.master.grid_columnconfigure(2, weight=1)  # Right side
        # # Set fixed grid size (button dimensions: 6 width, 2 height)
        # button_width = 6
        # button_height = 2
        # grid_padding = 5
        
        # Create a 3x3 grid of buttons for the board
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(main_frame, text="", font=("Inter", 36, "bold"), width=3, height=2,
                                   bg="#ecf0f1", fg="#34495e", activebackground="#bdc3c7",
                                   command=lambda r=row, c=col: self.button_click(r, c),
                                   relief="raised")
                button.grid(row=row, column=col, padx=10, pady=10)
                button_row.append(button)
            self.buttons.append(button_row)

        # Centre the grid in the window
        # self.master.place(relx=0.5, rely=0.5, anchor="center")

        # Create a status label with a modern font and color
        self.status_label = tk.Label(main_frame, text=f"{self.current_player.name}'s turn", font=("Inter", 18, "bold"),
                                     bg="#34495e", fg="#ecf0f1", padx=10, pady=5)
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Create a reset button with modern styling
        self.reset_button = tk.Button(main_frame, text="Reset", font=("Inter", 16), command=self.reset_game,
                                     bg="#3498db", fg="white", activebackground="#2980b9", relief="raised")
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Create an end session button with modern styling
        self.end_session_button = tk.Button(main_frame, text="End Session", font=("Inter", 16), command=self.end_session,
                                           bg="#e74c3c", fg="white", activebackground="#c0392b", relief="raised")
        self.end_session_button.grid(row=5, column=0, columnspan=3, pady=10)


    def update_final_game_state(self):
        """Updates the game winner attributes, player statistics and game over boolean."""
        self.game.update_winner_info()
        self.game.update_players_stats()
        self.game_over = True

    def display_final_message(self, message_title, message_text):
        """Displays info message box for game win or draw and displays updated end-of-game buttons."""
        messagebox.showinfo(message_title, message_text)
        self.reset_button.config(text="Play Again") # change the reset button to play again at end of session
        self.end_session_button.grid(row=5, column=0, columnspan=3, pady=10) # have a end session or quit button

    def button_click(self, row, col):
        """Runs the Tic Tac Toe game through button click and ends after a winner is found or all squares are filled."""
        if not self.game_over:
            # Send the move to the backend Tic Tac Toe Game for processing if valid
            is_valid_move = self.game.is_valid(row=row, col=col)
            
            # Updates the UI and Tic Tac Toe Game after valid move
            if is_valid_move:
                self.game.make_move(row=row, col=col, marker=self.current_player.marker)
                self.buttons[row][col].config(text=self.current_player.marker, state=tk.DISABLED, disabledforeground="black")
                
                winner = self.game.check_winner()
                
                if winner:
                    self.status_label.config(text=f"Game Over. {self.current_player.name} wins.")
                    self.update_final_game_state()
                    # Must call update_game() first to update the backend game state to get correct winner message
                    self.display_final_message("Game Over", self.game.get_winner_string())
                elif self.game.board_is_full():
                    self.status_label.config(text="Game Over. Cat's Game!")
                    self.update_final_game_state()
                    self.display_final_message("Cat's Game", "There was no winner so there will be no chicken dinner.")
                else:
                    self.current_player = self.player_2 if self.current_player.marker == 'x' else self.player_1
                    self.status_label.config(text=f"{self.current_player.name}'s turn")

    def reset_game(self):
        """Resets the Tic Tac Toe Game state and GUI states."""
        self.game.reset_game_state()
        self.game_over = False
        
        # === Resetting the UI board ===
        # Resets the first player to be the player who lost the current game
        self.current_player = self.player_2 if self.current_player.marker == 'x' else self.player_1
        self.status_label.config(text=f"{self.current_player.name}'s turn")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state=tk.NORMAL)
        self.reset_button.config(text="Reset") # change the reset button back
        self.end_session_button.grid_forget() # hide the end session button

    def end_session(self):
        """Ends the game session and closes the application."""
        end_message = "Game Session Ended.\n\n"
        for statistics in self.game.get_players_info_string_as_list():
            end_message += statistics
        
        messagebox.showinfo("Session Stats", end_message)
        self.master.destroy()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

