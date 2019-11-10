import re
with open('subtitles.srt', 'r') as f:
    text = f.read()
    f.seek(0)
subRegex = re.compile(r'''(\d\d)     # hour digits
                          (:)        # colon
                          (\d\d)     # minute digits
                          (:)        # colon
                          (\d\d)     # seconds
                          (,)        # comma
                          (\d\d\d)   # milliseconds
                           ''', re.VERBOSE)


def time(n, milsec, sec, minute, hr):
    sec1 = n + sec
    if sec1 > 60:
        x_minutes = sec1 // 60
        y_seconds = sec1 - x_minutes*60
        sec1 = y_seconds
        min1 = minute + x_minutes
        if min1 > 60:
            a = min1 // 60
            b = min1 - a*60
            min1 = b
            hr1 = hr + a
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
    return [hr1, min1, sec1, milsec]


list1 = []
k = 1
no_of_sec_to_be_changed = int(input('enter no of seconds to be changed '))
with open('sub2.txt', 'w') as file:
    h = 1
    for groups in subRegex.findall(text):
        subtitle_sec = groups[4]
        subtitle_min = groups[2]
        subtitle_hour = groups[0]
        subtitle_milsec = groups[6]
        # file.write(h)

        list1.append(time(int(no_of_sec_to_be_changed), int(subtitle_milsec), int(subtitle_sec)
                     , int(subtitle_min), int(subtitle_hour)))



segregate_left = []
segregate_right = []
for j in list1:
    if k % 2 == 0:
        segregate_left.append(j)
    else:
        segregate_right.append(j)
    k += 1
with open('sub2.txt', 'w') as file:
    h = 1
    string = []
    for ele1, ele2 in zip(segregate_left, segregate_right):
        #file.write(str(h))
        #print(str(h))
        #file.write(str(ele1) + ' --> ' + str(ele2))
        string.append(str(ele2) + ' --> ' + str(ele1))
        #string = list(string)

        h += 1
q = []
for x in list(string):
    for y in x:
        if y != '[' and y != ']':
            q.append(y)
        else:
            continue
print(string)