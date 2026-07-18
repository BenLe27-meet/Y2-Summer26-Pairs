import app1
import app2


def show_menu():
    print("Which agent do you want to use?\n")
    print("1. Agent 1 — Joy, your Jamaican uncle, gives life advice and remembers past chats")
    print("2. Agent 2 — Antonio Margheriti, an Italian cheesemaker who connects everything back to cheese")
    print()


def get_choice():
    while True:
        show_menu()
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            return "1"
        elif choice == "2":
            return "2"
        else:
            print(f"\n'{choice}' isn't a valid option. Please try again.\n")


def main():
    choice = get_choice()

    if choice == "1":
        print("\nStarting Agent 1 — Joy...\n")
        app1.run_agent()
    elif choice == "2":
        print("\nStarting Agent 2 — Antonio Margheriti...\n")
        app2.run_agent()


if __name__ == "__main__":
    main()