from youtubesearchpython import VideosSearch
import pandas as pd

search_queries = [
    "Donald Trump 2024 election",
    "Trump political analysis",
    "Trump supporters reaction"
]

video_data = []

for query in search_queries:
    videos_search = VideosSearch(query, limit=10)
    results = videos_search.result()['result']

    for video in results:
        video_data.append({
            'Title': video.get('title'),
            'Video ID': video.get('id'),
            'Channel': video['channel'].get('name'),
            'Channel Link': video['channel'].get('link'),
            'Duration': video.get('duration'),
            'Views': video['viewCount'].get('text'),
            'Published': video.get('publishedTime'),
            'Link': video.get('link'),
            'Description': " ".join([snippet['text'] for snippet in video.get('descriptionSnippet', [{'text':'No description'}])]),
            'Thumbnail': video['thumbnails'][0].get('url') if video.get('thumbnails') else None,
            'Accessibility Title': video.get('accessibility', {}).get('title')
        })

# Save data clearly to CSV
df_videos = pd.DataFrame(video_data)
df_videos.to_csv("Enhanced_YouTube_Trump_Videos.csv", index=False)

print(df_videos.head())
