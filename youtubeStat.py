# from main import API_KEY
import requests
import json
from tqdm import tqdm

class YT:
    def __init__(self, API_KEY, channelId) -> None:
        self.api_key=API_KEY
        self.channelId = channelId
        self.channel_statistics= None
        self.vid_data=None

    def getChannelStats(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channelId}&key={self.api_key}'
        json_url= requests.get(url)
        data=json.loads(json_url.text)
        try:
            data= data['items'][0]['statistics']
        except:
            data=None

        self.channel_statistics = data
        return data

    def get_channel_vid_data(self):
        channelVid= self._get_channel_vid(50)
        print(len(channelVid))

        parts = ['snippet', 'statistics', 'contentDetails']
        for vid_id in tqdm(channelVid):
            for part in parts:
                data=self._singleVidData(vid_id, part)
                channelVid[vid_id].update(data)
        self.vid_data=channelVid
        return channelVid

    def _singleVidData(self, vid_id, part):
        # url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={vid_id}&key={self.api_key}'
        json_url=requests.get(url)
        data=json.loads(json_url.text)
        try:
            data=data['items'][0][part]
        except:
            # print("555")
            data=dict()
        return data



    def _get_channel_vid(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?channelId={self.channelId}&key={self.api_key}&part=id&order=date'
        if limit and isinstance(limit, int):
            url+="&maxResults="+str(limit)
        # print(url)
        vid, npt = self._getChannelVidperPage(url)
        idx=0
        while(npt and idx<10):
            nexturl=url+"&pageToken="+npt
            next_vid, npt= self._getChannelVidperPage(nexturl)
            vid.update(next_vid)
            idx+=1
        return vid

    def _getChannelVidperPage(self, url):
        json_url = requests.get(url)
        data= json.loads(json_url.text)
        channel_videos = dict()

        if 'items' not in data:
            return channel_videos, None
        
        item_data = data['items']
        nextPageToken= data.get('nextPageToken', None)
        for item in item_data:
            try:
                kind= item['id']['kind']
                if kind == 'youtube#video':
                    vid_id=item['id']['videoId']
                    channel_videos[vid_id]=dict()
            except KeyError:
                print("Error")

        return channel_videos, nextPageToken


    def dump(self):
        if self.channel_statistics and self.vid_data:
            fusedData={self.channelId: {'channel_statistics': self.channel_statistics, 'video_data': self.vid_data}}
            channelName = self.vid_data.popitem()[1].get('channelTitle', self.channelId)
            # channelName = channelName.replace(" ", "_").lower()
            # filename=channelName+'.json'
            filename='data.json'
            fusedData[self.channelId]['channel_statistics']['channelName']=channelName
            with open(filename, 'w') as f:
                json.dump(fusedData, f, indent=4)
        print('File dumped')
