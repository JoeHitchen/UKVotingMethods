from requests import get as get_request
from bs4 import BeautifulSoup as Soup
import json
import sys

from wiki_scraper import get_constituency_results


# Get constituency list page
request = get_request('https://en.wikipedia.org/wiki/Results_of_the_United_Kingdom_general_election,_2015_by_parliamentary_constituency')
request.raise_for_status()
soup = Soup(request.text, 'html.parser')


# Loop over table rows
constituencies = {}
table = soup.find('table', class_='wikitable')
for row in table.findChildren('tr'):
    
    # Skip header row
    if row.get('valign'):
        continue
    
    # Skip bottom rows
    if row.get('class'):
        continue
    
    # Get constituency
    constituency_anchor = row.findChild('td').findChild('a')
    name = str(constituency_anchor.contents[0])
    
    # Get results
    print('({:03}/650) {}'.format(len(constituencies)+1, name))
    page_url = 'https://en.wikipedia.org' + constituency_anchor.get('href')
    constituencies[name] = get_constituency_results(page_url, 2015, parties)


# Write data to file
with open('./data/results_2015.json', 'w+') as file:
    json.dump(constituencies, file)

