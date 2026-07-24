# Semantic Search

This folder contains a LangChain-based semantic search demo that indexes and queries a PDF document (specifically, Nike's FY2023 10-K report, [nke-10k-2023.pdf](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/example_data/nke-10k-2023.pdf)) using Google's Generative AI Embeddings and a Chroma vector database.

## Structure and Files

* **[semantic_search.py](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/semantic_search.py)**: The main script containing the document loader, text splitter, vector database initialization, document indexing, and querying logic.
* **[example_data/](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/example_data)**: Contains the sample PDF document [nke-10k-2023.pdf](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/example_data/nke-10k-2023.pdf).
* **[chroma_langchain_db/](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/chroma_langchain_db)**: The local folder where the Chroma vector store persists its collection indexes and binaries.

## Implementation Details

The implementation in [semantic_search.py](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/semantic_search.py) consists of:

1. **Document Loading**:
   * Uses [load_pdf_pages](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/semantic_search.py#L34) to load the PDF page-by-page using `pypdf.PdfReader` and maps each page into a LangChain `Document` containing the extracted text and metadata (source path and page index).
2. **Text Splitting**:
   * Uses `RecursiveCharacterTextSplitter` with a chunk size of 1000 characters and a chunk overlap of 200 characters to break down the pages into overlapping splits.
3. **Embeddings & Vector Store**:
   * Initializes `GoogleGenerativeAIEmbeddings` using the model `models/gemini-embedding-001`.
   * Sets up a local persistent database directory [chroma_langchain_db/](file:///Users/sridharpatil/Documents/Agentic%20AI/start-new/semantic_search/chroma_langchain_db) with the collection name `semantic_search`.
4. **Similarity Search**:
   * Indexes the first 100 splits and runs a similarity search query using `similarity_search_with_score` to retrieve the most relevant text chunk along with a distance score.

## Getting Started

### Prerequisites

Ensure you have a `.env` file in the project root containing your Google API Key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### Usage

Run the semantic search demo:
```bash
python semantic_search/semantic_search.py
```

This will run the script, output the total pages loaded, the total splits created, index the splits into Chroma, and print the top search result for the query:
> *"How many distribution centers does Nike have in the US?"*
