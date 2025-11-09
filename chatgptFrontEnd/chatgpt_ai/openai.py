from dotenv import load_dotenv
import openai

load_dotenv()
gpt_client = openai.OpenAI()

def chatgpt_evaluate(question, answer):

    finished_prompt = f"""
    User Prompt: {question}
    Claude's Answer: {answer}
    
    Respond ONLY with a JSON object (no markdown, no preamble):
    {{
    "score": <0-100>,
    "reasoning_quality": "<assessment of Claude's reasoning>",
    "concerns": "<any red flags or issues>",
    "summary": "<overall evaluation>"
    }}"""

    response = gpt_client.chat.completions.create(
        model = "gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are an objective AI response evaluator. Your job is to assess the quality, reasoning, and accuracy of answers provided by Claude AI."},
            {"role": "system",
             "content": "Be critical and thorough. Respond with an assessment following the provided JSON format."},
            {"role": "user", "content": finished_prompt}
        ]
    )
    return response.choices[0].message.content
