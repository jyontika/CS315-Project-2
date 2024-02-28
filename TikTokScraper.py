from seleniumbase import BaseCase
import time
from datetime import datetime
from csv import DictReader
import os
from seleniumbase.common.exceptions import NoSuchElementException

class TestTiktok(BaseCase):
    def test_save_html_page(self):
        """
        1. log in manually 
        2. traverse through the vids in the vid_list
        3. where we scroll down once to get comments
        4. save html file fo each vid
        """
        current_time = datetime.now().strftime("%m-%d-%H-%M-%S")
        os.mkdir(current_time)

        self.open('https://www.tiktok.com/')
        time.sleep(30) #manually log in
        #self.click('//*[@id="loginContainer"]/div/div/div[3]/div/div[2]/div/div/div')
        
        vid_list = []
        with open('video_urls.csv',"r") as file:
            reader = DictReader(file)          
            for row in reader:
                vid_list.append(row['url'])

        print(f"we have {len(vid_list)} videos")

        for i,vid in enumerate(vid_list):
            time.sleep(5)
            self.open(vid)
            try: 
                self.scroll_to_bottom()
                soup = self.get_beautiful_soup(source=None)

                if soup.find(id="tiktok-verify-ele"):
                    print("element exception!! Check if CAPTCHA appeared!!")
                    time.sleep(15)
                    self.open(vid)
                    self.scroll_to_bottom()
                    soup = self.get_beautiful_soup(source=None)

                with open(f"{current_time}/vid_{i}.html", "w") as file:
                    file.write(str(soup))
            except:
                #if page x load:
                try:
                    self.click('/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div[1]')
                except NoSuchElementException:
                    time.sleep(5)
                    self.open(vid)
                    try:
                        self.click('//*[@id="main-content-video_detail"]/div/div[2]/div/div[3]/div[2]/div/div[5]')
                    except NoSuchElementException:
                            print("no element found, moving on to next vid..")
                            pass #just move on to next vid
        
