import threading
import requests
import subprocess
import sys
import json
import vlc
import time
import play

exitFlag=0
class customThread(threading.Thread):
    def __init__(self,threadID,funcname,par1,par2,counter):
        if(par1==0 and par2==0):
            threading.Thread.__init__(self)
            self.threadID=threadID
            self.funcname=funcname
            self.counter=counter
            self.flag=1
        else:
            threading.Thread.__init__(self)
            self.threadID=threadID
            self.funcname=funcname
            self.par1=par1
            self.par2=par2
            self.counter=counter
            self.flag=0

    def run(self):
        print("Starting ")
        if(self.flag==1):
            self.funcname()
        else:
            self.funcname(self.par1,self.par2)
        print_time(self.threadID,self.counter,5)

def print_time(threadID,delay,counter):
    try:
        while counter:
            if exitFlag:
                threadID.exit()
            time.sleep(delay)
            print("%s: %s" %(str(threadID),time.ctime(time.time())))
            counter-=1
    except:
        print("Thread Error....")
    finally:
        print("Exiting Thread.... ", str(threadID))


def vlc_play():
    # # # url="http://localhost:8000/0/Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4"
    # # # # video="Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4"
    # # print("Playing....")
    # # media=vlc.MediaPlayer("D:\\Libraries\\Extra\\Projects\\Netflix\\Marvel Studios Black Widow Official Teaser.mp4")
    # # media.play()
    # # time.sleep(5)
    # # while(media.get_position() < media.get_length()):
    #     # pass    
    # # # vlcInstance = vlc.Instance()
    # # # player = vlcInstance.media_player_new()
    # # # player.set_mrl("http://localhost:8000/0/Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4")
    # # # player.play() 
    # play.vlc_play()
    play.main()

def handler(magnet_link, download):
     cmd1 = []
     cmd1.append("webtorrent")
     cmd1.append(magnet_link)
     if(download == False):
         cmd1.append("--vlc")
     subprocess.call(cmd1,shell=True)
        #  url="https://localhost:8000/0/"
        #  video="Man.of.Steel.2013.1080p.BluRay.x264.YIFY.mp4"
        #  print("Playing....")
        #   subprocess.call()
        # media=vlc.MediaPlayer("D:\\Libraries\\Extra\\Projects\\Netflix\\Marvel Studios Black Widow Official Teaser.mp4")
        #  media=vlc.MediaPlayer(url+video)
        #  media.play()
        #  time.sleep(5)
        #  while(media.get_position() < media.get_length()):
        #         pass
        #  vlc_instance = vlc.Instance()
        #  media = vlc_instance.media_new('D:\\Libraries\\Extra\\Projects\\Netflix\\Marvel Studios Black Widow Official Teaser.mp4')
        #  player = vlc_instance.media_player_new()
        #  player.set_media(media)
        #  player.play()
        #  print (media.get_length())
        #  if sys.platform.startswith("win32"):
    #  subprocess.call(cmd1,shell=True)
#     if sys.platform.startswith("linux"):
#         subprocess.call(cmd1)

def api(name):
    index = 1
    magnet_links = []
    api_url = "https://api.sumanjay.cf/torrent/?query={}".format(name)
    torr_results = requests.get(api_url).json()
    for result in torr_results:
        if 'movie' in result['type'].lower():
            print(index, ". ", result['name'], "  ", result['size'])
            index += 1
            magnet_links.append(result['magnet'])
    sel = int(input("Index of the movie to be streamed:"))
    magnet_selected = magnet_links[sel-1]
    download = False
    stream_choice = input("Stream/Download:")
    if(stream_choice.lower() == "download"):
        download = True
    else:
        download = False
    # handler(magnet_selected,download)
    thread1=customThread(1,handler,magnet_selected,download,1)
    thread2=customThread(2,vlc_play,0,0,2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("Exiting....")
   # print("Waiting for 10 secs....")
    # time.sleep(10)
    # threading._start_new_thread(target=vlc_play).start()



def movie():
    m_name = input("Name of movie:")
    api(m_name)


def series():
    s_name = input("Name of series:")
    s_name_s = input("Season:")
    s_name_e = input("Episode:")
    series_name = "{} S{}E{}".format(s_name, s_name_s, s_name_e)
    api(series_name)


def main():
    sel_input = input("Movie/Series:")
    if(sel_input.lower() == "movie"):
        movie()
    elif(sel_input.lower() == "series"):
        series()
    else:
        print("Please select from the above options")


if __name__ == "__main__":
    main()
