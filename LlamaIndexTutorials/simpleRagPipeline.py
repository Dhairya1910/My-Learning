from llama_index.core import VectorStoreIndex, Document
from llama_index.embeddings.mistralai import MistralAIEmbedding



docs = Document(
    text="custom content",
    metadata={"source": "manual", "category": "docs"},
    doc_id="U1",
)
index = VectorStoreIndex.from_documents([docs])
print(index)