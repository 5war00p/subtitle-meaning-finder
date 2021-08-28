# PYPI libraries
import re  # for string manipulation
import time  # to sleep the program
from tqdm import tqdm  # to show progress bar while analysing .srt
from multiprocessing import Process  # to run different processes

# user-defined modules
from level import get_level
from vlcPlay import play_video
from dictionary import get_meaning

LEVELS = {1: 'Beginner', 2: 'Basic', 3: 'Intermediate', 4: 'Expert'}

def categorize(lis, prof):

    # params: list of words (List)
    # return: meanings of the words (Dict)

    words = re.findall(r'\w+', lis)
    words = list(map(lambda x: x.lower(), words))
    words = list(set(words))

    definitions = {}
    for word in words:
        level = get_level(word)
        if prof <= level[0]:
            definition = get_meaning(word)
            if definition is not None:
                definitions[word] = definition
    return definitions


def check_empty(s):

    # params: a line (string)
    # return: whether empty or not (bool)
    try:
        int(s)
        return True
    except ValueError:
        return False


def time_in_seconds(line):

    # params: a line (string)
    # return: convert into time if time exists in string (int)

    line = line.replace(',', ':')
    hours, minutes, seconds, milliseconds = [int(n) for n in line.split(":")]
    t = (hours * 3600) + (minutes * 60) + (seconds) + (milliseconds / 1000.0)
    return t


def get_data(file_name, prof):

    # params:  a filename (string)
    # return1: lyric_list (List)- dialogues
    # return2: delay_before (List)- delays before the dialogue appear
    # return3: result (Dict)- meanings of the words
    # return4: span_time (List)- span b/w start & end of the dialogue

    prevTime = 0
    delay_before = []
    span_time = []
    lyric_list = []
    result = {}

    with open(file_name, "r", encoding="utf-8") as srt_file:
        Lines = srt_file.readlines()
        LineCount = Lines.count('\n')

        srt_file.seek(0)

        for i, line in tqdm(enumerate(srt_file), total=LineCount):
            if check_empty(line):
                t = srt_file.readline()
                lyric = ""
                line2 = srt_file.readline()
                while line2:
                    if line2.strip() == "":
                        break
                    lyric = lyric + line2
                    line2 = srt_file.readline()

                begin, sep, end = t.strip().split()

                t_begin = time_in_seconds(begin)
                t_end = time_in_seconds(end)
                wait_before = t_begin - prevTime
                persists = t_end - t_begin

                prevTime = t_end
                delay_before.append(wait_before)
                span_time.append(persists)
                lyric_list.append(lyric)

                definitions = categorize(lyric, prof)
                if definitions != {}:
                    result[i] = definitions

                i += 1
    return lyric_list, delay_before, result, span_time


def display_subtitle(lyric_list, delay_before, definitions, span_time):

    # param1: lyric_list (List)- dialogues
    # param2: delay_before (List)- delays before the dialogue appear
    # param3: definitions (Dict)- meanings of the words
    # param4: span_time (List)- span b/w start & end of the dialogue
    # functionality: print subtitle by its respective time
    # return:  void

    for i in range(0, len(lyric_list)):
        try:
            time.sleep(delay_before[i])
        except:
            break
        print(lyric_list[i])
        if i in definitions:
            print(definitions[i])
        time.sleep(span_time[i])


if __name__ == '__main__':

    # files must be in current directory
    # or else u give path

    print('''---- English-Proficiency Levels --- \
            \n 1. Beginner 
            \n 2. Basic
            \n 3. Intermediate
            \n 4. Expert
            \n Choose an option: ''', end='')
    while True:
        try:
            prof_level = int(input())
            break
        except:
            print('Enter valid option [like 1]:')

    file_name = input('Enter .srt file name: ')
    video_name = input('Enter video name: ')

    lyric_list, delay_before, definitions, span_time = get_data(file_name, prof_level)
    time.sleep(3)
    p1 = Process(name='p1', target=play_video, args=(video_name, file_name))
    p2 = Process(name='p2', target=display_subtitle, args=(lyric_list, delay_before, definitions, span_time))
    p1.start()
    p2.start()