from dotenv import load_dotenv
from Spam_Filter import spam_filter
from Preprocess import prep_comments
import os
import requests
import demoji


def get_comment_corpus(videoid, num_comments):
    text_data = []
    comment_corpus = ""
    load_dotenv()
    api_key = os.getenv("API_key")
    url = "https://youtube.googleapis.com/youtube/v3/commentThreads?videoId=" + videoid
    params = {'key': api_key, 'Accept': "application/json", 'order': 'relevance', 'part': "snippet"}

    while len(text_data) <= num_comments:
        r = requests.get(url=url, params=params)
        data = r.json()
        for i in data["items"]:
            comm = i["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comm = prep_comments.remove_html(comm)
            comment = demoji.replace(comm, "")
            if comment != "":
                comment = comment.lower()
                if spam_filter.spam_or_ham(comment):
                    print(comment)
                text_data.append(comment)
        if data.get("nextPageToken"):
            params.update({"pageToken": data["nextPageToken"]})
    for i in text_data:
        comment_corpus += i
        comment_corpus += "\n"
    return comment_corpus


if __name__ == "__main__":
    get_comment_corpus("5QiW4kOxXVg", 1000)
