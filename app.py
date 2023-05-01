# %%
from flask import Flask
#from flask import Flask
from flask_cors import CORS

import pandas as pd
app = Flask(__name__)
CORS(app)

#df = pd.read_csv("recipe_voorbeeld.csv")
@app.route("/")
def read_csv():
    return '<table><tr><th>Company</th><th>Contact</th><th>Country</th></tr><tr><td>Alfreds Futterkiste</td><td>Maria Anders</td><td>Germany</td></tr><tr><td>Centro comercial Moctezuma</td><td>Francisco Chang</td><td>Mexico</td></tr></table>'

@app.route("/recipes")
def recipes():
    with open('recipe_voorbeeld.csv') as csvfile:
        csvreader = pd.read_csv(csvfile)
        df = pd.DataFrame(csvreader)
        return df.to_json()
