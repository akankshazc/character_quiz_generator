import json
import spacy
import re
from collections import defaultdict
from pathlib import Path
import argparse
import logging

# Load spacy model
nlp = spacy.load("en_core_web_sm")


# List of characters with their aliases
CHARACTERS = {
    "Murderbot": ['Murderbot', 'SecUnit', 'Eden', 'Rin'],
    "Mensah": ['Mensah', 'Dr. Mensah'],
    "ART": ['ART', 'Perihelion', 'Peri', 'Asshole Research Transport'],
    "Miki": ['Miki', 'Assistant Miki'],
    "Ratthi": ['Ratthi', 'Dr. Ratthi'],
    "Gurathin": ['Gurathin', 'Dr. Gurathin'],
    "Overse": ['Overse'],
    "Arada": ['Arada', 'Dr. Arada'],
    "Amena": ['Amena'],
    "Volescu": ['Volescu', 'Dr. Volescu'],
    "Pin-Lee": ['Pin-Lee'],
    "Bharadwaj": ['Bharadwaj', 'Dr. Bharadwaj'],
    "Thiago": ['Thiago', 'Dr. Thiago'],
    "Iris": ['Iris'],
    "Indah": ['Indah'],
}

all_aliases = set(alias for aliases in CHARACTERS.values()
                  for alias in aliases)

# Light cleaning


def clean_text(chapter_text: str) -> str:

    text = chapter_text.strip()

    # Replace the scene markers "***" with '[[Scene Break]]'
    text = text.replace('* * *', '...Scene Break...')

    # Replace newlines with spaces
    text = text.replace('\n', ' ')

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove non-printable characters
    text = ''.join(c for c in text if c.isprintable())

    return text


# Extract relevant traits from a sentence
def extract_traits_from_sentence(doc: str, aliases: list) -> list:
    traits = []

    for sent in doc.sents:
        if any(alias in sent.text for alias in aliases):
            for token in sent:
                if token.pos_ in ['ADJ', 'NOUN'] and token.dep_ not in ['acomp', 'amod', 'advmod', 'ROOT']:
                    traits.append(token.lemma_)

    return traits

# Main processing function


def extract_traits(book_dir: Path, output_dir: Path):
    if not book_dir.exists():
        logging.error(f"Input directory {book_dir} does not exist.")
        return

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # For each book subdirectory, extract traits and write to its own output JSON
    for subdir in book_dir.iterdir():
        if not subdir.is_dir():
            continue
        character_traits = defaultdict(list)
        for chapter_file in subdir.glob('*.txt'):
            text = clean_text(chapter_file.read_text(encoding='utf-8'))
            doc = nlp(text)
            for character, aliases in CHARACTERS.items():
                traits = extract_traits_from_sentence(doc, aliases)
                character_traits[character].extend(traits)

        # Remove duplicates and sort traits for each character
        result = {
            char: {
                # to make sure that traits are not just aliases and are meaningful
                "traits": sorted(set([t for t in traits if len(t) > 2 and t not in all_aliases])),
                "quotes:": []  # Placeholder for quotes, if needed later
            }
            for char, traits in character_traits.items()
        }

        # Output file: use subdir name with _traits.json in the output_dir
        output_file = output_dir / f"{subdir.name}_traits.json"
        output_file.write_text(json.dumps(result, indent=4), encoding='utf-8')
        print(f"Traits extracted and saved to {output_file}")


# CLI entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract character traits from text files.")
    parser.add_argument('book_dir', type=str, default='data/sample',
                        help="Directory containing book folders with chapter text files.")
    parser.add_argument('output_dir', type=str, default='data/sample_traits',
                        help="Output directory to save extracted traits JSON files.")

    args = parser.parse_args()
    input_dir = Path(args.book_dir)
    output_dir = Path(args.output_dir)

    extract_traits(input_dir, output_dir)
