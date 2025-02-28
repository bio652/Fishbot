from bs4 import BeautifulSoup
import requests
import re
import datetime
from data import data

FISHCLASSES = ["grid__oneday grid__oneday--current grid__col_0 grid__subcol",
               "grid__oneday grid__col_1 grid__subcol",
               "grid__oneday grid__col_2 grid__subcol",
               "grid__oneday grid__col_3 grid__last_day grid__subcol",
               "grid__oneday grid__col_4 grid__subcol"]

async def pageGet(url:str, userid):
    today = datetime.date.today()
    print(today, data.getPagedate(userid))
    if str(today) == str(data.getPagedate(userid)):
        soup = BeautifulSoup(data.getPage(userid), "lxml")
        print("soup is fresh")
        return soup
    else:
        res = requests.get(url=url)
        soup = BeautifulSoup(res.text, "lxml")
        data.setPage(userid=userid, page=str(soup), pagedate=today)
        print("soup wasnt fresh")
        return soup

def fishNamesArrConstructor(soup):
    fishnames = soup.find_all("div", class_="grid__left_panel fish")
    result = []
    for el in fishnames:
        br_tag = el.find('br')
        if br_tag:
            result.append(br_tag.next_sibling.strip().lower())
    return result

def fishNamesObjConstructor(soup):
    fishnames = soup.find_all("div", class_="grid__left_panel fish")
    rus = []
    eng = []
    result = {}
    for el in fishnames:
        eng.append(el.get("data-fish"))
        br_tag = el.find('br')
        if br_tag:
            rus.append(br_tag.next_sibling.strip().lower())
    for i in range(len(eng)):
        result[eng[i]] = rus[i]
    return result

async def oneFishCheck(url: str, namefu, userid):
    soup = await pageGet(url=url, userid=userid)
    fishnames = fishNamesObjConstructor(soup)
    for key, value in fishnames.items():
        if namefu in value:
            print("found one", key, value)
            return value
    return False

async def oneFishParser(url:str, datafu, userid):
    soup = await pageGet(url=url, userid=userid)
    fishnames = fishNamesObjConstructor(soup)
    curFish:str
    for key, value in fishnames.items():
        if datafu['fishname'] in value:
            print("found one", key, value)
            curFish = key
            break       
    fishData = soup.find("div", class_=FISHCLASSES[datafu['day']], attrs={"data-fish": f"{curFish}"})
    
    perArr = fishData.find_all("div", class_=re.compile(r"tt forecast bg_percent_\d+"))
    for i, el in enumerate(perArr):
        perArr[i] = el.find("div", class_=re.compile(r"forecast__value forecast__value--\d+")).get_text()
        
    comArr = fishData.find_all("div", class_="tt_box")
    for i, el in enumerate(comArr):
        comArr[i] = el.find("strong").get_text()
        
    comFin:str
    average_perArr =(int(perArr[0])+int(perArr[1])+int(perArr[2])+int(perArr[3]))/4
    if average_perArr >= 60:
        comFin = "🦈Шансы велики, однозначно стоит пробовать!"
    elif average_perArr >= 30:
        comFin = "🐟Если есть желание - можно и рискнуть)"
    elif average_perArr < 30:
        comFin = "🌊Эх, видимо сегодня не лучший день для ловли."
        
    print(perArr, comArr)
    return [perArr, comArr, comFin]
    
#allfishparser
async def allFishParser(url:str, userid):
    soup = await pageGet(url=url, userid=userid)
    fishNames = fishNamesArrConstructor(soup)
    
    fishData = soup.find_all("div", class_=FISHCLASSES[0], attrs={"data-fish": True})
    fdarr = []
    for el in fishData:
        fdarr.append(el.find_all("div", class_=re.compile(r"tt forecast bg_percent_\d+")))   
    for i, el in enumerate(fdarr):
        for j, el1 in enumerate(el):
            fdarr[i][j] = el1.find("div", class_=re.compile(r"forecast__value forecast__value--\d+")).get_text()
        fdarr[i] = (int(fdarr[i][0])+int(fdarr[i][1])+int(fdarr[i][2])+int(fdarr[i][3]))//4
        
    result = {}
    for i, el in enumerate(fishNames):
        result[fishNames[i]] = fdarr[i]
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:5])
    for key, value in result.items():
        if value == 0:
            print("one 0 to pop")
            result.pop(key)
    print(result)
    return result

#weather parser
WEATHERDAYSUBCLASSES = ["grid__oneday grid__oneday--current grid__col_0",
                        "grid__oneday grid__col_1",
                        "grid__oneday grid__col_2",
                        "grid__oneday grid__col_3 grid__last_day",
                        "grid__oneday grid__col_4"]

async def weatherParser(url:str, dayfu:int, userid):
    soup = await pageGet(url=url, userid=userid)
    #waterTemp
    waterTemp = soup.find("div",class_=f"{WEATHERDAYSUBCLASSES[dayfu]} grid__by_hiding temperature")
    waterTemp = waterTemp.find_all("span", class_="cel")
    for i, el in enumerate(waterTemp):
        waterTemp[i] = el.get_text()
    
    #windData
    windData = soup.find_all("div",class_=f"{WEATHERDAYSUBCLASSES[dayfu]} grid__subcol grid__by_hiding")
    windDirectionData = windData[1]
    windSpeedData = windData[2]
    windData.clear()
    #windSpeed
    windSpeedData = windSpeedData.find_all("div", class_=re.compile(r"tt wind_speed wind_speed-\d+"))
    for i, el in enumerate(windSpeedData):
        windSpeedData[i] = el.find("div", class_="tt_box")
        #windspeed
        winds = windSpeedData[i].find('span', class_='ms').get_text()
        windsMatch = re.search(r"скорость ветра (\d+)", winds)
        if windsMatch:
            winds = windsMatch.group(1)
        else:
            winds = "Точное значение не определено"
        #windgusts
        gusts = windSpeedData[i].get_text()
        gustsMatch = re.search(r"порывы до (\d+)", gusts)
        if gustsMatch:
            gusts = gustsMatch.group(1)
        else:
            gusts = "NA"
        #comentary
        com = windSpeedData[i].find_all('br')
        for j, el2 in enumerate(com):
            com[j] = el2.next_sibling.strip()
            if "порывы" in str(com[j]):
                com[j] = com[3].next_sibling.strip()
            break
        #finalformating
        windSpeedData[i] = [f"Скорость ветра: {winds} м/с",f"Порывы ветра до: {gusts} м/с",f"{com[0]}"]
    #windDir
    windDirectionData = windDirectionData.find_all("div", class_=re.compile(r"tt wind wind-[\d\w]+"))
    for i, el in enumerate(windDirectionData):
        windDirectionData[i] = el.find("div", class_="tt_box").get_text().strip()
    
    #Moon
    moonPhase = soup.find("div",class_=f"{WEATHERDAYSUBCLASSES[dayfu]} grid__by_hiding")
    #span checker - нужен в случае если в таблице имеется показатель по снегу, который ломает алгроритм для луны
    span_mt = moonPhase.find("span", class_="mt")
    if span_mt:
        moonPhase = span_mt.find_next("div", class_=f"{WEATHERDAYSUBCLASSES[dayfu]} grid__by_hiding")
        span_mt.clear()
    else:
        print("no spans<3")
        
    moonPhase = moonPhase.find("small").get_text(separator="<br>")
    moonPhase = [line for line in moonPhase.split("<br>") if "возраст:" in line][0].strip()
    
    result = [waterTemp, windSpeedData, windDirectionData, moonPhase]
    return result
