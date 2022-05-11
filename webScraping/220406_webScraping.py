from urllib.request import urlopen
from urllib.parse import urlparse
from attr import attr
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
site = "https://www.chicagomag.com/chicago-magazine/november-2020/sandwich-city/the-10-best-sandwiches/"
res = requests.get(site,headers=header)
res.raise_for_status()
bs = BeautifulSoup(res.text, "lxml")
siteTitle=bs.find_all("figure",attrs={"class":"capsule"})
ranking_num = []
menu_list = []
price = []
market = []

# 가게명 추출
for site in siteTitle :
    market_name = site.find_all("h2")[1].get_text()
    market.append(market_name)

# 가게 메뉴와 랭킹 추출
for site in siteTitle : 
    rankingNumber = site.find("h2").get_text()
    menus = list(site.find("p"))
    if(menus is not None):
        menu_tuple = (menus[0].get_text(),menus[2].get_text().strip())
        menu_list.append(menu_tuple)
        ranking_num.append(rankingNumber)


# 가격 추출
contents = bs.find_all("div",attrs={"class":"content post"})
for content in contents:
    text = content.get_text()
    price=(re.findall(r"\$\w+\.\w{0,2}",text))


# 데이터 병합(pandas 이용)
df = pd.DataFrame({"Ranking":ranking_num,"Market":market, "Menu":menu_list, "Price":price})
df.set_index("Ranking",inplace=True)
print(df)
df.to_csv("sandwich.csv",encoding="utf-8")