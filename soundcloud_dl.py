#from termcolor import colored, cprint
#import colorama
#colorama.init()

from colorama import init, Fore, Style
init()

#
#print(Fore.YELLOW + 'Warning: This program is pre-release and may be unstable.' + Style.RESET_ALL)
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

dir = os.path.dirname(sys.argv[0])




#client_id

#テスト用
#client_id = '00000000000000000000000000000000'

#有効期限がある
#client_id = '7z0rxinRI8F4NJnJYPokHFNqPSi0qraJ'

#こっちのほうが有効期限長いかも?
client_id = 'LBCcHmRB8XSStWL6wKH2HPACspQlXg2P'





userinput = input('url>>')

if("soundcloud.com" in urllib.parse.urlparse(userinput).netloc):
    pass
else:
    print(Fore.RED + 'Error: url is wrong' + Style.RESET_ALL)
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
    print(Fore.RED + 'Error: url is wrong' + Style.RESET_ALL)
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
    #app_version = '1586874666'
    #print("app_version(native): " + app_version)
    sys.exit(1)


#url_id to No.id
request_url = 'https://soundcloud.com/oembed?format=json&url=' + userinput
try:
    r = requests.get(request_url)
    Noid = re.search("tracks%2F(.*)&", json.loads(r.text)["html"]).group(1)
    print("Track ID: " + Noid)
except:
    print(Fore.RED + 'Error: url is wrong' + Style.RESET_ALL)
    #print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    #traceback.print_exc()
    #print('Error: url is wrong')
    sys.exit(1)


try:
    print("downloading...")
    
    request_url = 'https://api-v2.soundcloud.com/tracks?ids=' + Noid + '&client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
    r = requests.get(request_url)
    json2 = json.loads(r.text)
    if(json2[0]["downloadable"] and json2[0]["has_downloads_left"]):
        request_url = "https://api-v2.soundcloud.com/tracks/" + Noid + '/download?client_id=' + client_id + "&app_version=" + app_version + "&app_locale=en"
        r = requests.get(request_url)
        request_url = json.loads(r.text)["redirectUri"]
        res = requests.get(request_url,stream=True)
        if(res.headers["content-type"] == "audio/x-wav"):
            ctype = ".wav"
        elif(res.headers["content-type"] == "audio/mpeg"):
            ctype = ".mp3"
        else:
            print("format error")
            raise Exception
        pbar = tqdm(total=int(res.headers["content-length"]), unit="B", unit_scale=True)
        with open(Noid + ctype, 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()
    else:
        print(Fore.YELLOW + 'not free download' + Style.RESET_ALL)
        #print('not free download')
        request_url = json2[0]["media"]["transcodings"][1]["url"] + '?client_id=' + client_id
        r = requests.get(request_url)
        json3 = json.loads(r.text)
        url = json3["url"]
        request_url = url
        res = requests.get(request_url,stream=True)
        pbar = tqdm(total=int(res.headers["content-length"]), unit="B", unit_scale=True)
        with open(Noid + '.mp3', 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()
except:
    print(Fore.RED + 'Error: Unexpected error' + Style.RESET_ALL)
    traceback.print_exc()
    sys.exit(1)
