import pandas as pd
import re


def contains_arabic(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
    return arabic_pattern.search(text) is not None


df = pd.read_html('https://kworb.net/youtube/insights/il.html')[0]
df = df[~df['Track'].str.contains('short', case=False)]
df = df[df['Track'].str.contains(' - ', case=False)]
df = df[~df['Track'].apply(contains_arabic)]

# Split by '-' and filter
df['song_name'] = df['Track'].apply(lambda video: video.split('-')[1])
df['artist_names'] = df['Track'].apply(lambda video: video.split('-')[0])
df = df[['Track', 'song_name', 'artist_names']]
# Keep valid rows and add columns


# Reset index for clean output

a = 5
