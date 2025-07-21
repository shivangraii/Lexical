import os
import json
from utils import extract_headings_from_pdf

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_FOLDER, filename)
            result = extract_headings_from_pdf(pdf_path)

            output_path = os.path.join(OUTPUT_FOLDER, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
