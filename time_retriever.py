import os
from datetime import datetime, timedelta


def retrieve(working_folder):
    time_file = os.path.join(working_folder, "time_data.csv")
    if not os.path.exists(time_file):
        raise FileNotFoundError("Unable to find {}".format(time_file))
    delta_time_str_list = [x.split(',')[1] for x in open(time_file)][1:]
    delta_time_datetime_list = [datetime.strptime(x, "%M:%S.%f") for x in delta_time_str_list if x != '']
    timedelta_total = timedelta()
    time_delta_list = []
    for cur_dt in delta_time_datetime_list:
        cur_tdelta = timedelta(minutes=cur_dt.minute, seconds=cur_dt.second)
        timedelta_total += cur_tdelta
        time_delta_list.append(timedelta_total)

    return time_delta_list
