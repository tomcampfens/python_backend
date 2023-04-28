import requests, csv
from bs4 import BeautifulSoup

def getInfoVanDetail(nwurl):
    print("we gaan deze beoeken", nwurl)

def getallurl(zoekterm):
    page = requests.get('https://www.allrecipes.com/search?q='+zoekterm)
    dehtml = BeautifulSoup(page.content, 'html.parser')

    delijst = dehtml.find(id='search-results__content_1-0')

    #print(delijst.prettify())
    #print(delijst.find('a')['href'])
    for card in delijst.find_all('a'):
        getInfoVanDetail(card['href'])

getallurl('cheese')
print('==============================')
getallurl('beef')
url = 'https://www.allrecipes.com/recipe/'

extents = ['20608/super-simple-oven-barbequed-chicken/']

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