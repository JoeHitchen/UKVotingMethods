from requests import get as get_request
from bs4 import BeautifulSoup as Soup
import json
import re


# Get constituency group list
with open('./data/groups.json') as file:
    groups = json.load(file, encoding = 'utf-8')


# Get constituency list
request = get_request('https://en.wikipedia.org/wiki/List_of_United_Kingdom_Parliament_constituencies')
request.raise_for_status()
soup = Soup(request.text, 'html.parser')
table = soup.find('table', class_='wikitable sortable')
constituencies = []
for row in table.findChildren('tr'):
    cells = row.findChildren('td')
    if len(cells):
        constituencies.append({
            'name': str(cells[0].findChild('a').contents[0]),
            'link': cells[0].findChild('a').get('href'),
            'electorate': int(re.sub(',', '', cells[3].contents[0])),
            'country': str(cells[5].contents[0]),
            'region': str(cells[6].contents[0]) if len(cells) > 6 else None,
            'county': str(cells[4].contents[0].contents[0])
        })
print('Constituencies found: {}'.format(len(constituencies)))


# Check constituencies
for constituency in constituencies:
    
    # Loop over groups
    Found = False
    for group in groups:
        if constituency['name'] in group['constituencies']:
            
            # First match found
            if not Found:
                Found = True
            
            # Second match found
            else:
                print('Duplicated constituency: {}'.format(constituency['name']))
    
    # Unmatched constituency
    if not Found:
        print('Unmatched constituency: {}'.format(constituency['name']))


# Save to file
with open('./data/constituencies.json', 'w+') as file:
    groups = json.dump(constituencies, file)

