import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#setting up the title of the application and the subtitle
st.title('Interactive Dashboard 🐌')
st.sidebar.title('Interactive Dashboard 🐌')

st.markdown('This application is a small project I created to analyse the sentiment of comments and games ratings 🐌, data source is Google PLay🤖')
st.sidebar.markdown('This application is a small project I created to analyse the sentiment of comments and games ratings 🐌, data source is Google PLay🤖')

#Upload the data to the application
DATA_URL = ("here you pick the data by navegating into the data folder")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    #this code used in case you have a date: 
    #     data['at'] = pd.to_datetime(data['at'])
    return data

data = load_data()

#Display the random comments based on your selection 
st.sidebar.subheader('Show random comments')
random_tweet = st.sidebar.radio('Sentiment', ('Positive', 'Neutral', 'Negative'))
st.sidebar.markdown(data.query('comment_type == @random_tweet')[['content']].sample(n=1).iat[0,0])

#Creat a sub information to turn on and of the type of chart you want to show and counting the comments_type
st.sidebar.markdown('### Number of reviews by sentiment for both games')
select = st.sidebar.selectbox('Visualisation Type', ['Histogram', 'Pie chart'], key = '1')
sentiment_count = data['comment_type'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Reviews':sentiment_count.values})

#Using the if to link it to the selection in the sidebar in order to show the right chart
if not st.sidebar.checkbox('Hide reviews Chart', True):
    st.markdown('### Number of reviews by sentiment for both games')
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x = 'Sentiment', y = 'Reviews', color = 'Reviews', height = 500,
        labels = {'Reviews': 'Reviews Count'})
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'Reviews', names = 'Sentiment')
        st.plotly_chart(fig)

#--------------------------------------------------------------------------------------------------------

#Creating a side bar to pick the right game you want to show in a chart 
st.sidebar.subheader('Breakdown reviews by games title')
choice = st.sidebar.multiselect('Pick Game Title', ('name_of_game1', 'name_of_game2'), key = '0')

#Using the if to link the charts to the side bar of games which will be used for comparision also 
if len(choice) > 0:
    choice_data = data[data.appId.isin(choice)]
    fig_choice = px.histogram(choice_data, x = 'appId', y = 'comment_type', histfunc = 'count',
     color = 'comment_type', facet_col = 'comment_type', labels = {'comment_type': 'Sentiment Type',
    'appId': 'Game Title'}, height = 600, width = 1000)
    st.plotly_chart(fig_choice)
    

#Uloading diffrent data to the application
DATA_URL_month = ("here you pick the data by navegating into the data folder")
def load_data():
    data_month = pd.read_csv(DATA_URL_month)
    return data_month

data_month = load_data()

#Creating a side bar to slect the right visulisation 
st.sidebar.markdown('### Game ratings')
select_rate = st.sidebar.selectbox('Visualisation type', ['Scatter Plot', 'Line Chart'], key = '1')

#Using if to link the information to each visulisation type in case it was choosen in the side bar
if not st.sidebar.checkbox('Hide Rating Charts', True):
    st.markdown('### Average rating per a month for both games')
    if select_rate == 'Scatter Plot':
        fig = px.scatter(data_month, x = 'year_month', y = 'score', color = 'appId', height = 600
        , width = 1100, range_y = [0.001,5], range_x = [-2, 74],
        hover_data = {'count': True}, labels = dict(score = 'Average Score per a month',year_month = 'Monthly rate'))
        st.plotly_chart(fig)

    elif select_rate == 'Line Chart':
        fig = px.line(data_month, x = 'year_month', y = 'score', color = 'appId', height = 600
        , width = 1100, range_y = [0.001,5],range_x = [-2, 74],
        hover_data = {'count': True}, labels = dict(score = 'Average Score per a month',
        year_month = 'Monthly rate'))
        st.plotly_chart(fig)

if st.sidebar.checkbox('Show raw data monthly', False):
    st.write(data_month)

## This code is used in case you have a Latitude and a Longitude

#st.sidebar.subheader('when and where are users tweeting from?')
#hour = st.sidebar.slider('Hour of day', 0, 23)
# this is another code that let you creat a search bar to enter the time of the day you want
   #hour_search = st.sidebar.number_input('Input the hour of day', min_value = 1, max_value = 24)
#modified_data = data[data['at'].dt.hour == hour]
#if not st.sidebar.checkbox('Close', True, key = '1'):
    #st.markdown('### Tweets locations based on the time of day')
    #st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    #st.map(modified_data)
    #if st.sidebar.checkbox('Show raw data', False):
        #st.write(modified_data)


#Break down the data frame into 2 based ona give string value
name_of_game1 = data[(data['appId'] == "name_of_game1")]
name_of_game2 = data[(data['appId'] == "name_of_game1")]

#Creating a side bar about word cloud and slect by sentiment
st.sidebar.subheader('Word Cloud Chart')

word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('Positive', 'Neutral', 'Negative'))
select_game = st.sidebar.multiselect('Pick Game Title for Word Cloud', ('name_of_game1', 'name_of_game2'), key = '0')

#Let you select the chart of word cloud per a game
if not st.sidebar.checkbox('Close', True, key = '3'):
    st.markdown('### Cloud word chart showing most frequent words')
    if len(select_game) > 0:
        select_by_game = data[data.appId.isin(select_game)]
        st.header('Word cloud for %s sentiment' % (word_sentiment))
        df = select_by_game[select_by_game['comment_type'] == word_sentiment]
        words = ' '.join(df['content'].astype(str))
        processed_words = ' '.join([word for word in words.split() if 'game' not in word
            if 'level' not in word if 'will' not in word and word != 'play'])
        wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white', height = 800,
            width = 1000).generate(processed_words)
        plt.imshow(wordcloud)
        plt.xticks([])
        plt.yticks([])
        st.pyplot(plt)
    
