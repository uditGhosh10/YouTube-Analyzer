from youtubeStat import YT
import streamlit
@streamlit.cache
def m(id):
	API_KEY= 'AIzaSyBEEjAFGOKIn5gj_0D8Gp8OkylF4VW8mx8' #Enter your own youtube api
	channelID=id
	# channelID= 'UChDkP71cJOHop-iRgl_8pVg'
	yt = YT(API_KEY, channelID)
	# data = yt.getChannelStats()
	# print(data)
	# yt.dump()
	# yt.get_channel_vid_data()
	yt.getChannelStats()
	yt.get_channel_vid_data()
	yt.dump()

# m('UChDkP71cJOHop-iRgl_8pVg')