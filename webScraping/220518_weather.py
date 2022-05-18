import requests
import json
import datetime
import random

vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

service_key = "PEawh1fJV%2F6OnMG6wuhX0Aptr0KRM8mumNFZdHB8Sv%2FTP4JC00POYkQTrrLDMi6kPp%2BZjXh46SCPb81o84PW9g%3D%3D"
base_date = datetime.datetime.today().strftime("%Y%m%d") # 예) 20220518
base_time = "0800"
nx = "55"
ny = "123"
payload = "serviceKey="+service_key+"&"+"dataType=json"+"&"+"base_date="+base_date+"&"+"base_time="+base_time+"&"+"nx="+nx+"&"+"ny="+ny

pty_code = {"0":"없음","1":"비","2":"비/눈","3":"눈","4":"소나기","5":"빗방울","6":"빗방울/눈날림","7":"눈날림"}

data = dict()
data['data'] = base_date
weather = dict()

res = requests.get(vilage_weather_url+payload)
try:
    items = res.json().get('response').get('body').get('items')
    for item in items['item']:
        if item['category']=="TMP":
            weather['tmp'] = item['fcstValue']
        
        if item['category']=="PTY":
            weather['code'] = item['fcstValue']
            weather['state'] = pty_code[item['fcstValue']]
except:
    print("날씨 정보 요청 실패 : ",res.text)
data['weather'] = weather
print(data['weather'])


def get_pm10_state(pm10_value):
    if pm10_value<30:
        pm10_state = "좋음"
    elif pm10_value<80:
        pm10_state = "보통"
    elif pm10_value<150:
        pm10_state = "나쁨"
    else:
        pm10_state = "매우 나쁨"
    return pm10_state

def get_pm25_state(pm25_value):
    if pm25_value<30:
        pm25_state = "좋음"
    elif pm25_value<80:
        pm25_state = "보통"
    elif pm25_value<150:
        pm25_state = "나쁨"
    else:
        pm25_state = "매우 나쁨"
    return pm25_state


dust_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"

service_key = "PEawh1fJV%2F6OnMG6wuhX0Aptr0KRM8mumNFZdHB8Sv%2FTP4JC00POYkQTrrLDMi6kPp%2BZjXh46SCPb81o84PW9g%3D%3D"
base_date = datetime.datetime.today().strftime("%Y%m%d") # 예) 20220518
payload2 = "serviceKey="+service_key+"&"+"returnType=json"+"&"+"sidoName=인천"+"&"+"ver=1.0"

res = requests.get(dust_url+payload2)
result = res.json()
dust = dict()
if ((res.status_code==200)&(result['response']['header']['resultCode']=='00')):
    dust['PM10'] = {'value':int(result['response']['body']['items'][0]['pm10Value'])}
    dust['PM2.5'] = {'value':int(result['response']['body']['items'][0]['pm25Value'])}

    pm10_value = dust.get('PM10').get('value')
    pm10_state = get_pm10_state(pm10_value)
    pm25_value = dust.get('PM2.5').get('value')
    pm25_state = get_pm25_state(pm25_value)
    dust.get('PM10')['state'] = pm10_state
    dust.get('PM2.5')['state'] = pm25_state
else :
    print("미세먼지 가져오기 실패 : ", result['response']['header']['resultMsg'])
data['dust'] = dust
print(data['dust'])

rain_foods = "부대찌개,아구찜,해물탕,칼국수,수제비,짬뽕,우동,치킨,국밥,김치부침개,두부김치,파전".split(",")
pmhigh_foods = "콩나물국밥,고등어,굴,쌀국수,마라탕".split(',')

def get_foods_list(weather,dust_pm10,dust_pm25):
    if weather != "0":
        recommand_state = 'Case1'
        foods_list = random.sample(rain_foods,k=len(rain_foods))
    elif dust_pm10=="매우 나쁨" or dust_pm25=="매우 나쁨":
        recommand_state="Case2"
        foods_list=random.sample(pmhigh_foods,k=len(pmhigh_foods))
    else:
        recommand_state="Case3"
        foods_list=['']
    return recommand_state, foods_list

def naver_local_search(query,display):
    headers={"X-Naver-Client-Id":"8W_hkf6fkpUqGBgNgFKX", "X-Naver-Client-Secret":"Y2dXcMEN3j"}
    params={"sort":"comment","query":query,"display":display}
    naver_local_url = "https://openapi.naver.com/v1/search/local.json"
    res=requests.get(naver_local_url,headers=headers,params=params)
    res.raise_for_status()
    places = res.json().get('items')
    return places

weather = data.get('weather').get('code')
dust_pm10 = data.get('dust').get('PM10').get("state")
dust_pm25 = data.get('dust').get('PM2.5').get("state")

weather_state, foods_list = get_foods_list(weather, dust_pm10, dust_pm25)

location = "논현고잔동"
recommands = []
for food in foods_list :
    query = location + " " +food +" 맛집"
    result_list = naver_local_search(query,3)
    if len(result_list)>0:
        if weather_state =="Case3":
            recommands = result_list
            break
        else:
            recommands.append(result_list[0])
    else:
        print("검색 결과 없음")
    if len(recommands)==3:
        break
print(recommands)
