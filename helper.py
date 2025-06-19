from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import calendar
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    # Count number of messages per user
    user_counts = df['user'].value_counts()

    # Remove 'group_notification' if it exists
    if 'group_notification' in user_counts:
        user_counts = user_counts.drop('group_notification')

    # Top 5 users
    top_users = user_counts.head()

    # Calculate percent contribution of each user
    percent_df = (user_counts / user_counts.sum() * 100).round(2).reset_index()
    percent_df.columns = ['name', 'percent']

    return top_users, percent_df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[
        (df['user'] != 'group_notification') &
        (~df['message'].isin(['<Media omitted>\n', 'This message was deleted\n', 'null\n', ''])) 
    ]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[
        (df['user'] != 'group_notification') &
        (~df['message'].isin(['<Media omitted>\n', 'This message was deleted\n', 'null\n', ''])) 
    ]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

from collections import Counter
import pandas as pd
import emoji

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counts = Counter(emojis).most_common()
    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])

    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    weekdays = list(calendar.day_name)
    
    counts = [sum(df['day_name'] == day) for day in weekdays]
    return weekdays,counts

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    months=list(calendar.month_name)
    counts=[sum(df['month']==month) for month in months]
    return months,counts

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
def all_emotions(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    all_emotions = Counter()
    for emotions in df['emotion_scores']:
        all_emotions.update(emotions)
    emotion_df = pd.DataFrame(all_emotions.items(), columns=["Emotion", "Count"])
    emotion_df = emotion_df.sort_values(by="Count", ascending=False)
    return emotion_df

    














