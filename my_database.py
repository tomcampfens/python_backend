import mysql.connector
import pandas as pd
from datetime import date

with open('recipe_voorbeeld.csv') as csvfile:
    csvreader = pd.read_csv(csvfile)
    df = pd.DataFrame(csvreader)
    df["Rating"] = [3, 4]
    df["DateCreate"] = [date.today(), date.today()]
    new_df = df[["recipe_title", "article_id",\
                "prep_time", "recipe_description",\
                "recipe_directions", "status",\
                "Rating", "recipe_image",\
                "recipe_note", "recipe_category", "DateCreate"]]

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='griller',
                                         user='root',
                                         password='')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS recipes (\
        RecipeID bigint NOT NULL AUTO_INCREMENT,\
        RecipeTitle varchar(255),\
        UserId bigint,\
        PrepTime bigint,\
        PrepText varchar(255),\
        CookAttireId bigint,\
        BBQId bigint,\
        Rating bigint,\
        Foto varchar(255),\
        Intro varchar(255),\
        Diet enum('Dessert', 'vis', 'vlees'),\
        DateCreate datetime default now(),\
        PRIMARY KEY(RecipeID));")
        cursor.execute("select * from recipes")
        record = cursor.fetchall()
        print("You're connected to database: ", record)
        rows = len(record)
        for x in range(0, len(new_df["recipe_title"])):
            if rows != 0:
                cursor.execute("select * from recipes")
                record = cursor.fetchall()
                if new_df["recipe_title"][x] not in [z[1] for z in record]: #mss geen dubbele loop nodig, aan csv vragem.
                    print('oke, nieuwe!')
                    lists = [new_df["recipe_title"][x],new_df["article_id"][x],new_df["prep_time"][x],new_df["recipe_description"][x],new_df["recipe_directions"][x], new_df["status"][x], new_df["Rating"][x], new_df["recipe_image"][x], new_df["recipe_note"][x], new_df["recipe_category"][x], new_df["DateCreate"][x]]
                    sqlcode = "INSERT INTO `recipes` (`RecipeTitle`, `UserId`,\
                       `PrepTime`, `PrepText`, `CookAttireId`, `BBQId`,\
                       `Rating`, `Foto`, `Intro`, `Diet`, `DateCreate`)\
                        VALUES ('"+ lists[0] + "','"+ str(lists[1]) + "','"+ str(lists[2]) + "','"+ lists[3] + "','"+ lists[4] + "','"+ str(lists[5]) + "','"+ str(lists[6]) + "','"+ str(lists[7]) + "','" + lists[8] + "','" +  lists[9] + "', now());"
                    print(sqlcode)
                    cursor.execute(sqlcode) 
                    rows +=1
                else:
                    print("HOHO, hetzelfde")
            else:
                print("lege lijst, voeg toe")
                lists = [new_df["recipe_title"][x],new_df["article_id"][x],new_df["prep_time"][x],new_df["recipe_description"][x],new_df["recipe_directions"][x], new_df["status"][x], new_df["Rating"][x], new_df["recipe_image"][x], new_df["recipe_note"][x], new_df["recipe_category"][x], new_df["DateCreate"][x]]
                sqlcode = "INSERT INTO `recipes` (`RecipeTitle`, `UserId`,\
                       `PrepTime`, `PrepText`, `CookAttireId`, `BBQId`,\
                       `Rating`, `Foto`, `Intro`, `Diet`, `DateCreate`)\
                        VALUES ('"+ lists[0] + "','"+ str(lists[1]) + "','"+ str(lists[2]) + "','"+ lists[3] + "','"+ lists[4] + "','"+ str(lists[5]) + "','"+ str(lists[6]) + "','"+ str(lists[7]) + "','" + lists[8] + "','" +  lists[9] + "', now());"
                print(sqlcode)
                cursor.execute(sqlcode)
                rows +=1
                # the connection is not autocommited by default. So we must commit to save our changes.
            connection.commit()              
            print(x)

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
finally:
    print("MySQL connection is closed")

cursor.close()
connection.close()