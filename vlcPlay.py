import vlc  # to use media player services
import time  # to go sleep


def play_video(video_name, file_name):

    # params: a video_name (string)
    # functionality: plays a video
    # return: void

    media_player = vlc.MediaPlayer()
    media = vlc.Media(video_name)

    media_player.set_media(media)
    media_player.play()
    media_player.video_set_subtitle_file(file_name)

    time.sleep(3)
    while media_player.is_playing():
        pass

# Test Drive Code

# play_video(video_name, file_name)