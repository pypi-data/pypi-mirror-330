import numpy as np
import ollama
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity

class TinyRAG_Ollama:
    def __init__(self, embedding_model="nomic-embed-text", llm_model=None):
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.documents = []
        self.embeddings = []
        
    def add_documents(self, documents):
        if not documents:
            return
            
        self.documents.extend(documents)
        
        for doc in documents:
            try:
                response = ollama.embeddings(model=self.embedding_model, prompt=doc)
                self.embeddings.append(response['embedding'])
            except Exception as e:
                print(f"Error embedding document: {str(e)}")
                self.embeddings.append(None)
    
    def retrieve(self, query, top_k=3):
        if not self.documents:
            return []
            
        try:
            query_embedding_resp = ollama.embeddings(model=self.embedding_model, prompt=query)
            query_embedding = query_embedding_resp['embedding']
        except Exception as e:
            print(f"Error embedding query: {str(e)}")
            return []
            
        valid_docs = []
        valid_embeddings = []
        for i, emb in enumerate(self.embeddings):
            if emb is not None:
                valid_docs.append(self.documents[i])
                valid_embeddings.append(emb)
        
        if not valid_embeddings:
            return []
            
        query_embedding_np = np.array(query_embedding).reshape(1, -1)
        docs_embeddings_np = np.array(valid_embeddings)
        
        try:
            similarities = cosine_similarity(query_embedding_np, docs_embeddings_np)[0]
            top_k = min(top_k, len(valid_docs))
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            return [(valid_docs[i], similarities[i]) for i in top_indices]
        except Exception as e:
            print(f"Error calculating similarities: {str(e)}")
            return []
    
    def query(self, query, top_k=3, temperature=0.7):
        try:
            relevant_docs = self.retrieve(query, top_k)
            
            if not relevant_docs:
                return "No relevant information found."
            
            context = "\n\n".join([f"Doc (score: {score:.2f}):\n{doc}" for doc, score in relevant_docs])
            
            prompt = f"""Answer based on this info only:
            
            {context}

            Question: {query}

            Answer:"""
            
            response = ollama.chat(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response['message']['content']
        except Exception as e:
            print(f"Error during query: {str(e)}")
            return "An error occurred while processing your query."
