import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate(query, results):
    context = ""

    for r in results:
        context += f"From {r['source']}:\n{r['text']}\n\n"
    
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role": "system", "content": "Answer only using the context below. \n\n"+ context},
        {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content