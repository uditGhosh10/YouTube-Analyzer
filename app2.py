import streamlit as st
import json
# from eda import eda
from main import m
import  pandas as pd
import requests
import json
from tqdm import tqdm
import isodate
import matplotlib.pyplot as plt
import time
import seaborn as sns
from math import log, floor

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])


st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.markdown("<h1 style='text-align: center; color: white;'>YouTube Analyzer</h1>", unsafe_allow_html=True)
# st.sidebar.write("This is a webapp built on Streamlit to perform analysis of any youtube channel. On the backend, the app uses the YpouTube API to get the channel statistics in JSON format, and then it generates relevent graphs using the seaborn and matplotlib library.")
st.sidebar.markdown("<p style='text-align: center; color: grey;'>This is a webapp built on Streamlit to perform analysis of any youtube channel. On the backend, the app uses the YpouTube API to get the channel statistics in JSON format, and then it generates relevent graphs using the seaborn and matplotlib library.</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: left; color: white;'>Stack Used</p>", unsafe_allow_html=True)
st.sidebar.markdown("<li style='text-align: left; color: grey;'>Python</li>", unsafe_allow_html=True)
st.sidebar.markdown("<li style='text-align: left; color: grey;'>StreamLit</li>", unsafe_allow_html=True)
st.sidebar.markdown("<li style='text-align: left; color: grey;'>YouTube API</li>", unsafe_allow_html=True)
st.sidebar.markdown("<li style='text-align: left; color: grey;'>Pandas</li>", unsafe_allow_html=True)
st.sidebar.markdown("<li style='text-align: left; color: grey;'>Seaborn</li>", unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.subheader(" Created by Udit Ghosh ")
link1='[Github](https://github.com/GlobalSmurfWannabeee)'
link2='[LinkedIn](https://www.linkedin.com/in/uditghosh/)'
st.sidebar.markdown(link1,unsafe_allow_html=True)
st.sidebar.markdown(link2,unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>Analyzing your favourite YouTube Channels!!!</h1>", unsafe_allow_html=True)
# st.title('')
id = st.text_input('Enter the ChannelID')
# @st.cache
if len(id):
	m(id)
	# st.info('DataSet Loaded !!')

	# st.header("This is out homepage")
	file = 'data.json'
	data=None
	with open(file, 'r') as f:
		    data=json.load(f)

	channel_id, stats= data.popitem()
	# st.write(channel_id)

	channel_stats= stats['channel_statistics']
	video_stats=stats['video_data']

	channelName=channel_stats['channelName']

	html_str = f"""
<style>
h1.a {{
  font: bold Courier;
  text-align: center;
}}
</style>
<h1 class="a">{channelName}</p>
"""

	st.markdown(html_str, unsafe_allow_html=True)
	c1,c2,c3=st.columns(3)
	c1.metric(label="Total Views", value=human_format(int(channel_stats['viewCount'])), delta_color="off")
	c2.metric(label="Subscriber Count", value=human_format(int(channel_stats['subscriberCount'])),
     delta_color="off")
	c3.metric(label="Video Count", value=human_format(int(channel_stats['videoCount'])),
     delta_color="off")



	sorted_vids=sorted(video_stats.items(), key= lambda x: int(x[1]['viewCount']), reverse=True)
	stats=[]
	for vid in sorted_vids:
		    vId=vid[0]
		    date=vid[1]['publishedAt']
		    title=vid[1]['title']
		    likes=int(vid[1]['likeCount'])	if 'likeCount' in vid[1] else 0
		#     dislikes=vid[1]['dislikeCount']
		    comments=int(vid[1]['commentCount']) if 'commentCount' in vid[1] else 0
		    views=int(vid[1]['viewCount'])
		    duration=int(isodate.parse_duration(vid[1]['duration']).seconds)/60
		    stats.append([title, views, likes, comments, duration, date])

	df = pd.DataFrame(stats, columns=['Title', 'views', 'likes', 'comments', 'duration', 'date'])
	df['date']=pd.to_datetime(df['date']).dt.date
	df['month']=pd.to_datetime(df['date']).dt.month
	df['year']=pd.to_datetime(df['date']).dt.year
	bins = [0,20,40,60,80,100,120]
	labels =['0-20 min.','20-40 min.' , '40-60 min.', '60-80 min.', '80-100 min.', '>100 min.']
	df['span'] = pd.cut(df['duration'], bins,labels=labels)

	df['Percentage of Likes/View']=df['views']/df['likes']
	y=df.groupby(["span"])

	# z=df.groupby(['year','month']).size()
	# z.plot.bar()

	genre = st.selectbox(
     "Select the statistic you want to view",
     ('General Statistics', 'Frequency of Videos', 'Distribution of videos'))
	c11,c21,c31=st.columns(3)
	if genre == 'General Statistics':
		years=sorted([i for i in set(df.year)])+["All Time"]
		option1=c11.selectbox("Sort By", ['Top', 'Bottom'])
		option2=c21.selectbox("Select Release Year", years)
		option3=c31.selectbox("Sort By", ['views','likes', 'comments'])
		dt=df.sort_values(by=option3)[::-1]
		age = st.slider('Number of videos', 0, 20, 5)
		x="Here are the", option1.lower(), str(age), "watched videos"
		x=" ".join(x)
		_,mid,_=st.columns([1,3,1])
		mid.subheader(x)

		if option1 == 'Top':
			if option2=="All Time":
				ax=dt.head(age).plot.bar(x='Title', y=option3)
			else:
				ax=dt[dt['year']==option2].head(age).plot.bar(x='Title', y=option3)
			plt.xlabel("Title")
			plt.ylabel("Views")
			plt.show()
			st.pyplot()
		else:
			if option2=="All Time":
				ax=dt.tail(age).plot.bar(x='Title', y=option3, figsize=(12, 8))
			else:
				ax=dt[dt['year']==option2].tail(age).plot.bar(x='Title', y=option3, figsize=(12, 8))
			plt.xlabel("Title")
			plt.ylabel("Views")
			plt.show()
			st.pyplot()


		st.subheader("Some interesting Figures from the Channel !!")
		with st.expander("Reveal the most viewed video of the channel"):
			st.info(df.loc[0]['Title'])
		with st.expander("Reveal the like/view ratio"):
			st.info(str(sum(df.likes)/len(df)))
		with st.expander("Reveal the most liked video of the channel"):
			st.info(df[df['likes']==df['likes'].max()]['Title'][0])
		# st.write("The most viewed video is: ", df.loc[0]['Title'])

	elif genre == 'Frequency of Videos':
		st.header("Frequency of Videos Uploaded per month")
		df.groupby(['year','month']).size().unstack(fill_value=0).plot.bar()
		plt.show()
		st.pyplot()

	# df['most interacted vid']= 0.2*df['views']+0.3*df['likes']+0.5*df['comments']
	# df['normalized']=(df['most interacted vid']-df['most interacted vid'].min())/ (df['most interacted vid'].max() - df['most interacted vid'].min())

	else:
		st.markdown("<h1 style='text-align: center; color: white;'>Distribution of duration of videos in the channel</h1>", unsafe_allow_html=True)
		# st.title('Distribution of duration of videos in the channel')
		patches, texts = plt.pie(df['span'].value_counts(), shadow=True, startangle=90)
		plt.legend(patches, labels, loc="best")
		plt.axis('equal')
		st.pyplot()
		col1, col2= st.columns(2)
		option4=st.selectbox("Select appropriate attribute", ['Views', 'Likes'])	
		sns.catplot(x="span", y=option4.lower(), kind="swarm", data=df, aspect=2, height = 4)
		st.pyplot()
		st.write("The graph shows distribution of the attribute with respect to the video duration. The graph captures how positively a particular span of video is recieved by the viewers.")

	if st.checkbox('Show Raw Data'):
		st.write(df)#['Title', 'views', 'likes', 'comments', 'duration', 'date'])
		csv = convert_df(df)#['Title', 'views', 'likes', 'comments', 'duration', 'date'])

		st.download_button(
		     label="Download data as CSV",
		     data=csv,
		     file_name='large_df.csv',
		     mime='text/csv',
		 )
