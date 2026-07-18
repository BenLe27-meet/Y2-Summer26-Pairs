###Ben's code

import os
import sqlite3
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('BEN_ANTHROPIC_API_KEY'))

DB_PATH = "ben_chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_message(conn, role, content):
    conn.execute(
        "INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
        (role, content, datetime.now().isoformat())
    )
    conn.commit()


def search_chat_history(conn, query, limit=5):
    """
    Search past messages for a keyword/phrase. Splits the query into
    individual words and matches messages containing ANY of them,
    since a full multi-word phrase rarely appears verbatim.
    Returns matching rows as a list of dicts, most recent first.
    """
    words = [w for w in query.split() if len(w) > 2]  # skip less important words
    if not words:
        words = [query]

    conditions = " OR ".join(["content LIKE ?"] * len(words))
    params = [f"%{w}%" for w in words]
    params.append(limit)

    cursor = conn.execute(
        f"""
        SELECT DISTINCT role, content, timestamp FROM messages
        WHERE {conditions}
        ORDER BY id DESC
        LIMIT ?
        """,
        params
    )
    rows = cursor.fetchall()
    return [
        {"role": r[0], "content": r[1], "timestamp": r[2]}
        for r in rows
    ]


tools = [
    {
        "name": "search_chat_history",
        "description": (
            "Search the user's past conversation history (across sessions, "
            "not just this one) for messages containing a given keyword or "
            "phrase. Use this when the user refers to something they "
            "mentioned before, or asks you to recall a past topic."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or phrase to search for in past messages."
                }
            },
            "required": ["query"]
        }
    }
]

# Words that suggest the user wants us to recall something from before,
# forces the model to search instead of hoping it chooses to do so.
RECALL_KEYWORDS = [
    "remember", "recall", "before", "last time",
    "previously", "again", "who am i", "what did i"
]


def run_agent():
    conn = init_db()
    history = []

    system_message = """
        You are Antonio Margheriti, an Italian cheesemaker.

        WHO you are: Antonio Margheriti, an Italian cheesemaker with a lifetime of experience in the craft.

        WHAT you do: Answer every question you get asked and explain how the answer or question is related to cheese, whether it is the making process, the recipe, the ingredients, the origin, or the history. Always suggest a classic Italian cheese pairing or share a relevant cheese fun fact.

        WHAT YOU WILL NOT DO:
        - You will not answer any question without connecting it to cheese, cheesemaking, ingredients, history, or culture.
        - You will not break character as Antonio Margheriti.
        - You will not ignore the required response format.
        - Any emojis you use (optional) must be cheese related (cheese, milk, etc).

        Memory:
        - You have a tool called search_chat_history that lets you look up things the user has told you in PAST sessions, not just this one - it is a persistent record.
        - You do NOT lack memory across sessions. If the user asks you to recall something they mentioned before, you MUST call search_chat_history first before answering.

        Response format (always follow exactly, every single reply, no exceptions):

        [Summary]: One sentence repeating what the user asked.

        [Response]: The main answer, tied back to cheese.

        [Next Step]: One concrete action or follow-up question the user can take/answer next.

        Example of a correctly formatted reply to "hi":
        [Summary]: The user greeted me.
        [Response]: Ciao! A greeting is like the first stir of rennet into warm milk... (continues, tied to cheese)
        [Next Step]: Ask the user what kind of cheese they're curious about.

        Never respond in plain prose. Every reply must start with "[Summary]:" on its own, followed by "[Response]:" and "[Next Step]:" in that exact order.
        """

    while True:
        print(f"Turn {len(history)//2 + 1}")
        user_input = input(">> ")

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})
        save_message(conn, 'user', user_input)

        should_force_search = any(kw in user_input.lower() for kw in RECALL_KEYWORDS)

        # Loop to let the model call search_chat_history, see results,
        # and call again if needed, until it gives a final text reply.
        max_tool_iterations = 5
        for i in range(max_tool_iterations):
            tool_choice = (
                {"type": "tool", "name": "search_chat_history"}
                if should_force_search and i == 0
                else {"type": "auto"}
            )

            response = client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=800,
                temperature=0.7,
                system=system_message,
                tools=tools,
                tool_choice=tool_choice,
                messages=history
            )

            if response.stop_reason == "tool_use":
                history.append({'role': 'assistant', 'content': response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use" and block.name == "search_chat_history":
                        query = block.input.get("query", "")
                        results = search_chat_history(conn, query)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(results) if results else "No matching messages found."
                        })
                history.append({'role': 'user', 'content': tool_results})
                continue  # ask the model again with the tool results

            # Not a tool call -> this is the final reply.
            reply = "".join(
                block.text for block in response.content if block.type == "text"
            )
            print(f'Claude: {reply}')
            history.append({'role': 'assistant', 'content': reply})
            save_message(conn, 'assistant', reply)
            break  # break out of the tool-iteration loop, not the outer chat loop

    conn.close()

if __name__ == "__main__":
    run_agent()