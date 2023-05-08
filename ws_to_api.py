# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

# %%
def getInfoVanDetail(nwurl):
    print("we gaan deze bezoeken", nwurl)

def getallurl(zoekterm):
    page = requests.get('https://www.allrecipes.com/search?q='+zoekterm)
    dehtml = BeautifulSoup(page.content, 'html.parser')
    delijst = dehtml.find(id='search-results__content_1-0')
    lijsteen = []
    cardurl = ''
    for card in delijst.find_all('a'):
        cardurl = card['href']
        getInfoVanDetail(cardurl)
        lijsteen.append(cardurl)
    return lijsteen

# %%
urllist = getallurl('bbq')
urlrec = []
substr = 'recipes.com/recipes/'
for url in urllist:
    print(url)
    if substr in url:
        print(True)
    else:
        print(False)
        urlrec.append(url)
# %%
def checkrecipe(url):
    recpage = requests.get(url)
    rechtml = BeautifulSoup(recpage.content, 'html.parser')
    reclijst = rechtml.find(id="allrecipes-schema_1-0", attrs={'type':'application/ld+json'})
    return reclijst

def readrecipecontent(url):
    #for loop
    reclijst = checkrecipe(url)
    for data in reclijst:
        recipecontent = json.loads(data.string)
    return recipecontent

for url in urlrec:
    recipecontent = readrecipecontent(url)
    print(json.dumps(recipecontent, indent=4)) 
