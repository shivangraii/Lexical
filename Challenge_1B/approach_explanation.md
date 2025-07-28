**Approach Explanation: Adobe India Hackathon Round 1B**

**Problem Overview:**
We are tasked with building a document intelligence system that processes 3–10 input PDFs and extracts the most relevant sections based on a defined persona and job-to-be-done. The final output is structured as a JSON file with metadata, extracted section highlights, and sub-section analysis.

**Core Objective:**
Extract and rank relevant content sections from diverse PDFs without internet access, using a generic, domain-independent, offline, CPU-only pipeline.

---

**Methodology:**

1. **Document Parsing:**

   * The system uses PyMuPDF to extract text blocks from each page of all input PDFs.
   * Texts are chunked by visual blocks, maintaining page number references.

2. **Persona & Job Loading:**

   * The persona role and job-to-be-done are extracted from a provided JSON config file.

3. **Relevance Ranking (TF-IDF):**

   * All extracted blocks are vectorized using TF-IDF.
   * Cosine similarity is computed between each text block and the job-to-be-done statement.
   * The top-3 ranked blocks are extracted for each document.

4. **Output Structuring:**

   * The system produces a structured JSON with:

     * Metadata: filenames, persona, job-to-be-done, timestamp
     * Extracted Sections: page number, filename, importance rank
     * Sub-section Analysis: refined block content for deeper review

---

**Libraries Used:**

* `PyMuPDF`: Fast and lightweight PDF parsing with layout-aware block text extraction.
* `scikit-learn`: For TF-IDF vectorization and cosine similarity scoring.
* `datetime`, `os`, `json`: Standard I/O and metadata handling

---

**Execution & Deployment:**

* The code runs offline on CPU with model size <1GB.
* Docker is used for packaging. Build the container using:

  ```bash
  docker build -t adobe_round1b .
  ```
* Run using:

  ```bash
  docker run --rm -v ${PWD}/Challenge_1b:/app/Challenge_1b adobe_round1b
  ```

---

**Highlights:**

* No internet required
* Generalizes across domains (academic, financial, educational)
* Runs under 60 seconds for 5 PDFs on CPU (tested)
* Easily extendable to include keyword-weighted scores, persona vectorization, or document type classification.
