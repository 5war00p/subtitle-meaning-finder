-import re
import nltk
from level import get_level
from dictionary import get_meaning

fname = 'The Vampire Diaries - 1x02 - The Night of the Comet.HDTV.FQM.en.srt'

def categorize(lis):

    # params: list of words (List)
    # return: meanings of the words (Dict)

    words = re.findall(r'\w+', lis)
    words = list(map(lambda x: x.lower(), words))
    words = list(set(words))

    definitions = {}
    for word in words:
        level = get_level(word)
        if level[0] == 'Expert':
            definition = get_meaning(word)
            if definition is not None:
                definitions[word] = definition
    return definitions

def get_meanings(fname):
    with open(fname, 'r', encoding='utf-8') as ipfile:
        Lines = ipfile.readlines()
        Lines = list(map(lambda line: line.replace('\n', ''), Lines))
        updated = []
        pointer = 0
        for index,str in enumerate(Lines):
            each = {}
            if str == '':
                each['line_number'] = Lines[pointer]
                each['time_interval'] = Lines[pointer+1]
                each['messages'] = Lines[pointer+2: index]
                updated.append(each)
                pointer = index + 1

        result = {}
        for ln, line in enumerate(updated):
            messages = line['messages']
            message = ' '.join(messages)
            meanings = categorize(message)
            if meanings != {}:
                result[ln] = meanings

        # print(result)
        return result
            # for message in messages:
                # message = re.sub(r'[^\w]', ' ', message)
                #tokens = nltk.word_tokenize(message)
                #pos_tagged_tokens = nltk.pos_tag(tokens)
                #print(pos_tagged_tokens)
                # print(message)

get_meanings(fname)