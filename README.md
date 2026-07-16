# Y2-Summer26-Pair-Project
# Objective

During Labs 1-3, each of you built an AI agent using the Claude API. Your agent could complete a task through the terminal, but it worked independently and had no graphical interface.

By the end of Lab 6, your team should have a working multi-agent application with a fully functional backend and a frontend built using Bolt.

# Requirements

Your finished project should include:

- **One AI agent per team member.** Teams of two should build two collaborating agents. Teams of three should build three.
- **A clear responsibility for each agent.** Every agent should contribute something different to the overall product.
- **A deliverable for the user.** The user should receive something useful—not just text. Examples include a study plan, checklist, report, travel plan, exported document, or another useful result.
- **One working tool call.** a python function, e.g.: export to PDF/text, save a file, search past results, or generate a calendar-style output.
- **Relevant responses.** Your agents should react to the user's input and to information received from the other agents. Avoid generic responses that could fit every conversation.
- **Functional User Interface.** Your app has a well designed user interface created by Bolt.

## Milestone 1 — Design Before You Build

Before writing new code, design your product as a team.

Decide:

- What is the main idea of the web app?
- What responsibility does each agent have?
- How does the user move through the application from beginning to end?
- What is the final product?

**Next, get your idea approved by your instructors**

## Milestone 2 — System Prompts

Build a strong and precise System Prompt for each agent

Your system prompt should answer the following statements:

- WHO the agent is (name and role)
- WHAT it does (specific task)
- WHAT IT WILL NOT DO (clear boundaries)

> 💡 **Remember, Agents have a role and a goal.**

Update the system prompt so every response uses this exact format:

- [Summary]: one sentence repeating what the user asked
- [Response]: the main answer
- [Next Step]: one concrete action the user can take

## Milestone 3 — Build the Backend

Now begin implementing your complete backend, each agent on a different python file, you should have: app1.py and app2.py

By the end of this milestone, your team should have:

- every agent working independently
- all required tool calls functioning (python function that produces
- the complete workflow running successfully from the terminal

Do **not** use Bolt yet.

At this stage, everything should work without a graphical interface.

**Test: send a few messages and confirm the agent stays in role, follows the format, and gives a better answer on a hard question.**

Your file structure should look like this:

![][image1]

### ✅ Backend Checklist

Before moving on, make sure every statement below is true.

- [ ] Every agent works correctly by itself.
- [ ] Every agent has a clear responsibility.
- [ ] Tool calls work reliably.
- [ ] The complete workflow runs from start to finish in the terminal.
- [ ] Every team member understands how the backend works.

Only after completing this checklist should you continue.

## Milestone 4 — Connect your agents together

In this milestone, you'll bring both agents into one app. Instead of running app1.py and app2.py separately, the user picks which agent they want to use when they run the program.

What this means: you write one new file (like main.py) that starts by asking the user a question, like:

"Which agent do you want to use?

1. Agent 1 — [does X]
2. Agent 2 — [does Y]"

Based on what the user picks, main.py calls that agent's function and runs it.

Steps:

- Turn each agent into a callable function. Instead of running app1.py and app2.py on their own, each file should have one function like run_agent(input) that returns a result. main.py will import both.
- Write the selection menu. In main.py, ask the user which agent they want (by number or name), and use their answer to decide which function to call.
- Run only the chosen agent. Once the user picks, main.py should call that agent's function, pass along whatever input it needs, and show the result — the other agent should not run.
- Make sure both options actually work. Test picking Agent 1, then restart and test picking Agent 2. Each should complete its task and produce a result on its own.
- Handle a bad input. If the user types something that isn't a valid option, the app should ask again instead of crashing.

> 💡 **Remember Test each agent through the menu one at a time. Confirm Agent 1 works through main.py before testing Agent 2.**

Your file structure should look like this:

![][image2]

### Connection Checklist

- [ ] Running main.py shows a clear menu asking which agent to use.
- [ ] Picking Agent 1 runs only Agent 1 and gives a correct result.
- [ ] Picking Agent 2 runs only Agent 2 and gives a correct result.
- [ ] Invalid input doesn't crash the app.
- [ ] Both partners understand how main.py picks and runs the chosen agent.

Once every box is checked, you're ready to build the Bolt frontend.

## Milestone 5 — Building the face

Now it's time to turn your working backend into a real app using Bolt.

Write one detailed prompt for Bolt that explains:

- What your app does and the problem it solves
- What each agent does (its specific job)
- How you want the app to look and the features of it:
  - A tab and chat page for each agent
  - A loading indicator while the agent is thinking
  - A send button
  - A chat bar, etc...


Since you already have 3 Python files (your agents), you can import your GitHub repository directly into Bolt. This lets Bolt read and use your existing backend code to build the app around it, instead of writing the backend from scratch.

Copy this and include it in your prompts:

```
"Update the Anthropic client initialization to read the base URL from the environment:
`new Anthropic({ apiKey, baseURL: process.env.ANTHROPIC_BASE_URL })`. Then add `ANTHROPIC_API_KEY=your-key-here`
and `ANTHROPIC_BASE_URL=your-base-url` to the environment variables."
```

- Next, in the Bolt editor, find the `.env` file or the environment variables section.
- Then in Bolt's env panel, set both:
  ```
  ANTHROPIC_API_KEY=your-key-here
  ANTHROPIC_BASE_URL=your-base-url
  ```

> 💡 **Remember what we talked about in our previous sessions about clarity, feedback, and focus? Make sure to keep those in mind when prompting!**

! []

## Milestone 6 — Test and Improve

Test your complete application like a real user.

Try different inputs, including unexpected ones.

When you find a problem, fix one issue at a time and test again.

Continue improving your prompts, backend, and frontend until the entire system works reliably.

Once you reach this stage, deploy your web app: click on the publish button in Bolt so your project goes live!

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOwAAAC5CAYAAAArkNNQAAARvklEQVR4Xu3dS1cURxsH8HwNBUSQmwMqBBLiDQIaddQBxGDkVQyKRmSOcoJHJCj6Eh2d45lFVjk5sMkmKxe6yebd+NGet6tv0/1UdU9PT/dAzfwXvyN9q25w/l3Vl6n66sDBFvLK9A/4pgFg//iKz0BgAfYvBBZAIwgsgEYQWACNILAAGkFgATSCwAJoBIEF0AgCC6ARBLbRtWZo7GaeNl8XqPDGb3tjmbLHFdvAvoXANrjJ5SKV3m/Rw5tTlMuVLW2WqPTB8H6d5r6Rt6vF4eFzvn3lchdptE9eL3WtndR/5qLnOM7RaHe7Z50emrw5S8Otim2r0k4nJv1/X7V5ur0wVdPfAoFtaOfoYbFEa1f4/BbKrhphXZ01/hWBTi60wwtbVCqVqOitzd+nc2II1k6js6u0LU5IH4rl4ygUzWMrvc5TbkgE9zI9KW3R7WG+fTV6rL+hdz9hxN/iQ/x9IrANTXwgS/Qky+c7gb1M7gcuiUCdXKTt0jY9HPPWYi1mszyxfVTSOkJzz0WAtimfG6HDvPbsGKFcftsIbpHWZuZprdbAZuZo0/idl04rlikdo5tG66Zw74xiWWUIbEOLElgx7QltLR/e7KpRey3SMJ9vytDcRsmq4VSMGmorf5n6ecCqYv8ehTxlu/kyv74rq1Q0911jYIcXaKu0Slk+P4T7t8+co8kqT2BVBfbU3U3KZ3uk+Spd2Txt3o12FskWPtOXL19MnwpXpOWmbIE+2euUfaa39ofRW4a8fIV2nHmfCv4/7vJOeb7zc4DAY9u3ggPbf2NT2VyMe+Y3icC+WlAGdvjGuhGQIj3JDVFfJiMZvbhI60ZzsZi/SIcV20cyuUxF0dwMDEEnTd7fcn/nomgy72VgxbbbizSqWCdIVYHtn3pq/dErhLYrK85eRpNj6pi0THaF3n7yBIMH6mBQGIUYgTXsLHvKb9LAqm6U3LyXpyfz44p1IxKBLW7RWj5Pea/VLetzcyUjb+N1Pm+EKE8X+PxIOin31Aj8yjnFsrL+K/etY7o3b//e47XV6rUGtsptqwqs0D9jhzbgj281NcT1QZSwtpQDs7tjh6ocQt9yc50V37bZwo4cWLaOxR/YL1926BEvn50owsvTRVhgy9q6yzWddM1XDRFY1c2Xl6t083v58yLt98gIzeQXYwb2IuU/FKq4lkwID11rp9R6MHnuTtc1sEJQaKsOq+HRbrn28v5sLffUvhWCEx4wJ7CfaWeXrdfEge0am6cnr/m1ZIHWFsapL05wQ5rEXonvVzA//Js0l1EsSxMP3Q95+fpc2JijfnudugdWcELrhJNPR1MOkllTSuEp14xOM1Zq+tqBkuYryxH7KZ8EzDKlfbL9NGhgrcuW8gdq+/m69RjEni4+n6v++WSEwKayXyFmYPt+XKeSsc8+xbJIYoRuTwIruCHNxwlriyIsLMCpBJbtVzoGtp9GDOzAHG16QlIqPaVsq/1B8oRp6+cRRZkhKgU2rf2a4jWJzRdL8hel+ZHFCN2eBVaIV7NanCawitUsDm4S80DxaT9+IvA0xT/Z2zVRYM0PqScgJftDw4NT+rBqBkouN0CFwKa2X1O0m04+recoL14smeqUl0UVI3R7GlihrZ09KI+E3whi7AB5a07vXVoeKD6t3pf3hhbbf9MEdoRuv7KCUSw4N4aWadJYNvlL+UaR9cijSA8neZkhQgOb4n4dFR/r+A3/vEWl98YxVH1y8IgRuj0PbCzu3V/PHVvBfd7qhIs99uF4YBmrKa0KrPcYvjRRYEXTUYTCao7K21jGlgtmuHjtHCr0xYkU9+tyXgBZjfjiROVHlBUdmaK1D0YLM5eRl6n0Gf8n741m/60hOnD6PhV0CWxQUzeoGawMpCdkyuWVAnvQ0yxvmsAOuTVdxaZpqcprwqBXE9Per1frMZp5GvJqYt93NOO+mlj9ZZzK8C3r/enIXi6YN9bMS4SN6m547VlgoR7UL/+P3hUfWO+HKCA4RnNxTCoznPLl/zdPaW4g3f36tdOJXJ62jN9d9TZX8ZXz8j/fLj7vM+VwPdQmjm/WuvdTbdMfgW1w5lncqG3WnTd7vjdqlSNG81R8a8QNyTrNHDGC86t3Xvzmovz1uinKnuxJfb+yduoa9R4L/3pdwo5fpiX+lpdklTbfiBNJIVYNj8A2OukL7Os0J760/s2c+e6uG5Si/w7u1q04j1Yi2Kv91knf9/P05KW3dcG8XKf8vdnY34lFYJtZ+xDlftmkbSdARvNR9EIxM5pUDRdgr/bbABBYAI0gsAAaQWABNILAAmgEgQXQCAILoBEEFkAjCCyARhBYAI2kH1gM1QGQmHQDi6E6ABKVbmC1GaojRu8SAHsgpcDqNlQHAgt6SCGwjTJUB8D+k3xgG3moDoA9lnxg0xyqw+lWZdnqD8nqM8n+/qmvHyX5O6lRh/jg0873V01hPUS4Xb6UO4IzeZrZvBM5vi+pTAAm1cAmPlSH3XFZOTiecPB5vmBEG+KDB1aUW17H6iUiMFjOsfn6abI7jXP2rfqCO/p2giokH9g0h+pQfbjNEKjmybVsmTqgfJrXhqH9MEknAZvvWKxyveuYZUq1LoBa8oFNc6iOwMCycKrmVTXEB5+2VA6soqZk8/0BlQMMECaFwHolO1QH//CbVOFk86of4oNPe8qpMbDWtH1s4ueg8gAU6hhYobahOqQPv1AxsKrw8XmVpi1xAqvaxhmew+r9P+CaGEAh5cAmO1SHMhQVAyvfnQ0a4iN42rOdGz52E8q96eQ5FnseL8c8vt0COePr+JYBhEg5sEKCQ3XEDCy/fg0e4iNo2lI5sJ/ZIye5DN/x4GYTVKkOgW0SqpNJIHQkDvEgsEmpJrBSCwAgGgQ2KZEDq25uA0SBwCYlQmDd1yNx7QoxIbAAGkFgATSCwAJoBIEF0AgCC6ARBBZAIwgsgEYQWACNILAAGkFgATSCwAJoBIEF0AgCC6ARBBZAIwgsgEYQWACNILAAGkFgATTyfwAlUgfkLsrsAAAAAElFTkSuQmCC>
