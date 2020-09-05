import vlc
import time
import keyboard
import app

media=None
notEndVideoPlayback=1


def startVideoPlayback(filename):
    global media
    print("Playing....")
    time.sleep(10)
    media = vlc.MediaPlayer("http://localhost:8000/0/{}".format(filename)) #D:\\Libraries\\Extra\\Projects\\Netflix\\Marvel Studios Black Widow Official Teaser.mp4)
    media.play()
    while(media.get_position() < media.get_length() and notEndVideoPlayback):
        pass

def toggleVideoPlayback():
    if(media.get_state()==vlc.State.Playing):
        media.pause()
    elif(media.get_state()==vlc.State.Paused):
        media.play()

def endVideoPlay():
    global media
    global notEndVideoPlayback
    notEndVideoPlayback=0
    media.stop()