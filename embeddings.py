import os
import pandas as pd
import tensorflow_hub as hub

# Laden des Universal Sentence Encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Funktion zur Berechnung der Einbettung
def get_embedding(text):
    embedding = embed([text])[0].numpy()
    return " ".join([str(num) for num in embedding])  # Einbettung als Zeichenfolge von Zahlen

# Funktion zum Erstellen von Einbettungen und CSV-Dateien für die Dateien im Ordner
def create_embeddings():
    directory = "chatbot_docs"
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    embeddings = []
    contents = []

    for idx, filename in enumerate(files):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            content_sections = content.split("\n\n")  # Annahme: Jede Abschnittsüberschrift ist durch zwei neue Zeilen getrennt
            for section in content_sections:
                embedding = get_embedding(section)
                embeddings.append(embedding)
                contents.append(section)

    df = pd.DataFrame({
        'content': contents,
        'embedding': embeddings
    })

    # CSV-Datei mit korrektem Format für Einbettungen speichern
    df.to_csv("embs0.csv", index=False, float_format='%.10f')  # Format für Fließkommazahlen festlegen

# Aufrufen der Funktion zum Erstellen von Einbettungen und CSV-Dateien
create_embeddings()

