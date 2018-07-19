from moviepy.editor import concatenate_videoclips
from datetime import timedelta, datetime
import subprocess
import os


def get_sub_clip(res, time_delta, duration_sec, force_add):
    absolute_time = res.absolute_start_time + time_delta
    for clip in res.clip_list:
        if absolute_time - timedelta(
                seconds=duration_sec) > clip.absolute_start_time and absolute_time < clip.absolute_end_time:
            end_time = (absolute_time - clip.absolute_start_time).seconds
            cur_sub_clip = clip.video_clip.subclip(end_time - duration_sec, end_time + 3)
            if force_add:
                print('Adding sub clip at {}'.format(absolute_time))
                return [time_delta, cur_sub_clip]
            show_clip(clip.video_clip.subclip(end_time - duration_sec / 4, end_time))
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
    sub_clip_list = [get_sub_clip(concatenated_result, x, duration_sec=10, force_add=True) for x in times]
    for sub_clip in sub_clip_list:
        seconds = sub_clip[0].seconds
        hours = seconds // 3600
        seconds = seconds - (hours * 3600)
        minutes = seconds // 60
        seconds = seconds - (minutes * 60)
        sub_clip[1].write_videofile(
            os.path.join(output_folder, '{}h{}m{}s_{}.mp4'.format(hours, minutes, seconds, go_pro_folder)))

        # final_clip = concatenate_videoclips([x for x in sub_clip_list if x is not None])
        # final_clip.write_videofile(concatenated_result.file_path)


def show_clip(clip):
    file_name = os.path.abspath('rsrc/temp.mp4')
    clip.write_videofile(file_name)
    subprocess.call('open {}'.format(file_name), shell=True)
