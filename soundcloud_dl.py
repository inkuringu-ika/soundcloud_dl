from colorama import init, Fore, Style
init()

#
print('Copyright (c) 2020 inkuringu-ika')
print('This software is released under the GPL3.0 License, see LICENSE file.')
#

import os
import requests
import urllib
import json
import re
import sys
import traceback
from tqdm import tqdm


client_id = 'LBCcHmRB8XSStWL6wKH2HPACspQlXg2P'


userinput = input('url>>')

if("soundcloud.com" in urllib.parse.urlparse(userinput).netloc):
    pass
else:
    print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
    sys.exit(1)
try:
    request_url = userinput
    r = requests.get(request_url)
except:
    print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
if(r.status_code == requests.codes.ok):
    pass
else:
    print("status_code:" + r.status_code)
    print(Fore.RED + 'Error: Url is wrong' + Style.RESET_ALL)
    sys.exit(1)

try:
    json_result = json.loads(re.search('e.data.forEach\(function\(e\){n\(e\)}\)}catch\(t\){}}\)},(.*)\);', r.text).group(1))[5]
except:
    print(Fore.RED + 'Error: Error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)

#app_version
try:
    #https://soundcloud.com/version.txt
    #request_url = "https://soundcloud.com/"
    app_version = re.search('window.__sc_version = "(.*)";</script>', r.text).group(1)
    print("app_version: " + app_version)
except:
    print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)



if(json_result["data"][0]["kind"] == "track"):
    json_result_split = json_result["data"]
elif(json_result["data"][0]["kind"] == "playlist"):
    json_result_split = json_result["data"][0]["tracks"]
else:
    print(Fore.RED + 'Error: Error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)


try:
    for json_result_split_onedata in json_result_split:
        try:
            print("downloading...")
            Noid = str(json_result_split_onedata["id"])
            print("Track ID: " + Noid)
            request_url = 'https://api-v2.soundcloud.com/tracks?ids=' + Noid + '&client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
            r = requests.get(request_url)
            json2 = json.loads(r.text)
            if(json2[0]["downloadable"] and json2[0]["has_downloads_left"]):
                request_url = "https://api-v2.soundcloud.com/tracks/" + Noid + '/download?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
                r = requests.get(request_url)
                request_url = json.loads(r.text)["redirectUri"]
                res = requests.get(request_url,stream=True)
                filename = res.headers["content-disposition"][res.headers["content-disposition"].find("filename=") + len("filename="):].replace('"',"")
                pbar = tqdm(total=int(res.headers["content-length"]), unit="B", unit_scale=True)
                with open(filename, 'wb') as file:
                    for chunk in res.iter_content(chunk_size=1024):
                        file.write(chunk)
                        pbar.update(len(chunk))
                    pbar.close()
            else:
                print(Fore.YELLOW + 'Not a free download!' + Style.RESET_ALL)
                #print('not free download')
                filename = re.sub(r'[\\|/|:|\*|?|"|<|>|\|]',"_",json2[0]["title"] + ".mp3")
                request_url = json2[0]["media"]["transcodings"][1]["url"] + '?client_id=' + client_id
                r = requests.get(request_url)
                url = json.loads(r.text)["url"]
                request_url = url
                res = requests.get(request_url,stream=True)
                pbar = tqdm(total=int(res.headers["content-length"]), unit="B", unit_scale=True)
                with open(filename, 'wb') as file:
                    for chunk in res.iter_content(chunk_size=1024):
                        file.write(chunk)
                        pbar.update(len(chunk))
                    pbar.close()
        except:
            print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
            traceback.print_exc()
except:
    print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
