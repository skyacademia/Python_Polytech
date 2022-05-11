# 네이버 영화의 박스오피스 1~10위까지의 영화 제목과 줄거리를 csv에 저장

from urllib.request import Request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import csv

url = "https://movie.naver.com/#none"

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화
browser.get(url)
movies_info = []

filename = "movie.csv"
f = open(filename,"w",encoding="utf-8-sig", newline="")
writer = csv.writer(f)

for i in range(1,11):
    browser.find_element(by=By.LINK_TEXT,value="박스오피스").click()
    browser.find_element(by=By.CLASS_NAME,value="item{}".format(i)).click()
    
    movie_url=browser.current_url

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
    res = requests.get(movie_url,headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text,"lxml")
    title_frame = soup.find("h3",attrs={"class":"h_movie"})
    movie_info = []
    movie_info.append(title_frame.find("a").get_text())

    story_area = soup.find("div",attrs={"class":"story_area"})

    # text = story_area.find("h5",attrs={"class":"h_tx_story"}).get_text()
    text= story_area.find("p",attrs={"class":"con_tx"}).get_text()
    movie_info.append(text)
    movies_info.append(movie_info)
    browser.back()

for movie in movies_info :
    writer.writerow(movie)