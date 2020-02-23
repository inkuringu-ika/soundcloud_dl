from termcolor import colored, cprint
import colorama
colorama.init()

#
cprint('Warning: This program is pre-release and may be unstable.', 'yellow')
print('Copyright (c) 2020 inkuringu-ika')
print('This software is released under the GPL3.0 License, see LICENSE file.')
#

import os
import requests
import json
import re
import sys
from tqdm import tqdm

dir = os.path.dirname(sys.argv[0])




#client_id

#テスト用
#client_id = '00000000000000000000000000000000'

#有効期限がある
#client_id = 'qWUPqUOvYPTG1SDjwXJCNm9gOwM3rNeP'

#こっちのほうが有効期限長いかも?
client_id = 'LBCcHmRB8XSStWL6wKH2HPACspQlXg2P'




userinput = input('url>>')


#url_id to No.id
request_url = 'https://soundcloud.com/oembed?format=json&url=' + userinput
try:
    r = requests.get(request_url)
    json1 = json.loads(r.text)
except:
    cprint('Error: url is wrong', 'red')
    #print('Error: url is wrong')
    sys.exit(1)

try:
    Noid_html = json1["html"]
    research = "tracks%2F(.*)&"
    resultresearch = re.search(research, Noid_html)
    Noid = resultresearch.group(1)
    print(Noid)
    
    print("downloading...")
    
    request_url = 'https://api-v2.soundcloud.com/tracks?ids=' + Noid + '&client_id=' + client_id
    r = requests.get(request_url)
    json2 = json.loads(r.text)
    if(json2[0]["downloadable"] and json2[0]["has_downloads_left"]):
        request_url = json2[0]["download_url"] + '?client_id=' + client_id
        res = requests.get(request_url,stream=True)
        pbar = tqdm(total=int(res.headers["content-length"]), unit="B", unit_scale=True)
        with open(Noid + '.mp3', 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()
    else:
        cprint('not free download', 'yellow')
        #print('not free download')
        request_url = json2[0]["media"]["transcodings"][1]["url"] + '?client_id=' + client_id
        r = requests.get(request_url)
        json3 = json.loads(r.text)
        url = json3["url"]
        request_url = url
        res = requests.get(request_url)
        pbar = tqdm(total=int(res.headers["content-length"]), unit="B", unit_scale=True)
        with open(Noid + '.mp3', 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))
            pbar.close()
except:
    cprint('Error: Unexpected error', 'red')
    sys.exit(1)
