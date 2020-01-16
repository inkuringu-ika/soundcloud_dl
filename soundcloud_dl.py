import os
import requests
import json
import re
import sys
from termcolor import colored, cprint
import colorama
colorama.init()

dir = os.path.dirname(sys.argv[0])

#
cprint('Warning: This program is pre-release and may be unstable.', 'yellow')
print('Copyright (c) 2020 inkuringu-ika')
print('This software is released under the GPL3.0 License, see LICENSE.txt.')
#



#client_id

#テスト用
#client_id = '00000000000000000000000000000000'

#有効期限がある
#client_id = 'L1Tsmo5VZ0rup3p9fjY67862DyPiWGaG'

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
        r = requests.get(request_url)
        filesave = open(Noid + '.mp3', 'wb')
        filesave.write(r.content)
    else:
        cprint('not free download', 'yellow')
        #print('not free download')
        request_url = json2[0]["media"]["transcodings"][1]["url"] + '?client_id=' + client_id
        r = requests.get(request_url)
        json3 = json.loads(r.text)
        url = json3["url"]
        request_url = url
        r = requests.get(request_url)
        filesave = open(Noid + '.mp3', 'wb')
        filesave.write(r.content)
except:
    cprint('Error: Unexpected error', 'red')
    sys.exit(1)
