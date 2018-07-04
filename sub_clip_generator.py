from moviepy.editor import concatenate_videoclips
from datetime import timedelta, datetime
import subprocess
import os


def get_sub_clip(res, time, duration_sec):
    absolute_time = datetime.combine(res.absolute_start_time.date(), time)
    for clip in res.clip_list:
        if absolute_time - timedelta(
                seconds=duration_sec) > clip.absolute_start_time and absolute_time < clip.absolute_end_time:
            end_time = (absolute_time - clip.absolute_start_time).seconds
            cur_sub_clip = clip.video_clip.subclip(end_time - duration_sec, end_time)
            show_clip(clip.video_clip.subclip(end_time - duration_sec/4, end_time))
            input_str = input('clip ok ? (Y/n)')
            if input_str.upper() == 'Y':
                print('Adding sub clip')
                return cur_sub_clip
            else:
                print('Skipping sub clip')
                return None
    print('cross clip not supported yet')
    return None


def generate(concatenated_result, times):
    sub_clip_list = [get_sub_clip(concatenated_result, x, 10) for x in times]
    final_clip = concatenate_videoclips([x for x in sub_clip_list if x is not None])
    final_clip.write_videofile(concatenated_result.file_path)


def show_clip(clip):
    file_name = os.path.abspath('rsrc/temp.mp4')
    clip.write_videofile(file_name)
    subprocess.call('open {}'.format(file_name), shell=True)
