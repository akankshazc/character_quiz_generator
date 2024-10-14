import os
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
import spacy


def preprocessing(input_dir, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all chapter files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            chapter_path = os.path.join(input_dir, filename)

            with open(chapter_path, 'r', encoding='utf-8') as chapter_file:
                chapter_text = chapter_file.read()

                # Remove Whitespace
                chapter_text = re.sub(r'\s+', ' ', chapter_text)

                # Remove Punctuation and Special Characters
                chapter_text = re.sub(r'[^A-Za-z0-9\s]', '', chapter_text)

                # Convert to lowercase
                clean_chapter_text = chapter_text.lower()

        # Tokenizing chapter text
        tokenized_chapter_text = word_tokenize(clean_chapter_text)

        # Remove Stopwords
        stop_words = set(stopwords.words('english'))
        filtered_chapter_text = [
            token for token in tokenized_chapter_text if token not in stop_words]

        # Lemmatization with spaCy
        nlp = spacy.load('en_core_web_sm')
        lemmatized_chapter_text = ' '.join(
            [str(nlp(token)) for token in filtered_chapter_text])

        # Save the lemmatized_chapter_text to file
        original_file_name = filename.replace('.txt', '')
        lemma_file_name = f'{original_file_name}_lemma.txt'
        lemma_file_path = os.path.join(output_dir, lemma_file_name)

        with open(lemma_file_path, 'w', encoding='utf-8') as lemma_file:
            lemma_file.write(lemmatized_chapter_text)

    print(
        f'All chapter files in {input_dir} have been cleaned and saved in {output_dir}')


# Example use:
# preprocessing('Text_Preprocessing/IR_Chapters',
#               'Text_Preprocessing/IR_Chapters_lemma')

# preprocessing('Text_Preprocessing/TMBD_Chapters',
#               'Text_Preprocessing/TMBD_Chapters_lemma')
