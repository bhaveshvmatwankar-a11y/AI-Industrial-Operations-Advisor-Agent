from document_loader import load_knowledge
from langchain_text_splitters import RecursiveCharacterTextSplitter

documents = load_knowledge()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Total Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks):
    print("=" * 60)
    print(f"Chunk {i+1}")
    print(chunk.page_content)