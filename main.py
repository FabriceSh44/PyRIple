import concatenated_result_processor, sub_clip_generator
import os
import datetime


date = '20180628'
working_folder = os.path.join('rsrc', date)

times = [datetime.time(20, 10, 5), datetime.time(20, 20, 5), datetime.time(20, 30, 5)]

concatenated_result = concatenated_result_processor.process(working_folder)

sub_clip_generator.generate(concatenated_result, times)



print('End')
