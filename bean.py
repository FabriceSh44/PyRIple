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
        return 'VCTS: {} st:{} et:{} dur:{}s'.format(self.file_path, self.absolute_start_time.strftime('%H:%M:%S'),
                                                    self.absolute_end_time.strftime('%H:%M:%S'),
                                                    self.video_clip.duration)
