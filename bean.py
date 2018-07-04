import os
from datetime import timedelta, datetime
from moviepy.editor import VideoFileClip


class VideoClipTimeStamped:
    def __init__(self, file_path):
        self.file_path = file_path
        self.video_clip = VideoFileClip(file_path)
        self.absolute_start_time = datetime.fromtimestamp(os.stat(file_path).st_birthtime)
        self.absolute_end_time = self.absolute_start_time + timedelta(seconds=self.video_clip.duration)

    def __str__(self) -> str:
        return 'VCTS: {} st:{} et:{} dur:{:2.2f}min'.format(self.file_path, self.absolute_start_time.strftime('%H:%M:%S'),
                                                     self.absolute_end_time.strftime('%H:%M:%S'),
                                                     self.video_clip.duration/60)


class ConcatenatedResult:
    def __init__(self, file_path):
        self.file_path = file_path
        self.clip_list = []
        self.absolute_start_time = None
        self.absolute_end_time = None

    def add_clip(self, clip):
        self.clip_list.append(clip)
        if self.absolute_start_time == None:
            self.absolute_start_time = clip.absolute_start_time
        self.absolute_end_time = clip.absolute_end_time


    def __str__(self) -> str:
        return 'CR: {} st:{} et:{} dur:{:2.2f}min'.format(self.file_path, self.absolute_start_time.strftime('%H:%M:%S'),
                                                   self.absolute_end_time.strftime('%H:%M:%S'),
                                                   sum(map(lambda x: x.video_clip.duration, self.clip_list))/60)
