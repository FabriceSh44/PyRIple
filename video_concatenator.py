from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("rsrc/20180628/input/GOPR0737.MP4")
clip2 = VideoFileClip("rsrc/20180628/input/GOPR0738.MP4").subclip(0,5)
final_clip = concatenate_videoclips([clip1,clip2])
final_clip.write_videofile("rsrc/20180628/output/my_concatenation.mp4")