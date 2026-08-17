"""
ConnectFourGui.py 
Author: Robert Pal
Updated: 2025-09-11

This module contains all control flow logic for running the Connect Four Desktop Application.
It includes:
- button_click() which acts as the main() game running function
- helper functions to manage game states and UI display
"""
import tkinter as tk
from tkinter import messagebox
from games.connect4 import ConnectFour

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        master.title("Connect Four")
        self.master_colour = "#4682B4"  # Steel Blue
        self.master_text_colour = "#000000"
        self.master_select_colour = "#34495e"
        self.master_red =  "#CD5C5C" # "#B22222" <- alt darker red 
        self.master_yellow = "#F0E68C" #"#DAA520" <- alt bit darker yellow
        self.master.configure(bg=self.master_colour)
        master.geometry("800x650")
        master.resizable(True, True)

        # Initialize the backend game state with variables set by user input for one or two players
        self.game = ConnectFour()
        self.player_1 = None 
        self.player_2 = None 
        self.current_player = None 
        
        # Set front end application variables for game tracking and widgets
        self.board = [['' for _ in range(7)] for _ in range(6)]
        self.game_over = False
        self.buttons = []
        self.column_buttons = []

        self.difficulty = tk.StringVar(value="easy") # easy or intermediate mode only at this point
        self.game_mode = tk.IntVar(value=1) # 1 for single player, 2 for two players

        self.create_start_menu()

    def create_start_menu(self):
        """Creates the initial start screen widgets to set 1 or 2 player game mode and difficulty level for AI player in 1 player mode."""
        # Main frame for containing and centring all widgets
        self.main_frame = tk.Frame(self.master, bg=self.master_colour)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        title_label = tk.Label(self.main_frame, text="Connect Four", font=("Inter", 36, "bold"),
                               bg=self.master_colour, fg=self.master_text_colour)
        title_label.pack(pady=(0, 20))

        # Game mode selection widgets
        mode_label = tk.Label(self.main_frame, text="Select the Game Play Mode:", font=("Inter", 16),
                              bg=self.master_colour, fg=self.master_text_colour)
        mode_label.pack(pady=(10, 5))

        tk.Radiobutton(self.main_frame, text="One Player (vs AI Player)", font=("Inter", 14), variable=self.game_mode, value=1,
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor=self.master_select_colour, command=self.show_or_hide_difficulty_options_frame).pack(pady=2)
        tk.Radiobutton(self.main_frame, text="Two Players", font=("Inter", 14), variable=self.game_mode, value=2,
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor=self.master_select_colour, command=self.show_or_hide_difficulty_options_frame).pack(pady=2)    

        # AI Difficulty selection widgets wrapped in a frame to hide/show based on game mode
        self.difficulty_options_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        self.difficulty_options_frame.pack(pady=(20, 5))

        difficulty_label = tk.Label(self.difficulty_options_frame, text="Select AI Difficulty Level:", font=("Inter", 16),
                                    bg=self.master_colour, fg=self.master_text_colour)
        difficulty_label.pack(pady=(0, 5))

        tk.Radiobutton(self.difficulty_options_frame, text="Blind", font=("Inter", 14), variable=self.difficulty, value="easy",
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor=self.master_select_colour).pack(pady=2)
        tk.Radiobutton(self.difficulty_options_frame, text="Intermediate", font=("Inter", 14), variable=self.difficulty, value="intmed",
                       bg=self.master_colour, fg=self.master_text_colour, selectcolor=self.master_select_colour).pack(pady=2)
        # Allow for future option of advanced AI player as with Tic Tac Toe Game
        # tk.Radiobutton(self.difficulty_options_frame, text="Impossible", font=("Inter", 14), variable=self.difficulty, value="hard",
        #                bg=self.master_colour, fg=self.master_text_colour, selectcolor=self.master_select_colour).pack(pady=2)

        # Start Button to set the game variables and move on to game play widget
        self.start_button_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        self.start_button_frame.pack(pady=(20, 5))
        start_button = tk.Button(self.start_button_frame, text="Start Game", font=("Inter", 16), command=self.start_game,
                                 fg=self.master_text_colour, highlightbackground=self.master_text_colour, 
                                 highlightthickness=3, relief="raised")
        start_button.pack(pady=20)


    def start_game(self):
        """Initializes the game and switches from the start menu to the game board."""
        # Destroy start menu widgets since game variables for play will be set based on configs from start widgets
        self.main_frame.destroy()
        
        # Initialize the backend game state based on selections - allow for future hard mode optionality - based on two mappings for backend args
        difficulty_dictionary = {
            "easy": None, 
            "intmed": False
            # "hard": True
        }
        name_dictionary = {
            "easy": "CPU Easy",
            "intmed": "CPU Intermediate"
            # "hard": "CPU Hard"
        }

        if self.game_mode.get() == 1:
             self.game.create_ai_player(difficulty=difficulty_dictionary[self.difficulty.get()]) 
       
        self.player_1 = self.game.get_player(0)
        self.player_2 = self.game.get_player(1)
        self.current_player = self.player_1 if self.game.go_first else self.player_2

        # Create and display the game board
        self.create_game_board_gui()
        # Play AI player if AI player is set to go first
        self.check_ai_player_turn()

    def create_game_board_gui(self):
        """Creates and places all GUI widgets for the main game board."""
        self.main_frame = tk.Frame(self.master, bg=self.master_colour)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        player_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        player_frame.pack()
        self.status_label = tk.Label(player_frame, text=f"● plays", font=("Inter", 18, "bold"),
                                     bg="white", fg=self.get_current_colour(),
                                     padx=10, pady=5, relief="raised", borderwidth=2)
        # Use pack with side='left' to push it to the left
        self.status_label.pack(side='left', padx=(0, 60), expand=True, fill='x')

        self.reset_button = tk.Button(player_frame, text="Reset", font=("Inter", 18), command=self.reset_game,
                                      bg="white", fg="black", activebackground=self.master_select_colour,
                                      relief="raised", takefocus=0)
        # Use pack with side='right' to push it to the right
        self.reset_button.pack(side='right', padx=(60, 0), expand=True, fill='x')

        self.end_session_button = tk.Button(player_frame, text="End Session", font=("Inter", 18), command=self.end_session,
                                      fg="black", activebackground=self.master_select_colour, 
                                      relief="raised",takefocus=0)
        
        # Add space after the player_frame
        spacer = tk.Frame(self.main_frame, height=20, bg=self.master_colour)
        spacer.pack()

        # Create a frame for the column buttons
        column_button_frame = tk.Frame(self.main_frame, bg=self.master_colour)
        column_button_frame.pack(pady=10)

        # Create 7 buttons, one for each column
        for col in range(7):
            button = tk.Button(column_button_frame, text="▼", font=("Inter", 24, "bold"), width=2,
                               fg="#ffffff", activebackground=self.get_current_colour(),
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
        if not self.game_over and self.current_player.is_human:
            # Send the move to the backend Connect 4 for processing if valid
            is_valid_move = self.make_valid_move(col=col, marker=self.current_player.marker)
            
            # Updates the UI and Connect 4 Game after a valid move
            if is_valid_move:
                winner = self.end_game_if_winner()
                if not winner:  
                    if not self.game_over:
                        self.change_current_player()
                        self.status_label.config(text=f"● plays", fg=self.get_current_colour())
                        self.check_ai_player_turn()

    def end_game_if_winner(self):
        winner = self.game.check_winner()
        if winner:
            self.update_final_gui_state(final_message=f"{self.current_player.marker_name} wins the game!")
            self.update_final_game_state()
            return True
        else:
            if self.game.is_full_board():
                self.update_final_gui_state(final_message="The game is a draw!")
                self.update_final_game_state()
                return False
            return False
        
    def update_final_gui_state(self, final_message):
        messagebox.showinfo("Game Over", final_message)
        self.reset_button.config(text="Play Again")
        self.end_session_button.pack(side='left', padx=20, expand=True, fill='x')
    
    def update_square(self, col):
        row = self.game.height_list[col] # Game height list tells us which row is available for play for any column
        canvas_to_update = self.buttons[row][col]
        canvas_to_update.itemconfig(canvas_to_update.find_all()[0], fill=self.get_current_colour())

    def make_valid_move(self, col, marker):
        # Updates the UI and Connect 4 Game after valid move
        is_valid = self.game.make_move(col=col, marker=self.current_player.marker)
        if is_valid:
            self.update_square(col=col)
            return True
        else:
            return False

        
    def make_ai_move(self):
        """Handles the AI player's move."""
        if not self.game_over and not self.current_player.is_human:
            # AI move is validated in Player Class by move()
            col = self.current_player.move()
            self.game.make_move(col, self.current_player.marker)
           
            # Make the move and update the UI
            self.update_square(col)
            winner = self.end_game_if_winner()
            if not winner:
                self.change_current_player()
                self.status_label.config(text=f"● plays", fg=self.get_current_colour())
  
        
    def show_or_hide_difficulty_options_frame(self):
        """Shows or hides the difficulty selection based on the game mode."""
        if self.game_mode.get() == 1:
            self.start_button_frame.pack_forget()
            self.difficulty_options_frame.pack(pady=(20, 5))
            self.start_button_frame.pack(pady=20)
        else:
            self.difficulty_options_frame.pack_forget()
        
    def update_final_game_state(self):
        """Updates the game winner attributes, player statistics and game over boolean."""
        self.game.update_winner_info()
        self.game.update_players_stats()
        self.game_over = True

    def reset_game(self):
        """Resets the Connect Four Game state and GUI states."""
        self.game.reset_game_state()
        self.game_over = False

        # === Resetting the UI board ===
        # Resets the first player to be the player who lost the current game or the last player to move in case of draw
        self.change_current_player()
        self.status_label.config(text=f"● plays", fg=self.get_current_colour())
        
        for row in range(6):
            for col in range(7):
                canvas = self.buttons[row][col]
                # Get the ID of the oval (the only item on the canvas)
                oval_id = canvas.find_all()[0]
                # Change the oval's fill color back to the original gray
                canvas.itemconfig(oval_id, fill="#ecf0f1")
        self.reset_button.config(text="Reset") # change the reset button back
        self.end_session_button.pack_forget() # hide the end session button
        self.check_ai_player_turn()

    def get_current_colour(self):
        return self.master_red if self.current_player.marker == 'r' else self.master_yellow


    def change_current_player(self):
        self.current_player = self.player_2 if self.current_player.marker == 'r' else self.player_1
        # self.status_label.config(text=f"{self.current_player.name}'s turn")

    def check_ai_player_turn(self):
        if not self.current_player.is_human:
            self.master.after(575, self.make_ai_move) # Wait a moment before the AI move for user experience   

    def end_session(self):
        """Ends the game session and closes the application."""
        end_message = "Game Session Ended.\n\n"
        for statistics in self.game.get_players_info_string_as_list():
            end_message += statistics
        messagebox.showinfo("Session Stats", end_message)
        self.master.destroy()
        
def run():
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run()