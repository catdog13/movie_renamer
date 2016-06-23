import os
import re

extensions_to_keep = ('.mp4', '.mkv', '.img', '.iso', '.wmv', '.avi', '.mov', '.m4v')
title_parser = re.compile(r'(?P<title>[\w,.\-!\s]+)(?P<year>(?:(?:20)|(?:19))\d{2})')


def file_walker(path_to_craw):
    for folders in os.listdir(path_to_craw):
        for root, subdir, files in os.walk(os.path.join(path_to_craw, folders)):
            for file in files:
                if not file.endswith(extensions_to_keep) or 'sample' in file:
                    os.remove(os.path.join(root, file))
                else:
                    title_year = rephraser(folders)
                    movie_name = title_year[0].rstrip() + file[-4:]
                    movie_path = os.path.join(root, movie_name)
                    os.rename(os.path.join(root, file), movie_path)
            folder_name = title_year[0].rstrip() + ' ' + title_year[1]
            os.rename(root, os.path.join(path_to_craw, folder_name))


def rephraser(phrase):
    name_clean = re.sub('[^\w ]', '', phrase.replace('.', ' '))
    title_data = title_parser.match(name_clean)
    title = title_data.group(1).rstrip()
    year = '(' + title_data.group(2) + ')'
    return title, year


if __name__ == '__main__':
    file_walker(r'D:\complete\Movies')
