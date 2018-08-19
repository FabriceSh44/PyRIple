from datetime import timedelta, datetime
import subprocess
import os
from time_tools import relative_to_string, second_to_string


def get_sub_clip(res, time_delta):
    absolute_time_st = res.absolute_start_time + time_delta[0]
    absolute_time_et = res.absolute_start_time + time_delta[1]

    if res.absolute_end_time < absolute_time_st:
        print('No video for this interval {}'.format(time_delta))
        return []

    cursor = 0
    cur_video = res.clip_list[cursor]

    # get correct video for start of interval
    while cur_video.absolute_start_time < absolute_time_st:
        if cursor + 1 == len(res.clip_list):
            cursor += 1
            break
        cursor += 1
        cur_video = res.clip_list[cursor]
    cursor -= 1
    cur_video = res.clip_list[cursor]

    start_time = (absolute_time_st - cur_video.absolute_start_time).seconds
    # easy case : start time and end time are within the same video
    if absolute_time_et < cur_video.absolute_end_time:
        duration_second = (absolute_time_et - cur_video.absolute_start_time).seconds
        cur_sub_clip = cur_video.video_clip.subclip(start_time, duration_second)
        print('Video {} for interval {}=>{}'.format(os.path.basename(cur_video.file_path),
            relative_to_string(cur_video.absolute_start_time, absolute_time_st),
            relative_to_string(cur_video.absolute_start_time, absolute_time_et)))
        return [[time_delta, cur_sub_clip]]

    new_end_time = time_delta[0] + timedelta(seconds=(cur_video.absolute_end_time - absolute_time_st).seconds)
    sub_clip_list = [[[time_delta[0], new_end_time], cur_video.video_clip.subclip(start_time)]]
    if cursor + 1 == len(res.clip_list):
        # interval is off recorded video
        print('Cut off video {} for interval {}=>{}'.format(os.path.basename(cur_video.file_path),
              relative_to_string(cur_video.absolute_start_time, absolute_time_st),
              second_to_string(cur_video.video_clip.duration)))
        return sub_clip_list
    print('Video {} for interval {}=>{}'.format(os.path.basename(cur_video.file_path),
              relative_to_string(cur_video.absolute_start_time, absolute_time_st),
              second_to_string(cur_video.video_clip.duration)))
    cursor += 1
    cur_video = res.clip_list[cursor]
    if absolute_time_et < cur_video.absolute_end_time:
        duration_second = (absolute_time_et - cur_video.absolute_start_time).seconds
        cur_sub_clip = cur_video.video_clip.subclip(0, duration_second)
        new_start_time = time_delta[1] - timedelta(seconds=duration_second)
        print('Second video {} for interval {}=>{}'.format(os.path.basename(cur_video.file_path),
                                                           second_to_string(0),
                                                           second_to_string(duration_second)))
        sub_clip_list.append([[new_start_time, time_delta[1]], cur_sub_clip])
        return sub_clip_list
    else:
        raise ValueError('That\'s weird, it means that the subclip is bigger than an entire video (~17min)')


def generate(concatenated_result, times, go_pro_folder, output_folder):
    print('Generating subclip from interval and list video clip')
    sub_clip_list = []
    for time_interval in times:
        sub_clip_list += get_sub_clip(concatenated_result, time_interval)

    print('Found {} sub clips'.format(len(sub_clip_list)))
    for sub_clip in sub_clip_list:
        seconds = sub_clip[0][0].seconds
        hours = seconds // 3600
        seconds = seconds - (hours * 3600)
        minutes = seconds // 60
        seconds = seconds - (minutes * 60)
        sub_clip[1].write_videofile(
            os.path.join(output_folder,
                         '{0:02d}h{1:02d}m{2:02d}s_{3}.mp4'.format(hours, minutes, seconds, go_pro_folder)))


def show_clip(clip):
    file_name = os.path.abspath('rsrc/temp.mp4')
    clip.write_videofile(file_name)
    subprocess.call('open {}'.format(file_name), shell=True)
