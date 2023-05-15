import pyodbc
server = 'powerbitrialserver.database.windows.net'
database = 'PowerBItrial'
username = 'bitestadmin'
password = '{abcd12!$}'   
driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        #cursor.execute("""IF OBJECT_ID(N'ingredientID', N'U') IS NULL
        #REATE TABLE ingredients (
        #IngredientID bigint PRIMARY KEY,
        #Name varchar(255));""")
        #cursor.execute("DROP TABLE recipes")
        cursor.execute('DROP TABLE recipes')
        cursor.execute("""IF OBJECT_ID(N'recipeID', N'U') IS NULL
        CREATE TABLE recipes (
                    RecipeID int IDENTITY(1,1) PRIMARY KEY,
                    RecipeTitle nvarchar(255),
                    UserId bigint, 
                    PrepTime nvarchar(255),
                    PrepText nvarchar(255),
                    CookAttireId bigint,
                    BBQId bigint,
                    Rating float,
                    Foto nvarchar(255),
                    Intro nvarchar(255),
                    [Diet]  nvarchar (255) NOT NULL CHECK ([Diet] IN('vlees', 'vis', 'vega')) DEFAULT 'vlees',
                    DateCreate datetime);""")
        #row = cursor.fetchone()
        #while row:
       #    print (str(row[0]) + " " + str(row[1]))
        #    row = cursor.fetchone()
                  #  UserId bigint,
                  #  PrepTime nvarchar(255),
                  #  PrepText nvarchar(255),
                  ##  CookAttireId bigint,
                  #  BBQId bigint,
                  #  Rating double,
                  ##  Foto nvarchar(255),
                  #  Intro nvarchar(255),
                  #  Diet enum('Dessert', 'vis', 'vlees'),
                  #  DateCreate datetime default now()