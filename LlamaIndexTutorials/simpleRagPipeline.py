from llama_index.core import get_response_synthesizer
from llama_index.core.schema import QueryType
from llama_index.core import VectorStoreIndex, Settings  # vectorstore
from llama_index.core import SimpleDirectoryReader  # loader
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.llms.mistralai import MistralAI
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Step-1 : Loading the document...
documents = SimpleDirectoryReader(r"d:\My-Learning\Docs").load_data()

text_splitter = SentenceSplitter(chunk_size=256, chunk_overlap=10)

# step-2 : Configure your model you are using
Settings.embed_model = MistralAIEmbedding()
Settings.llm = MistralAI()
Settings.text_splitter = text_splitter

vector_index = VectorStoreIndex.from_documents(
    documents, transformations=[text_splitter]
)

retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=10)

response_synthesizer = get_response_synthesizer()

# step-3 :
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.6)],
)

response = query_engine.query("when did the cricketer made his debut.")
print(response)
