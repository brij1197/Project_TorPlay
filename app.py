import requests
import subprocess
import sys
import asyncio
import magnet2torrent


async def torrent_file_Extractor(magnet_link):
     mt = magnet2torrent.Magnet2Torrent(magnet2torrent)
     try:
        filename, torrent_data = await mt.retrieve_torrent()
     except magnet2torrent.FailedToFetchException:
        print("Failed")


def handler(magnet_link,download):
     cmd1=[]
     cmd1.append("webtorrent")
     cmd1.append(magnet_link)
     if(download==False):
         cmd1.append("--vlc")

     print (cmd1)
#     if sys.platform.startswith("linux"):
#         subprocess.call(cmd1)
#     elif sys.platform.startswith("win32"):
#         subprocess.call(cmd1,shell=True)

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
    handler(magnet_selected,download)
    asyncio.run(torrent_file_Extractor(magnet_selected))


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
