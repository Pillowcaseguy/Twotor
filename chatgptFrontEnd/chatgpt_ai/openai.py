from dotenv import load_dotenv
import os
from utils import *
import openai

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI()

def chatgpt_response(prompt, client):
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages =[
            {"role": "system", "content": "You are a helpful financial planner who assists in giving knowledge about the economy and stock tickers."},
            {"role": "system", "content": "Answer the question in the sense that you have to have a long or short bias in the SP500 or NASDAQ indices in the near term."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

  
    # # Access the 'choices' from the response directly
    # if response['choices'] and len(response['choices']) > 0:
    #     prompt_response = response['choices'][0]['text'].strip() 
    # else:
    #     prompt_response = "No response generated."
    # return prompt_response

