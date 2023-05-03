# %% Extracting data from a website like allrecipes.
import requests, csv
from bs4 import BeautifulSoup
import json

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

urllist = getallurl('bbq')
# %%
print('==============================')

def checkrecipe(url):
    recpage = requests.get(url)
    rechtml = BeautifulSoup(recpage.content, 'html.parser')
    reclijst = rechtml.find(id="allrecipes-schema_1-0", attrs={'type':'application/ld+json'})
    #['headline']
    #print(reclijst)
    return reclijst

def readrecipecontent():
    #for loop
    reclijst = checkrecipe(urllist[0])
    for data in reclijst:
        recipecontent = json.loads(data.string)
    
    return recipecontent

recipecontent = readrecipecontent()
print(json.dumps(recipecontent, indent=4))


# %%
#for url in urllist:
#    checkrecipe(url)
#    print('nice one')
# %%
with open('Recipe.csv', "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "UserID", "Cookingtime","Cookingdescription", "cookingutensilsID", "BbqID", "mealtype", "Rating", "Photo", "Intro", "diettype"])
                                                                               #should be recipeInstructions                                 
    writer.writerow([recipecontent['headline'], 0, recipecontent['totalTime'], recipecontent['description'], \
                     'empty', recipecontent['headline'], recipecontent['headline'], recipecontent['headline'],\
                        recipecontent[''], recipecontent['description'], recipecontent['headline']])
#still needs some stuff done above: It will probably