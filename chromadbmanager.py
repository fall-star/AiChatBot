import chromadb
from chromadb.utils import embedding_functions

class ChromadbManager:
    def __init__(self):
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            device="cpu",
            model_name="BAAI/bge-small-zh-v1.5"
            )
        self.client = chromadb.PersistentClient("./chroma_db")
        self.collection = self.client.get_or_create_collection("my_docs", 
                                                               embedding_function=self.ef)
    
    #add message to chromadb
    def add_message_to_chromadb(self, session_id: str, role: str, message: str, turn: int, timestamp):
        """add message to chroma"""
        # timestamp = datetime.timestamp
        message_id = f"{session_id}_{timestamp}"
        self.collection.add(
            documents=[message],
            ids=[message_id],
            metadatas={
                "session_id": session_id,
                "role": role,
                "turn": turn
            }
        )
    
    #retrieve
    def retrieve_history(self, session_id: str, query_text: str, turn: int, top_k: int = 5):
        """return top-k similar message from collection"""
        pre_results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k,
            where={
                "$and": [
                    {"session_id": session_id}, 
                    {"turn": {"$lt":turn-5}}
                    ]
                }
        )
        documents = []
        for document in pre_results["documents"][0]:
            documents.append(document)
        roles = []
        for metadata in pre_results["metadatas"][0]:
            roles.append(metadata['role'])
        results = []
        for i in range(len(documents)):
            results.append({"role": roles(i), "message": documents[i]})
        return results