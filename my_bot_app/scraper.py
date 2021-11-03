import requests
from bs4 import BeautifulSoup
from bs4 import element
import abc
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image
import time
import os


class School(abc.ABC):
    def __init__(self, sasasa):
        self.sasasa = sasasa

    @abc.abstractmethod
    def scrape(self):
        pass


class bulletin(School):
    def scrape(self):
        re = requests.get("http://www.saihs.edu.tw/")
        soup = BeautifulSoup(re.content, "lxml")
        title = soup.find("div", {"class": "panel-panel panel-col"}
                          ).find("h2").string.replace(" ", "").replace("\n", "")
        content = "---{}---\n".format(title)
        tr = soup.find(
            "table", {"class": "views-table cols-4"}).tbody.find_all("tr")
        for i in tr:
            hr = i.find("a").get("href")
            info = i.find(
                "td", {"class": "views-field views-field-phpcode"}).text
            where = i.find(
                "td", {"class": "views-field views-field-value"}).string.replace(" ", "").replace("\n", "")
            date = i.find(
                "td", {"class": "views-field views-field-created"}).string.replace(" ", "").replace("\n", "")
            content += "{}\n出處:{}\n日期:{}\n連結:http://www.saihs.edu.tw/{}\n\n-----\n".format(
                info, where, date, hr)
        return content
