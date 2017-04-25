#!/usr/bin/env python3
import os
import re
import shutil


extensions_to_keep = ('.mp4', '.mkv', '.img', '.iso', '.wmv', '.avi', '.mov', '.m4v')
test_name = 'Terra Nova S01E01-E02 1080p WEB-DL DD+ 5.1 x264-TrollHD'


def file_walker(path_to_craw):
    for entry in os.scandir(path_to_craw):
        if entry.is_dir:
            for dir_path, dir_names, file_names in os.walk(entry.path):
                for file in file_names:
                    if os.path.splitext(file)[-1] in extensions_to_keep and 'sample' not in file:
                        organizer(file, entry.path, path_to_craw)
            shutil.rmtree(entry.path)  # commit for no delete


def organizer(file_name, folder_path, base_folder):
    move_to_path_base = base_folder.replace('!.unsorted','!.TV')
    title_se = rephraser(os.path.split(folder_path)[-1])
    show_name = title_se[0]
    show_s_e = title_se[1]
    show_res = title_se[2]
    show_source = title_se[3]
    new_file_name = '{} {} {} {}{}'.format(show_name, show_s_e, show_res, show_source, os.path.splitext(file_name)[-1])
    move_to_dir = os.path.join(move_to_path_base, show_name)
    if not os.path.isdir(move_to_dir):
        os.mkdir(move_to_dir)
    shutil.move(os.path.join(folder_path, file_name), os.path.join(move_to_dir, new_file_name))


def rephraser(phrase):
    name_clean = re.sub('[^\w\'\-\s]', '', phrase.replace('.', ' '))
    season_episode = re.search("[S][0-9][0-9][E][0-9][0-9]", name_clean)
    show_name = re.search("[\w\'\-!\s]+", name_clean[:season_episode.start(0)-1])
    video_res = re.search("\d{3,4}\w{1}", name_clean)
    video_source = re.search("(?:HDTV)|(?:WEBRip)|(?:WEB-DL)", name_clean)
    return show_name.group(0), season_episode.group(0), video_res.group(0), video_source.group(0)



if __name__ == '__main__':
    file_walker(r'/home/tom/Desktop/nzbget/dst/!.unsorted')
#    print(rephraser(test_name))

