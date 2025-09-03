"""
TicTacToeGui.py 
Author: Robert Pal
Updated: 2025-09-02

This module contains all control flow logic for running the Tic Tac Toe Desktop Application.
It includes:
- button_click() which acts as the main() game running function
- helper functions to manage game states and UI display
"""
# import tkinter as tk
# from tkinter import messagebox
# import games.tictactoe as tictactoe

# # Initialize the main window and game
# root = tk.Tk()
# root.title("Tic Tac Toe")

# # Tic Tac Toe Game State variables
# game = tictactoe.TicTacToe()
# game.update_player_name(name="Player 1", marker="x")
# game.update_player_name(name="Player 2", marker="o")
# player_1 = game.get_player(0)
# player_2 = game.get_player(1)

# # Global variables
# current_player = player_1 if game.go_first else player_2
# board = [["" for _ in range(3)] for _ in range(3)]
# buttons = []
# game_over = False
# # === Main Game Play Function with two helper functions for handling GUI and Tic Tac Toe Game states ====
# def update_game():
#     """Updates the Tic Tac Toe Game Object summary results and updates the global Game Over boolean tag."""
#     global game_over
#     game.update_winner_info()
#     game.update_players_stats()
#     game_over = True

# def display_final_message(message_title, message_text):
#     """Displays info message box for game win or draw and displays updated end-of-game buttons."""
#     messagebox.showinfo(message_title, message_text)
#     reset_button.config(text="Play Again") # update reset button to play again button
#     end_session_button.grid(row=5, column=0, columnspan=3, pady=10) # add the end session button

# def button_click(row, col):
#     """Runs the Tic Tac Toe game through button click and ends after a winner is found or all squares are filled."""
#     global current_player, game_over
    
#     if not game_over:
#         # Send the move to the backend Tic Tac Toe Game for processing
#         is_valid_move = game.is_valid(row, col) 
#         # Only update the UI and Tic Tac Toe Game state if the move was valid
#         if is_valid_move:
#             game.make_move(row, col, current_player.marker)
#             buttons[row][col].config(text=current_player.marker, state=tk.DISABLED, disabledforeground="black")         
#             winner = game.check_winner()  
#             if winner:
#                 status_label.config(text=f"Game Over. {current_player.name} wins.")
#                 update_game()
#                 display_final_message("Game Over", game.get_winner_string())
                   
#             elif game.board_is_full():
#                 status_label.config(text="Game Over. It's a draw!") 
#                 update_game()
#                 display_final_message("Cat's Game", "There was no winner so there will be no chicken dinner.")
                       
#             else:
#                 current_player = player_2 if current_player.marker == 'x' else player_1
#                 status_label.config(text=f"{current_player.name}'s turn")

# # Function to reset the GUI and Tic Tac Toe Game states
# def reset_game():
#     """Resets the Tic Tac Toe Game state and global variable game states."""
#     global current_player, board, game_over
#     # Reset the Tic Tac Toe Gane state
#     game.reset_game_state()

#     # Reset the global variables
#     current_player = player_2 if current_player.marker == 'x' else player_1 # Resets the first player to be the player who lost the current game
#     game_over = False
#     board = [["" for _ in range(3)] for _ in range(3)]
#     status_label.config(text=f"{current_player.name}'s turn")
#     for row in range(3):
#         for col in range(3):
#             buttons[row][col].config(text="", state=tk.NORMAL)
#     reset_button.config(text="Reset") # return the play again button to reset button
#     end_session_button.grid_forget() # hide the end session button

# # Function to end the game session and close the application
# def end_session():
#     end_message = "Game Session Ended.\n\n"
#     # Create a summary string of the final stats between the two players for all played games
#     for statistics in game.get_players_info_string_as_list():
#         end_message += statistics
#     # Display final message and end the game
#     messagebox.showinfo("Session Stats", end_message)
#     root.destroy()
# # ==== GUI related functions
# # Create a 3x3 grid of buttons for the board
# for row in range(3):
#     button_row = []
#     for col in range(3):
#         button = tk.Button(root, text="", font=("Helvetica", 24), width=5, height=2,
#                            command=lambda r=row, c=col: button_click(r, c))
#         button.grid(row=row, column=col, padx=5, pady=5)
#         button_row.append(button)
#     buttons.append(button_row)

# # Create a status label
# status_label = tk.Label(root, text=f"{current_player.name}'s turn", font=("Helvetica", 16))
# status_label.grid(row=3, column=0, columnspan=3, pady=10)

# # Create a reset button
# reset_button = tk.Button(root, text="Reset", font=("Helvetica", 16), command=reset_game)
# reset_button.grid(row=4, column=0, columnspan=3, pady=10)

# # Create an end session button
# end_session_button = tk.Button(root, text="End Session", font=("Helvetica", 16), command=end_session)

# # Start the main event loop
# root.mainloop()

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

    def create_board(self):
        """Creates and places all GUI widgets for the Tic Tac Toe game."""
        # Create a 3x3 grid of buttons for the board
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(self.master, text="", font=("Helvetica", 24), width=5, height=2,
                                   command=lambda r=row, c=col: self.button_click(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        # Create a status label
        self.status_label = tk.Label(self.master, text=f"{self.current_player.name}'s turn", font=("Helvetica", 16))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Create a reset button
        self.reset_button = tk.Button(self.master, text="Reset", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Create an end session button
        self.end_session_button = tk.Button(self.master, text="End Session", font=("Helvetica", 16), command=self.end_session)

    def create_gui_elements(self):
        """Creates and places all GUI widgets for the game."""
        # Create a 3x3 grid of buttons for the board
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(self.master, text="", font=("Inter", 36, "bold"), width=4, height=2,
                                   bg="#ecf0f1", fg="#34495e", activebackground="#bdc3c7",
                                   command=lambda r=row, c=col: self.button_click(r, c),
                                   relief="raised")
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        # Create a status label with a modern font and color
        self.status_label = tk.Label(self.master, text=f"{self.current_player.name}'s turn", font=("Inter", 18, "bold"),
                                     bg="#34495e", fg="#ecf0f1", padx=10, pady=5)
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Create a reset button with modern styling
        self.reset_button = tk.Button(self.master, text="Reset", font=("Inter", 16), command=self.reset_game,
                                     bg="#3498db", fg="white", activebackground="#2980b9", relief="raised")
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Create an end session button with modern styling
        self.end_session_button = tk.Button(self.master, text="End Session", font=("Inter", 16), command=self.end_session,
                                           bg="#e74c3c", fg="white", activebackground="#c0392b", relief="raised")


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

