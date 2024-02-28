from bs4 import BeautifulSoup as BS
import pandas as pd
import os
import re
import json
import sys

"""
on console, run python parse_html.py
"""
def extract_vid_info(video_file):
    """
    param: .html video_file
    return: extracted username, nickname, description, counts (like,share,comment,play,collect), comments in one video file
    """
    with open(video_file, 'r') as f:
        print(video_file)
        contents = f.read()

        soup = BS(contents, "html.parser")

        url = soup.find("meta", property="og:url")['content']
        username = soup.find("span", {"class": "css-1c7urt-SpanUniqueId evv7pft1"}).text
        nickname = soup.find("span", {"class": "css-1xccqfx-SpanNickName e17fzhrb1"}).text
        description = soup.find("span", {"class": "css-j2a19r-SpanText efbd9f0"}).text
        music = soup.find("div", {"class": "css-pvx3oa-DivMusicText epjbyn3"}).text

        #print("username:", username,"\nnickname:", nickname, "\ndescription:", description,"\nmusic:",music)

        script_tag = soup.find('script', text=re.compile('stats'))
        script_content = script_tag.string 
        data = json.loads(script_content)["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']["stats"] #json to python dict, and keep looking
        like_count = data['diggCount']
        share_count = data['shareCount']
        comment_count = data['commentCount']
        play_count = data['playCount']
        collect_count = data['collectCount']
        #print("\nlike:",like_count, "\nshare:",share_count, "\ncomment:", comment_count, "\nplay:", play_count, "\ncollect:", collect_count)

        comment_div = soup.find_all("p", {"class": "css-xm2h10-PCommentText e1g2efjf6"})
        comments = []
        for comment in comment_div:
            comments.append(comment.text)

        f.close()

    return url, username, nickname, description, music, like_count, share_count, comment_count, play_count, collect_count, comments
    


def all_videos_info(video_files,data_folder):
    """
    param: list of video_files saved by TikTokScraper.py
    return: dataframe with all video_info
    """
    infos = {'url':[],'username':[],'nickname':[],'description':[], 'music':[], 'like_count':[], 'share_count':[], 'comment_count':[], 'play_count':[], 'collect_count':[], 'comments':[]}
    for vid in video_files:
        url, username, nickname, description, music, like_count, share_count, comment_count, play_count, collect_count, comments = extract_vid_info(vid)
        infos['url'].append(url)
        infos['username'].append(username)
        infos['nickname'].append(nickname)
        infos['description'].append(description)
        infos['music'].append(music)
        infos['like_count'].append(like_count)
        infos['share_count'].append(share_count)
        infos['comment_count'].append(comment_count)
        infos['play_count'].append(play_count)
        infos['collect_count'].append(collect_count)
        infos['comments'].append(comments)
    df = pd.DataFrame(infos)
    df.to_csv(f'./{data_folder}/videos_info.csv')
    return df

def get_html_list(pathName):
    """
    gets all .html files scraped and saved by TikTokScraper.py
    """
    all_vid_files = []
    for dirpath, _, filenames in os.walk(pathName):
        for fN in filenames: 
            if fN.endswith('.html') and fN.startswith('vid'):
                filePath = os.path.join(dirpath, fN) # create the whole path of a file
                all_vid_files.append(filePath)
    return all_vid_files


def main():
    data_folder = sys.argv[1]
    all_vid_files = get_html_list(data_folder)
    all_videos_info(all_vid_files,data_folder)

if __name__ == "__main__":
    main()
