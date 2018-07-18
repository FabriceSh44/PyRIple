import concatenated_result_processor, sub_clip_generator, time_retriever
import os

date = '20180712'
working_folder = os.path.join('rsrc', date)
times = time_retriever.retrieve(working_folder)

for root, go_pro_folders, files in os.walk(os.path.join(working_folder)):
    for go_pro_folder in go_pro_folders:
        concatenated_result = concatenated_result_processor.process(os.path.join(root, go_pro_folder))
        sub_clip_generator.generate(concatenated_result, times, go_pro_folder)

print('End')
