import requests
import re
import os
import demjson
from threading import Thread
class download_img:
    def __init__(self):
        self.headers={"":""}
        self.trial=0
    def download_img(self,img_url):
        path=os.getcwd()+"/pixiv"
        if not os.path.exists(path):
            os.makedirs(path)
        self.headers["Referer"]=img_url
        while self.trial<=3:
            try:
                img=requests.get(img_url,headers=self.headers,timeout=30)
            except:
                print("Error. Try again")
                self.trial+=1
            else:
                with open(path+"/"+re.findall(r".{26}$",img_url)[0],"wb") as f:
                    f.write(img.content)
                print("Download successfully")
                break
        print("Download failed")
class download_by_following_list(download_img):
    def download_by_following_list(self,page):
        assert page>0 and type(page)==int,"The number entered should be positive integers."
        for i in range(1,1+page):
            following_url=f"https://www.pixiv.net/bookmark_new_illust.php?p={page}"
            self.headers["Referer"]=following_url
            following_html=requests.get(following_url,headers=self.headers)
            img_urls=re.findall(r"https:\\\/\\\/.*?1200.jpg",following_html.text)
            if not img_urls:
                break
            for img_url in img_urls:
                img_url=re.sub(r"\\","",img_url)
                self.download_img(img_url)
            print("Download complete")
class download_by_illust_page(download_img):
    def download_by_illust_page(self,illust_id):
        illust_url=f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=en"
        self.headers["Referer"]=illust_url
        illust_html=requests.get(illust_url,headers=self.headers)
        print(illust_html.text)
        if illust_html.json()["body"]:
            img_urls=re.findall(r"https:\\\/\\\/i.pximg.net\\\/img-master\\\/img\\\/.*?1200.jpg",illust_html.text)
            for img_url in img_urls:
                img_url=re.sub(r"\\","",img_url)
                self.download_img(img_url)
        else:
            print("The image doesn't exist")
class download_by_author_page(download_by_illust_page):
    def download_by_author_page(self,author_id):
        author_url=f"https://www.pixiv.net/ajax/user/{author_id}/profile/all?lang=en"
        self.headers["Referer"]=author_url
        author_html=requests.get(author_url,headers=self.headers)
        img_ids=demjson.decode(author_html.text)["body"]["illusts"].keys()
        for img_id in img_ids:
            self.download_by_illust_page(img_id)
        print("Download complete")

