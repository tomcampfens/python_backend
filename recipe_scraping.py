import requests, csv
from bs4 import BeautifulSoup

url = 'https://github.com/cweber/cookbook/blob/master/recipes.csv'

for i in range(0,len(extents)):
    total_url = url + extents[i]
    with open('Recipe.csv', "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Directions", "Quantity","Unit01", "Ingredient01", "Quantity02", "Unit02", "Ingredient02"])

        while True:
            html = requests.get(total_url)
            soup = BeautifulSoup(html.content, 'html.parser')
            for row in soup.find('h1').text:
                #writer.writerow([c.text if c.text else '' for c in row.find('td')])
                print(row)

            if soup.select_one('li.active + li a'):
                total_url = soup.select_one('li.active + li a')['href']
            else:
                break