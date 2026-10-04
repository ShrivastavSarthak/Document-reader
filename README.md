# Document Reader — Context-Aware RAG with Embeddings

A document reader system that uses **embeddings, vector similarity search, and an LLM** to answer questions based on the most relevant parts of a document.

Instead of sending the **entire document context** to the LLM for every query, the system converts document content into embeddings and retrieves only the chunks that have the highest similarity score with the user's question. This helps **reduce the context size, lower token usage, and provide more focused answers**.

## How It Works

1. **Document Processing**

   * Reads and splits documents into smaller text chunks.
   * Converts each chunk into a vector embedding.

2. **Query Embedding**

   * Converts the user's question into an embedding using the same embedding model.

3. **Similarity Search**

   * Compares the query embedding with document chunk embeddings.
   * Calculates a similarity score for each chunk.

4. **Relevant Context Selection**

   * Retrieves only the chunks whose similarity score is above the configured threshold or ranks highest.
   * Irrelevant parts of the document are excluded from the LLM context.

5. **LLM Response**

   * Sends the user's question along with the selected relevant context to the LLM.
   * The LLM generates an answer based on the retrieved information.

## Why This Approach?

Passing an entire document to an LLM can result in:

* Large context windows
* Higher token consumption
* Increased latency
* More expensive API calls
* Irrelevant information being included in the prompt

This project addresses these issues by using **semantic retrieval** to provide the LLM with only the information relevant to the user's question.

### Architecture

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Store
   ↓
User Question
   ↓
Query Embedding
   ↓
Similarity Search
   ↓
Relevant Chunks
   ↓
LLM + Context
   ↓
Answer
```

## Key Concepts

* **Text Embeddings**
* **Semantic Search**
* **Vector Similarity**
* **Retrieval-Augmented Generation (RAG)**
* **Context Optimization**
* **LLM-based Question Answering**
* **Token/Context Reduction**

The goal of this project is to demonstrate how **retrieval-based context selection** can make document-based LLM applications more efficient without requiring the complete document to be passed to the model.
