import mysql.connector
import pandas as pd
from datetime import date

with open('recipe_voorbeeld.csv') as csvfile:
    csvreader = pd.read_csv(csvfile)
    df = pd.DataFrame(csvreader)
    df["Rating"] = [3, 4]
    df["DateCreate"] = [date.today(), date.today()]
    new_df = df[["recipe_title", "recipe_author",\
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
        RecipeID bigint NOT NULL,\
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
        DateCreate datetime,\
        PRIMARY KEY(RecipeID));")
        cursor.execute("select * from recipes")
        record = cursor.fetchall()
        print("You're connected to database: ", record)
        for x in new_df["recipe_title"]:
            rows = len(record)
            if rows != 0:
                if x not in record[1]: #mss geen dubbele loop nodig, aan csv vragem.
                    print("niet hetzelfde, toevoegen!")
            else:
                print("lege lijst, voeg toe")
                for y in range(0, len(new_df)):
                    lists = [new_df["recipe_title"][y],new_df["recipe_author"][y],new_df["prep_time"][y],new_df["recipe_description"][y],new_df["recipe_directions"][y], new_df["status"][y], new_df["Rating"][y], new_df["recipe_image"][y], new_df["recipe_note"][y], new_df["recipe_category"][y], new_df["DateCreate"][y]]
                    sqlcode = "INSERT INTO `recipes` (`RecipeTitle`, `UserId`,\
                                `PrepTime`, `PrepText`, `CookAttireId`, `BBQId`,\
                                `Rating`, `Foto`, `Intro`, `Diet`, `DateCreate`)\
                                 VALUES ("+ lists[0] + ","+ lists[1] + ","+ str(lists[2]) + ","+ lists[3] + ","+ lists[4] + ","+ str(lists[5]) + ","+ str(lists[6]) + ","+ str(lists[7]) + ",",  lists[8] + "," +  lists[9] + ",NOW());"
                    print(sqlcode)
                    cursor.execute("""INSERT INTO `recipes` (`RecipeTitle`, `UserId`,
                                   `PrepTime`, `PrepText`, `CookAttireId`, `BBQId`,
                                   `Rating`, `Foto`, `Intro`, `Diet`, `DateCreate`)
                                   VALUES ('"""+ lists[0] + "','"+ lists[1] + "','"+ str(lists[2]) + "','"+ lists[3] + "','"+ lists[4] + "','"+ str(lists[5]) + "','"+ str(lists[6]) + "','"+ str(lists[7]) + "','",  lists[8] + "','" +  lists[9] + "','NOW()');")

                # the connection is not autocommited by default. So we must commit to save our changes.
                connection.commit()              
            print(x)

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
finally:
    print("MySQL connection is closed")

cursor.close()
connection.close()