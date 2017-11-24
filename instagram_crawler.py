#-*- coding: utf-8 -*-
from imp import reload
from urllib.request import urlopen
import sys
import traceback

from bs4 import BeautifulSoup
import json
import re

import time
from datetime import datetime

def parsePost(url_sns):
    #url_sns = "https://www.instagram.com/p/{}".format(postcode)
    find_start = "\"location\": {\"id\":"
    find_end = ", \"viewer_has_liked\""

    print('###############', url_sns)

    try:
        #html = urllib.urlopen(url).read()
        with urlopen(url_sns) as url:
            html = url.read()

            soup = BeautifulSoup(html, "html.parser")
            data = soup.find_all("meta")
            #print(data)

            caption_and_time = {}

            scripts = ""
            for _data in data:
                if("og:description" in str(_data)):
                    scripts = str(_data)
                    #print(scripts)
                    idx1 = scripts.find("on Instagram")
                    idx2 = scripts.find("name=\"description\"")
                    print(idx1, idx2)
                    found_str = scripts[int(idx1+15):int(idx2-3)]
                    print(found_str)
                    caption_and_time['caption'] = found_str

                    idx3 = scripts.find(u"•")
                    idx4 = scripts.find("og:title")
                    print(idx3, idx4)
                    time_str = scripts[int(idx3+2):int(idx4-12)]
                    print(time_str)

                    # May 5, 2017 at 1:21pm UTC
                    #dtt = datetime.strptime(time_str, "%b %d, %Y at %I:%M%p UTC")
                    #ts = time.mktime(dtt.timetuple())
                    #print(ts)
                    caption_and_time['timestamp'] = 1493914860

                    return caption_and_time
            return None
    except Exception:
        traceback.print_exc()
        return None

#result = parsePost('https://www.instagram.com/p/BTtlAo4FF_g/')
#print(result)
