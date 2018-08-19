import os
from datetime import timedelta, datetime
from moviepy.editor import VideoFileClip


def second_to_string(second):
    return '{:02.0f}:{:02.0f}min'.format(second//60, second - second//60*60)

def relative_to_string(absolute_time_1, absolute_time_2):
    return second_to_string((absolute_time_2 - absolute_time_1).seconds)