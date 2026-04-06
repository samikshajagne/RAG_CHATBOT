from chatbot import BankingChatbot


def main():
    print("=" * 50)
    print("      AI Banking Assistant (CLI)")
    print("  Type 'exit' or 'quit' to stop")
    print("=" * 50 + "\n")

    bot = BankingChatbot()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "bye", "q"]:
            print("Goodbye!")
            break

        reply = bot.ask(user_input)
        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    main()
