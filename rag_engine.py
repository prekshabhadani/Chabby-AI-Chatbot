from io import BytesIO

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


def extract_pdf_text(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:
        reader = PdfReader(BytesIO(uploaded_file.getvalue()))

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            if page_text.strip():
                documents.append(
                    Document(
                        page_content=page_text,
                        metadata={
                            "source": uploaded_file.name,
                            "page": page_number,
                        },
                    )
                )

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def create_vector_store(chunks):
    if not chunks:
        return None

    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
    )


def get_relevant_context(vector_store, question, k=4):
    if vector_store is None:
        return "", []

    results = vector_store.similarity_search(question, k=k)

    context_parts = []
    sources = []

    for document in results:
        context_parts.append(document.page_content)
        sources.append(
            {
                "source": document.metadata.get("source", "Unknown"),
                "page": document.metadata.get("page", "Unknown"),
            }
        )

    return "\n\n---\n\n".join(context_parts), sources
