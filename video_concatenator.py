import os
from moviepy.editor import concatenate_videoclips
from bean import VideoClipTimeStamped
from datetime import timedelta

def generate_clip_list(working_folder):
    clip_list = []
    for root, dirs, files in os.walk(os.path.join(working_folder, 'input')):
        for file in files:
            clip_list.append(VideoClipTimeStamped(os.path.join(root, file)))
    return sorted(clip_list, key=lambda x: x.absolute_start_time)


date = '20180628'
working_folder = os.path.join('rsrc', date)

print('Working in folder {}'.format(working_folder))

clip_list = generate_clip_list(working_folder)
print('Found {} clips :\n{}'.format(len(clip_list),'\n'.join([str(x) for x in clip_list])))

for index in range(1, len(clip_list)):
    if clip_list[index].absolute_start_time - clip_list[index - 1].absolute_end_time > timedelta(seconds=30):
        clip_list

final_clip = concatenate_videoclips(clip_list)
final_clip.write_videofile(os.path.join(working_folder, 'output', 'my_concatenation.mp4'))
