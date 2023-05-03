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

def readrecipecontent(url):
    #for loop
    
    reclijst = checkrecipe(url)
    for data in reclijst:
        recipecontent = json.loads(data.string)
    
    return recipecontent



# %%
#for url in urllist:
#    checkrecipe(url)
#    print('nice one')
# %%
#instructions = []

#for i in range(0,len(recipecontent[0]['recipeInstructions'])):
#    instructions += [list(recipecontent[0]['recipeInstructions'][i].values())[5]]
    

#%%

with open('Recipe.csv', "w", encoding="utf-16") as f:
    writer = csv.writer(f,delimiter=',',quotechar="'")
    writer.writerow(["Title", "UserID", "Cookingtime","Cookingdescription", "cookingutensilsID", "BbqID", "mealtype", "Rating", "Photo", "Intro", "diettype"])
    
    for url in urllist:                                                                            #should be recipeInstructions    
        recipecontent = readrecipecontent(url)
        print(json.dumps(recipecontent, indent=4))                             
        #writer.writerow([recipecontent[0]['headline'], 0, recipecontent[0]['totalTime'], list(recipecontent[0]['recipeInstructions'][0].values())[2], \
                            #1, 1, recipecontent[0]['recipeCategory'], list(recipecontent[0]['aggregateRating'].values())[1],\
                            #list(recipecontent[0]['image'].values())[1], recipecontent[0]['description'], 'vlees'])
        # %%
