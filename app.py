# %%
import requests, csv
from bs4 import BeautifulSoup
import json
from flask import Flask
#from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#df = pd.read_csv("recipe_voorbeeld.csv")
@app.route("/")
def read_csv():
    def getInfoVanDetail(nwurl):
        pass#print("we gaan deze bezoeken", nwurl)

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
    urlrec = []
    substr = 'recipes.com/recipes/'
    for url in urllist:
        print(url)
        if substr in url:
            print(True)
        else:
            print(False)
            urlrec.append(url)
        
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

    instructions = ""
    instruction = ""
    u = 0
    with open('Recipe.csv', "w", encoding="utf-8") as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(["Title", "UserID", "Cookingtime","Cookingdescription", "cookingutensilsID", "BbqID", "Rating", "Photo", "Intro", "diettype"])
        
        for url in urlrec: 
            recipecontent = readrecipecontent(url)
    return recipecontent

@app.route("/recipes")
def recipes():
    with open('Recipe.csv') as csvfile:
        csvreader = pd.read_csv(csvfile)
        df = pd.DataFrame(csvreader)
        return df.to_json()
