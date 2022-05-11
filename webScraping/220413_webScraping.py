from urllib.request import urlopen
from urllib.parse import urlparse
from attr import attr
from bs4 import BeautifulSoup
import re
import pymysql

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
connection = pymysql.connect(host="localhost:3308" user="admin" passwd="1234" db="mysql" charset="utf8")
cursor = connection.cursor()
cursor.execute("USE ")