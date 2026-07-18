## Hiba's agent
import os
# sqlite is an anthropic database that stores chat history
import sqlite3
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime



load_dotenv()
client = Anthropic(api_key=os.getenv('HIBA_ANTHROPIC_API_KEY'))

DB_PATH = "chat_history.db"

# Database setup:
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
    Search past messages for a keyword/phrase. Returns matching rows
    as a list of dicts, most recent first.
    """
    cursor = conn.execute(
        """
        SELECT role, content, timestamp FROM messages
        WHERE content LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{query}%", limit)
    )
    rows = cursor.fetchall()
    return [
        {"role": r[0], "content": r[1], "timestamp": r[2]}
        for r in rows
    ]

# Defining the tool:
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

# Chat loop:
def run_chat():
    print('You: (type exit to quit)')
    system_message = "Your name is Joy. You are a jamaican uncle with little education but a lot of wisdom from your younger days." \
    " Your job is to give the user life advice. You speak patois. " \
    "Always be friendly. " \
    "Always be positive, meaning when the user asks for adviice shine a positive light on them and their problems. " \
    "Always be funny and try to lighten up the users mood. " \
    "Never laugh at or make fun of the user. " \
    "Response format: " \
    "Start with A sentence long summary of the users mesae, then start with grounding and calming down the user, after that say youur advice for them and lastly give them a motivational quote to shed a postive light for them. If they are asking for anything else and not asking for advice tell them to go to another source but still give them a motivational quote and shed a light on them and always redicrt them to ask you for advice." 
    conn = init_db()
    history = []

    while True:
        user_input = input('>> ')
        

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})
        #print('History:',history)
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1024,
            temperature=0.7,
            system=system_message,
            tools=tools,
            messages=history
        )
        if response.stop_reason == "tool_use":
            history.append({'role': 'assistant', 'content': response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use" and block.name == "search_chat_history":
                    query = block.input.get("query", "")
                    results = search_chat_history(conn, query)
                    tool_results.append({ "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(results) if results else "No matching messages found."
                        })
            history.append({'role': 'user', 'content': tool_results})
            continue
            break        
        reply = "".join(
            block.text for block in response.content if block.type == "text"
        )
        #print(response)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})
        save_message(conn, 'assistant', reply)
 
    conn.close()
if __name__ == "__main__":
    run_chat()