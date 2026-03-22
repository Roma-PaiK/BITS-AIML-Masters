# Assignment 2: Hybrid RAG System with Automated Evaluation

## 📝 Problem Statement
The objective of this project was to build a complete **Hybrid Retrieval-Augmented Generation (RAG) system** combining dense vector retrieval, sparse keyword retrieval (BM25), and Reciprocal Rank Fusion (RRF) to answer questions from a corpus of 500 Wikipedia articles. It also includes an automated evaluation framework utilizing 100 generated Q&A pairs to mathematically measure retrieval and generation performance using MRR and custom metrics.

**Course:** Conversational AI (AIMLCZG521) - BITS Pilani
**Team:** Group 46

## 🚀 Version 1.0 Implementation (Current)
Our V1 approach successfully implements the complete hybrid pipeline, balancing semantic understanding with exact-keyword matching.

* **Dynamic Corpus Engine:** Fetches, cleans, and chunks text from 200 fixed Wikipedia URLs and 300 randomly sampled URLs (200-400 token chunks, 50-token overlap).
* **Hybrid Retrieval System:** * *Dense Retrieval:* Embeddings generated using `sentence-transformers` and indexed via **FAISS** (Cosine Similarity).
  * *Sparse Retrieval:* Keyword matching implemented using **BM25**.
  * *Fusion Strategy:* Combined both retrieval streams using **Reciprocal Rank Fusion (RRF)** (with k=60) to select the final top-N context chunks.
* **Generation:** Utilized an open-source LLM to synthesize final answers based on the retrieved context.
* **Automated Evaluation Pipeline:** * Automatically generated 100 Q&A pairs spanning diverse categories.
  * Evaluated using **Mean Reciprocal Rank (MRR)** at the URL level.
  * Implemented additional custom metrics for answer and retrieval quality assessment.

## 📂 Repository Structure
* `CAI_Group_46_Assignment_2.ipynb`: Main implementation notebook containing the full RAG pipeline and evaluation logic.
* `CAI_Group_46_Assignment_2_report.pdf`: Comprehensive architecture and evaluation report with visualizations and ablation studies.
* `CAI_Group_46_Assignment_2.pdf`: Assignment presentation/documentation.
* `data/`
  * `fixed_urls.json`: The required 200 static Wikipedia URLs.
  * `random_urls_rebuilt.json`: 300 dynamically fetched URLs.
  * `documents.json` & `chunks.json`: Preprocessed and chunked corpus.
  * `qa_dataset.json`: 100 auto-generated QA pairs for evaluation.
  * `faiss_index.index`: Exported FAISS vector database.

## 🛠️ How to Run

### 1. Dependencies
This project requires Python and the following core libraries:
`sentence-transformers`, `faiss-cpu`, `rank-bm25`, `transformers`, `wikipedia-api`, `beautifulsoup4`, `nltk`, `rouge-score`, `bert-score`, `scikit-learn`.

### 2. Installation
1. Clone the repository to your local machine.
2. Create and activate a virtual environment.
3. Install the required dependencies:
   ```bash
   pip install sentence-transformers faiss-cpu rank-bm25 transformers wikipedia-api beautifulsoup4 nltk rouge-score bert-score scikit-learn
3. Execution
Launch Jupyter Notebook or an equivalent environment:

Bash
jupyter notebook
Open CAI_Group_46_Assignment_2.ipynb.

Ensure the data/ directory is in the same root folder to load the pre-built FAISS index and datasets without re-fetching all 500 Wikipedia pages.

Run the cells sequentially to initialize the Hybrid Retriever, instantiate the model, and execute the automated evaluation pipeline.

🌱 Planned Improvements (V2.0)
[ ] UI Integration: Migrate the interactive querying components into a standalone Streamlit or Gradio web application.

[ ] Advanced Chunking: Replace fixed-size token chunking with semantic chunking to preserve better sentence boundaries.

[ ] LLM Upgrade: Experiment with quantized models to improve generation quality and reduce hallucinations.