import openai
import os
from qdrant_client import QdrantClient

collection_name = 'Fed_Speeches'
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_embeddings(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"  # Check the latest documentation for available engines
    )
    return response.data[0].embedding  # Extracting the embedding vector


def qdrant_client():
    client = QdrantClient(url=os.getenv("Qdrant_cluster_url"),
                          api_key=os.getenv("Qdrant_API_KEY"))
    return client


def search_for_context(client, collection_name, search_vector):
    search_response = client.search(collection_name=collection_name,
                                    query_vector=search_vector,
                                    limit=20)  # change for more context
    contexts = [hit.payload['text'] for hit in search_response]
    return contexts


def form_prompt(contexts, question):
    prompt = f"Context: {contexts} \nQuestion: {question} \nAnswer:"
    return prompt


def response_chat(prompt, model="gpt-3.5-turbo-instruct"):
    response = openai.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=256,
    )
    return response.choices[0].text.strip()

