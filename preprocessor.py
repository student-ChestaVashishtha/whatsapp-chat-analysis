import re
import pandas as pd
from nrclex import NRCLex
import nltk
import textblob

# Download only once on first run
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M ')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        
        if(entry[1:]):
            pat=r'-\s'
            mes = re.split(pat, entry[1])[1]
            users.append(mes)
            messages.append("".join(entry[2:]))
        else:
                users.append('group_notification')
                messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df=df[df['message']!='Waiting for this message\n']
    
    def extract_emotions(text):
        emotion = NRCLex(text)
        return emotion.raw_emotion_scores

    df['emotion_scores'] = df['message'].apply(extract_emotions)
    
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df