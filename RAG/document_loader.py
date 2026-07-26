from pathlib import Path
from langchain_community.document_loaders import TextLoader


# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the knowledge document
KNOWLEDGE_FILE = BASE_DIR / "RAG" / "knowledge" / "Machine_maintanence"


def load_knowledge():
    loader = TextLoader(
        str(KNOWLEDGE_FILE),
        encoding="utf-8"
    )

    documents = loader.load()

    return documents


if __name__ == "__main__":
    documents = load_knowledge()

    print("Knowledge document loaded successfully!")
    print(f"Number of documents: {len(documents)}")
    print(documents[0].page_content[:500])