# 네이버 영화의 박스오피스 1~10위까지의 영화 제목, 감독, 국가, 개봉연도, 장르, 영상길이, 등급

from urllib.request import Request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import csv
import re

# 네이버 영화 웹페이지 접속
url = "https://movie.naver.com/#none"

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화
browser.get(url)
movies_info = []

filename = "movie.csv"
f = open(filename,"w",encoding="utf-8-sig", newline="")
writer = csv.writer(f)

# 총 10개의 영화를 스크래핑 실시
for i in range(1,11):
    # 박스오피스에 있는 영화 선택
    browser.find_element(by=By.LINK_TEXT,value="박스오피스").click()
    browser.find_element(by=By.CLASS_NAME,value="item{}".format(i)).click()
    
    # 클릭 후 BeatuifulSoup을 이용하여 웹페이지 정보 가져오기
    movie_url=browser.current_url
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
    res = requests.get(movie_url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")

    # 영화 제목
    title_area = soup.find("h3",attrs={"class":"h_movie"})
    
    movie_info = []
    movie_info.append(title_area.find("a").get_text())

    # 영화의 장르, 제작국가, 상영시간, 개봉날짜 가져오기
    information_area = soup.find("dl", attrs={"class":"info_spec"})
    information_pointer = information_area.find("dt",attrs={"class":"step1"}).find_next_sibling("dd")

    informations = information_pointer.find_all("span")
    for info in informations : 
        text = info.get_text().replace("\r","")
        text = text.replace("\t","")
        text = text.replace("\n","")
        text = text.strip()
        movie_info.append(text)

    # 영화의 감독 가져오기
    information_pointer=information_area.find("dt",attrs={"class":"step2"}).find_next_sibling("dd")
    movie_info.append(information_pointer.find("a").get_text())
    
    information_pointer=information_area.find("dt",attrs={"class":"step4"}).find_next_sibling("dd")
    movie_info.append(information_pointer.find("a").get_text())
    
    movies_info.append(movie_info)
    browser.back()

for info in movies_info : 
    if re.match("^[0-9]{4}[.][0-9]{2}[.][0-9]{2} 개봉",info[4]) :
        info[4]=re.match("^[0-9]{4}[.][0-9]{2}[.][0-9]{2}",info[4]).group()

    if re.match("^[0-9]{4}[.][0-9]{2}[.][0-9]{2} 재개봉",info[4]) :
        info[4]=re.match("^[0-9]{4}[.][0-9]{2}[.][0-9]{2}",info[4]).group()

writer.writerow(["제목","장르","국가","상영 시간","개봉일","감독","상영등급"])
for movie in movies_info :
    writer.writerow(movie)
print("박스오피스 영화 목록 작성이 완료되었습니다.")