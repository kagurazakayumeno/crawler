import requests
import re
import os
import demjson
from threading import Thread
class download_img:
    def __init__(self):
        self.headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie":"first_visit_datetime_pc=2020-05-16+19%3A19%3A26; p_ab_id=8; p_ab_id_2=7; p_ab_d_id=666600320; yuid_b=cxhJVYA; _ga=GA1.2.595109545.1589624370; PHPSESSID=34008969_QyAGV8lR5XeEM34bZ4jbEgf8y8sLPVwb; a_type=0; b_type=2; login_ever=yes; _fbp=fb.1.1589624455407.2079112852; __utmv=235335808.|2=login%20ever=yes=1^3=plan=premium=1^5=gender=female=1^6=user_id=34008969=1^9=p_ab_id=8=1^10=p_ab_id_2=7=1^11=lang=zh=1; __gads=ID=5b80d4f2603a90a1:T=1589987291:S=ALNI_MbPYIcJFR7nVaHU_OoxjcC6SVAgAA; adr_id=1mqJdChYjqrGMKMSOQJ4B87CSS3ZTq57aLfgHoqW1S6tIdru; privacy_policy_agreement=2; c_type=18; ki_u=f37513b6-5d12-deac-261c-5602; ki_s=207133%3A0.0.0.0.0%3B208245%3A0.0.0.0.0%3B209879%3A0.0.0.0.0%3B210251%3A1.0.0.0.1; __utmz=235335808.1605925427.40.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ki_r=; tag_view_ranking=0xsDLqCEW6~RTJMXD26Ak~aLBjcKpvWL~MM6RXH_rlN~_bee-JX46i~nAtxkwJ5Sy~_vCZ2RLsY2~KN7uxuR89w~_hSAdpN9rx~dbWQByG3DG~NsbQEogeyL~0PBSfjVdjb~5oPIfUbtd6~XDEWeW9f9i~sqGkVxMuMR~fUS-Ay2M9Z~ML8s4PH95U~MkgAbGkXH6~RybylJRnhJ~TcgCqYbydo~wEhO86jcco~leIwAgTj8E~I2lfHE5kDb~CiSz61UwrQ~NU3zgypfFy~pzzjRSV6ZO~GX5cZxE2GY~RcahSSzeRf~Ie2c51_4Sp~_3oeEue7S7~q3eUobDMJW~wKl4cqK7Gl~aKhT3n4RHZ~3Vtp7n-t0Z~1F9SMtTyiX~jH0uD88V6F~K8esoIs2eW~b_G3UDfpN0~yZf1XmIy-U~nriWjM9urd~8p7FrLtVHU~gpglyfLkWs~jEoxuA2PIS~aMSPvw-ONW~X_1kwTzaXt~ZKaEaSznut~zZZn32I7eS~44pdhtPlNE~qtVr8SCFs5~4rDNkkAuj_~VN7cgWyMmg~xwreRQ-lzj~pa4LoD4xuT~Lt-oEicbBr~Ngz9KxUrJt~BU9SQkS-zU~cBCZ7AW8P7~3m96uv1ItV~-o--a5rIBR~Hry6GxyqEm~qWFESUmfEs~X4Eo-DdiUB~9wN-K8_crj~t5TdQ1_z8-~sWnpdresEj~fbUyQrXMR3~4i9bTBXFoE~W4_X_Af3yY~FuiUhV49xc~V2duETde5d~3gc3uGrU1V~B_OtVkMSZT~xjfPXTyrpQ~iFcW6hPGPU~EGefOqA6KB~RokSaRBUGr~y0H0q1mN2T~lH5YZxnbfC~kGYw4gQ11Z~nQRrj5c6w_~MSNRmMUDgC~3W4zqr4Xlx~y8GNntYHsi~WVrsHleeCL~ouiK2OKQ-A~tgP8r-gOe_~OgdypjrwdX~rOnsP2Q5UN~w8ffkPoJ_S~uaW8ZI1LWH~q_J28dYJ9d~QYP1NVhSHo~HY55MqmzzQ~ujS7cIBGO-~kjfJ5uXq4m~BG8I5WOok9~ZBoVMjk2oM~Hvc3ekMyyh~TWrozby2UO~iVTmZJMGJj; __utma=235335808.595109545.1589624370.1608554220.1608993269.47; __cfduid=d886e1283a32ddefb8203a25624224b271610536713; __cf_bm=193fe463ee29bab826a943922fce860946cbb298-1612179260-1800-AeCcIJ+1x6B3dJgYQXvMKJeUPnFSDXe4MAv/E+EsPnydJEX6L24U1Me8zzV6IIAQdigqfO0lSuh/J+ZbvxnUWNazLxdKeuk7TH86SvccifLE+bRQSph+InIqGwe2CxjiXhq3YGWzP2LeAhtmn8bAA55mUpVf5OUBbBsifwy2APCb; ki_t=1589624462462%3B1612179267983%3B1612179312225%3B35%3B58; _gid=GA1.2.1417072303.1612179393",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        }
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

