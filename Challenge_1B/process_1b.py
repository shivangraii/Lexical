import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Config paths
INPUT_DIR = "input/docs"
OUTPUT_FILE = "output/output.json"
CONFIG_FILE = "input/persona_job.json"

# Load persona & job
with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

persona = config["persona"]
job = config["job_to_be_done"]

# Extract text chunks with page numbers
def extract_text_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    chunks = []
    for i, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text.split()) > 10:  # Ignore too short
                chunks.append((i, text))
    return chunks

# Analyze all docs
def analyze_docs():
    extracted_sections = []
    sub_sections = []
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    
    all_docs = []
    for filename in files:
        filepath = os.path.join(INPUT_DIR, filename)
        chunks = extract_text_chunks(filepath)
        texts = [chunk[1] for chunk in chunks]

        # TF-IDF matching
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform(texts + [job])
        similarities = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()

        top_indices = similarities.argsort()[-3:][::-1]
        for rank, idx in enumerate(top_indices, 1):
            page_num, content = chunks[idx]
            extracted_sections.append({
                "document": filename,
                "page_number": page_num,
                "section_title": content[:40] + ("..." if len(content) > 40 else ""),
                "importance_rank": rank
            })
            sub_sections.append({
                "document": filename,
                "refined_text": content,
                "page_number": page_num
            })

    return files, extracted_sections, sub_sections

# Main
if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    docs, sections, subs = analyze_docs()
    result = {
        "metadata": {
            "input_documents": docs,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": sections,
        "sub_section_analysis": subs
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
