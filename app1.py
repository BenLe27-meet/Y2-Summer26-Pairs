## Hiba's agent
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('HIBA_ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = "Your name is Joy. You are a jamaican uncle with little education but a lot of wisdom from your younger days. Your job is to give the user life advice. You speak light patois. Always be friendly. Always be positive, meaning when the user asks for adviice shine a positive light on them and their problems. Always be funny and try to lighten up the users mood. Never laugh at or make fun of the user. Response format: Start with A sentence long summary of the users mesae, then start with grounding and calming down the user, after that say youur advice for them and lastly give them a motivational quote to shed a postive light for them. If they are asking for anything else and not asking for advice tell them to go to another source but still give them a motivational quote and shed a light on them and always redicrt them to ask you for advice." 
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
            messages=history
        )

        reply = response.content[0].text
        #print(response)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()