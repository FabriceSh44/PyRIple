import os
from datetime import datetime, timedelta


def squash_time_delta(time_delta_list, duration_mini_clip):
    print('Squashing time into intervals..')
    time_interval_list = []
    fraction_duration = 2 / 3  # if 15 sec duration, interval get 10 sec before and 5 sec after the tick
    cursor = 0
    while cursor < len(time_delta_list):
        message = 'Transformed: '
        cur_time_delta = [timedelta(seconds=time_delta_list[cursor].seconds - duration_mini_clip * fraction_duration
                                    ), None]
        while cursor + 1 < len(time_delta_list) \
                and time_delta_list[cursor].seconds + duration_mini_clip >= time_delta_list[cursor + 1].seconds:
            #found another tick in duration => concatenate
            message += str(time_delta_list[cursor]) + " + "
            cursor += 1
        cur_time_delta[1] = timedelta(seconds=time_delta_list[cursor].seconds + duration_mini_clip * (1-fraction_duration))
        time_interval_list.append(cur_time_delta)
        print('{}{} into:{}'.format(message, str(time_delta_list[cursor]), '[{};{}]'.format(str(cur_time_delta[0]), str(cur_time_delta[1]))))
        cursor += 1
    print('Found {} intervals'.format(len(time_interval_list)))
    return time_interval_list


def retrieve(working_folder, duration_mini_clip):
    time_file = os.path.join(working_folder, "time_data.csv")
    if not os.path.exists(time_file):
        raise FileNotFoundError("Unable to find {}".format(time_file))
    print('Retrieving time in {}'.format(time_file))
    delta_time_str_list = [x.split(',')[1] for x in open(time_file)][1:]
    for fmt in ["%H:%M:%S", "%H:%M:%S.%f"]:
        try:
            delta_time_datetime_list = [datetime.strptime(x, fmt) for x in delta_time_str_list if x != '']
        except ValueError:
            pass
    if len(delta_time_datetime_list) == 0:
        raise ValueError('no valid date format found')
    timedelta_total = timedelta()
    time_delta_list = []
    for cur_dt in delta_time_datetime_list:
        cur_tdelta = timedelta(minutes=cur_dt.minute, seconds=cur_dt.second)
        timedelta_total += cur_tdelta
        time_delta_list.append(timedelta_total)

    time_interval_list = squash_time_delta(time_delta_list, duration_mini_clip)

    return time_interval_list
