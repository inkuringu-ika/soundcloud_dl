import sys
import json
import requests
import subprocess
import os
import urllib
import re
import traceback
import platform
import time
from distutils.version import StrictVersion
from tqdm import tqdm
from colorama import init, Fore, Style
init()
if getattr(sys, 'frozen', False):
    program_directory_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory_path = os.path.dirname(os.path.abspath(__file__))
os_name = platform.system()

print('Copyright (c) 2020 inkuringu-ika')
print('This software is released under the "GNU GENERAL PUBLIC LICENSE Version 3", see LICENSE file.')
print()

native_version = "7.1.1"
update_test = False

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
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
}

def client_id(force_update=False):
    print("Getting latest client_id...")
    if(os.path.isfile(program_directory_path + "/client_id.json") and not force_update):
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
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    request_url = "https://soundcloud.com/"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    status_code = r.status_code
    r.raise_for_status()
    for src in reversed(re.findall(r'<script[^>]+src="([^"]+)"', r.content.decode())):
        print("Downloading JavaScript...")
        request_url = src
        r = requests.get(request_url, headers=requests_option, timeout=10)
        r.raise_for_status()
        if(r.content.decode()):
            print("Parsing JavaScript...")
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
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    request_url = "https://soundcloud.com/version.txt"
    r = requests.get(request_url, headers=requests_option, timeout=10)
    r.raise_for_status()
    return r.content.decode()

def get_info(inputurl):
    print("Downloading trackinfo...")
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    request_url = "https://api-v2.soundcloud.com/resolve?url=" + inputurl + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
    r = requests.get(request_url, headers=requests_option, timeout=10)
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

def download_track(track_info, kind, save_directory):
    requests_option = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    print("Downloading...")
    Noid = str(track_info["id"])
    print("Track ID: " + Noid)
    if(kind == "playlist"):
        request_url = 'https://api-v2.soundcloud.com/tracks/' + Noid + '?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        r.raise_for_status()
        track_info_2 = json.loads(r.content.decode())
    else:
        track_info_2 = track_info
    if(not track_info_2["streamable"]):
        print(Fore.YELLOW + "Stream is not available." + Style.RESET_ALL)
        return
    if(track_info_2["policy"] == "BLOCK"):
        print(Fore.YELLOW + "The download of this track is blocked in your country." + Style.RESET_ALL)
        return
    elif(track_info_2["policy"] == "SNIP"):
        print(Fore.YELLOW + "The download of this track is restricted. Only 30-second preview is available for download." + Style.RESET_ALL)
    if(track_info_2["downloadable"] and track_info_2["has_downloads_left"]):
        request_url = "https://api-v2.soundcloud.com/tracks/" + Noid + '/download?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
        r = requests.get(request_url, headers=requests_option, timeout=10)
        r.raise_for_status()
        request_url = json.loads(r.content.decode())["redirectUri"]
        r = requests.get(request_url, headers=requests_option, stream=True, timeout=10)
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
        filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\||\n]',"_",track_info_2["title"] + ".mp3")
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
            r.raise_for_status()
            request_url = json.loads(r.content.decode())["url"]
            r = requests.get(request_url, headers=requests_option, stream=True, timeout=10)
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
            r.raise_for_status()
            request_url = json.loads(r.content.decode())["url"]
            ffmpeg_path = program_directory_path + "/ffmpeg.exe"
            if(os.path.isfile(ffmpeg_path)):
                print("ffmpeg_path: " + ffmpeg_path)
                subprocess.call([ffmpeg_path,"-y","-i",request_url,"-c","copy",save_directory + "/" + filename])
            else:
                print(Fore.YELLOW + "Download using the built-in hls downloader. Use ffmpeg if it does not download properly." + Style.RESET_ALL)
                r = requests.get(request_url)
                file = open(save_directory + "/" + filename,mode="wb")
                for for_data in r.content.decode().split("\n"):
                    if(not for_data[0] == "#"):
                        print("Downloading segment...")
                        r = requests.get(for_data, headers=requests_option, timeout=10)
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
            print("-c,--copyright: Show copyright")
            print("-v,--version: Show version")
            print("-U,--update: Update")
            print("-CU,--client_id-update: Force client_id update")
            sys.exit(0)
        elif(argv == "-c" or argv == "--copyright"):
            print('soundcloud_dl: Copyright (c) 2020 inkuringu-ika\n               GNU GENERAL PUBLIC LICENSE Version 3')
            print()
            print('Python: Copyright (c) 2001-2020 Python Software Foundation\n        Python Software Foundation License')
            print()
            print('FFmpeg: Copyright (c) 2000-2020 the FFmpeg developers\n        GNU GENERAL PUBLIC LICENSE Version 3')
            print()
            print('Colorama: Copyright (c) 2010 Jonathan Hartley\n          BSD 3-Clause "New" or "Revised" License')
            print()
            print('Requests: Copyright (c) 2019 Kenneth Reitz\n          Apache License Version 2.0')
            print()
            print('tqdm: Copyright: Copyright (c) 2013 noamraph\n      Copyright (c) 2015-2020 Casper da Costa-Luis\n      Copyright (c) 2016 [PR #96] on behalf of Google Inc\n      Copyright (c) 2013 Noam Yorav-Raphael\n      [PR #96]: https://github.com/tqdm/tqdm/pull/96\n      MIT License , Mozilla Public Licence v2.0')
            sys.exit(0)
        elif(argv == "-v" or argv == "--version"):
            print("Version " + native_version)
            sys.exit(0)
        elif(argv == "-U" or argv == "--update"):
            if(os_name == "Windows"):
                if(getattr(sys, 'frozen', False) or update_test):
                    print("Checking for updates...")
                    r = requests.get("https://inkuringu-ika.github.io/soundcloud_dl/versions.json")
                    r.raise_for_status()
                    json_result = json.loads(r.content.decode())
                    if(not StrictVersion(json_result["minimum_version_available"]) > StrictVersion(native_version)):
                        for for_data in json_result["versions"]:
                            if(for_data["available"]):
                                latest_version = for_data["version"]
                                latest_download_url = for_data["download_url"]
                                break
                        if(StrictVersion(latest_version) > StrictVersion(native_version) or update_test):
                            print("Updates found!")
                            print(native_version + " -> " + latest_version)
                            request_url = latest_download_url
                            r = requests.get(request_url, headers=requests_option, stream=True, timeout=10)
                            r.raise_for_status()
                            pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
                            with open(program_directory_path + "/" + "soundcloud_dl_latest_tmp.bin", 'wb') as file:
                                for chunk in r.iter_content(chunk_size=1024):
                                    file.write(chunk)
                                    pbar.update(len(chunk))
                                pbar.close()
                            print("Updating... (Please wait.)")
                            subprocess.Popen('echo Waiting for the program to exit... && ping 127.0.0.1 -n 5 -w 1000 > nul && echo Updating... && del soundcloud_dl.exe > nul && ren soundcloud_dl_latest_tmp.bin soundcloud_dl.exe > nul && echo Successful update', shell=True, cwd=program_directory_path)
                            sys.exit(0)
                        else:
                            print("No updates found.")
                            sys.exit(0)
                    else:
                        print(Fore.YELLOW + "Update found but must be done manually." + Style.RESET_ALL)
                        print("Please download from here.")
                        print("https://github.com/inkuringu-ika/soundcloud_dl/releases")
                        sys.exit(0)
                else:
                    print(Fore.YELLOW + "This option is only available in the exe version." + Style.RESET_ALL)
                    sys.exit(0)
            else:
                print(Fore.YELLOW + "The update function is currently only available on Windows." + Style.RESET_ALL)
                sys.exit(0)
        elif(argv == "-CU" or argv == "--client_id-update"):
            client_id(True)
            sys.exit(0)
        else:
            userinput = argv
else:
    userinput = input('url>>')


client_id = client_id()

app_version = app_version()

print("client_id: " + client_id)
print("app_version: " + app_version)

json_result = get_info(userinput)

kind = json_result["kind"]
if(kind == "track"):
    track_list = [json_result]
elif(kind == "playlist"):
    track_list = json_result["tracks"]
elif(kind == "user"):
    user_id = str(json_result["id"])
    track_list = download_user_track_list(user_id)
else:
    print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
    sys.exit(1)

print("Track count: " + str(len(track_list)))

for for_json in track_list:
    while True:
        try:
            download_track(for_json, kind, save_directory)
        except requests.exceptions.ConnectionError:
            traceback.print_exc()
        except requests.exceptions.HTTPError:
            traceback.print_exc()
        except requests.exceptions.ConnectTimeout:
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
