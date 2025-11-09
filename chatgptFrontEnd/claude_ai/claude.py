from dotenv import load_dotenv
import anthropic

load_dotenv()
claude_client = anthropic.Anthropic()

def claude_answer(question):

    prompt = f"""Answer this question from the user, and explain your reasoning.

    Question: {question}
    
    """

    response = claude_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are an AI tutor.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text
