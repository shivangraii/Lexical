import os
import json
import fitz  # PyMuPDF

INPUT_DIR = "Challenge_1a/sample_dataset/pdfs"
OUTPUT_DIR = "Challenge_1a/sample_dataset/outputs"

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = []

    title = ""

    # Step 1: Collect all font sizes for hierarchy
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    if span["text"].strip():
                        font_sizes.append(size)

    # Step 2: Rank font sizes by frequency
    top_sizes = sorted(set(font_sizes), reverse=True)
    size_to_level = {}
    if len(top_sizes) > 0:
        size_to_level[top_sizes[0]] = "H1"
    if len(top_sizes) > 1:
        size_to_level[top_sizes[1]] = "H2"
    if len(top_sizes) > 2:
        size_to_level[top_sizes[2]] = "H3"

    # Step 3: Extract content + heading
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = round(span["size"], 1)

                    if not text:
                        continue

                    if page_num == 0 and size == top_sizes[0] and not title:
                        title = text

                    if size in size_to_level:
                        headings.append({
                            "level": size_to_level[size],
                            "text": text,
                            "page": page_num
                        })

    return title or "Untitled", headings

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            title, outline = extract_outline_from_pdf(pdf_path)

            output = {
                "title": title,
                "outline": outline
            }

            out_name = filename.replace(".pdf", ".json")
            with open(os.path.join(OUTPUT_DIR, out_name), "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
