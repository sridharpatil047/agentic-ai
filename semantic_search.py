from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf
from dotenv import load_dotenv

load_dotenv()

# documents = [
#     Document(
#         page_content="Dogs are great companions, known for their loyalty and friendliness.",
#         metadata={"source": "mammal-pets-doc"},
#     ),
#     Document(
#         page_content="Cats are independent pets that often enjoy their own space.",
#         metadata={"source": "mammal-pets-doc"},
#     ),
# ]

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# for doc in documents:
#     embeddings.embed_query(doc.page_content)


vector_store = Chroma(
    collection_name="semantic_search",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)


def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    # print(reader.pages[1].extract_text())
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]


file_path = "./example_data/nke-10k-2023.pdf"
docs = load_pdf_pages(file_path)
print(len(docs))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))

ids = vector_store.add_documents(documents=all_splits[:100])

print(len(ids))

results = vector_store.similarity_search_with_score(
    "How many distribution centers does Nike have in the US?"
)

print(results[0])

