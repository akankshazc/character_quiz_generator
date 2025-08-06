from pathlib import Path
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Function to split book files into chapters
def split_book_files_into_chapters(input_dir: str, output_dir: str, separator: str) -> None:
    """Split book files into chapters based on a separator.

    This function assumes the filename format is like '1_BookInitials.txt' where the first number is the book number and the second part
    is the book initials.

    Args:
        input_dir (str): Directory containing book files.
        output_dir (str): Directory to save the chapter files.
        separator (str): String used to split the book into chapters.

    Returns:
        None: The function saves the chapter files in the specified output directory.

    Example:
        split_book_files_into_chapters('MB_Books', 'MB_Chapters', 'Chapter ')"""

    # Ensure output directory exists
    if not input_dir.exists():
        logging.error(f"Input directory {input_dir} does not exist.")
        return

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Output directory {output_dir} created.")

    # Loop through all book files in the input directory
    for file_path in input_dir.glob("*.txt"):

        # Read the book file and split it into chapters
        book_text = file_path.read_text(encoding='utf-8')
        chapters = book_text.split(separator)

        # Extract book number and initials from the filename
        book_number = file_path.stem.split('_')[0]
        book_initials = file_path.stem.split('_')[1]

        # Write each chapter to a separate file (skip empty chapters and remove the Chapter number if present)
        chapter_idx = 1
        for chapter in chapters:
            chapter_content = chapter.strip()
            if not chapter_content:
                continue
            chapter_content = ' '.join(chapter_content.split()[1:]).strip()
            if not chapter_content:
                continue
            chapter_file_name = f"{book_number}_{book_initials}_{chapter_idx}.txt"
            chapter_file_path = output_dir / chapter_file_name
            chapter_file_path.write_text(chapter_content, encoding='utf-8')
            chapter_idx += 1

    logging.info(
        f"All book files in {input_dir} have been split into chapters and saved in {output_dir}.")


if __name__ == "__main__":

    # Input arguments for the script
    parser = argparse.ArgumentParser(
        description='Split book files into chapters.')
    parser.add_argument('input_directory', type=str,
                        help='Input directory containing book files.')
    parser.add_argument('output_directory', type=str,
                        help='Output directory for chapter files.')
    parser.add_argument('separator', type=str,
                        help='Separator for splitting chapters.')

    # Parse the input arguments
    args = parser.parse_args()
    input_directory = Path(args.input_directory)
    output_directory = Path(args.output_directory)
    separator = args.separator

    # Call the function with parsed arguments
    split_book_files_into_chapters(
        input_directory, output_directory, separator)
