import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = "UCddiUEpeqJcYeBxX1IVBKvQ"
def get_channel_stats(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    stats = data["items"][0]["statistics"]
    return stats

def get_video_ids(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=id&order=date&maxResults=10"
    response = requests.get(url)
    data = response.json()
    ids = [item["id"]["videoId"] for item in data["items"] if item["id"]["kind"] == "youtube#video"]
    return ids

def get_video_stats(video_ids):
    ids_str = ",".join(video_ids)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={ids_str}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    videos = []
    for item in data["items"]:
        video = {
            "title": item["snippet"]["title"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
        }
        videos.append(video)
    return videos

# --- Main ---
print("Fetching channel stats...")
channel_stats = get_channel_stats(CHANNEL_ID)

print(f"Subscribers: {channel_stats['subscriberCount']}")
print(f"Total Views: {channel_stats['viewCount']}")
print(f"Total Videos: {channel_stats['videoCount']}")

print("\nFetching videos...")
video_ids = get_video_ids(CHANNEL_ID)
videos = get_video_stats(video_ids)

df = pd.DataFrame(videos)
df["engagement_rate"] = ((df["likes"] + df["comments"]) / df["views"] * 100).round(2)

print("\n--- Video Analysis ---")
print(df)
print(f"\nMost viewed: {df.loc[df['views'].idxmax(), 'title']}")
print(f"Best engagement: {df.loc[df['engagement_rate'].idxmax(), 'title']}")

df.to_csv("analysis_results.csv", index=False)

plt.figure(figsize=(10, 6))
plt.bar(df["title"], df["views"])
plt.title("Views per Video")
plt.xlabel("Video")
plt.ylabel("Views")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("views_chart.png")
plt.show()
print("\nDone! Results saved.")