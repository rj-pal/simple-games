from cli import TicTacToeCLI, ConnectFourCLI

def main():
    print("Select a game:")
    print("1. Tic Tac Toe")
    print("2. Connect 4")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        TicTacToeCLI.run()
    elif choice == '2':
        ConnectFourCLI.run()
    else:
        print("Invalid choice. See you next time.")

if __name__ == '__main__':
    main()
