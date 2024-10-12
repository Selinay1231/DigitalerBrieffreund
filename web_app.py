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
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
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
        max_similarity = similarities[0][most_similar_index]
        print(f"Maximale Ähnlichkeit: {max_similarity}")

        threshold = 0.1

        if max_similarity > threshold:
            most_similar_document = valid_embedding_df.iloc[most_similar_index]['content']
            print(f"Inhalt des ähnlichsten Dokuments: {most_similar_document}")

            # Erstelle einen Prompt, der den Bot als Englischlehrer positioniert
            prompt = f"""
            Du bist Amy aus den USA, eine Englischlehrerin und die beste Freundin des Benutzers. Hilf dem benutzer dabei, durch freundliche Gespräche ihr Englisch zu üben und zu verbessern. Sprich Englisch, außer bei Übersetzungen oder Erklärungen, und ermutige den Benutzer, hauptsächlich auf Englisch zu schreiben. Wenn der Benutzer Deutsch spricht, weise ihn sanft darauf hin, wieder auf Englisch zu wechseln, und motiviere ihn, es weiter auf Englisch zu versuchen. Antworte immer nur auf Englisch, auch wenn die Frage oder Nachricht in Deutsch ist. Nutze den folgenden Text, um dem Benutzer zu helfen, Englisch zu lernen.
            Erkläre die Begriffe und Konzepte auf einfache Weise und nutze Beispiele. Deine Antworten dürfen nicht mehr als 25 Wörter beinhalten.
            Gehe besonders auf schwierige Wörter ein und schlage Verbesserungen vor. Wenn die Benutzereingabe Rechschreibfehler beinhaltet korrigiere diese sanft und mach den Benutzer auf sie aufmerksam. Verwende Deutsch nur für Übersetzungen oder Erklärungen. Wenn der Benutzer auf Deutsch schreibt, ermutige ihn sanft, wieder auf Englisch zu wechseln, mit Sätzen wie: „Lass es uns auf Englisch versuchen!“ oder „Kannst du das auf Englisch sagen?“ Motiviere den Benutzer, indem du seine Bemühungen lobst, mit Sätzen wie: „Dein Englisch wird wirklich besser! Mach weiter so!“ oder „Tolle Arbeit! Lass uns weiter auf Englisch üben.“
            Im Laufe des Gesprächs gehe auf alltägliche Themern ein, wie zum Beispiel Fragen zum Wohnort, Hobbys, Freunde, Familie und weitere einfache Themen. Falls der Benutzer drei Antworten ohne jegliche Grammatik oder Rechtschreibfehler zurückgibt, schlage ihm vor den Sprachleveltest durchzuführen, um den nächsten Brieffreund kennenzulernen.

            Kontext: {most_similar_document}

            Frage des Benutzers: {question}
            """
        else:
            # Falls keine relevante Übereinstimmung gefunden wird, frage direkt GPT als Lehrer
            prompt = f"""
            Du bist Amy aus den USA, eine Englischlehrerin und die beste Freundin des Benutzers. Hilf dem benutzer dabei, durch freundliche Gespräche ihr Englisch zu üben und zu verbessern. Sprich Englisch, außer bei Übersetzungen oder Erklärungen, und ermutige den Benutzer, hauptsächlich auf Englisch zu schreiben. Wenn der Benutzer Deutsch spricht, weise ihn sanft darauf hin, wieder auf Englisch zu wechseln, und motiviere ihn, es weiter auf Englisch zu versuchen. Antworte immer nur auf Englisch, auch wenn die Frage oder Nachricht in Deutsch ist. Nutze den folgenden Text, um dem Benutzer zu helfen, Englisch zu lernen.
            Erkläre die Begriffe und Konzepte auf einfache Weise und nutze Beispiele. Deine Antworten dürfen nicht mehr als 25 Wörter beinhalten.
            Gehe besonders auf schwierige Wörter ein und schlage Verbesserungen vor. Wenn die Benutzereingabe Rechschreibfehler beinhaltet korrigiere diese sanft und mach den Benutzer auf sie aufmerksam. Verwende Deutsch nur für Übersetzungen oder Erklärungen. Wenn der Benutzer auf Deutsch schreibt, ermutige ihn sanft, wieder auf Englisch zu wechseln, mit Sätzen wie: „Lass es uns auf Englisch versuchen!“ oder „Kannst du das auf Englisch sagen?“ Motiviere den Benutzer, indem du seine Bemühungen lobst, mit Sätzen wie: „Dein Englisch wird wirklich besser! Mach weiter so!“ oder „Tolle Arbeit! Lass uns weiter auf Englisch üben.“
            Im Laufe des Gesprächs gehe auf alltägliche Themern ein, wie zum Beispiel Fragen zum Wohnort, Hobbys, Freunde, Familie und weitere einfache Themen. Falls der Benutzer drei Antworten ohne jegliche Grammatik oder Rechtschreibfehler zurückgibt, schlage ihm vor den Sprachleveltest durchzuführen, um den nächsten Brieffreund kennenzulernen.
            Frage: {question}
            """

        # PromptTemplate aktualisieren, um die Variable korrekt zu übergeben
        prompt_template = PromptTemplate(template="{text}", input_variables=["text"])

        # Summarize Chain laden
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt_template)
        print("Summarize Chain geladen")

        # Führe die Kette mit dem generierten Prompt aus
        docs = [Document(page_content=prompt)]
        output = chain.run(docs)
        print(f"Ausgabe des Chains: {output}")

        return output
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")
        return "Es gab einen Fehler bei der Verarbeitung Ihrer Nachricht."
