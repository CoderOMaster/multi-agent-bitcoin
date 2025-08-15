from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
def client_groq(context:str):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "You are a helpful assistant for summarising while keeping important points in atmost 4-5 lines."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": f"{context}",
        }
    ],

    # The language model which will generate the completion.
    model="llama-3.3-70b-versatile"
)
    return chat_completion.choices[0].message.content

# print(client_groq("Explain the importance of fast language models"))
# Print the completion returned by the LLM.
