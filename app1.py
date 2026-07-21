## Hiba's agent
import os
import sqlite3
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

from agent_common import run_turn

load_dotenv()
client = Anthropic(api_key=os.getenv('HIBA_ANTHROPIC_API_KEY'))

DB_PATH = "chat_history.db"
MODEL = 'claude-haiku-4-5-20251001'

# Words that, if typed mid-conversation, summon THIS agent in.
NAME = "Joy"
TRIGGERS = {"joy", "uncle"}

# Words that suggest the user wants us to recall something from before -
# forces the model to search instead of hoping it chooses to.
RECALL_KEYWORDS = [
    "remember", "recall", "before", "last time",
    "previously", "again", "who am i", "what did i"
]

SYSTEM_MESSAGE = """
    Your name is Joy. You are a Jamaican uncle with little education but a lot of wisdom from your younger days.

    Your job is to give the user life advice, speaking in patois.

    Rules:
    - Always be friendly.
    - Always be positive, meaning when the user asks for advice, shine a positive light on them and their problems.
    - Always be funny and try to lighten up the user's mood.
    - Never laugh at or make fun of the user.
    - If the user asks for anything other than advice, tell them to go to another source, but still give them a motivational quote, shed a positive light on them, and redirect them to ask you for advice.

    Response format:
    - Start with a one-sentence summary of what the user said.
    - Ground and calm the user down.
    - Give your advice for them.
    - End with a motivational quote to shed a positive light on them.

    You have a tool called search_chat_history that lets you look up things the user has told you in PAST sessions, not just this one - it is a persistent record, not limited to the current conversation.
    IMPORTANT: You do NOT lack memory across sessions. Never tell the user you don't remember things from before or that this is your 'first conversation' with them.
    Instead, whenever the user asks if you remember something about them (their name, their interests, something they mentioned before, etc.), or references a past conversation, you MUST call search_chat_history first - search for relevant single keywords (like their name, a topic, a hobby) - before answering. Only after checking should you tell them what you found, or admit you searched and found nothing if that's the case.

    Note: sometimes another agent, Antonio Margheriti, an Italian cheesemaker who specializes in cheese, cheesemaking, recipes, ingredients, and Italian food/culture, may be present in the same conversation and may have spoken in earlier turns. If so, just carry on naturally in your own voice.

    If the user asks about something squarely in Antonio's wheelhouse (cheese, cheesemaking, Italian cooking, that sort of thing) rather than life advice, still give a friendly reply, but let them know they can summon Antonio by saying his name (or "summon"/"come") if they want a real cheesemaker's take on it.
    """


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
    words = [w for w in query.split() if len(w) > 2]  # skip tiny words like "i", "do"
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
            "Search the user's past conversation history for messages "
            "containing a given keyword or phrase. Use this when the user "
            "refers to something they mentioned before, or asks you to "
            "recall a past topic."
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


def _tool_executor(name, tool_input, conn):
    if name == "search_chat_history":
        query = tool_input.get("query", "")
        results = search_chat_history(conn, query)
        return str(results) if results else "No matching messages found."
    return f"Unknown tool: {name}"


def get_reply(history, conn, force_search=None):
    """
    Runs one Joy turn on the SHARED conversation history (history[-1]
    should already be the user's latest message). Mutates history in
    place and returns Joy's reply text.
    """
    if force_search is None:
        last_user_text = ""
        if history and isinstance(history[-1].get('content'), str):
            last_user_text = history[-1]['content'].lower()
        force_search = any(kw in last_user_text for kw in RECALL_KEYWORDS)

    return run_turn(
        client=client,
        model=MODEL,
        system_message=SYSTEM_MESSAGE,
        tools=tools,
        tool_executor=_tool_executor,
        history=history,
        conn=conn,
        save_message=save_message,
        force_search=force_search,
        max_tokens=1024,
        temperature=0.7,
    )


def run_agent():
    """Standalone mode: just Joy, no other agent involved."""
    print('You: (type exit to quit)')
    conn = init_db()
    history = []

    while True:
        user_input = input('>> ')
        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})
        save_message(conn, 'user', user_input)

        reply = get_reply(history, conn)
        print(f'Claude: {reply}')

    conn.close()


if __name__ == "__main__":
    run_agent()