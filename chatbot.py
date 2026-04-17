import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer


# the model i'm using for converting text to vectors
MODEL_NAME = "all-MiniLM-L6-v2"


def load_data(filename="banking_qa.json"):
    # ensure we find the file regardless of where the app is run from
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data



def get_embeddings(questions, model):
    # convert each question into a vector (normalized so cosine = dot product)
    return model.encode(questions, normalize_embeddings=True)


def find_best_match(query, model, data, embeddings, threshold=0.30):
    # embed the user's query and compare it against all stored questions
    query_vec = model.encode(query, normalize_embeddings=True)
    scores = [float(np.dot(query_vec, emb)) for emb in embeddings]

    best_idx = int(np.argmax(scores))
    best_score = scores[best_idx]

    # if similarity is too low, we don't have a good answer
    if best_score < threshold:
        return None

    return data[best_idx]


def ask_llm(query, context):
    backend = os.environ.get("LLM_BACKEND", "groq").lower()

    system_msg = (
        "You are a helpful banking assistant. Answer the user's question "
        "using only the context given. Keep your answer short and clear."
    )
    user_msg = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"

    if backend == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": user_msg},
            ],
            temperature=0.3,
            max_tokens=300,
        )
        return res.choices[0].message.content.strip()

    elif backend == "fallback":
        # no API key needed, just return the context directly
        return context.strip()

    else:
        # groq is the default (free tier available at console.groq.com)
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": user_msg},
            ],
            temperature=0.3,
            max_tokens=300,
        )
        return res.choices[0].message.content.strip()


class BankingChatbot:
    def __init__(self):
        print("Loading model...")
        self.model = SentenceTransformer(MODEL_NAME)

        print("Loading dataset...")
        self.data = load_data()

        print("Building embeddings...")
        questions = [entry["question"] for entry in self.data]
        self.embeddings = get_embeddings(questions, self.model)

        print("Ready!\n")

    def ask(self, query):
        query = query.strip()
        if not query:
            return "Please type a question."

        match = find_best_match(query, self.model, self.data, self.embeddings)

        if match is None:
            return (
                "Sorry, I don't have information on that. "
                "Please contact your bank directly for help."
            )

        try:
            answer = ask_llm(query, match["answer"])
        except Exception as e:
            # if LLM fails for any reason, fall back to the raw answer
            print(f"LLM error: {e}")
            answer = match["answer"]

        return answer
