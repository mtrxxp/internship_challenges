from googleapiclient.discovery import build
from youtube_scrapper_for_internship_main.config import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)

def search_channels(query, max_results=10):
    request = youtube.search().list(
        q=query,
        type="channel",
        part="snippet",
        maxResults=max_results
    )
    response = request.execute()
    return [item["snippet"]["channelId"] for item in response["items"]]

def get_channel_info(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics,topicDetails",
        id=channel_id
    )
    response = request.execute()
    if not response["items"]:
        return None

    data = response["items"][0]
    title = data["snippet"]["title"]

   #by name
    if title.lower().endswith(" - topic"):
            ch_type = "t"
    else:
            ch_type = "c"

    return {
        "channel_id": channel_id,
        "title": title,
        "country": data["snippet"].get("country", "N/A"),
        "subscribers": int(data["statistics"].get("subscriberCount", 0)),
        "views": int(data["statistics"]["viewCount"]),
        "video_count": int(data["statistics"]["videoCount"]),
        "url": f"https://www.youtube.com/channel/{channel_id}",
        "type": ch_type
    }
