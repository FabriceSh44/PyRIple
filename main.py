import concatenated_result_processor, sub_clip_generator, time_retriever
import os
import argparse
from moviepy.editor import VideoFileClip,concatenate_videoclips


parser = argparse.ArgumentParser(description='Processor of go pro video')

parser.add_argument('-gsc', "--generate_sub_clip", action='store_true')
parser.add_argument('-csc', "--concatenate_sub_clip", action='store_true')
parser.add_argument('-wf', "--working_folder", required=True)
results = parser.parse_args()


working_folder = results.working_folder
output_folder = os.path.join(working_folder, 'output')
input_folder = os.path.join(working_folder, 'input')

print("Working folder is {}".format(working_folder))
print("Input folder is {}".format(input_folder))
print("Output folder is {}".format(output_folder))

print("Checking folders..")
if not os.path.exists(input_folder):
    raise FileNotFoundError("No folder {} found. Please put your videos under input/GOPRO1 folder")

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

if results.generate_sub_clip:
    times = time_retriever.retrieve(working_folder)
    for root, go_pro_folders, files in os.walk(os.path.join(input_folder)):
        for go_pro_folder in go_pro_folders:
            concatenated_result = concatenated_result_processor.process(os.path.join(root, go_pro_folder))
            sub_clip_generator.generate(concatenated_result, times, go_pro_folder, output_folder)

if results.concatenate_sub_clip:
    final_clip_file_path = os.path.join(output_folder,"final_video.mp4")
    sub_clip_to_concat = []
    print("Adding resulting sub clip")
    for root, folders, files in os.walk(os.path.join(output_folder)):
        for file in files:
            if "bof" not in file and "GOPRO" in file:
                sub_clip_to_concat.append(VideoFileClip(os.path.join(root, file)))
    print("Concatenation sub clip")
    sub_clip_to_concat = sorted(sub_clip_to_concat, key=lambda x : x.filename)
    final_clip = concatenate_videoclips(sub_clip_to_concat)
    final_clip.write_videofile(final_clip_file_path)


print('End')
