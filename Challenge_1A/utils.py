
import fitz  # PyMuPDF
from collections import defaultdict


def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = []
    title = ""

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if len(text) < 3:
                        continue

                    size = round(span["size"], 1)
                    font_sizes.append(size)

    # Define top 3 font sizes
    top_sizes = sorted(list(set(font_sizes)), reverse=True)[:3]
    size_to_level = {top_sizes[0]: "H1", top_sizes[1]: "H2", top_sizes[2]: "H3"} if len(top_sizes) >= 3 else {}

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if len(text) < 3:
                        continue

                    size = round(span["size"], 1)
                    if page_num == 1 and size == top_sizes[0] and title == "":
                        title = text

                    level = size_to_level.get(size)
                    if level:
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })

    return {
        "title": title,
        "outline": headings
    }

