from sentence_transformers import SentenceTransformer
import numpy as np
import json

MODEL_NAME = 'intfloat/multilingual-e5-base'

if __name__ == "__main__":
    data = []
    with open("chunks.json", "r",encoding= "utf-8" ) as file:
        docs = json.load(file)
        for doc in docs:
            data.append("passage: " + doc["title"] + ". " + doc["section"] + ". " + doc["text"])

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(data, normalize_embeddings= True, show_progress_bar= True)
    #print(embeddings.shape)

    np.save("embeddings.npy", embeddings)
            
