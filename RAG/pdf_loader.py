from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path):
    """
    Load text from an industrial PDF document.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    loader = PyPDFLoader(
        str(pdf_path)
    )

    documents = loader.load()

    return documents


if __name__ == "__main__":

    print("PDF loader is ready.")

    print(
        "Use load_pdf('path/to/file.pdf') "
        "to load a PDF document."
    )