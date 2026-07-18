###Ben's code

import os
import re
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('BEN_ANTHROPIC_API_KEY'))

def run_chat():
    history = []

    goal_tracker = input("Please enter your goal for this session: ")

    system_message = f"""
        You are Antonio Margheriti, an Italian cheesemaker.

        Your job is to answer every question you get asked and explain how the answer or question is related to cheese, whether it is the making process, the recipe, the ingredients, the origin, or the history.
        
        goals:
        {goal_tracker}

        Rules:
        - Always explain the connection to cheese, no matter the topic of the user's question.
        - Always suggest a classic Italian cheese pairing or share a relevant cheese fun fact.
        - All emojis you use (you don't have to use them) must be cheese related (cheese, milk etc)
        - Never give a plain answer without tying it back to cheesemaking, ingredients, history, or culture.
        - You will not answer questions without connecting them to cheese.
        - You will not break character as Antonio Margheriti.
        - You will not ignore the required response format.

       Response format (always follow exactly):

        [Summary]: One sentence repeating what the user asked.

        [Response]:
        - Give your answer.
        - Explain how it relates to cheese.
        - Include the scoring rubric (1–5).
        - Suggest a classic Italian cheese pairing or a cheese fun fact.

        [Next Step]:
        Ask one follow-up question that the user can answer and that you can score.

        The last line of every response must be:
        Score: X
        where X is the score (1–5) of the user's previous answer. Do not write anything after this line.
        """
    
    count_tokens = 0
    total_tokens_cost = 0
    user_responses_scores = []

    while True:
        print(f"Turn {len(history)//2 + 1}")
        user_input = input(">> ")


        if user_input.lower() == 'exit':
            if user_responses_scores:
                average_answer_score = sum(user_responses_scores) / len(user_responses_scores)
                print(f"Your average answer score was: {average_answer_score}")
            break

        elif user_input.lower() == 'reset':
            history.clear()
            user_responses_scores.clear()
            print("Chat History Cleared")
            continue

        elif user_input.lower() == '/summary':
            print(history)
            continue

        if len(history)>3:
            print('History:', history) ##There will be 6 messages because the history includes both the AI's and the user's

        history.append({'role': 'user', 'content': user_input})

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=800,
            temperature=1, ## Temprature controls the randomness of the output the AI gives,
                            ## higher values make the answer more random while lower values make it more dull and boring
            system=system_message,
            messages=history
        )

        print(f"The amount of tokens used is: {response.usage.input_tokens + response.usage.output_tokens}")
        
        count_tokens += (response.usage.input_tokens + response.usage.output_tokens)
        print(f"The total amount of tokens used is: {count_tokens}")

        total_tokens_cost += ((response.usage.input_tokens / 1000000) * 0.25 + (response.usage.output_tokens / 1000000) * 1.25)
        print(f"The estimated total cost is: {total_tokens_cost}")


        #print(response)
        ## usage.input_tokens is the amount of tokens the prompt you sent "costs"
        ## usage.output_tokens is the amount of tokens the AI's response costs
        reply = response.content[0].text
        
        match = re.search(r"Score:\s*([1-5])\s*$", reply)

        if match:
            digit = int(match.group(1))
            user_responses_scores.append(digit)
        else:
            backup_match = re.findall(r"Score:\s*([1-5])", reply)
            if backup_match:
                digit = int(backup_match[-1])
                user_responses_scores.append(digit)
            else:
                digit = None

        print(digit)
        print (user_responses_scores)
        print("this is the comment were searching for")
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()


###Lab 1 Reflection
'''
1. An example of a situation in which I have to bring the entire backstory every single time in order to get what 
I want is when I talk to one of my teachers. Her name is Shirly and every time I see she forgets my name and I
need to remind her what it is.

2. 
If you delete this line: history.append({'role': 'assistant', 'content': reply}), 
The AI won't add any information to history and will completly lose the ability to remember.

If you delete this line: load_dotenv(), the code will run the parts that are not related to the API,
the moment you need to use the API and try to connect to the Anthropic servers you will not be able to.
Without loading .env, your code doesnt have access to the API key.

If you delete the 'break' in this line: if user_input.lower() == 'exit':, when you try to quit you will not be
able to because there isn't a way to stop the loop.

3. The major bug I had while working on Lab 1 was that the API key we got was wrong and I wasn't able to 
test my code. At first I thought there was something wrong with my code, later with the help of Said
we fixed it and it worked.
'''

###Lab 2 Reflection
'''
1. A personal analogy in my life that is a bit similar (not too much similarity) to the use of tokens when the
price slowly but surely keeps rising is when I'm adding things to my AliExpress cart and the price goes
up without me noticing. Another example is Netflix/Spotify subscriptions that become more expensive.

2.
If you delete this line: history.append({'role': 'user', 'content': user_input}), the AI will not keep
track of your questions. The amount of input tokens will not increase (due to the previous questions) because
it isn't resending them.

3. I had another bug with the API key. At first I assumed thete was another issue with my code because I
thought it wasn't likely the API had another issue. There ended up being another issue with it and this time Lil
helped Yotam and I solve it by giving us a new one. After it we could test our code and continue working.
'''

###Lab 3 Reflection
'''
1. I'd say that compared to the system message giving a lot of context without you needing to send/view it,
something that works similarly in my personal life (and in most people's) is that when others see you, 
they get informaion based on your appearance, voice, friends, etc.

2. Without the line: system=system_message, your AI results to it's default personality. It doesn't have 
anything unique and will overall act bland and be very regular.

3. One major bug I had was while trying to solve the 3rd bonus (scoring system). I assumed that it was possible
to move the scoring mechanisem through the system to the list but it turned out to be wrong. I figured it out by
researching a solution. That is how I found out I needed to use the 're' library and it solved everything.

Bonus: because I was originally told I wasn't supposed to do the reflecction I completed it today with my
current POV and knowledge. I think that the way I phrased the analogy was pretty good because it's a personal
experience from me and for those reasons there ins't a way I could phrase it better at the moment.
'''
