# A python script to add/subtract seconds in a .srt subtitles file
import re
import os


def time_regex():
    subregex = re.compile(r'''(\d\d)     # hour digits
                              (:)        # colon
                              (\d\d)     # minute digits
                              (:)        # colon
                              (\d\d)     # seconds
                              (,)        # comma
                              (\d\d\d)   # milliseconds
                               ''', re.VERBOSE)
    return subregex


def text_regex():
    reg = re.compile(r'''(--> \d\d:\d\d:\d\d,\d{3}(.*?)\n\n)''', re.DOTALL)
    return reg


def add_time(n, milsec, sec, minute, hr):
    sec1 = n + sec
    if sec1 > 60:
        x_minutes = sec1 // 60
        y_seconds = sec1 - x_minutes * 60
        sec1 = y_seconds
        min1 = minute + x_minutes
        if min1 > 60:
            a = min1 // 60
            b = min1 - a * 60
            min1 = b
            # hr1 = hr + a
        if min1 == 60:
            min1 = 0
            hr1 = hr + 1
        else:
            sec1 = y_seconds
            min1 = minute + x_minutes
            hr1 = hr
    elif sec1 == 60:
        min1 = minute + 1
        if min1 == 60:
            min1 = 0
            hr1 = hr + 1
            sec1 = 0
        else:
            sec1 = 00
            hr1 = hr
    else:
        min1 = minute
        hr1 = hr
    return f'{hr1:02d}:{min1:02d}:{sec1:02d},{milsec}'


def subtract_time(n, milsec, sec, minute, hr):
    n = abs(n)
    if n > (hr*3600 + minute*60 + sec):
        print('ERROR: The decrease in subtitle time cannot be more than the runtime of file.')
        print('try giving smaller amounts of time')
        exit()
    if n > 3600:
        hr1 = n // 3600
        hr = hr - hr1
        sec1 = n - hr1 * 3600
        if sec1 < 60:
            if sec >= sec1:
                n = sec - sec1
            else:
                minute = minute - 1
                sec1 = sec1 - sec
                n = 60 - sec1
        elif 60 < sec1 < 3600:
            min1 = sec1 // 60
            minute = minute - min1
            sec1 = sec1 - min1 * 60
            n = sec - sec1
        elif sec1 == 60:
            minute = minute + 1
        elif sec1 == 0:
            pass
    elif 60 < n < 3600:
        min1 = n // 60
        minute = minute - min1
        sec1 = n - min1 * 60
        n = sec - sec1
    elif 0 < n < 60:
        if n < sec:
            n = sec - n
        elif n > sec:
            minute = minute - 1
            sec1 = n - sec
            n = 60 - sec1
    elif n == 3600:
        hr = hr - 1
        n = sec
    elif n == 60:
        minute = minute - 1
        n = sec
    elif n == 0:
        n = sec
    return f'{hr:02d}:{minute:02d}:{n:02d},{milsec}'


def segregate(list1):
    k = 1
    segregate_left = []
    segregate_right = []
    for j in list1:
        if k % 2 == 0:
            segregate_left.append(j)
        else:
            segregate_right.append(j)
        k += 1

    return segregate_right, segregate_left


def write_times(segregate_left, segregate_right, sub_text, fname):
    with open(fname, 'w') as timefile:
        count = 1
        for i, j, k in zip(segregate_left, segregate_right, sub_text):
            joined_list = []
            joined_list.append(str(i))
            joined_list.append(str(j))
            timefile.write(str(count) + '\n')
            timefile.write(' --> '.join(joined_list))
            timefile.write(k + '\n\n')
            count += 1
        print('done')


def choose_subfile():
    c = 1
    print('choose the subtitle file: ')
    checkname = ''
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.srt'):
            checkname = filename
            print(f'{c}. {filename}')
            c += 1
        continue
    if checkname.endswith('.srt') is False:
        print(f'ERROR: no .srt file found in {os.getcwd()}')
        exit()
    c_input = int(input('enter the file number '))
    c = 1
    subfile_initial_name = ''
    for filename in os.listdir(os.curdir):
        if filename.endswith('.srt'):
            if c == c_input:
                subfile_initial_name = filename
            else:
                c += 1
                continue
        else:
            continue
    return subfile_initial_name


def main():

    subfile_name = choose_subfile()
    try:
        with open(f'{subfile_name}', 'r') as subfile:
            text = subfile.read()
    except FileNotFoundError:
        print('no such file found in directory')
        exit()
    list1 = []
    no_of_sec_to_be_changed = int(input('enter no of seconds to be changed: \n'
                                        '(ex: 5 for adding five seconds\n'
                                        '    -7 for subtracting seven seconds)'))

    for groups in time_regex().findall(text):
        subtitle_sec = groups[4]
        subtitle_min = groups[2]
        subtitle_hour = groups[0]
        subtitle_milsec = groups[6]

        if no_of_sec_to_be_changed > 0:
            list1.append(add_time(int(no_of_sec_to_be_changed), int(subtitle_milsec), int(subtitle_sec),
                                  int(subtitle_min), int(subtitle_hour)))

        elif no_of_sec_to_be_changed <= 0:
            list1.append(subtract_time(int(no_of_sec_to_be_changed), int(subtitle_milsec),
                                       int(subtitle_sec), int(subtitle_min), int(subtitle_hour)))

    left_list, right_list = segregate(list1)
    i_text = []
    for groups in text_regex().findall(text):
        i_text.append(groups[1])

    write_times(left_list, right_list, i_text, subfile_name)


if __name__ == '__main__':
    main()
