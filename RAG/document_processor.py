from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split LangChain documents into smaller chunks
    for embedding and vector storage.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(
        documents
    )

    return chunks