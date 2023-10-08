from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import streamlit as st
extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!='All users':
        df = df[df['user'] == selected_user]

    num_message=df.shape[0]          #number of messages

    words=[]
    for message in df['message']:       #number of words
        words.extend(message.split())

    num_media_messages=df[df['message'] == '<Media omitted>\n'].shape[0] #number of media messages

    links=[]
    for message in df['message']:                       #number of urls
        links.extend(extractor.find_urls(message))


    return num_message,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

# def create_word_cloud(selected_user,df):
#     if selected_user!='All users':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'Group notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']

def create_word_cloud(selected_user, df):
    if selected_user != 'All users':
        temp = df[df['user'] == selected_user]
    else:
        temp = df

    temp = temp[temp['message'] != '<Media omitted>']
    text = temp['message'].str.cat(sep=" ")

    if not text.strip():
        print("No words to display in the word cloud.")
        return None

    wc = WordCloud()
    df_wc = wc.generate(text)


    f = open("stop_higlish.txt", 'r')
    stop_words = f.read()
    words = []

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!='All users':
        df = df[df['user'] == selected_user]

    temp=df[df['user']!='Group notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    f=open("stop_higlish.txt",'r')
    stop_words=f.read()
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def imoji_helper(selected_user,df):
    if selected_user!='All users':
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA.keys()])

    emojis_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojis_df

def monthly_timeline(selected_user,df):
    if selected_user!='All users':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):
    if selected_user!='All users':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='All users':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'All users':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

