import vlc
import time
import keyboard

def vlc_play():
    # url="http://localhost:8000/0/Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4"
    # # video="Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4"
    print("Playing....")
    media=vlc.MediaPlayer("D:\\Libraries\\Extra\\Projects\\Netflix\\Marvel Studios Black Widow Official Teaser.mp4")
    media.play()
    time.sleep(3)
    while(media.get_position() < media.get_length()):
        try:
            if(keyboard.is_pressed('spacebar')):
                if(media.get_state() == "State.Paused"):
                    media.play()
                media.pause()
            if(keyboard.is_pressed('q')):
                print("App Quit..")
                break
        except:
            break
    # vlcInstance = vlc.Instance()
    # player = vlcInstance.media_player_new()
    # player.set_mrl("http://localhost:8000/0/Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4")
    # player.play()

def main():
    print("Main")
    vlc_play()

if __name__ == "__main__":
     main()