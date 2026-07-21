import app1
import app2

# Generic words that summon "whichever agent isn't currently active",
# in addition to each agent's own name-style triggers (defined in
# app1.TRIGGERS / app2.TRIGGERS, e.g. "joy", "antonio").
GENERIC_SUMMON_WORDS = {"summon", "come", "come here", "come in", "join"}

AGENTS = {
    "joy": {
        "display": app1.NAME,
        "module": app1,
        "conn": app1.init_db(),
    },
    "antonio": {
        "display": app2.NAME,
        "module": app2,
        "conn": app2.init_db(),
    },
}


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
            return "joy"
        elif choice == "2":
            return "antonio"
        else:
            print(f"\n'{choice}' isn't a valid option. Please try again.\n")


def detect_summon(user_input, active_key):
    """
    Returns the key of the agent that should become active based on the
    user's message, or None if no summon was triggered.
    """
    text = user_input.lower()

    # Named triggers, e.g. typing "antonio" or "uncle" or "joy".
    for key, info in AGENTS.items():
        if key == active_key:
            continue
        if any(trig in text for trig in info["module"].TRIGGERS):
            return key

    # Generic triggers, e.g. "summon" or "come" -> bring in the other one.
    if any(word in text for word in GENERIC_SUMMON_WORDS):
        others = [k for k in AGENTS if k != active_key]
        if others:
            return others[0]

    return None


REPEAT_WORDS = {"repeat", "same", "yes", "same question", "the same one",
                 "repeat it", "repeat that", "same one"}
NEW_WORDS = {"new", "new one", "something new", "no", "ask new", "a new one"}


def classify_followup(text):
    """
    Interprets the user's answer to 'repeat the old question or ask a
    new one?'. Returns 'repeat', 'new' (meaning: prompt them again for
    the actual new question), or 'custom' (meaning: the text they just
    typed IS the new question, so use it directly).
    """
    t = text.lower().strip()
    if t in REPEAT_WORDS:
        return "repeat"
    if t in NEW_WORDS:
        return "new"
    return "custom"


def ask_agent(history, info, question):
    """Appends `question` as the user turn, gets this agent's reply, prints it."""
    history.append({'role': 'user', 'content': question})
    info["module"].save_message(info["conn"], 'user', question)
    reply = info["module"].get_reply(history, info["conn"])
    print(f"{info['display']}: {reply}")


def run_shared_conversation(active_key):
    """
    Runs a single conversation with a shared message history. The user
    can type a summon word at any point to switch which agent responds
    next; both agents see the same history, but each still keeps its
    own database of turns it personally spoke.

    When a new agent is summoned, before they answer anything, they ask
    whether the user wants their previous question repeated to the new
    agent, or wants to ask something new.
    """
    history = []
    last_question = None
    print(f"\nStarting with {AGENTS[active_key]['display']}. "
          f"(type 'exit' to quit; type the other agent's name, or 'summon'/'come', to bring them in)\n")

    while True:
        user_input = input(">> ").strip()
        if user_input.lower() == 'exit':
            break
        if not user_input:
            continue

        summoned_key = detect_summon(user_input, active_key)

        if summoned_key and summoned_key != active_key:
            previous_display = AGENTS[active_key]['display']
            active_key = summoned_key
            info = AGENTS[active_key]
            print(f"*{info['display']} joins the conversation*")

            if last_question:
                print(f"{info['display']}: Do you want me to repeat the question "
                      f"you asked {previous_display}, or ask a new one?")
                followup = input(">> ").strip()
                choice = classify_followup(followup)

                if choice == "repeat":
                    question = last_question
                elif choice == "new":
                    question = input(">> ").strip()
                else:
                    question = followup  # they typed the new question directly
            else:
                # Nobody's asked anything yet, nothing to repeat.
                print(f"{info['display']}: What can I help you with?")
                question = input(">> ").strip()

            ask_agent(history, info, question)
            last_question = question
            continue

        # Normal turn, no summon involved.
        info = AGENTS[active_key]
        ask_agent(history, info, user_input)
        last_question = user_input

    for info in AGENTS.values():
        info["conn"].close()


def main():
    starting_agent = get_choice()
    run_shared_conversation(starting_agent)


if __name__ == "__main__":
    main()