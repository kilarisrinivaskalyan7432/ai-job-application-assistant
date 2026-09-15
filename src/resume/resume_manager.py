from pathlib import Path
from .resume_parser import extract_resume_text


RESUME_FOLDER = Path("data/resumes")


def load_all_resumes():
    resumes = {}

    for pdf_file in RESUME_FOLDER.glob("*.pdf"):
        try:
            text = extract_resume_text(pdf_file)
            resumes[pdf_file.name] = text

        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")

    return resumes


if __name__ == "__main__":
    resumes = load_all_resumes()

    print(f"\nTotal resumes found: {len(resumes)}\n")

    for filename, text in resumes.items():
        print("=" * 60)
        print(f"RESUME: {filename}")
        print("=" * 60)
        print(text[:500])
        print()