import os
import csv

# Extract metadata before Preprocessing


def extract_metadata(input_dirs):

    # Extract series name from input_dir
    series_initials = [input_dir.split('_')[0] for input_dir in input_dirs]

    metadata = []

    for series, input_dir in zip(series_initials, input_dirs):

        # Loop through all book files in the series
        for filename in os.listdir(input_dir):
            # Remove '.txt' from filename
            filename = filename.replace('.txt', '')

            # Extract Metadata from filename
            book_number, book_initials, chapter_number = filename.split('_')

            # Append each chapter with filename and metadata
            metadata.append({'File Name': filename+'.txt',
                            'Series Code': series,
                             'Book Number': book_number,
                             'Book Code': book_initials,
                             'Chapter Number': chapter_number
                             })

    # Convert to csv format and output
    keys = metadata[0].keys()

    with open('Text_Preprocessing/metadata.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(metadata)

    print(
        f'Metadata has been extract from filenames for all files of {input_dirs} into metadata.csv')


# Example Use:
# extract_metadata(['TMBD_Chapters', 'IR_Chapters'])


# Extract Metadata after Preprocessing

def extract_preprocessed_metadata(input_dirs):

    # Extract series name from input_dir
    series_initials = [input_dir.split(
        '/')[1].split('_')[0] for input_dir in input_dirs]

    metadata = []

    for series, input_dir in zip(series_initials, input_dirs):

        # Loop through all book files in the series
        for filename in os.listdir(input_dir):

            # Extract Metadata from filename (ignoring the lemma part of the file names)
            book_number, book_initials, chapter_number, _ = filename.split('_')

            # Original File Name
            original_file_name = '_'.join(filename.split('_')[:3])

            # Append each chapter with filename and metadata
            metadata.append({'File Name': original_file_name+'.txt',
                             'Lemmatized File Name': filename,
                            'Series Code': series,
                             'Book Number': book_number,
                             'Book Code': book_initials,
                             'Chapter Number': chapter_number
                             })

    # Convert to csv format and output
    keys = metadata[0].keys()

    with open('Text_Preprocessing/metadata_lemma.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(metadata)

    print(
        f'Metadata has been extract from lemmatized filenames for all files of {input_dirs} into metadata_lemma.csv')


# Example Use:
# extract_preprocessed_metadata(['Text_Preprocessing/TMBD_Chapters_lemma',
#                               'Text_Preprocessing/IR_Chapters_lemma'])
