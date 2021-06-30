import vlc
from time import sleep
from os.path import splitext, isfile
from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def read_srt(path):
    content = ""
    with open(path, 'r', encoding='UTF-8') as f:
        content = f.read()
        return content


def get_sequences(content):
    sequences = content.split('\n\n')
    sequences = [seq.split('\n') for seq in sequences]

    sequences = [list(filter(None, seq)) for seq in sequences]

    return list(filter(None, sequences))

def strFloatTime(strTime):
    xx = strTime.split(':')
    hr = int(xx[0])
    mn = int(xx[1])
    sc = int(xx[2].split(',')[0])
    ms = int(xx[2].split(',')[1])
    actual_time = hr * 60 * 60 + mn * 60 + sc + (ms/1000)
    return actual_time

# srt_path = './The Vampire Diaries - 1x01 - Pilot.HDTV.FQM.en.srt'
# content = read_srt(srt_path)
# sequences = get_sequences(content)
#
# print(sequences)

# strTime = '00:00:11,235'
#
# print(strFloatTime(strTime))

class RealizeAddSubtitles():
    def __init__(self, videoFile, srtFile):
        self.src_video = videoFile
        self.sentences = srtFile

        if not (isfile(self.src_video) and isfile(self.sentences)):
            print('File doesn\'t exists')
        elif not (self.sentences.endswith('.srt')):
            print('Unsupported file type')
        else:
            video = VideoFileClip(self.src_video)
            duration = video.duration
            w, h = video.w, video.h

            txts = []
            content = read_srt(self.sentences)
            sequences = get_sequences(content)

            for line in sequences:
                if len(line) < 3:
                    continue
                sentences = line[2]
                start = line[1].split(' --> ')[0]
                end = line[1].split(' --> ')[1]

                start = strFloatTime(start)
                end = strFloatTime(end)

                start, end = map(float, (start, end))
                span = end - start
                txt = (TextClip(sentences, fontsize=40,
                               font='Forte', size=(w-20, 40),
                               align='center', color='white')
                        .set_position((10, h - 150))
                        .set_duration(span)
                        .set_start(start))
                txts.append(txt)

            video = CompositeVideoClip([video, *txts])
            print(video.duration)
            fn, ext = splitext(self.src_video)

            video.ipython_display(width=280, maxduration=int(duration))


if __name__ == '__main__':
    srt_path = './The Vampire Diaries - 1x02 - The Night of the Comet.HDTV.FQM.en.srt'
    vid_path = './The Vampire Diaries S01E02 TheNight of the Comet.avi'
    addSubtitles = RealizeAddSubtitles(vid_path, srt_path)