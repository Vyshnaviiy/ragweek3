
import chromadb

from pypdf import PdfReader

from services.embedding_service import (
    generate_embedding
)

# Create ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="voltstream_docs"
)


def load_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    return text


def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


def index_pdf():

    pdf_text = load_pdf(
    "data/energy 3.pdf"
)

    chunks = split_text(pdf_text)

    for i, chunk in enumerate(chunks):

        embedding = generate_embedding(
            chunk
        )

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)]
        )

    print("PDF Indexed Successfully")


def retrieve_chunks(query, top_k=3):

    query_embedding = generate_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]

