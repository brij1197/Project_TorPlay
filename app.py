import threading
import requests
import subprocess
import sys
import json
import vlc
import time
import player
import pathlib
import os
import keyboard
import signal
import atexit


exitFlag=0
webtorrentProc=0

#MultiThreading Class Definition(ASync.)
class customThread(threading.Thread):
    def __init__(self,threadID,funcname,par1,counter):
            threading.Thread.__init__(self)
            self.threadID=threadID
            self.funcname=funcname
            self.par1=par1
            self.counter=counter

    def run(self):
        print("Starting Thread",self.threadID)
        self.funcname(self.par1)
        processHandler(self)

def processHandler(self):
    global webtorrentProc
    try:
        while (exitFlag!=1):
            try:
                if(keyboard.is_pressed('spacebar')):
                    player.toggleVideoPlayback()
                    print("Video Toggled...")
                    time.sleep(1)
                if(keyboard.is_pressed('q')):
                    print(webtorrentProc)
                    if(webtorrentProc!=None):
                            setExitFlag()
                            print("App Quit..")
                            print(webtorrentProc)
                            webtorrentProc.terminate()
                            break
            except Exception as e:
                    print(e)
        # threadID.get_id()            
        # self.join()
    except Exception as ex:
        print(ex)
        print("Thread Error....")
    finally:
        print("Exiting Thread.... ", str(self.threadID))

# Exit Flag Definition
def setExitFlag():
    global exitFlag
    exitFlag=1
    player.endVideoPlay()

#Definition to play the video being streamed on localhost
def vlc_play(magnet_selected):
     filename=movieFileHandler(magnet_selected)
     player.startVideoPlayback(filename)

def dirHandler():
    currDir=pathlib.Path().absolute()
    downloadDir="Torrents"
    path=os.path.join(currDir,downloadDir)
    print(os.path.isdir(path))
    if(os.path.isdir(path)):
        print("Path Exists")
        pass
    else:
        os.mkdir(path)
    return path

def movieFileHandler(magnet_selected):
    magnetUrl="http://localhost:5000/torrent_file"
    payload={"magnet":magnet_selected}
    magnetResult=requests.get(url=magnetUrl,json=payload).json()
    filesize=0
    fileName=None
    for element in magnetResult:
        if(element["filesize"]>filesize):
            filesize=element["filesize"]
            if "filename" in element:
                fileName=element["filename"]
                return fileName

#Definition to handle the webtorrent client while downloading
def handler(magnet_link):
    path=dirHandler()
    os.chdir(path)
    cmd1=[]
    cmd1.append("webtorrent")
    cmd1.append(magnet_link)
    #Torrent can be closed using ctrl+c
    

#Definition to handle the webtorrent client when streaming
def streamHandler(magnet_link):
      global webtorrentProc
      path=dirHandler()
      os.chdir(path)
      cmd0="webtorrent download "+magnet_link+" -o "+path
      if sys.platform.startswith("win32"):
         webtorrentProc=subprocess.Popen(cmd0,shell=True,stdout=subprocess.PIPE)
         print(webtorrentProc)
       #  webtorrentProc=subprocess.Popen(cmd0, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
      elif sys.platform.startswith("linux"):
         webtorrentProc=subprocess.call(cmd0,stdout=subprocess.PIPE)
      else:
         print("System Platform Not Supported")

#Method to handle torrent api calls and call torrent handler and vlc player
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
    
    if(download==False):
      thread1=customThread(1,streamHandler,magnet_selected,1)
      thread2=customThread(2,vlc_play,magnet_selected,2)
      thread1.start()
      thread2.start()
      thread1.join()
      thread2.join()
      print("Exiting....")
        #   cwd=os.getcwd()
        #   os.chdir(os.path.dirname(cwd))
        #   os.rmdir(cwd)
        #   print(os.getcwd())
    else:
        handler(magnet_selected)
        

#Method to input movie name
def movie():
    m_name = input("Name of movie:")
    api(m_name)

#Method to input series name
def series():
    s_name = input("Name of series:")
    s_name_s = input("Season:")
    s_name_e = input("Episode:")
    series_name = "{} S{}E{}".format(s_name, s_name_s, s_name_e)
    api(series_name)

#Main
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
