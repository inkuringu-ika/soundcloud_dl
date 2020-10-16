import sys
import json
import requests
import subprocess
import os
import urllib
import re
import traceback
from bs4 import BeautifulSoup
from tqdm import tqdm
from colorama import init, Fore, Style
init()
if getattr(sys, 'frozen', False):
    program_directory_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory_path = os.path.dirname(os.path.abspath(__file__))

print('Copyright (c) 2020 inkuringu-ika')
print('This software is released under the "GNU GENERAL PUBLIC LICENSE Version 3", see LICENSE file.')
print()

native_version = "6.3.0"
if(program_directory_path == os.getcwd()):
    if(not os.path.exists("./downloads/")):
        os.mkdir("./downloads")
    save_directory = "./downloads"
else:
    save_directory = "."
requests_option = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

def client_id():
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    try:
        print("Fetching latest client_id...")
        request_url = "https://soundcloud.com/"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        request_url = soup.find_all("script")[-2].get("src")
        r = requests.get(request_url, headers=requests_option, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        for for_data in r.text.split("{")[3].split("}")[0].split(","):
            if(for_data.split(":")[0] == "client_id"):
                #print(for_data.split(":")[1][1:][:-1])
                #break
                #testcode raise Exception
                return for_data.split(":")[1][1:][:-1]
        print(Fore.RED + "No Data" + Style.RESET_ALL)
        raise Exception
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        traceback.print_exc()
        print(Fore.YELLOW + "Failed to get the latest client_id. Fetching old client_id..." + Style.RESET_ALL)
        #github page
        request_url = "https://inkuringu-ika.github.io/api/soundcloud-client_id.json"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        for for_json in json.loads(r.text):
            if(for_json["type"] == "pc_browser"):
                return for_json["client_id"]

def app_version():
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    request_url = "https://soundcloud.com/version.txt"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    return r.text

def get_info(inputurl):
    global status_code
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    request_url = "https://api-v2.soundcloud.com/resolve?url=" + inputurl + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    return json.loads(r.text)

def download_track(track_info, save_directory):
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    print("downloading...")
    Noid = str(track_info["id"])
    print("Track ID: " + Noid)
    request_url = 'https://api-v2.soundcloud.com/tracks/' + Noid + '?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    track_info_2 = json.loads(r.text)
    if(not track_info_2["streamable"]):
        print(Fore.YELLOW + "Stream is not available." + Style.RESET_ALL)
        return
    if(track_info_2["policy"] == "BLOCK"):
        print(Fore.YELLOW + "The download of this track is blocked in your country." + Style.RESET_ALL)
        return
    if(track_info_2["downloadable"] and track_info_2["has_downloads_left"]):
        request_url = "https://api-v2.soundcloud.com/tracks/" + Noid + '/download?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        request_url = json.loads(r.text)["redirectUri"]
        r = requests.get(request_url, headers=requests_option, stream=True, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\||\n]',"_",track_info_2["title"] + "." + r.headers["content-disposition"][r.headers["content-disposition"].find("filename=") + len("filename="):].replace('"',"").split(".")[-1])
        pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
        with open(save_directory + "/" + filename, 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()
    else:
        print(Fore.YELLOW + 'Not a free download!' + Style.RESET_ALL)
        filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\|]',"_",track_info_2["title"] + ".mp3")
        hls_active = 0
        progressive_active = 0
        format_for_count = 0
        for transcoding in track_info_2["media"]["transcodings"]:
            if(transcoding["format"]["protocol"] == "hls" and transcoding["format"]["mime_type"] == "audio/mpeg"):
                hls_active = 1
                hls_active_count = format_for_count
            elif(transcoding["format"]["protocol"] == "progressive" and transcoding["format"]["mime_type"] == "audio/mpeg"):
                progressive_active = 1
                progressive_active_count = format_for_count
            format_for_count = format_for_count + 1
        if(progressive_active == 1):
            request_url = track_info_2["media"]["transcodings"][progressive_active_count]["url"] + '?client_id=' + client_id
            r = requests.get(request_url, headers=requests_option, timeout=10)
            status_code = r.status_code
            r.raise_for_status()
            request_url = json.loads(r.text)["url"]
            r = requests.get(request_url, headers=requests_option, stream=True, timeout=10)
            status_code = r.status_code
            r.raise_for_status()
            pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
            with open(save_directory + "/" + filename, 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024):
                    file.write(chunk)
                    pbar.update(len(chunk))
                pbar.close()
        elif(hls_active == 1):
            request_url = track_info_2["media"]["transcodings"][hls_active_count]["url"] + '?client_id=' + client_id
            r = requests.get(request_url, headers=requests_option, timeout=10)
            status_code = r.status_code
            r.raise_for_status()
            request_url = json.loads(r.text)["url"]
            ffmpeg_path = program_directory_path + "\\ffmpeg.exe"
            if(os.path.isfile(ffmpeg_path)):
                print("ffmpeg_path: " + ffmpeg_path)
                subprocess.call([ffmpeg_path,"-y","-i",request_url,"-c","copy",save_directory + "/" + filename])
            else:
                #print(Fore.YELLOW + "FFmpeg is required to download this audio." + Style.RESET_ALL)
                print(Fore.YELLOW + "Download using the built-in hls downloader. Use ffmpeg if it does not download properly." + Style.RESET_ALL)
                r = requests.get(request_url)
                file = open(save_directory + "/" + filename,mode="wb")
                for for_data in r.text.split("\n"):
                    if(not for_data[0] == "#"):
                        print("Downloading segment...")
                        r = requests.get(for_data, headers=requests_option, timeout=10)
                        status_code = r.status_code
                        r.raise_for_status()
                        print("Writing to file...")
                        file.write(r.content)
                file.close()
        else:
            print(Fore.YELLOW + "Error: Not supported type" + Style.RESET_ALL)

if(len(sys.argv) > 1):
    for argv in sys.argv[1:]:
        if(argv == "-h" or argv == "--help"):
            print("soundcloud_dl.py [option]")
            print("soundcloud_dl.exe [option]")
            print("-h,--help: Show usage")
            print("-C,--copyright: Show copyright")
            print("-V,--version: Show version")
            print("-U,--update: Update (Experimental option)")
            print("--ffmpeg-download: Download ffmpeg")
            sys.exit(1)
        elif(argv == "-C" or argv == "--copyright"):
            print('soundcloud_dl: Copyright (c) 2020 inkuringu-ika    GNU GENERAL PUBLIC LICENSE Version 3')
            print('Colorama: Copyright (c) 2010 Jonathan Hartley    BSD 3-Clause "New" or "Revised" License')
            print('Requests: Copyright (c) 2019 Kenneth Reitz    Apache License Version 2.0')
            print('tqdm: Copyright (c) 2013 noamraph    MIT License , Mozilla Public Licence v2.0')
            sys.exit(1)
        elif(argv == "-V" or argv == "--version"):
            print("Version " + native_version)
            sys.exit(1)
        else:
            userinput = argv
else:
    userinput = input('url>>')


try:
    client_id = client_id()
except requests.exceptions.ConnectionError:
    print(Fore.RED + 'Error: network error.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
except requests.exceptions.HTTPError:
    print(Fore.RED + 'Error: Status code error.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
except requests.exceptions.ConnectTimeout:
    print(Fore.RED + 'Error: Failed to get client_id. The GitHub server may be down.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)

try:
    app_version = app_version()
except requests.exceptions.ConnectionError:
    print(Fore.RED + 'Error: network error.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
except requests.exceptions.HTTPError:
    print(Fore.RED + 'Error: Status code error.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
except requests.exceptions.ConnectTimeout:
    print(Fore.RED + 'Error: Timed out. The SoundCloud server may be down.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)

try:
    json_result = get_info(userinput)
except requests.exceptions.ConnectionError:
    print(Fore.RED + 'Error: network error.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
except requests.exceptions.HTTPError:
    if(status_code == 404):
        print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
        sys.exit(1)
    else:
        print(Fore.RED + 'Error: Status code error.' + Style.RESET_ALL)
        traceback.print_exc()
        sys.exit(1)
except requests.exceptions.ConnectTimeout:
    print(Fore.RED + 'Error: Timed out. The SoundCloud server may be down.' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)

print("client_id: " + client_id)
print("app_version: " + app_version)

if(json_result["kind"] == "track"):
    track_list = [json_result]
elif(json_result["kind"] == "playlist"):
    track_list = json_result["tracks"]
elif(json_result["kind"] == "user"):
    print("Downloading track list...")
    userid = str(json_result["id"])
    try:
        request_url = "https://api-v2.soundcloud.com/users/" + userid + "/tracks?representation=&client_id=" + client_id + "&limit=20&offset=0&linked_partitioning=1&app_version=" + app_version + "&app_locale=en"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(Fore.RED + 'Error: network error.' + Style.RESET_ALL)
        traceback.print_exc()
        sys.exit(1)
    except requests.exceptions.HTTPError:
        print(Fore.RED + 'Error: Status code error.' + Style.RESET_ALL)
        traceback.print_exc()
        sys.exit(1)
    except requests.exceptions.ConnectTimeout:
        print(Fore.RED + 'Error: Timed out. The SoundCloud server may be down.' + Style.RESET_ALL)
        traceback.print_exc()
        sys.exit(1)
    json_result_user = json.loads(r.text)
    track_list = json_result_user["collection"]
    while True:
        try:
            request_url = json_result_user["next_href"] + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
            r = requests.get(request_url, headers=requests_option, timeout=10)
            r.raise_for_status()
        except requests.exceptions.ConnectionError:
            print(Fore.RED + 'Error: network error.' + Style.RESET_ALL)
            traceback.print_exc()
            sys.exit(1)
        except requests.exceptions.HTTPError:
            print(Fore.RED + 'Error: Status code error.' + Style.RESET_ALL)
            traceback.print_exc()
            sys.exit(1)
        except requests.exceptions.ConnectTimeout:
            print(Fore.RED + 'Error: Timed out. The SoundCloud server may be down.' + Style.RESET_ALL)
            traceback.print_exc()
            sys.exit(1)
        json_result_user = json.loads(r.text)
        if(json_result_user["next_href"]):
            track_list = track_list + json_result_user["collection"]
        else:
            break
else:
    print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
    sys.exit(1)


for for_json in track_list:
    try:
        download_track(for_json, save_directory)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + 'Error: network error.' + Style.RESET_ALL)
        traceback.print_exc()
    except requests.exceptions.HTTPError:
        print(Fore.RED + 'Error: Status code error.' + Style.RESET_ALL)
        traceback.print_exc()
    except requests.exceptions.ConnectTimeout:
        print(Fore.RED + 'Error: Timed out. The SoundCloud server may be down.' + Style.RESET_ALL)
        traceback.print_exc()
