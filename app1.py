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
    system_message = f"""
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
        """
    
    history = []
 
    while True:
        user_input = input('>> ')
 
        if user_input.lower() == 'exit':
            break
 
        history.append({'role': 'user', 'content': user_input})
        save_message(conn, 'user', user_input)
<<<<<<< Updated upstream
 
        # If the user seems to be asking us to recall something, force a
        # search on the first call instead of hoping the model chooses to.
        recall_keywords = [
            "remember", "recall", "before", "last time",
            "previously", "again", "who am i", "what did i"
        ]
        should_force_search = any(kw in user_input.lower() for kw in recall_keywords)
 
        # Loop here to let the model call the tool, see the result,
        # and call it again if needed, until it gives a final text reply.
        max_tool_iterations = 5
        for i in range(max_tool_iterations):
            tool_choice = (
                {"type": "tool", "name": "search_chat_history"}
                if should_force_search and i == 0
                else {"type": "auto"}
            )
            response = client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=1024,
                temperature=0.7,
                system=system_message,
                tools=tools,
                tool_choice=tool_choice,
                messages=history
            )
 
=======
        #print('History:',history)


        while True:
            response = client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=500,
                temperature=0.7,
                system=system_message,
                tools=tools,
                messages=history
            )
>>>>>>> Stashed changes
            if response.stop_reason == "tool_use":
                history.append({'role': 'assistant', 'content': response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use" and block.name == "search_chat_history":
                        query = block.input.get("query", "")
<<<<<<< Updated upstream
                        print(f"[DEBUG] Forced/auto search query: {query!r}")
                        results = search_chat_history(conn, query)
                        print(f"[DEBUG] Found {len(results)} result(s)")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(results) if results else "No matching messages found."
                        })
                history.append({'role': 'user', 'content': tool_results})
                continue  # go around the for-loop, ask the model again with tool results
 
            # Not a tool call -> this is the final reply
            reply = "".join(
                block.text for block in response.content if block.type == "text"
            )
            print(f'Claude: {reply}')
            history.append({'role': 'assistant', 'content': reply})
            save_message(conn, 'assistant', reply)
            break  # break out of the for-loop (tool iterations), NOT the outer chat loop
=======
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
>>>>>>> Stashed changes
 
    conn.close()
 
if __name__ == "__main__":
    run_chat()