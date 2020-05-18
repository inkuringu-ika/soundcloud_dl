#
print('Copyright (c) 2020 inkuringu-ika')
#print('This software is released under the GPL3.0 License, see LICENSE file.')
print('This software is released under the "GNU GENERAL PUBLIC LICENSE Version 3", see LICENSE file.')
#
import sys
import json
import requests
import subprocess
import os
import urllib
import re
import traceback
from tqdm import tqdm
from colorama import init, Fore, Style
init()
if getattr(sys, 'frozen', False):
    program_directory_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory_path = os.path.dirname(os.path.abspath(__file__))

native_version = "4.0.0"

if(len(sys.argv) >= 2):
    argv = sys.argv[1]
    if(argv == "-C"):
        print()
        print()
        print('soundcloud_dl: Copyright (c) 2020 inkuringu-ika    GNU GENERAL PUBLIC LICENSE Version 3')
        print('Colorama: Copyright (c) 2010 Jonathan Hartley    BSD 3-Clause "New" or "Revised" License')
        print('Requests: Copyright (c) 2019 Kenneth Reitz    Apache License Version 2.0')
        print('tqdm: Copyright (c) 2013 noamraph    MIT License , Mozilla Public Licence v2.0')
        sys.exit(0)
    if(argv == "-U"):
        print()
        print()
        print("Checking for updates...")
        try:
            r = requests.get("https://api.github.com/repos/inkuringu-ika/soundcloud_dl/releases/latest")
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print(Fore.RED + "Failed to check for updates." + Style.RESET_ALL)
            sys.exit(1)
        latest_version = json.loads(r.text)["tag_name"][1:]
        print("native_version: " + native_version)
        print("latest_version: " + latest_version)
        native_version_if = float(native_version.split(".")[0] + "." + ''.join(native_version.split(".")[1:]))
        latest_version_if = float(latest_version.split(".")[0] + "." + ''.join(latest_version.split(".")[1:]))
        if(native_version_if < latest_version_if):
            print("Updates found!")
            print("downloading... (Please wait until soundcloud_dl starts automatically.)")
            url = json.loads(r.text)["assets"][0]["browser_download_url"]
            #subprocess.Popen('curl -o tmp.bin -L "' + url + '" > && del soundcloud_dl.exe && ren tmp.bin soundcloud_dl.exe', shell=True, cwd=dir)
            subprocess.Popen('powershell "($WebClient = New-Object System.Net.WebClient).DownloadFile(\'' + url + '\', \'tmp.bin\')" && del soundcloud_dl.exe && ren tmp.bin soundcloud_dl.exe && echo Successful update && start soundcloud_dl.exe', shell=True, cwd=program_directory_path)
            sys.exit(0)
        else:
            print("No updates found.")
            sys.exit(0)
    if(argv == "-V"):
        print()
        print()
        print("Version " + native_version)
        sys.exit(0)
    if(argv == "--ffmpeg-download"):
        print()
        print()
        print("Downloading list...")
        import zipfile
        import shutil
        request_url = "https://inkuringu-ika.github.io/api/soundcloud_dl-ffmpeg-download-url.json"
        try:
            r = requests.get(request_url, stream=True, timeout=10)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
            traceback.print_exc()
            sys.exit(1)
        print("Downloading ffmpeg...")
        request_url = json.loads(r.text)["url"]
        filepath = program_directory_path + "\\" + json.loads(r.text)["filename"] + ".zip"
        filename = json.loads(r.text)["filename"]
        try:
            r = requests.get(request_url, stream=True, timeout=10)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
            traceback.print_exc()
            sys.exit(1)
        pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
        with open(filepath, 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()
        with zipfile.ZipFile(filepath) as open_zip:
            open_zip.extract(filename + "/bin/ffmpeg.exe", program_directory_path)
        try:
            os.remove(program_directory_path + "\\ffmpeg.exe")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            pass
        shutil.move(program_directory_path + "\\" + filename + "\\bin\\ffmpeg.exe", program_directory_path + "\\")
        os.remove(filepath)
        shutil.rmtree(program_directory_path + "\\" + filename + "\\")
        sys.exit(0)

class Exit(Exception):
    pass

#for test
#client_id = '00000000000000000000000000000000'

#browser
#client_id = 'oFMSnVZoxS9WWBM4SpSI6t67QeJOKGvd'
#client_id = '7z0rxinRI8F4NJnJYPokHFNqPSi0qraJ'
#client_id = 'PANENeeumEFxeUKuTj575zguSBQI5DwE'

#ios app
#client_id = 'iZIs9mchVcX5lhVRyQGGAYlNPVldzAoX'

#widget
client_id = 'LBCcHmRB8XSStWL6wKH2HPACspQlXg2P'


userinput = input('url>>')

inputurl = userinput

try:
    if(urllib.parse.urlparse(userinput).netloc == "soundcloud.com"):
        pass
    elif(urllib.parse.urlparse(userinput).netloc == "m.soundcloud.com"):
        inputurl_parse = urllib.parse.urlparse(inputurl)
        inputurl = urllib.parse.ParseResult(inputurl_parse.scheme, "soundcloud.com", inputurl_parse.path, inputurl_parse.params, inputurl_parse.query, inputurl_parse.fragment).geturl()
    elif("soundcloud.com" in urllib.parse.urlparse(userinput).netloc):
        print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
        raise Exit
    else:
        print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
        raise Exit
    try:
        request_url = inputurl
        r = requests.get(request_url, timeout=10)
        r.raise_for_status()
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except requests.RequestException:
        print("status_code:" + str(r.status_code))
        print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
        raise Exit
    except:
        print(Fore.RED + 'Error: Connection error' + Style.RESET_ALL)
        traceback.print_exc()
        raise Exit
    
    try:
        json_result = json.loads(re.search('e.data.forEach\(function\(e\){n\(e\)}\)}catch\(t\){}}\)},(.*)\);', r.text).group(1))[-1]
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
        traceback.print_exc()
        raise Exit
    
    #app_version
    try:
        #https://soundcloud.com/version.txt
        #request_url = "https://soundcloud.com/"
        app_version = re.search('window.__sc_version = "(.*)";</script>', r.text).group(1)
        print("app_version: " + app_version)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
        traceback.print_exc()
        raise Exit
    
    if(json_result["data"][0]["kind"] == "track"):
        json_result_split = json_result["data"]
    elif(json_result["data"][0]["kind"] == "playlist"):
        json_result_split = json_result["data"][0]["tracks"]
    elif(json_result["data"][0]["kind"] == "user"):
        userid = str(json_result["data"][0]["id"])
        request_url = "https://api-v2.soundcloud.com/users/" + userid + "/tracks?representation=&client_id=" + client_id + "&limit=20&offset=0&linked_partitioning=1&app_version=" + app_version + "&app_locale=en"
        try:
            r = requests.get(request_url, timeout=10)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
            traceback.print_exc()
            raise Exit
        json1 = json.loads(r.text)
        json_result_split = json1["collection"]
        while True:
            request_url = json1["next_href"] + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
            try:
                r = requests.get(request_url, timeout=10)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                raise Exit
            json1 = json.loads(r.text)
            if(json1["next_href"]):
                json_result_split = json_result_split + json1["collection"]
            else:
                break
    else:
        print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
        raise Exit
except Exit:
    sys.exit(1)
except KeyboardInterrupt:
    sys.exit(0)
except:
    print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)


for json_result_split_onedata in json_result_split:
    try:
        print("downloading...")
        if(json_result_split_onedata["streamable"]):
            pass
        else:
            print(Fore.YELLOW + "Stream unable!" + Style.RESET_ALL)
            raise Exit
        Noid = str(json_result_split_onedata["id"])
        print("Track ID: " + Noid)
        request_url = 'https://api-v2.soundcloud.com/tracks?ids=' + Noid + '&client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
        try:
            r = requests.get(request_url, timeout=10)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
            traceback.print_exc()
            raise Exit
        json2 = json.loads(r.text)
        if(json2[0]["downloadable"] and json2[0]["has_downloads_left"]):
            request_url = "https://api-v2.soundcloud.com/tracks/" + Noid + '/download?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
            try:
                r = requests.get(request_url, timeout=10)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                raise Exit
            request_url = json.loads(r.text)["redirectUri"]
            try:
                r = requests.get(request_url, stream=True, timeout=10)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                raise Exit
            filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\|]',"_",json2[0]["title"] + "." + r.headers["content-disposition"][r.headers["content-disposition"].find("filename=") + len("filename="):].replace('"',"").split(".")[-1])
            pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
            with open(filename, 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024):
                    file.write(chunk)
                    pbar.update(len(chunk))
                pbar.close()
        else:
            print(Fore.YELLOW + 'Not a free download!' + Style.RESET_ALL)
            filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\|]',"_",json2[0]["title"] + ".mp3")
            for transcoding in json2[0]["media"]["transcodings"]:
                if(transcoding["format"]["protocol"] == "progressive"):
                    request_url = transcoding["url"] + '?client_id=' + client_id
                    break
                else:
                    request_url = "null"
            if(request_url == "null"):
                request_url = json2[0]["media"]["transcodings"][0]["url"] + '?client_id=' + client_id
                try:
                    r = requests.get(request_url, timeout=10)
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                    traceback.print_exc()
                    raise Exit
                request_url = json.loads(r.text)["url"]
                ffmpeg_path = program_directory_path + "\\ffmpeg.exe"
                if(os.path.isfile(ffmpeg_path)):
                    print("ffmpeg_path: " + ffmpeg_path)
                    subprocess.call([ffmpeg_path,"-y","-i",request_url,"-c","copy",filename])
                else:
                    print(Fore.YELLOW + "FFmpeg is required to download this audio." + Style.RESET_ALL)
                    print(Fore.YELLOW + "Download FFmpeg using the --ffmpeg-download option." + Style.RESET_ALL)
                    raise Exit
            else:
                #request_url = json2[0]["media"]["transcodings"][1]["url"]
                try:
                    r = requests.get(request_url, timeout=10)
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                    traceback.print_exc()
                    raise Exit
                url = json.loads(r.text)["url"]
                request_url = url
                try:
                    r = requests.get(request_url, stream=True, timeout=10)
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                    traceback.print_exc()
                    raise Exit
                pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
                with open(filename, 'wb') as file:
                    for chunk in r.iter_content(chunk_size=1024):
                        file.write(chunk)
                        pbar.update(len(chunk))
                    pbar.close()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exit:
        pass
    except:
        print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
        traceback.print_exc()
