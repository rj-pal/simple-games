import tkinter as tk
from tkinter import messagebox
import games.tictactoe as tictactoe

# Initialize the main window and game
root = tk.Tk()
root.title("Tic Tac Toe")

game = tictactoe.TicTacToe()
game.update_player_name(name="Player 1", marker="x")
game.update_player_name(name="Player 2", marker="o")
player_1 = game.get_player(0)
player_2 = game.get_player(1)

# Global variables
current_player = player_1 if game.go_first else player_2
board = [["" for _ in range(3)] for _ in range(3)]
buttons = []
game_over = False

# Function to handle button clicks
def button_click(row, col):
    global current_player, game_over
    current_marker = current_player.marker
    current_name = current_player.name

    if board[row][col] == "" and not game_over:
        # Update the visual board
        board[row][col] = current_marker
        buttons[row][col].config(text=current_marker, state=tk.DISABLED, disabledforeground="black")
        
        # Call the backend game logic
        game.make_move(row, col, current_marker)
        
        # Check for winner or draw from the backend
        winner = game.check_winner()
        if winner:
            status_label.config(text=f"{current_name} wins!")
            game.update_winner_info()    
            messagebox.showinfo("Game Over", game.get_winner_string())
            game_over = True
            game.update_players_stats()
            reset_button.config(text="Play Again")
            end_session_button.grid(row=5, column=0, columnspan=3, pady=10)
        elif len(game.move_list) == 9:
            status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            game_over = True
            game.update_players_stats()
            reset_button.config(text="Play Again")
            end_session_button.grid(row=5, column=0, columnspan=3, pady=10)
        else:
            current_player = player_2 if current_marker == 'x' else player_1
            status_label.config(text=f"{current_player.name}'s turn")

# Function to reset the game state
def reset_game():
    global current_player, board, game_over
    # Reset game state based on who goes next
    current_player = player_2 if current_player.marker == 'x' else player_1
    game_over = False
    game.reset_game_state()
    board = [["" for _ in range(3)] for _ in range(3)]
    status_label.config(text=f"{current_player.name}'s turn")
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state=tk.NORMAL)
    reset_button.config(text="Reset")
    end_session_button.grid_forget()

# Function to end the game session
def end_session():
    # Assuming the 'game' object has a method to get final stats
    # Replace with your actual method to get stats from the backend
    end_message = "Game Session Ended.\n\n"
    for statistic in game.get_players_info_string_as_list():
        end_message += statistic
    
    # Display the message box
    messagebox.showinfo("Session Stats", end_message)
    
    # Close the application window
    root.destroy()

# Create a 3x3 grid of buttons for the board
for row in range(3):
    button_row = []
    for col in range(3):
        button = tk.Button(root, text="", font=("Helvetica", 24), width=5, height=2,
                           command=lambda r=row, c=col: button_click(r, c))
        button.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(button)
    buttons.append(button_row)

# Create a status label
status_label = tk.Label(root, text=f"{current_player.name}'s turn", font=("Helvetica", 16))
status_label.grid(row=3, column=0, columnspan=3, pady=10)

# Create a reset button
reset_button = tk.Button(root, text="Reset", font=("Helvetica", 16), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

# Create an end session button
end_session_button = tk.Button(root, text="End Session", font=("Helvetica", 16), command=end_session)


# Start the main event loop
root.mainloop()
