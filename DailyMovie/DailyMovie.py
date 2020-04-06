import queue
import threading
import traceback
from bs4 import BeautifulSoup
from urllib import request
import re
from urllib.parse import urljoin
import os
from AddFocus import AddFocus
from logger import Logger
import datetime
import time


class DailyMovie(object):
    def __init__(self, url):
        self.url = url
        self.allowed_domain = self.url.split("www.")[1]
        self.logger = Logger("daily_movie")

    downloadLinks = []
    movie_page_links = set()
    movie_page_queue = queue.Queue(maxsize=-1)
    isNeedToChange = None
    filePath = None
    allowed_domain = None

    def setPath(self):
        desktopPath = os.path.join(os.path.expanduser("~"), 'Desktop')
        self.filePath = desktopPath + "/{}.txt".format(self.allowed_domain)

    def openPage(self, url):
        webHeader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close'
        }
        try:
            req = request.Request(url=url, headers=webHeader)
            page = request.urlopen(req)
            a = page.getcode()
            if a != 200:
                print("获取页面失败", str(a))
            pageData = page.read()
            pageData = pageData.decode("gb18030", "ignore")
            page.close()
            return pageData
        except BaseException as error:
            print(error)

    def get_movie_page_links(self):
        fList = ["综艺", "电视剧", "设为主页", "彩票购买", "动漫", "国产剧", "美剧", "韩剧",
                 "港台剧", "剧集", "单机游戏", "游戏资源"]

        homePageUrl = self.url

        pageContent = self.openPage(homePageUrl)
        soup = BeautifulSoup(pageContent, 'html.parser')
        tags = soup.find_all('a')
        for tag in tags:
            try:
                if "http" in tag['href'] or "javascript" in tag['href'] or "index" in tag['href']:
                    continue
                else:
                    count = 0
                    for word in fList:
                        if word in tag.text:
                            count += 1
                    if count == 0:
                        if tag['href'] not in self.movie_page_links:
                            self.movie_page_queue.put(tag['href'])
                            self.movie_page_links.add(tag['href'])

            except BaseException as err:
                print("get movie page links error: {}".format(err))

        self.logger.info("start visiting")
        self.logger.info("total links to visit：{}".format(len(self.movie_page_links)))

    def get_download_links(self):
        """
        获取下载地址
        """
        while True:
            try:
                partial_movie_link = self.movie_page_queue.get(True, 20)
            except queue.Empty:
                break
            else:
                if "javascript" not in partial_movie_link:
                    movieUrl = urljoin(self.url, partial_movie_link)
                    try:
                        time.sleep(0.4)
                        moviePage = self.openPage(movieUrl)
                        moviePageSoup = BeautifulSoup(moviePage, 'html.parser')
                        moviePageTags = moviePageSoup.find_all('a')
                        for moviePageTag in moviePageTags:
                            if "ftp" in moviePageTag['href'] or "magnet" in moviePageTag['href']:
                                movie_name = DailyMovie.get_movie_name(moviePage)
                                print("<{}>".format(movie_name))
                                releaseTime = self.getReleaseTime(moviePage)
                                release_time = DailyMovie.tran_rtime(releaseTime)
                                grade = DailyMovie.getGrade(moviePage)
                                movieLinkItem = (
                                    release_time, movie_name,
                                    moviePageTag.text + " " + "发布时间：{} 豆瓣评分：{}".format(releaseTime, grade))

                                if movieLinkItem not in self.downloadLinks:
                                    self.downloadLinks.append(movieLinkItem)
                                    # print(movieLinkItem)

                    except Exception as error2:
                        print("get download links error: {}".format(error2))
                        with open("error.log", 'a+') as f:
                            f.write("get download links\n" + movieUrl + "\n" + traceback.format_exc() + "\n\t")

    def save_links(self):
        """
        将下载地址写到本地
        """
        focus_films = AddFocus.add_focus()
        self.downloadLinks.sort(key=lambda rtime: rtime[0], reverse=True)
        count = 0
        with open(self.filePath, "w+") as f:
            f.write("==============================================" + "\n")
            f.write("来自{}的下载链接".format(self.allowed_domain) + "\n")
            f.write("==============================================" + "\n")
            try:
                for link in self.downloadLinks:
                    appear = 0
                    for focus_film in focus_films:
                        if focus_film in link[1] or focus_film in link[2]:
                            appear += 1

                    if appear > 0:
                        f.write("======@{}@======【{}】".format("关注的", link[1]) + link[2] + "\n")
                    f.write("【{}】".format(link[1]) + link[2] + "\n")
                    count += 1
            except IOError as error_info:
                print("save links error: {}".format(error_info))
                with open("error.log", 'a+') as f_e:
                    f_e.write("save links\n" + traceback.format_exc() + "\n\t")

            f.write("下载链接总数：%d" % count)
            self.logger.info("download links have been saved")

    def save_download_links(self, thread):
        while thread.is_alive():
            time.sleep(2)
        self.save_links()
        self.logger.info("finished")

    @staticmethod
    def get_movie_name(page):
        rexg = re.compile(r'译\s+名(.*?)\<\/p')
        try:
            name = re.findall(rexg, page)
            if len(name) == 0:
                rexg = re.compile(r'片\s+名(.*?)\<\/p')
                name = re.findall(rexg, page)
                if len(name) == 0:
                    return None
                else:
                    return name[0].strip()
            else:
                return name[0].strip()
        except Exception as e:
            print("get movie name error: {}".format(e))

    def getReleaseTime(self, page):
        # 获取电影发布日期
        try:
            rexg_1 = re.compile(r'上映日期(.*?)\<\/p')  # 2018
            rexg_2 = re.compile(r'上映日期(.*?)\<br')  # ygdy
            if "dy2018.com" in self.allowed_domain:
                releaseTime = re.findall(rexg_1, page)
                if len(releaseTime) != 0:
                    return releaseTime[0].strip()
                else:
                    return None
            elif "ygdy8.com" in self.allowed_domain:
                releaseTime = re.findall(rexg_2, page)

                if len(releaseTime) > 0:
                    return releaseTime[0].strip()
                else:
                    return None
        except BaseException as info_1:
            print("getReleaseTime error：{}".format(info_1))

    @staticmethod
    def tran_rtime(releaseTime):
        # 将获取的字符串发布时间转换为数字
        if releaseTime is None:
            release_time = 0
            return release_time
        else:
            if "/" in releaseTime:
                release_time = re.sub("\D", "", releaseTime.split("/")[0])
                return int(release_time)
            else:
                release_time = re.sub("\D", "", releaseTime)
                return int(release_time)

    @staticmethod
    def getGrade(page):
        # 获取电影评分
        rexg = re.compile(r'\b豆瓣评分\s+(.*?)\/')
        grade = re.findall(rexg, page)
        if len(grade) >= 1:
            return grade[0]
        else:
            return "null"

    def checkTime(self):
        self.setPath()
        now = datetime.date.today()  # 返回datetime.date类型
        if os.path.exists(self.filePath):
            t_time = os.path.getctime(self.filePath)
            f_time = datetime.datetime.fromtimestamp(t_time)
            cTime = f_time.strftime("%Y-%m-%d")
            if cTime == str(now):
                self.isNeedToChange = False
                self.logger.info("file is last-updated")
                time.sleep(5)
            else:
                self.isNeedToChange = True
        else:
            self.isNeedToChange = True

    def start(self):
        threads = []
        self.checkTime()
        if self.isNeedToChange:
            job_get_movie_page_links = threading.Thread(target=self.get_movie_page_links,
                                                        name="get_movie_page_links")
            threads.append(job_get_movie_page_links)
            job_get_download_links = threading.Thread(target=self.get_download_links,
                                                      name="get_download_links")
            threads.append(job_get_download_links)
            job_save_links = threading.Thread(target=self.save_download_links,
                                              args=(job_get_download_links,),
                                              name="save_links")
            threads.append(job_save_links)
            try:
                for thread in threads:
                    thread.start()
            except BaseException as err_2:
                print("start error {}: ".format(err_2))
                with open("error.log", 'a+') as f_e:
                    f_e.write("start\n" + traceback.format_exc() + "\n\t")
        else:
            pass

    @staticmethod
    def doTest():
        # url = "https://www.dy2018.com/"
        url = "https://www.ygdy8.com"
        dm = DailyMovie(url)
        dm.get_download_links()


if __name__ == '__main__':
    dailyMovie = DailyMovie("https://www.dy2018.com")
    dailyMovie.start()


