# %%
from flask import Flask, jsonify
import pandas as pd
app = Flask(__name__)
#df = pd.read_csv("recipe_voorbeeld.csv")
@app.route("/")
def read_csv():
    return '<table><tr><th>Company</th><th>Contact</th><th>Country</th></tr><tr><td>Alfreds Futterkiste</td><td>Maria Anders</td><td>Germany</td></tr><tr><td>Centro comercial Moctezuma</td><td>Francisco Chang</td><td>Mexico</td></tr></table>'

@app.route("/recipes")
def recipes():
    with open('recipe_voorbeeld.csv') as csvfile:
        csvreader = pd.read_csv(csvfile)
        data = []
        for row in csvreader:
            data.append(row)
        return jsonify(data)
    #return '<table><tr><td>{df[1]}</td><td>Maria Anders</td><td>Germany</td></tr><tr><td>Centro comercial Moctezuma</td><td>Francisco Chang</td><td>Mexico</td></tr></table>'

# %%
