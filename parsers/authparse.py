from bs4 import BeautifulSoup
import requests

async def mainAuthParser(url:str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, "lxml")
    tags = soup.find_all("td", class_="td_3_column")
    return tags

def listConstructor(elements):
    result = {}
    for el in elements:
        name = el.find("a").get_text()
        link = el.find("a").get("href")
        result[name] = link 
    return result
          
async def countryCityParser(url:str, datafc):
    elements = await mainAuthParser(url=url)
    countrylist = listConstructor(elements)
    result = []
    for key, value in countrylist.items():
        if datafc in key.lower():
            result.append(key)
            result.append(value)
            break
    return result

async def RegDistKbParser(url:str):
    elements = await mainAuthParser(url=url)
    for i in range(len(elements)):
        elements[i] = elements[i].find("a").get_text()
    return elements
 
async def RegDistLinkParser(url:str, datafc):
    elements = await mainAuthParser(url=url)
    regionlist = listConstructor(elements)
    return [datafc,regionlist[datafc]]
    
  