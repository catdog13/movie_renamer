import os
import re

extensions_to_delete = ('.nfo', '.txt', '.jpg', '.srt', '.url', '.srr', '.png', '.nzb', '.docx')
title_parser = re.compile(r'(?P<title>[\w,.\-!\s]+)(?P<year>(?:(?:20)|(?:19))\d{2})')


def file_walker(path_to_craw):
    for folders in os.listdir(path_to_craw):
        for root, subdir, files in os.walk(os.path.join(path_to_craw, folders)):
            for file in files:
                if file.endswith(extensions_to_delete) or 'sample' in file:
                    os.remove(os.path.join(root, file))
                else:
                    title_year = rephraser(folders)
                    movie_name = title_year[0].rstrip() + file[-4:]
                    movie_path = os.path.join(root, movie_name)
                    os.rename(os.path.join(root, file), movie_path)
            folder_name = title_year[0].rstrip() + ' ' + title_year[1]
            os.rename(root, os.path.join(path_to_craw, folder_name))


def rephraser(phrase):
    old_name = phrase
    new_name_space = old_name.replace('.', ' ')
    new_name_clean = re.sub('[^\w ]', '', new_name_space)
    title_data = title_parser.match(new_name_clean)
    title = title_data.group(1)
    year = '(' + title_data.group(2) + ')'
    return title, year


if __name__ == '__main__':
    file_walker(r'D:\complete\Movies')
