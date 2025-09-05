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
        self.master_colour = "#37353E"
        self.master_text_colour = "#FFFCFB"

        self.master_label_colour = "#44444E"
        self.master_label_text="#ecf0f1"

        self.master_button_text_highlight_colour = "#34495e"

        
        master.configure(bg=self.master_colour)

        master.geometry("800x600")
        master.resizable(True, True)
       
        # Initialize the backend game state and update backend player based on user selections
        self.game = tictactoe.TicTacToe()
        self.current_player = None
        self.player_1 = None 
        self.player_2 = None

        # Game state variables
        self.buttons = []
        self.game_over = False
        self.difficulty_options_frame = None
        self.start_button_frame = None
        self.difficulty = tk.StringVar(value="easy") # None for easy, False for intermedia, True for hard
        self.game_mode = tk.IntVar(value=1) # 1 for single player, 2 for two players

        self.create_start_menu()

    def create_start_menu(self):
        """Creates the initial start screen widgets to set 1 or 2 player game mode and difficulty level for AI player."""
        # Use a main frame to contain all widgets for centering
        self.main_frame = tk.Frame(self.master, bg=self.master_colour)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        title_label = tk.Label(self.main_frame, text="Tic Tac Toe", font=("Inter", 36, "bold"),
                               bg=self.master_colour, fg=self.master_text_colour)
        title_label.pack(pady=(0, 20))

        # Game Mode selection
        mode_label = tk.Label(self.main_frame, text="Select the Game Play Mode:", font=("Inter", 16),
                              bg=self.master_label_colour, fg=self.master_label_text)
        mode_label.pack(pady=(10, 5))

        tk.Radiobutton(self.main_frame, text="One Player (vs AI Player)", font=("Inter", 14), variable=self.game_mode, value=1,
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor="#34495e", command=self.update_difficulty_options).pack(pady=2)
        tk.Radiobutton(self.main_frame, text="Two Players", font=("Inter", 14), variable=self.game_mode, value=2,
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor="#34495e", command=self.update_difficulty_options).pack(pady=2)    

        # AI Difficulty selection, wrapped in a frame to easily hide/show
        self.difficulty_options_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        self.difficulty_options_frame.pack(pady=(20, 5))

        difficulty_label = tk.Label(self.difficulty_options_frame, text="Select AI Difficulty Level:", font=("Inter", 16),
                                    bg=self.master_label_colour, fg=self.master_label_text)
        difficulty_label.pack(pady=(0, 5))

        tk.Radiobutton(self.difficulty_options_frame, text="Blind", font=("Inter", 14), variable=self.difficulty, value="easy",
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor="#34495e").pack(pady=2)
        tk.Radiobutton(self.difficulty_options_frame, text="Intermediate", font=("Inter", 14), variable=self.difficulty, value="intmed",
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor="#34495e").pack(pady=2)
        tk.Radiobutton(self.difficulty_options_frame, text="Impossible", font=("Inter", 14), variable=self.difficulty, value="hard",
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor="#34495e").pack(pady=2)

        # Start Button
        self.start_button_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        self.start_button_frame.pack(pady=(20, 5))
        start_button = tk.Button(self.start_button_frame, text="Start Game", font=("Inter", 16), command=self.start_game,
                                 fg=self.master_button_text_highlight_colour, highlightbackground=self.master_button_text_highlight_colour, 
                                 highlightthickness=3, relief="raised")
        start_button.pack(pady=20)


    def start_game(self):
        """Initializes the game and switches from the start menu to the game board."""
        # Destroy start menu widgets
        self.main_frame.destroy()
        
        # Initialize the backend game state based on selections
        difficulty_dictionary = {
            "easy": None, 
            "intmed": False,
            "hard": True
        }

        name_dictionary = {
            "easy": "CPU Easy",
            "intmed": "CPU Intermediate",
            "hard": "CPU Hard"
        }
        # Use two mappings to set the correct difficulty level and CPU Name
        if self.game_mode.get() == 1:
             self.game.create_ai_player(name=name_dictionary[self.difficulty.get()], difficulty=difficulty_dictionary[self.difficulty.get()]) 
            #  self.game.set_difficulty()
        else:
            self.game.update_player_name(name="Player 1", marker="x")
            self.game.update_player_name(name="Player 2", marker="o")
            
        self.player_1 = self.game.get_player(0)
        self.player_2 = self.game.get_player(1)
        self.current_player = self.player_1

        # Create and display the game board
        self.create_game_board_gui()
        self.check_ai_player_turn()


    def create_game_board_gui(self):
        """Creates and places all GUI widgets for the game using two main frames."""
        # Use a main frame to contain all widgets for centering
        main_frame = tk.Frame(self.master, bg=self.master_colour)
        main_frame.pack(expand=True, padx=20, pady=20)
        
        # Frame for the game board buttons
        board_frame = tk.Frame(main_frame, bg=self.master_colour, borderwidth=0, highlightthickness=0)
        board_frame.grid(row=0, column=0)

        # Create a 3x3 grid of buttons for the board
        for row in range(3):
            button_row = []
            for col in range(3):
                # Apply custom padding based on the button's position to create Tic Tac Toe grid board effect
                pad_x = 0
                pad_y = 0
                # Add horizontal padding to the right for the first two columns
                if col < 2:
                    pad_x = (0, 20)
                # Add vertical padding to the bottom for the first two rows
                if row < 2:
                    pad_y = (0, 20)
        
                button = tk.Button(board_frame, text="", font=("Inter", 36, "bold"), width=3, height=2,
                   activebackground="#34495e",  # Optional: for click feedback
                   relief="flat", borderwidth=0, highlightthickness=0, highlightbackground="#ecf0f1",
                   command=lambda r=row, c=col: self.button_click(r, c))

                button.grid(row=row, column=col, padx=pad_x, pady=pad_y)
                button_row.append(button)
            self.buttons.append(button_row)

        # --- Frame for the status label and control buttons ---
        control_frame = tk.Frame(main_frame, bg=self.master_colour)
        control_frame.grid(row=1, column=0, pady=(20, 0)) # Add top padding to separate frames

        # Create a status label with a modern font and color
        self.status_label = tk.Label(control_frame, text=f"{self.current_player.name}'s turn", font=("Inter", 18, "bold"),
                                     bg=self.master_colour, fg="#ecf0f1", padx=10, pady=5)
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create a reset button with modern styling
        self.reset_button = tk.Button(control_frame, text="Reset", font=("Inter", 16), command=self.reset_game,
                                      fg=self.master_button_text_highlight_colour, activebackground="#34495e", 
                                      highlightbackground=self.master_button_text_highlight_colour, 
                                      relief="raised", takefocus=0)
        self.reset_button.grid(row=1, column=0, columnspan=3, pady=10)

        # self.reset_button = tk.Button(control_frame, text="Reset", font=("Inter", 16), command=self.reset_game,
        #                              bg="#3498db", fg="white", activebackground="#2980b9", relief="raised")
        # self.reset_button.grid(row=1, column=0, columnspan=3, pady=10)

        # Create an end session button with modern styling
        self.end_session_button = tk.Button(control_frame, text="End Session", font=("Inter", 16), command=self.end_session,
                                      fg=self.master_button_text_highlight_colour, activebackground="#34495e", 
                                      highlightbackground=self.master_button_text_highlight_colour, 
                                      relief="raised")
        # self.end_session_button.grid(row=2, column=0, columnspan=3, pady=10)


    def update_final_game_state(self):
        """Updates the game winner attributes, player statistics and game over boolean."""
        self.game.update_winner_info()
        self.game.update_players_stats()
        self.game_over = True


    def display_custom_message(self, title, message):
        """Creates and displays a custom message dialog using a Toplevel window."""
        dialog = tk.Toplevel(self.master, bg="#2c3e50")
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.master) # Make the dialog a child of the main window
        dialog.grab_set() # Prevent interaction with the main window

        message_label = tk.Label(dialog, text=message, font=("Inter", 12),
                                 bg="#2c3e50", fg="#ecf0f1", wraplength=250)
        message_label.pack(padx=10, pady=20)

        ok_button = tk.Button(dialog, text="OK", command=dialog.destroy, font=("Inter", 14),
                              bg="#2ecc71", fg="white", activebackground="#27ae60", relief="raised")
        ok_button.pack(pady=10)

    def handle_end_of_game(self, message_title, message_text):
        """Handles all UI updates and game state changes that occur at the end of a game."""
        self.game.update_winner_info()
        self.game.update_players_stats()
        self.game_over = True
        
        self.display_custom_message(message_title, message_text)
        self.reset_button.config(text="Play Again")
        self.end_session_button.grid(row=5, column=0, columnspan=3, pady=10)
    

    def display_final_message(self, message_title, message_text):
        """Displays info message box for game win or draw and displays updated end-of-game buttons."""
        # messagebox.showinfo(message_title, message_text)
        self.display_custom_message(message_title, message_text)
        
        self.reset_button.config(text="Play Again") # change the reset button to play again at end of session
        self.end_session_button.grid(row=5, column=0, columnspan=3, pady=10) # have a end session or quit button
        self.master.after(100, lambda: self.master.focus_set())

    def button_click(self, row, col):
        """Handles the human player's move."""
        if not self.game_over and not self.current_player.is_ai_player:
            # Send the move to the backend Tic Tac Toe Game for processing if valid
            is_valid_move = self.game.is_valid(row=row, col=col)
            
            # Updates the UI and Tic Tac Toe Game after a valid move
            if is_valid_move:
                game_over = self.make_valid_move(row=row, col=col, marker=self.current_player.marker)
                if not game_over:
                    self.change_current_player()
                    self.check_ai_player_turn()
                    
    def check_ai_player_turn(self):
        if self.current_player.is_ai_player:
            self.master.after(575, self.make_ai_move) # Wait a moment before the AI move for user experience
    
    def change_current_player(self):
        self.current_player = self.player_2 if self.current_player.marker == 'x' else self.player_1
        self.status_label.config(text=f"{self.current_player.name}'s turn")

    def set_current_player(self):
        self.current_player = self.player_1 if self.game.go_first else self.player_2
        self.status_label.config(text=f"{self.current_player.name}'s turn")

    def make_valid_move(self, row, col, marker):
        # Updates the UI and Tic Tac Toe Game after valid move
        self.game.make_move(row=row, col=col, marker=self.current_player.marker)
        if self.current_player.marker == 'x':
            marker_colour =  "#8C1007" # "#660B05" # Crimson Red
        else:
            marker_colour =  "#3D74B6" # "#0D1164"  # Inidgo Blue
        self.buttons[row][col].config(text=self.current_player.marker, state=tk.DISABLED, disabledforeground=marker_colour)
        
        winner = self.game.check_winner()
        
        if winner:
            self.status_label.config(text=f"Game Over. {self.current_player.name} wins.")
            self.update_final_game_state()
            # Must call update_game() first to update the backend game state to get correct winner message
            self.display_final_message("Game Over", self.game.get_winner_string())
            return True
        elif self.game.board_is_full():
            self.status_label.config(text="Game Over. Cat's Game!")
            self.update_final_game_state()
            self.display_final_message("Cat's Game", "There was no winner so there will be no chicken dinner.")
            return True

        return False
        
    def make_ai_move(self):
        """Handles the AI player's move."""
        if not self.game_over and self.current_player.is_ai_player:
            # AI move is validated in Player Class by move()
            row, col = self.current_player.move(board=self.game.board.get_board())
            
            # Make the move and update the UI
            game_over = self.make_valid_move(row=row, col=col, marker=self.current_player.marker)
            if not game_over:
                self.change_current_player()

    def update_difficulty_options(self):
        """Shows or hides the difficulty selection based on the game mode."""
        if self.game_mode.get() == 1:
            self.start_button_frame.pack_forget()
            self.difficulty_options_frame.pack(pady=(20, 5))
            self.start_button_frame.pack(pady=20)
        else:
            self.difficulty_options_frame.pack_forget()

    def reset_game(self):
        """Resets the Tic Tac Toe Game state and GUI states."""
        self.game.reset_game_state()
        self.game_over = False
        
        # === Resetting the UI board ===
        # Resets the first player to be the player who lost the current game or the last player to move in case of draw
        self.set_current_player()
        print(self.game.move_list)
        if self.game.go_first:
            print("Player human")
        else:
            print("Player AI")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state=tk.NORMAL)
        self.reset_button.config(text="Reset") # change the reset button back
        self.end_session_button.grid_forget() # hide the end session button
        self.check_ai_player_turn()


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
