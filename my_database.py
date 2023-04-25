import mysql.connector
import pandas as pd
with open('recipe_voorbeeld.csv') as csvfile:
    csvreader = pd.read_csv(csvfile)
    df = pd.DataFrame(csvreader)

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='griller',
                                         user='root',
                                         password='')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select * from ingredients")
        record = cursor.fetchall()
        for x in record:
            print(x)
        print("You're connected to database: ", record)

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
finally:
    print("MySQL connection is closed")

cursor.close()
connection.close()