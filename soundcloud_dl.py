import sys
import json
import requests
import subprocess
import os
import urllib
import re
import traceback
import time
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

native_version = "7.0.0"
if(program_directory_path == os.getcwd()):
    if(not os.path.isdir("./downloads")):
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
    print("Getting latest client_id...")
    if(os.path.isfile(program_directory_path + "/client_id.json")):
        f = open(program_directory_path + "/client_id.json")
        data = f.read()
        f.close()
        data_json = json.loads(data)
        if(data_json["generated_version"] == native_version and data_json["expires"] > int(time.time())):
            return data_json["client_id"]
        else:
            pass
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    request_url = "https://soundcloud.com/"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    #by youtube-dl
    for src in reversed(re.findall(r'<script[^>]+src="([^"]+)"', r.content.decode())):
        print("Downloading JavaScript...")
        request_url = src
        r = requests.get(request_url, headers=requests_option, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        '''
        r = requests.get(request_url, headers=requests_option, stream=True, timeout=10)
        status_code = r.status_code
        r.raise_for_status()
        pbar = tqdm(unit="B", unit_scale=True)
        javascript_text = ""
        for chunk in r.iter_content(chunk_size=1024):
            javascript_text += chunk.decode()
            pbar.update(len(chunk))
        pbar.close()
        '''
        #javascript_text = r.content.decode()
        if(r.content.decode()):
            print("Parsing JavaScript...")
            #client_ids = re.findall(r'client_id\s*:\s*"([0-9a-zA-Z]{32})"',r.text)
            re_result = re.search(r'client_id\s*:\s*"([0-9a-zA-Z]{32})"', r.content.decode())
            if(re_result is not None):
                client_id = re_result.group(1)
                if(client_id):
                    f = open(program_directory_path + "/client_id.json", 'w')
                    f.write('{"client_id":"' + client_id + '","expires":' + str(int(time.time()) + 1209600)  + ',"generated_version":"' + native_version + '"}')
                    f.close()
                    return client_id
                else:
                    print(Fore.YELLOW + "Failed to get latest client_id" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Failed to get latest client_id" + Style.RESET_ALL)
    print("Getting client_id that may be old...")
    request_url = "https://inkuringu-ika.github.io/api/soundcloud-client_id.json"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    for for_json in json.loads(r.content.decode()):
        if(for_json["type"] == "pc_browser"):
            return for_json["client_id"]

def app_version():
    print("Getting latest app_version...")
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
    return r.content.decode()

def get_info(inputurl):
    global status_code
    print("Downloading trackinfo...")
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
    return json.loads(r.content.decode())

def download_user_track_list(user_id):
    page_count = 1
    print("Downloading track list " + str(page_count))
    request_url = "https://api-v2.soundcloud.com/users/" + user_id + "/tracks?client_id=" + client_id + "&limit=200&app_version=" + app_version + "&app_locale=en"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    r.raise_for_status()
    json_result_user = json.loads(r.content.decode())
    track_list = json_result_user["collection"]
    #May not work properly.
    while True:
        page_count = page_count + 1
        print("Downloading track list " + str(page_count))
        request_url = json_result_user["next_href"] + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        r.raise_for_status()
        json_result_user = json.loads(r.content.decode())
        if(json_result_user["next_href"]):
            track_list = track_list + json_result_user["collection"]
        else:
            break
    return track_list

def download_track(track_info, save_directory):
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    print("Downloading...")
    Noid = str(track_info["id"])
    print("Track ID: " + Noid)
    request_url = 'https://api-v2.soundcloud.com/tracks/' + Noid + '?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    track_info_2 = json.loads(r.content.decode())
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
        request_url = json.loads(r.content.decode())["redirectUri"]
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
            request_url = json.loads(r.content.decode())["url"]
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
            request_url = json.loads(r.content.decode())["url"]
            ffmpeg_path = program_directory_path + "\\ffmpeg.exe"
            if(os.path.isfile(ffmpeg_path)):
                print("ffmpeg_path: " + ffmpeg_path)
                subprocess.call([ffmpeg_path,"-y","-i",request_url,"-c","copy",save_directory + "/" + filename])
            else:
                #print(Fore.YELLOW + "FFmpeg is required to download this audio." + Style.RESET_ALL)
                print(Fore.YELLOW + "Download using the built-in hls downloader. Use ffmpeg if it does not download properly." + Style.RESET_ALL)
                r = requests.get(request_url)
                file = open(save_directory + "/" + filename,mode="wb")
                for for_data in r.content.decode().split("\n"):
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

print("client_id: " + client_id)
print("app_version: " + app_version)

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

if(json_result["kind"] == "track"):
    track_list = [json_result]
elif(json_result["kind"] == "playlist"):
    track_list = json_result["tracks"]
elif(json_result["kind"] == "user"):
    user_id = str(json_result["id"])
    try:
        track_list = download_user_track_list(user_id)
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
else:
    print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
    sys.exit(1)

print("Track count: " + str(len(track_list)))

for for_json in track_list:
    while True:
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
        else:
            break
        result = input('Enter "r" to retry. Enter "c" to continue downloading. Enter nothing to exit. : ')
        if(result == "r"):
            pass
        elif(result == "c"):
            break
        else:
            sys.exit(1)
