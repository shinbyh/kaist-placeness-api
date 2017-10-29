#-*- coding: utf-8 -*-

#import urllib # Python 2.7
from urllib.request import urlopen # Python 3.x
import json
import sys
from bs4 import BeautifulSoup
import requests



def extract_instagram_data(post_url):
    #print('URL = ', post_url) # Debug
    #html = urllib.urlopen(post_url).read() # Python 2.7
    html = urlopen(post_url).read() # Python 3.x

    try:
        soup = BeautifulSoup(html, "html.parser")
        data = soup.find_all("script", { "type" : "text/javascript" })
    except:
        print("[extract_instagram_data] Error: page error")
        return None

    if(data == None):
        print("[extract_instagram_data] Error: no data found")
        return None

    # Find a script tag which contains instagram post data as text.
    for element in data:
        if('"text":' in element.text):
            #print(element.text) # Debug
            element_text = element.text
            key = 'window._sharedData = '
            temp = element_text[len(key):len(element_text)-1]
            json_element = json.loads(temp)

            # Extract caption, time.
            caption = json_element['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
            timestamp = json_element['entry_data']['PostPage'][0]['graphql']['shortcode_media']['taken_at_timestamp']
            comments = json_element['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['edges']
            location = json_element['entry_data']['PostPage'][0]['graphql']['shortcode_media']['location']
            #print(caption) # Debug
            #print(timestamp) # Debug
            #print(comments) # Debug
            #print(location) # Debug

            # Create a dict to return
            insta_data_dict = {}
            insta_data_dict['caption'] = caption
            insta_data_dict['timestamp'] = timestamp
            insta_data_dict['comments'] = comments
            insta_data_dict['location'] = location
            return insta_data_dict

    # No text found from the crawled page.
    return None


def post_hotspot_extraction(insta_data_dict):
    url_api_hotspot = "http://placeness.kaist.ac.kr:8001/feature_extraction.json"
    res = requests.post(url_api_hotspot, data=insta_data_dict)
    print(res)
    return res

#
# Main
#
def main(argv):
    #url = "https://www.instagram.com/p/BXsLO_zhM0z/"
    #url = "https://www.instagram.com/p/BZaPY_xlZ-f/"
    url = argv[1]
    data_dict = extract_instagram_data(url)
    print(data_dict['caption'])
    print(data_dict['timestamp'])
    print(data_dict['location'])
    res = post_hotspot_extraction(data_dict)
    print(res.json())

if __name__ == "__main__":
    main(sys.argv)
