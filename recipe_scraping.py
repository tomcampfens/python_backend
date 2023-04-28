import requests, csv
from bs4 import BeautifulSoup

url = 'https://github.com/cweber/cookbook/blob/master/recipes.csv'

with open('Recipe.csv', "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Directions", "Quantity","Unit01", "Ingredient01", "Quantity02", "Unit02", "Ingredient02"])

    while True:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        for row in soup.select('table tbody tr'):
            writer.writerow([c.text if c.text else '' for c in row.select('td')])


        if soup.select_one('li.active + li a'):
            url = soup.select_one('li.active + li a')['href']
        else:
            break