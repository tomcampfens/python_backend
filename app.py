# %%
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

from flask import Flask
from flask_mysqldb import MySQL
#from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'griller'
 
mysql = MySQL(app)

def getallurl(zoekterm):
    page = requests.get('https://www.allrecipes.com/search?q='+zoekterm)
    dehtml = BeautifulSoup(page.content, 'html.parser')
    delijst = dehtml.find(id='search-results__content_1-0')
    lijsteen = []
    cardurl = ''
    for card in delijst.find_all('a'):
        cardurl = card['href']
        lijsteen.append(cardurl)
    return lijsteen

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

def checkurl(url):
    substr = 'recipes.com/recipes/'
    substr2 = 'recipes.com/article/'
    #print(url)
    if substr in url:
        print(True)
        pass
    elif substr2 in url:
        print(True)
        pass
    else:
        print(False)
        return url
    
@app.route("/recipes", methods = ["GET","POST"])
def recipes():
    cursor = mysql.connection.cursor()
    record = cursor.execute("select * from recipes")
    recipes = cursor.fetchall()
    df = pd.DataFrame(recipes)
    result = df.to_json()
    parsed = json.loads(result)
    recjson = json.dumps(parsed, indent=4, default=str)
    print("MySQL connection is closed")
    cursor.close()
    return recjson

@app.route("/ingredients", methods = ["GET","POST"])
def ingredients():
    cursor = mysql.connection.cursor()
    record = cursor.execute("select * from ingredients")
    ingredients = cursor.fetchall()
    df = pd.DataFrame(ingredients)
    result = df.to_json()
    parsed = json.loads(result)
    ingjson = json.dumps(parsed, indent=4, default=str)
    cursor.close()
    return ingjson

@app.route("/dump")
def dump():
    with open('griller.json') as f:
        q = json.loads(f.read())
    return json.dumps(q, indent = 4)
