# %% Extracting data from a website like allrecipes.
import requests
from bs4 import BeautifulSoup
import json
import mysql.connector
import re
#%%
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
    print(url)
    if substr in url:
        print(True)
        pass
    elif substr2 in url:
        print(True)
        pass
    else:
        print(False)
        return url
# %%
urllist = getallurl('beef')
urlrec = []
count = 0

for url in urllist:
    if checkurl(url) != None:
        urlrec.append(checkurl(url))
    else:
        pass
    
#%% Writing data to DataBase in SQL.
instructions = ""
instruction = ""
description = ""
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='griller',
                                         user='root',
                                         password='')
    if connection.is_connected():
        # Here we start with creating a recipe table
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS recipes (\
        RecipeID bigint NOT NULL AUTO_INCREMENT,\
        RecipeTitle varchar(255),\
        UserId bigint,\
        PrepTime varchar(255),\
        PrepText varchar(255),\
        CookAttireId bigint,\
        BBQId bigint,\
        Rating double,\
        Foto varchar(255),\
        Intro varchar(255),\
        Diet enum('Dessert', 'vis', 'vlees'),\
        DateCreate datetime default now(),\
        PRIMARY KEY(RecipeID));")
        cursor.execute("select * from recipes")
        record = cursor.fetchall()
        print("You're connected to database: ", record)
        rows = len(record)

        for url in urlrec: 
            recipecontent = readrecipecontent(url)
            print(json.dumps(recipecontent, indent=4))
            for i in range(0,len(recipecontent[0]['recipeInstructions'])):
                u = len(list(recipecontent[0]['recipeInstructions'][i].values())) - 1
                instruction = list(recipecontent[0]['recipeInstructions'][i].values())[u] 
                instructions += instruction
                instructions = instructions.replace(",", "@")
            instructions = '"{0}"'.format(instructions)
            description = recipecontent[0]['description']
            description = description.replace(",", "@")
            description = description.replace('"', "'")
            description = description.replace("&#39;", "$")
            description = '"{0}"'.format(description)
            image = '"{0}"'.format(list(recipecontent[0]['image'].values())[1])
            recipeTitle = recipecontent[0]['headline']
            recipeTitle = recipeTitle.replace("&#39;", "$")

            df = [recipeTitle, 0, recipecontent[0]['totalTime'],instructions, \
                1, 1, list(recipecontent[0]['aggregateRating'].values())[1],\
                image, description, 'vlees']
            if rows != 0:
                cursor.execute("select * from recipes")
                record = cursor.fetchall()
                if df[0] not in [z[1] for z in record]: #mss geen dubbele loop nodig, aan csv vragem.
                    print('oke, nieuwe!')
                    sqlcode = "INSERT INTO `recipes` (`RecipeTitle`, `UserId`,\
                    `PrepTime`, `PrepText`, `CookAttireId`, `BBQId`,\
                    `Rating`, `Foto`, `Intro`, `Diet`, `DateCreate`)\
                        VALUES ('"+ df[0] + "','"+ str(df[1]) + "','"+ df[2] + "','"+ df[3] + "','"+ str(df[4]) + "','"+ str(df[5]) + "','"+ str(df[6]) + "','"+ df[7] + "','" + df[8] + "','" +  df[9] + "', now());"
                    print(sqlcode)
                    cursor.execute(sqlcode) 
                    rows +=1
                else:
                    print("HOHO, hetzelfde")
            else:
                print("lege lijst, voeg toe")
                sqlcode = "INSERT INTO `recipes` (`RecipeTitle`, `UserId`,\
                    `PrepTime`, `PrepText`, `CookAttireId`, `BBQId`,\
                    `Rating`, `Foto`, `Intro`, `Diet`, `DateCreate`)\
                    VALUES ('"+ df[0] + "','"+ str(df[1]) + "','"+ df[2] + "','"+ df[3] + "','"+ str(df[4]) + "','"+ str(df[5]) + "','"+ str(df[6]) + "','"+ df[7] + "','" + df[8] + "','" +  df[9] + "', now());"
                print(sqlcode)
                cursor.execute(sqlcode)
                rows +=1
                # the connection is not autocommited by default. So we must commit to save our changes.
            connection.commit()              
            description = ""
            instructions = ""
        
        #Here we start creatinge and filling an ingredient table
        cursor.execute("CREATE TABLE IF NOT EXISTS ingredients (\
        IngredientID bigint NOT NULL AUTO_INCREMENT,\
        Name varchar(255),\
        PRIMARY KEY(IngredientID));")
        cursor.execute("select * from ingredients")
        record2 = cursor.fetchall()
        rows2 = len(record2)
        for url in urlrec:
            recipecontent = readrecipecontent(url)
            for ingredient in recipecontent[0]["recipeIngredient"]:
                ingredientlist = re.split(',', ingredient)
                ingredient_imp_list = re.split('\s', ingredientlist[0])
                ingredient_imp = ingredient_imp_list[-1]
                if rows2 != 0:
                    cursor.execute("select * from ingredients")
                    record2 = cursor.fetchall()
                    if ingredient_imp not in [z2[1] for z2 in record2]:
                        print('nieuwe rij')
                        sqlcode = "INSERT INTO `ingredients` (`Name`)\
                                    VALUES ('" + ingredient_imp + "');"
                        #print(sqlcode)
                        cursor.execute(sqlcode) 
                        rows2 +=1
                    else:
                        print("HOHO, hetzelfde")
                else:
                    print("Lege lijst, voeg toe")
                    sqlcode = "INSERT INTO `ingredients` (`Name`)\
                                    VALUES ('" + ingredient_imp + "');"
                        #print(sqlcode)
                    cursor.execute(sqlcode) 
                    rows2 +=1
                connection.commit()
            
     
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
finally:
    print("MySQL connection is closed")

    cursor.close()
    connection.close()
# %%