from dotenv import load_dotenv
import os
import re
import html
import requests
import demoji
import string


def remove_html(raw_comment):
    raw_comment = html.unescape(raw_comment)
    raw_comment = "".join(x for x in raw_comment if x in string.printable)
    raw_comment = re.sub(r'<[^<]+?>', ' ', raw_comment)
    return raw_comment


def get_comment_corpus(videoID):
    text_data = []
    comment_corpus = ""
    load_dotenv()
    api_key = os.getenv("API_key")
    url = "https://youtube.googleapis.com/youtube/v3/commentThreads?videoId=" + videoID
    params = {'key': api_key, 'Accept': "application/json", 'order': 'relevance', 'part': "snippet"}

    while len(text_data) <= 100:
        r = requests.get(url=url, params=params)
        data = r.json()
        for i in data["items"]:
            comm = i["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comm = remove_html(comm)
            comment = demoji.replace(comm, "")
            if comment != "":
                comment = comment.lower()
                text_data.append(comment)
        if data.get("nextPageToken"):
            params.update({"pageToken": data["nextPageToken"]})
    for i in text_data:
        comment_corpus += i
        comment_corpus += "\n"
    return comment_corpus


# if __name__ == "__main__":
#     print(get_comment_corpus("5QiW4kOxXVg"))
