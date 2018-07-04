from moviepy.editor import concatenate_videoclips
from datetime import timedelta, datetime
from PIL import Image


def get_sub_clip(res, time, duration_sec):
    absolute_time = datetime.combine(res.absolute_start_time.date(), time)
    for clip in res.clip_list:
        if absolute_time - timedelta(
                seconds=duration_sec) > clip.absolute_start_time and absolute_time < clip.absolute_end_time:
            end_time = (absolute_time - clip.absolute_start_time).seconds
            res.show_frame(clip.video_clip, (end_time - duration_sec) / 2)
            input_str = input('Pic ok ? (Y/n)')
            return clip.video_clip.subclip(end_time - duration_sec, end_time) if input_str == 'Y' else None
    print('cross clip not supported yet')
    return None


def generate(concatenated_result, times):
    sub_clip_list = [get_sub_clip(concatenated_result, x, 10) for x in times]
    final_clip = concatenate_videoclips([x for x in sub_clip_list if x is not None])
    final_clip.write_videofile(concatenated_result.file_path)


def show_frame(clip, time_sec):
    file_name = 'rsrc/temp.jpg'
    clip.save_frame(file_name, time_sec)
    image = Image.open(file_name)
    image.show()
