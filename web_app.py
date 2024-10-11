import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tensorflow_hub as hub
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import openai

# OpenAI API-Key setzen
openai.api_key = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

def calculate_similarity_with_embeddings(user_message, embedding_df, embed):
    try:
        user_embedding = embed([user_message])[0].numpy()
        print(f"User Embedding: {user_embedding}")

        if np.isnan(user_embedding).any():
            raise ValueError("User embedding contains NaN values.")

        embedding_matrix = np.array(embedding_df['embedding'].tolist())
        print(f"Embedding Matrix Shape: {embedding_matrix.shape}")

        if embedding_matrix.ndim != 2:
            raise ValueError("Embedding matrix is not 2-dimensional")

        valid_indices = ~np.isnan(embedding_matrix).any(axis=1)
        embedding_matrix = embedding_matrix[valid_indices]
        valid_embedding_df = embedding_df[valid_indices]
        print(f"Filtered Embedding Matrix Shape: {embedding_matrix.shape}")

        user_embedding = user_embedding.reshape(1, -1)
        print(f"Reshaped User Embedding Shape: {user_embedding.shape}")

        similarities = cosine_similarity(user_embedding, embedding_matrix)
        print(f"Similarities: {similarities}")
        return similarities, valid_embedding_df
    except Exception as e:
        print(f"Fehler bei der Berechnung der Ähnlichkeit: {e}")
        raise

def process_embedding(embedding_str):
    print("Einbettungs-String:", embedding_str)
    if isinstance(embedding_str, str):
        return list(map(float, embedding_str.split()))
    else:
        return embedding_str

def logic(question):
    try:
        df = pd.read_csv("embs0.csv")
        print("embs0.csv geladen")
        print("Inhalt der DataFrame:")
        print(df.head())

        df['embedding'] = df['embedding'].apply(process_embedding)
        print("Einbettungen konvertiert")

        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        print("Universal Sentence Encoder geladen")

        similarities, valid_embedding_df = calculate_similarity_with_embeddings(question, df, embed)
        print("Ähnlichkeiten berechnet")

        most_similar_index = np.argmax(similarities)
        print(f"Index des ähnlichsten Dokuments: {most_similar_index}")
        most_similar_document = valid_embedding_df.iloc[most_similar_index]['content']
        print(f"Inhalt des ähnlichsten Dokuments: {most_similar_document}")

        docs = [Document(page_content=most_similar_document)]

        prompt_template = "Beantworte die folgende Frage:\n\n{text}\n\n"
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
        print("Summarize Chain geladen")

        output = chain.run(docs)
        print(f"Ausgabe des Chains: {output}")

        return output
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")
        return "Es gab einen Fehler bei der Verarbeitung Ihrer Nachricht."


df = pd.read_csv("embs0.csv")
print(df.head())







