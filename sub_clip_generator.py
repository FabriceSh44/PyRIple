from moviepy.editor import concatenate_videoclips
from datetime import timedelta, datetime
import subprocess
import os


def get_sub_clip(res, time_delta, force_add):
    absolute_time_st = res.absolute_start_time + time_delta[0]
    absolute_time_et = res.absolute_start_time + time_delta[1]
    for clip in res.clip_list:
        if absolute_time_st > clip.absolute_start_time and absolute_time_et < clip.absolute_end_time:
            start_time = (absolute_time_st - clip.absolute_start_time).seconds
            end_time = (absolute_time_et - clip.absolute_start_time).seconds
            cur_sub_clip = clip.video_clip.subclip(start_time, end_time)
            if force_add:
                print('Adding sub clip at {}'.format(start_time))
                return [time_delta, cur_sub_clip]
            show_clip(clip.video_clip.subclip(end_time - 10 / 4, end_time))
            input_str = input('clip ok ? (Y/n)')
            if input_str.upper() == 'Y':
                print('Adding sub clip')
                return [time_delta, cur_sub_clip]
            else:
                print('Skipping sub clip')
                return None
    print('Cross clip not supported yet')
    return None


def generate(concatenated_result, times, go_pro_folder, output_folder):
    sub_clip_list = [x for x in [get_sub_clip(concatenated_result, x, force_add=True) for x in times] if x is not None]
    print('Found {} sub clips'.format(len(sub_clip_list)))
    for sub_clip in sub_clip_list:
        seconds = sub_clip[0][0].seconds
        hours = seconds // 3600
        seconds = seconds - (hours * 3600)
        minutes = seconds // 60
        seconds = seconds - (minutes * 60)
        sub_clip[1].write_videofile(
            os.path.join(output_folder, '{0:02d}h{1:02d}m{2:02d}s_{3}.mp4'.format(hours, minutes, seconds, go_pro_folder)))


def show_clip(clip):
    file_name = os.path.abspath('rsrc/temp.mp4')
    clip.write_videofile(file_name)
    subprocess.call('open {}'.format(file_name), shell=True)
