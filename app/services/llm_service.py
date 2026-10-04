import json
from openai import OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= "USE_YOUR_OWN_KEY_BRO!"
)

SYSTEM_PROMPT = '''
You are a document question-answering assistant
Answer using only the provided document context or the context the user gave.
If the answer is not present, say you don't know. 
Do not invent information.
'''

def generate_answer(history:list[dict[str,str]], chunks:list[str]):
    context = "\n\n".join(chunks)
    response = client.chat.completions.create(
        model=  "openrouter/free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {"history":history, "document_context":context},
                    ensure_ascii= False
                ),
            }
        ],
        temperature=1.5
        
    )
    return response.choices[0].message.content