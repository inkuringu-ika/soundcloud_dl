try:
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
    #
    print('Copyright (c) 2020 inkuringu-ika')
    print('This software is released under the "GNU GENERAL PUBLIC LICENSE Version 3", see LICENSE file.')
    print()
    #
    native_version = "5.2.0"
    
    if(len(sys.argv) >= 2):
        argv = sys.argv[1]
        if(argv == "-h" or argv == "--help"):
            print("soundcloud_dl.py [option]")
            print("soundcloud_dl.exe [option]")
            print("-h,--help: Show usage")
            print("-C,--copyright: Show copyright")
            print("-V,--version: Show version")
            print("-U,--update: Update (Experimental option)")
            print("--ffmpeg-download: Download ffmpeg")
            os._exit(0)
        if(argv == "-C" or argv == "--copyright"):
            print('soundcloud_dl: Copyright (c) 2020 inkuringu-ika    GNU GENERAL PUBLIC LICENSE Version 3')
            print('Colorama: Copyright (c) 2010 Jonathan Hartley    BSD 3-Clause "New" or "Revised" License')
            print('Requests: Copyright (c) 2019 Kenneth Reitz    Apache License Version 2.0')
            print('tqdm: Copyright (c) 2013 noamraph    MIT License , Mozilla Public Licence v2.0')
            os._exit(0)
        if(argv == "-U" or argv == "--update"):
            print("Checking for updates...")
            try:
                r = requests.get("https://api.github.com/repos/inkuringu-ika/soundcloud_dl/releases/latest")
                r.raise_for_status()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except requests.RequestException:
                print("status_code:" + str(r.status_code))
                print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                os._exit(1)
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                print(Fore.RED + "Failed to check for updates." + Style.RESET_ALL)
                os._exit(1)
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
                os._exit(0)
            else:
                print("No updates found.")
                os._exit(0)
        if(argv == "-V" or argv == "--version"):
            print("Version " + native_version)
            os._exit(0)
        if(argv == "--ffmpeg-download"):
            print("Downloading list...")
            import zipfile
            import shutil
            request_url = "https://inkuringu-ika.github.io/api/soundcloud_dl-ffmpeg-download-url.json"
            try:
                r = requests.get(request_url, stream=True, timeout=10)
                r.raise_for_status()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except requests.RequestException:
                print("status_code:" + str(r.status_code))
                print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                os._exit(1)
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                os._exit(1)
            print("Downloading ffmpeg...")
            request_url = json.loads(r.text)["url"]
            filepath = program_directory_path + "\\" + json.loads(r.text)["filename"] + ".zip"
            filename = json.loads(r.text)["filename"]
            try:
                r = requests.get(request_url, stream=True, timeout=10)
                r.raise_for_status()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except requests.RequestException:
                print("status_code:" + str(r.status_code))
                print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                os._exit(1)
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                os._exit(1)
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
            print("Successful update")
            os._exit(0)
    
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
    
    if(urllib.parse.urlparse(userinput).netloc == "soundcloud.com"):
        pass
    elif(urllib.parse.urlparse(userinput).netloc == "m.soundcloud.com"):
        inputurl_parse = urllib.parse.urlparse(inputurl)
        inputurl = urllib.parse.ParseResult(inputurl_parse.scheme, "soundcloud.com", inputurl_parse.path, inputurl_parse.params, inputurl_parse.query, inputurl_parse.fragment).geturl()
    elif("soundcloud.com" in urllib.parse.urlparse(userinput).netloc):
        print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
        os._exit(1)
    else:
        print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
        os._exit(1)
    
    #app_version
    try:
        request_url = "https://soundcloud.com/version.txt"
        r = requests.get(request_url, timeout=10)
        r.raise_for_status()
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except requests.RequestException:
        print("status_code:" + str(r.status_code))
        print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
        os._exit(1)
    except:
        print(Fore.RED + 'Error: Connection error' + Style.RESET_ALL)
        traceback.print_exc()
        os._exit(1)
    app_version = r.text
    
    #get meta
    request_url = "https://api-v2.soundcloud.com/resolve?url=" + inputurl + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
    try:
        r = requests.get(request_url, timeout=10)
        r.raise_for_status()
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except requests.RequestException:
        print("status_code:" + str(r.status_code))
        print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
        os._exit(1)
    except:
        print(Fore.RED + 'Error: Connection error' + Style.RESET_ALL)
        traceback.print_exc()
        os._exit(1)
    json_result = json.loads(r.text)
    
    if(json_result["kind"] == "track"):
        json_result_split = [json_result]
    elif(json_result["kind"] == "playlist"):
        json_result_split = json_result["tracks"]
    elif(json_result["kind"] == "user"):
        userid = str(json_result["id"])
        request_url = "https://api-v2.soundcloud.com/users/" + userid + "/tracks?representation=&client_id=" + client_id + "&limit=20&offset=0&linked_partitioning=1&app_version=" + app_version + "&app_locale=en"
        try:
            r = requests.get(request_url, timeout=10)
            r.raise_for_status()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except requests.RequestException:
            print("status_code:" + str(r.status_code))
            print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
            os._exit(1)
        except:
            print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
            traceback.print_exc()
            os._exit(1)
        json_result_user = json.loads(r.text)
        json_result_split = json_result_user["collection"]
        while True:
            request_url = json_result_user["next_href"] + "&client_id=" + client_id + "&app_version=" + app_version + "&app_locale=en"
            try:
                r = requests.get(request_url, timeout=10)
                r.raise_for_status()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except requests.RequestException:
                print("status_code:" + str(r.status_code))
                print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                os._exit(1)
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                os._exit(1)
            json_result_user = json.loads(r.text)
            if(json_result_user["next_href"]):
                json_result_split = json_result_split + json_result_user["collection"]
            else:
                break
    else:
        print(Fore.YELLOW + 'Error: Unsupported url' + Style.RESET_ALL)
        os._exit(1)

    class skip(Exception):
        pass
    for json_result_split_onedata in json_result_split:
        try:
            print("downloading...")
            Noid = str(json_result_split_onedata["id"])
            print("Track ID: " + Noid)
            request_url = 'https://api-v2.soundcloud.com/tracks/' + Noid + '?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
            try:
                r = requests.get(request_url, timeout=10)
                r.raise_for_status()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except requests.RequestException:
                print("status_code:" + str(r.status_code))
                print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                raise skip
            except:
                print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                traceback.print_exc()
                raise skip
            json_result_track_meta = json.loads(r.text)
            if(json_result_track_meta["streamable"]):
                pass
            else:
                print(Fore.YELLOW + "Stream unable!" + Style.RESET_ALL)
                raise skip
            if(json_result_track_meta["downloadable"] and json_result_track_meta["has_downloads_left"]):
                request_url = "https://api-v2.soundcloud.com/tracks/" + Noid + '/download?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
                try:
                    r = requests.get(request_url, timeout=10)
                    r.raise_for_status()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except requests.RequestException:
                    print("status_code:" + str(r.status_code))
                    print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                    raise skip
                except:
                    print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                    traceback.print_exc()
                    raise skip
                request_url = json.loads(r.text)["redirectUri"]
                try:
                    r = requests.get(request_url, stream=True, timeout=10)
                    r.raise_for_status()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except requests.RequestException:
                    print("status_code:" + str(r.status_code))
                    print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                    raise skip
                except:
                    print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                    traceback.print_exc()
                    raise skip
                filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\|]',"_",json_result_track_meta["title"] + "." + r.headers["content-disposition"][r.headers["content-disposition"].find("filename=") + len("filename="):].replace('"',"").split(".")[-1])
                pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
                with open(filename, 'wb') as file:
                    for chunk in r.iter_content(chunk_size=1024):
                        file.write(chunk)
                        pbar.update(len(chunk))
                    pbar.close()
            else:
                print(Fore.YELLOW + 'Not a free download!' + Style.RESET_ALL)
                filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\|]',"_",json_result_track_meta["title"] + ".mp3")
                hls_active = 0
                progressive_active = 0
                format_for_count = 0
                for transcoding in json_result_track_meta["media"]["transcodings"]:
                    if(transcoding["format"]["protocol"] == "hls" and transcoding["format"]["mime_type"] == "audio/mpeg"):
                        hls_active = 1
                        hls_active_count = format_for_count
                    elif(transcoding["format"]["protocol"] == "progressive" and transcoding["format"]["mime_type"] == "audio/mpeg"):
                        progressive_active = 1
                        progressive_active_count = format_for_count
                    format_for_count = format_for_count + 1
                if(progressive_active == 1):
                    request_url = json_result_track_meta["media"]["transcodings"][progressive_active_count]["url"] + '?client_id=' + client_id
                    try:
                        r = requests.get(request_url, timeout=10)
                        r.raise_for_status()
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except requests.RequestException:
                        print("status_code:" + str(r.status_code))
                        print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                        raise skip
                    except:
                        print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                        traceback.print_exc()
                        raise skip
                    url = json.loads(r.text)["url"]
                    request_url = url
                    try:
                        r = requests.get(request_url, stream=True, timeout=10)
                        r.raise_for_status()
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except requests.RequestException:
                        print("status_code:" + str(r.status_code))
                        print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                        raise skip
                    except:
                        print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                        traceback.print_exc()
                        raise skip
                    pbar = tqdm(total=int(r.headers["content-length"]), unit="B", unit_scale=True)
                    with open(filename, 'wb') as file:
                        for chunk in r.iter_content(chunk_size=1024):
                            file.write(chunk)
                            pbar.update(len(chunk))
                        pbar.close()
                elif(hls_active == 1):
                    request_url = json_result_track_meta["media"]["transcodings"][hls_active_count]["url"] + '?client_id=' + client_id
                    try:
                        r = requests.get(request_url, timeout=10)
                        r.raise_for_status()
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except requests.RequestException:
                        print("status_code:" + str(r.status_code))
                        print(Fore.RED + 'Error: status code error' + Style.RESET_ALL)
                        raise skip
                    except:
                        print(Fore.RED + "Error: Connection error" + Style.RESET_ALL)
                        traceback.print_exc()
                        raise skip
                    request_url = json.loads(r.text)["url"]
                    ffmpeg_path = program_directory_path + "\\ffmpeg.exe"
                    if(os.path.isfile(ffmpeg_path)):
                        print("ffmpeg_path: " + ffmpeg_path)
                        subprocess.call([ffmpeg_path,"-y","-i",request_url,"-c","copy",filename])
                    else:
                        print(Fore.YELLOW + "FFmpeg is required to download this audio." + Style.RESET_ALL)
                        print(Fore.YELLOW + "Download FFmpeg using the --ffmpeg-download option." + Style.RESET_ALL)
                        raise skip
                else:
                    print(Fore.YELLOW + "Error: Not supported type" + Style.RESET_ALL)
                    raise skip
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except skip:
            pass
        except:
            print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
            traceback.print_exc()
except KeyboardInterrupt:
    print()
    print("KeyboardInterrupt")
    import os
    os._exit(0)
except:
    print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    import traceback
    traceback.print_exc()
    import os
    os._exit(1)
