import os
import re
import shutil

extensions_to_keep = ('.mp4', '.mkv', '.img', '.iso', '.wmv', '.avi', '.mov', '.m4v')
title_parser = re.compile(r'(?P<title>[\w,.\-!\s]+)(?P<year>(?:(?:20)|(?:19))\d{2})')


def file_walker(path_to_craw):
    for entry in os.scandir(path_to_craw):
        if entry.is_dir:
            for dir_path, dir_names, file_names in os.walk(entry.path):
                for file in file_names:
                    if os.path.splitext(file)[-1] in extensions_to_keep and 'sample' not in file:
                        organizer(file, dir_path, path_to_craw, entry.path, os.path.split(entry.path)[-1])


def organizer(file_name, file_path, base_path, remove_path, rename_this):
    title_year = rephraser(rename_this)
    movie_name = title_year[0]
    movie_file_name = movie_name + os.path.splitext(file_name)[-1]
    movie_year = title_year[1]
    folder_name = '{} {}'.format(movie_name, movie_year)
    move_to_dir = os.path.join(base_path, folder_name)
    if not os.path.isdir(move_to_dir):
        os.mkdir(move_to_dir)
        shutil.move(os.path.join(file_path, file_name), os.path.join(move_to_dir, movie_file_name))
        shutil.rmtree(remove_path)


def rephraser(phrase):
    name_clean = re.sub('[^\w ]', '', phrase.replace('.', ' '))
    title_data = title_parser.match(name_clean)
    title = title_data.group(1).rstrip()
    year = '(' + title_data.group(2) + ')'
    return title, year


if __name__ == '__main__':
    file_walker(r'D:\complete\Movies')
