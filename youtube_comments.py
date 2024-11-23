import pandas as pd
from googleapiclient.discovery import build
import time
import random

# Your YouTube Data API v3 key
api_key = 'DEMO API KEY'  # Replace with your YouTube Data API Key

# Build the YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to extract channel ID from a YouTube channel URL
def extract_channel_id(url):
    if 'channel' in url:
        return url.split('/')[-1]
    elif '@' in url:
        return url.split('@')[-1]
    return None

# Function to get the channel ID from the handle (if custom URL)
def get_channel_id_from_handle(handle):
    try:
        request = youtube.channels().list(
            part="id",
            forUsername=handle
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['id']
    except Exception as e:
        print(f"Error fetching channel ID for handle {handle}: {e}")
    return None

# Function to get the top 30 video IDs from a given channel
def get_top_video_ids(channel_id):
    video_ids = []
    request = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        maxResults=30,
        type='video',
        order='date'  
    )
    try:
        while request and len(video_ids) < 30:
            response = request.execute()
            if 'items' in response:
                for item in response['items']:
                    if 'videoId' in item['id']:
                        video_ids.append(item['id']['videoId'])
            request = youtube.search().list_next(request, response)
    except Exception as e:
        print(f"Error fetching video IDs for channel {channel_id}: {e}")
    return video_ids[:30]  # Ensure we only return 30 video IDs

# Function to get up to 30 comments from a video
def get_top_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,  # Request 100, but limit to 30 in final result
        textFormat='plainText'
    )
    try:
        while request and len(comments) < 30:
            response = request.execute()
            if 'items' in response:
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)
                    if len(comments) >= 30:
                        break
            request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        print(f"Error fetching comments for video {video_id}: {e}")
    return comments[:30]  # Ensure we only return 30 comments

# Load the CSV file 
df = pd.read_csv('YT_Links.csv')

# Extract channel IDs from the CSV file
df['channel_id'] = df['link_column'].apply(extract_channel_id)  # Replace 'link_column' with the actual column name
channel_ids = df['channel_id'].dropna().tolist()

# List to store the final ordered data
all_comments = []

# Collect comments for each video of each channel
for channel_id in channel_ids:
    if not channel_id.startswith('UC'):
        print(f"Fetching actual channel ID for handle: {channel_id}")
        channel_id = get_channel_id_from_handle(channel_id)
        if not channel_id:
            continue
    
    print(f"Fetching top 30 videos for channel: {channel_id}")
    video_ids = get_top_video_ids(channel_id)
    
    if not video_ids:
        print(f"No videos found for channel {channel_id}")
        continue
    
    for video_id in video_ids:
        print(f"Fetching top comments for video: {video_id}")
        comments = get_top_comments(video_id)
        
        if comments:
            for comment in comments:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                all_comments.append({
                    'channel_id': channel_id,
                    'video_url': video_url,
                    'comment': comment
                })
        time.sleep(random.uniform(1, 3))  # Adding a random delay to avoid rate limits

# Create a DataFrame and save the results to a CSV file in ordered format
comments_df = pd.DataFrame(all_comments)
comments_df = comments_df[['channel_id', 'video_url', 'comment']]  # Ensure the correct order of columns
comments_df.to_csv('YT_Comments_Ordered.csv', index=False)

print("Comments have been saved to 'YT_Comments_Ordered.csv'.")
