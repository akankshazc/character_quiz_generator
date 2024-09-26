import os


def split_book_files_into_chapters(input_dir, output_dir, separator):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all book files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            book_path = os.path.join(input_dir, filename)

            with open(book_path, 'r', encoding='utf-8') as book_file:
                book_text = book_file.read()

            # Split chapter into scenes using separator
            chapter = book_text.split(separator)

            # Extract book number from the filename (assuming format like '1_BookInitials.txt')
            book_number = filename.split('_')[0]
            book_initials = filename.split('_')[1].replace('.txt', '')

            # Write each scene to a separate file
            for idx, chapter in enumerate(chapter, 1):
                chapter_file_name = f'{book_number}_{book_initials}_{idx}.txt'
                chapter_file_path = os.path.join(output_dir, chapter_file_name)

                with open(chapter_file_path, 'w', encoding='utf-8') as chapter_file:
                    chapter_file.write(chapter.strip())

    print(
        f'All book files in {input_dir} have been split into chapters and saved in {output_dir}.')


# Example Use:
# split_book_files_into_chapters('IR_Books', 'IR_Chapters', 'CHAPTER ')
