import os
from bean import VideoClipTimeStamped, ConcatenatedResult
from datetime import timedelta


def generate_clip_list(working_folder):
    print('Getting clip list...')
    clip_list = []
    for root, dirs, files in os.walk(working_folder):
        for file in files:
            if 'MP4' in file:
                clip_list.append(VideoClipTimeStamped(os.path.join(root, file)))
    return sorted(clip_list, key=lambda x: x.absolute_start_time)


def generate_concatenaded_file(working_folder, result):
    print('Generating concatenated result...')
    clip_list = generate_clip_list(working_folder)
    print('Found {} clips :\n{}'.format(len(clip_list), '\n'.join([str(x) for x in clip_list])))
    indexes_to_skip = []
    for index in range(1, len(clip_list)):
        if clip_list[index].absolute_start_time - clip_list[index - 1].absolute_end_time > timedelta(seconds=5):
            print(
                'Big gap in input videos.\n[{}]\nis far too distant of:\n[{}]\nSkipping'.format(
                    clip_list[index - 1], clip_list[index]))
            indexes_to_skip.append(index-1)
    for index in range(0, len(clip_list)):
        if index not in indexes_to_skip:
            result.add_clip(clip_list[index])



def process(working_folder):

    print('Working in folder {}'.format(working_folder))
    result = ConcatenatedResult(working_folder)
    generate_concatenaded_file(working_folder, result)
    print('Got {} result'.format(result))
    return result
