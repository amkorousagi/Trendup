# -*-coding:utf-8-*-
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# print(json.dumps(pretty_json, indent=4, ensure_ascii=False))
# export GOOGLE_APPLICATION_CREDENTIALS="/home/psc/TrendUp-090b119d90eb.json"


from langdetect import detect
import json
import requests
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

URL_SEARCH = "https://www.googleapis.com/youtube/v3/search"
URL_VIDEO = "https://www.googleapis.com/youtube/v3/videos"
URL_COMMENT_THREAD = "https://www.googleapis.com/youtube/v3/commentThreads"
URL_ACTIVITY = "https://www.googleapis.com/youtube/v3/activities"
API_KEY = "AIzaSyABYt3bjXmFzFyzZxJJut7J93Bv_3BkhUE"
MAX_RESULT = "5"
MAX_PAGE = 5
MAX_CHANNEL = 100

# https://www.googleapis.com/youtube/v3/videoCategories?&key=AIzaSyABYt3bjXmFzFyzZxJJut7J93Bv_3BkhUE&part=snippet&regionCode=KR&hl=ko_KR

channel_dict = dict()
channel_count = 0
vector_2d_channel = [[0]*MAX_CHANNEL]*MAX_CHANNEL

def get_keyword(text_content):
    lst =[]
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = detect(text_content)
    print(language)
    if (language != "en" and language != "ko"):
        return lst

    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        print(u"Salience score: {}".format(entity.salience))
        if (
                (enums.Entity.Type(entity.type).name == "PERSON" or
                enums.Entity.Type(entity.type).name == "UNKNOWN" or
                enums.Entity.Type(entity.type).name == "CONSUMER_GOOD" or
                enums.Entity.Type(entity.type).name == "OTHER") and
                entity.salience > 0.1):
            lst.append(entity.name.decode('utf-8').encode('utf-8'))
        #print(u"Representative name for the entity: {}".format(entity.name))
        #print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        #print(u"Salience score: {}".format(entity.salience))
    return lst


def get_view_count_by_id(videoId):
    response = requests.get(URL_VIDEO + "?part=statistics" + "&key=" + API_KEY + "&id=" + videoId)
    temp = json.loads(response.text)
    #print(json.dumps(temp, indent=4, ensure_ascii=False))
    return temp["items"][0]["statistics"]["viewCount"]

def get_youtube_data_by_q(q):
    i = 0
    is_next = False
    next = ""
    while True:
        i += 1
        if is_next:
            response = requests.get(URL_SEARCH + "?pageToken=" + next + "&part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&type=video&regionCode=KR&relevanceLanguage=ko")
        else :
            response = requests.get(URL_SEARCH + "?q=" + q + "&part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&type=video&regionCode=KR&relevanceLanguage=ko")

        res = json.loads(response.text)


        for item in res["items"]:
            get_view_count_by_id(item["id"]["videoId"])
            print(u"category: {}".format(unicode(q,'euc-kr'))
            print(u"keyword_title: {}".format(get_keyword(item["snippet"]["title"])))
            print(u"keyword_desc: {}".format(get_keyword(item["snippet"]["description"])))
            print(u"viewCount: {}".format(get_view_count_by_id(item["id"]["videoId"])))
            print(u"publish time: {}".format(item["snippet"]["publishTime"]))

        if i < MAX_PAGE :
            # 더이상 자료가 없을때
            if "nextPageToken" in res:
                next = res["nextPageToken"]
                is_next = True
            else:
                break
            continue
        break



def analyze_channel_map(videoId):
    # find comment's author channel ID by commentThread.list
    # detect subscription data by activity.list
    # count and append properly
    # return 2 dimension vector
    result_dict = dict()
    response = requests.get(URL_COMMENT_THREAD + "?part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&videoId=" + videoId + "&order=relevance")
    temp = json.loads(response.text)
    #print(json.dumps(temp, indent=4, ensure_ascii=False))

    for item in temp["items"]:
        author_channelId = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
        response2 = requests.get(URL_ACTIVITY + "?part=contentDetails" + "&key=" + API_KEY + "&maxResults=" + "10" + "&channelId=" + author_channelId)
        temp2 = json.loads(response2.text)

        if "nextPageToken" in temp2:
            i = 0
            is_next = False
            next = ""
            while True:
                i+=1
                if is_next:
                    response2 = requests.get(URL_ACTIVITY + "?part=contentDetails" + "&key=" + API_KEY + "&maxResults=" + "10" + "&pageToken=" + next + "&channelId=" + author_channelId)
                else:
                    response2 = requests.get(URL_ACTIVITY + "?part=contentDetails" + "&key=" + API_KEY + "&maxResults=" + "10" + "&channelId=" + author_channelId)

                temp2 = json.loads(response2.text)
                print(json.dumps(temp2, indent=4, ensure_ascii=False))
                sub_channel = []
                for item2 in temp2["items"]:
                    sub_channel.append(item2["contentDetails"]["subscription"]["resourceId"]["channelId"])
                for channel in sub_channel:
                    result_dict.update({channel:{}})
                    for channel2 in sub_channel:
                        if channel != channel2:
                            result_dict[channel].update({channel2:1})
                print(result_dict)

                if i < MAX_PAGE :
                    if "nextPageToken" in temp2:
                        next = temp2["nextPageToken"]
                        is_next = True
                    else:
                        break
                    continue
                break





if __name__ == '__main__':
    get_youtube_data_by_q("여름옷")
    #analyze_channel_map("r51UJMj9M6Y")
    '''
    response = requests.get(
        URL_COMMENT_THREAD + "?part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&videoId=" + "r51UJMj9M6Y" + "&order=relevance")
    temp = json.loads(response.text)
    author_channelId = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
    next = "CAoQAA"
    while True:
        response2 = requests.get(URL_ACTIVITY + "?part=contentDetails" + "&key=" + API_KEY + "&maxResults=" + "10" + "&pageToken=" + next + "&channelId=" + author_channelId)
        temp2 = json.loads(response2.text)
        print(json.dumps(temp2, indent=4, ensure_ascii=False))
    '''
