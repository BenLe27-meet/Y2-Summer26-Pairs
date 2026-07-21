"""
Shared logic used by both agents: the tool-call loop that talks to the
Anthropic API, lets the model call search_chat_history if it wants to,
feeds the result back, and returns the final text reply.

Kept in one place so app1.py and app2.py don't duplicate this logic.
"""


def run_turn(client, model, system_message, tools, tool_executor,
             history, conn, save_message, force_search=False,
             max_tokens=1024, temperature=0.7, max_tool_iterations=5):
    """
    Runs one agent "turn" against the shared conversation history.

    - history: the SHARED list of {'role':..., 'content':...} messages.
               Mutated in place (tool_use / tool_result / final reply all
               get appended here), since both agents read/write the same
               conversation.
    - conn:    this agent's own sqlite connection (for saving + search).
    - tool_executor(name, input_dict, conn) -> str : runs the named tool
               and returns a string result.
    - force_search: if True, forces a tool call on the first iteration
               (used when the user's message looks like a recall request).

    Returns the final reply text (also appended to history + saved to conn).
    """
    for i in range(max_tool_iterations):
        tool_choice = (
            {"type": "tool", "name": tools[0]["name"]}
            if force_search and i == 0
            else {"type": "auto"}
        )

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            tools=tools,
            tool_choice=tool_choice,
            messages=history
        )

        if response.stop_reason == "tool_use":
            history.append({'role': 'assistant', 'content': response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = tool_executor(block.name, block.input, conn)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            history.append({'role': 'user', 'content': tool_results})
            continue  # let the model see the tool result and respond again

        # Not a tool call -> final reply for this turn.
        reply = "".join(
            block.text for block in response.content if block.type == "text"
        )
        history.append({'role': 'assistant', 'content': reply})
        if conn is not None:
            save_message(conn, 'assistant', reply)
        return reply

    # Ran out of tool iterations without a final text reply.
    fallback = "(trouble putting that into words right now, try again?)"
    history.append({'role': 'assistant', 'content': fallback})
    if conn is not None:
        save_message(conn, 'assistant', fallback)
    return fallback