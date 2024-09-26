import os


def split_chapter_files_into_scenes(input_dir, output_dir, separator):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all chapter files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            chapter_path = os.path.join(input_dir, filename)

            with open(chapter_path, 'r', encoding='utf-8') as chapter_file:
                chapter_text = chapter_file.read()

            # Split chapter into scenes using separator
            scenes = chapter_text.split(separator)

            # Extract chapter number from the filename (assuming format like '1_BookInitials_1.txt')
            # The First number signifying book order and Second signifying chapter number
            book_number, book_initials = filename.split(
                '_')[0], filename.split('_')[1]
            chapter_number = filename.split('_')[2].replace('.txt', '')

            # Write each scene to a separate file
            for idx, scene in enumerate(scenes, 1):
                scene_file_name = f'{book_number}_{book_initials}_{chapter_number}_{idx}.txt'
                scene_file_path = os.path.join(output_dir, scene_file_name)

                with open(scene_file_path, 'w', encoding='utf-8') as scene_file:
                    scene_file.write(scene.strip())

    print(
        f'All chapter files in {input_dir} have been split into scenes and saved in {output_dir}.')


# Example Use:
# split_chapter_files_into_scenes('TMBD_Chapters', 'TMBD_Scenes', '* * *')
