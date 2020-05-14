#
print('Copyright (c) 2020 inkuringu-ika')
print('This software is released under the GPL3.0 License, see LICENSE file.')
#
import sys

try:
    if(sys.argv[1] == "-U"):
        #print("Checking for updates...")
        #print("Failed to check for updates.")
        #print
        input()
        sys.exit(1)
except KeyboardInterrupt:
    sys.exit(0)
except:
    pass

from colorama import init, Fore, Style
init()
import os
import requests
import urllib
import json
import re
import traceback
from tqdm import tqdm

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
            request_url = json2[0]["media"]["transcodings"][1]["url"] + '?client_id=' + client_id
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
