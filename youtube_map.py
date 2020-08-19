# -*-coding:utf-8-*-
# This is a sample Python script.

# Press Shift+F10 to execute it[0] or replace it[0] with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# print(json.dumps(pretty_json, indent=4, ensure_ascii=False))
# export GOOGLE_APPLICATION_CREDENTIALS="/home/psc/Trendup2020-39205bfb2ca5.json"


import tcp
from langdetect import detect
import json
import requests
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import pymysql.cursors

'''
#python3 is default is utf8
from importlib import reload
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''

QUERY_INSERT_YOUTUBE = "insert into youtube (rank, keyword, date_, gender, score) values(%s, %s, cast(now() as char), %s, %s)"
QUERY_INSERT_YOUTUBE_LIVE = "insert into youtube_live (rank, keyword, date_, gender, score) values(%s, %s, cast(now() as char), %s, %s)"
QUERY_DELETE_YOUTUBE_LIVE = "delete from youtube_live"

QUERY_INSERT_YOUTUBE_VIDEO_ID = "insert into youtube_video_id (id) values(%s)"
QUERY_SELECT_ALL_YOUTUBE_VIDEO_ID ="select * from youtube_video_id"


QUERY_INSERT_YOUTUBE_MAP_NODE = "insert into youtube_map_node_live (channel_id, title, subscriber_count) values(%s, %s, %s)"
QUERY_INSERT_YOUTUBE_MAP_EDGE = "insert into youtube_map_edge_live (source_id, target_id, size) values(%s, %s, %s)"

URL_CHANNEL = "https://www.googleapis.com/youtube/v3/channels"
URL_SEARCH = "https://www.googleapis.com/youtube/v3/search"
URL_VIDEO = "https://www.googleapis.com/youtube/v3/videos"
URL_COMMENT_THREAD = "https://www.googleapis.com/youtube/v3/commentThreads"
URL_ACTIVITY = "https://www.googleapis.com/youtube/v3/activities"
API_KEY = ""
with open("/home/psc/api_key.txt", "r") as file:
    API_KEY = file.read()
MAX_RESULT = "5"
MAX_PAGE = 2
MAX_CHANNEL = 100

# https://www.googleapis.com/youtube/v3/videoCategories?&key=AIzaSyABYt3bjXmFzFyzZxJJut7J93Bv_3BkhUE&part=snippet&regionCode=KR&hl=ko_KR

channel_dict = dict()
channel_count = 0
vector_2d_channel = [[0]*MAX_CHANNEL]*MAX_CHANNEL

conn = pymysql.connect(
    host="101.101.217.206",
    port=3306,
    user="trendup",
    passwd="2020",
    database="dbtrendup",
    charset='utf8'
)
curs=conn.cursor()


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
    if not (language == "en" or language == "ko"):
        return lst

    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    # Loop through entitites returned from the API
    for entity in response.entities:
        '''
        print("Representative name for the entity: {}".format(entity.name))
        print("Entity type: {}".format(enums.Entity.Type(entity.type).name))
        print("Salience score: {}".format(entity.salience))
        '''
        if (
                (enums.Entity.Type(entity.type).name == "PERSON" or
                enums.Entity.Type(entity.type).name == "UNKNOWN" or
                enums.Entity.Type(entity.type).name == "CONSUMER_GOOD" or
                enums.Entity.Type(entity.type).name == "OTHER") and
                entity.salience > 0.1):
            lst.append(entity.name)
        #print(u"Representative name for the entity: {}".format(entity.name))
        #print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        #print(u"Salience score: {}".format(entity.salience))
    return lst


def get_view_count_by_id(videoId):
    response = requests.get(URL_VIDEO + "?part=statistics" + "&key=" + API_KEY + "&id=" + videoId)
    temp = json.loads(response.text)
    print(json.dumps(temp, indent=4, ensure_ascii=False))
    return temp["items"][0]["statistics"]["viewCount"]


def get_youtube_data_by_q(q):
    '''&regionCode=KR&relevanceLanguage=ko'''
    result_dict = dict()
    cnt = 0
    is_next = False
    next = ""
    while True:
        cnt += 1
        print(next)
        if is_next:
            response = requests.get(URL_SEARCH + "?q=" + q + "&pageToken=" + next + "&part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&type=video")
        else :
            response = requests.get(URL_SEARCH + "?q=" + q + "&part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&type=video")

        res = json.loads(response.text)
        
        for item in res["items"]:
            curs.execute(QUERY_INSERT_YOUTUBE_VIDEO_ID, (item["id"]["videoId"]))
            viewCount = int(get_view_count_by_id(item["id"]["videoId"]))
            for i in get_keyword(item["snippet"]["title"]):
                if i in result_dict.keys():
                    result_dict[i] += viewCount
                else:
                    result_dict[i] = viewCount
            '''
            for i in get_keyword(item["snippet"]["description"]):
                if i in result_dict.keys():
                    result_dict[i] += viewCount
                elif i != "여자":
                    result_dict[i] = viewCount
            '''
            

            '''
            get_view_count_by_id(item["id"]["videoId"])
            print("category:", q)
            print("keyword_title:")
            for i in get_keyword(item["snippet"]["title"]):
                print(i)
            print("keyword_desc: {}".format(get_keyword(item["snippet"]["description"])))
            print("viewCount: {}".format(get_view_count_by_id(item["id"]["videoId"])))
            print("publish time: {}".format(item["snippet"]["publishTime"]))
            '''

        if cnt < MAX_PAGE :
            # 더이상 자료가 없을때
            if "nextPageToken" in res:
                next = res["nextPageToken"]
                is_next = True
            else:
                break
            continue
        break
    sorted_result =sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    cnt2=0
    curs.execute(QUERY_DELETE_YOUTUBE_LIVE)
    for it in sorted_result:
        if( it[0].find("여자") != -1 or it[0].find("여성") != -1 or it[0][0].find("여름") != -1 or it[0].find("옷") != -1 or it[0].find("문제점") != -1 or it[0].find("공통") != -1 or it[0].find("코디") != -1
        or it[0].find("패션") != -1 or it[0].find("남자") != -1 or it[0].find("남성") != -1 or it[0].find("입") != -1 or it[0].find("할인") != -1 or it[0].find("완전") != -1 or it[0].find("노하우") != -1
        or it[0].find("계절별") != -1 or it[0].find("리뷰") != -1 or it[0].find("이유") != -1 or it[0].find("기본") != -1 or it[0].find("정리") != -1 or it[0].find("요청") != -1 or it[0].find("구독자") != -1
        or it[0].find("모음") != -1 or it[0].find("추천") != -1 or it[0].find("!!") != -1 or it[0].find("그림") != -1 or it[0].find("팁") != -1 or it[0].find("성공") != -1 or it[0].find("증정") != -1
        or it[0].find("옆") != -1 or it[0].find("친구") != -1 or it[0].find("템") != -1 or it[0].find("포함") != -1 or it[0].find("영상") != -1 or it[0].find("쿠폰") != -1 or it[0].find("언박싱") != -1) :
            continue
        cnt2+=1
        curs.execute(QUERY_INSERT_YOUTUBE, (cnt2, it[0], "여자", str(it[1])))
        curs.execute(QUERY_INSERT_YOUTUBE_LIVE, (cnt2, it[0], "여자", str(it[1])))
        if cnt2 == 20:
            break
    print(sorted_result)
    return 0



def analyze_channel_map(videoId):
    # find comment's author channel ID by commentThread.list
    # detect subscription data by activity.list
    # count and append properly
    # return 2 dimension vector
    result_dict = dict()
    response = requests.get(URL_COMMENT_THREAD + "?part=snippet" + "&key=" + API_KEY + "&maxResults=" + MAX_RESULT + "&videoId=" + videoId + "&order=relevance")
    temp = json.loads(response.text)
    print(json.dumps(temp, indent=4, ensure_ascii=False))

    for item in temp["items"]:
        author_channelId = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
        response2 = requests.get(URL_ACTIVITY + "?part=contentDetails" + "&key=" + API_KEY + "&maxResults=" + "10" + "&channelId=" + author_channelId)
        temp2 = json.loads(response2.text)
        print(json.dumps(temp2, indent=4, ensure_ascii=False))
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
                        # add
                        # check existing key and update value++ (for checking common subscription)
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

    return result_dict

def make_map(result_dict):
    # result_dict = {'UCYwx4uxuwZ0i_hdjaHmWn-Q': {'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCBjSSuABxI9mIvDCkYV-Hnw': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCFHOhnjF1KpoxpYfMn2pOKA': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCkHIIJqbXrkq0TFChpthCVg': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCk5bhZYNtbPJyNLRxN8D8NQ': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCfldmTAkWErTcbiAA9GeVxg': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCADOqr6bwKK4JuENxsoFDng': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UC-Bsa2ivAGWq7bsSPrPGFVA': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCFCtZJTuJhE18k8IXwmXTYQ': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': 1}, 'UCJ6ffXRHtnXLhM2MFYsOrhQ': {'UCYwx4uxuwZ0i_hdjaHmWn-Q': 1, 'UCBjSSuABxI9mIvDCkYV-Hnw': 1, 'UCFHOhnjF1KpoxpYfMn2pOKA': 1, 'UCkHIIJqbXrkq0TFChpthCVg': 1, 'UCk5bhZYNtbPJyNLRxN8D8NQ': 1, 'UCfldmTAkWErTcbiAA9GeVxg': 1, 'UCADOqr6bwKK4JuENxsoFDng': 1, 'UC-Bsa2ivAGWq7bsSPrPGFVA': 1, 'UCFCtZJTuJhE18k8IXwmXTYQ': 1}, 'UCHKDlM4UOmtEBhwDTg8lqJQ': {'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UCZuaBVFU70xJUTpHpkuav8g': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UCoC47do520os_4DBMEFGg4A': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UC6eAzxps7dpL7wfbVnunmgQ': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UC1of9ELYwB623fWaAMRDVFA': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UC9XkOhrpTs3ibUqvjQmT8uA': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UC8a6z7i9qypp9PqJ_0HhBrw': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UCZVD--cl8FLRn7kmSudAuBA': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCuh6Br1vzgo1LivYgKvno5Q': 1}, 'UCuh6Br1vzgo1LivYgKvno5Q': {'UCHKDlM4UOmtEBhwDTg8lqJQ': 1, 'UCZuaBVFU70xJUTpHpkuav8g': 1, 'UCoC47do520os_4DBMEFGg4A': 1, 'UC6eAzxps7dpL7wfbVnunmgQ': 1, 'UCPtTNQQxoBF4Gzdw5o9Zc2g': 1, 'UC1of9ELYwB623fWaAMRDVFA': 1, 'UC9XkOhrpTs3ibUqvjQmT8uA': 1, 'UC8a6z7i9qypp9PqJ_0HhBrw': 1, 'UCZVD--cl8FLRn7kmSudAuBA': 1}}
    
    
    for source in result_dict:
        response = requests.get(URL_CHANNEL + "?part=snippet" + "&key=" + API_KEY + "&id=" + source)
        temp = json.loads(response.text)
        # print(temp)
        title = temp["items"][0]["snippet"]["title"]
        response = requests.get(URL_CHANNEL + "?part=statistics" + "&key=" + API_KEY+ "&id=" + source)
        temp = json.loads(response.text)
        subscription = temp["items"][0]["statistics"]["subscriberCount"]
        curs.execute(QUERY_INSERT_YOUTUBE_MAP_NODE,(source, title, str(subscription)))
        # print(title, subscription)
        for target in result_dict[source]:
            # print(source, target, title, subscription)
            curs.execute(QUERY_INSERT_YOUTUBE_MAP_EDGE,(source, target, str(result_dict[source][target])))

def do_map(no):
    curs.execute(QUERY_SELECT_ALL_YOUTUBE_VIDEO_ID)
    rows = curs.fetchall()
    result_dict = analyze_channel_map(rows[0][0])
    make_map(result_dict)
    return 0

if __name__ == '__main__':
    staff_socket = tcp.staff_ready(5003)
    tcp.staff_update(do_map, "여자 여름옷", staff_socket)
    conn.commit()
    conn.close()
    # analyze_channel_map("r51UJMj9M6Y")
    # print(API_KEY)
