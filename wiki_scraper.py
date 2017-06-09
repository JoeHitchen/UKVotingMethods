from requests import get as get_request
from bs4 import BeautifulSoup as Soup
import re


# Primary constituency results scraper
def get_constituency_results(page_url, year):
    """
    This method is the main constituency results scraper.
    The constituency page url and election year must be provided.
    A list of dictionaries containing candiate names, parties, and vote tallies is returned.
    """
    
    # Get page as soup
    request = get_request(page_url)
    request.raise_for_status()
    soup = Soup(request.text, 'html.parser')
    
    # Find results table
    election_table = False
    tables = soup.find_all('caption')
    for table in tables:
        if re.match('General [Ee]lection {}'.format(year), table.find('a').contents[0]):
            election_table = table.parent
            break
            
    # Try alternative scraper
    if not election_table:
        return alternative_constituency_results(soup, year)
    
    # Process results table
    candidates = []
    for candidate in election_table.findChildren('tr', class_='vcard'):
        
        # Add candidate to list
        candidates.append(get_candidate_from_row(candidate, 3))
    
    # Return candidates
    return candidates


# Alternative constituency results scraper
def alternative_constituency_results(soup, year):
    """
    This method scrapes election results from the alternative layout.
    The election year must be provided.
    A list of dictionaries containing candiate names, parties, and vote tallies is returned.
    """
    
    # Find links to main election page...
    row = None
    links = soup.find_all('a', href='/wiki/United_Kingdom_general_election,_{}'.format(year))
    for link in links:
        
        # ... Contained in cells spanning multiple rows
        leading_cell = link.find_parents('td')
        if leading_cell and leading_cell[0].get('rowspan'):
            row = leading_cell[0].parent
            row_span = int(leading_cell[0].get('rowspan'))
            break
    
    # Raise error if unable to find right box
    if not row:
        raise LookupError('Could not find election')
    
    # Prepare for candidate scraping
    rows = row.parent.find_all('tr')
    start_index = rows.index(row)
    candidates = []
    
    # Loop over candidate rows
    for row in rows[start_index:start_index+row_span]:
        vote_index = 6 if row == rows[start_index] else 3
        candidates.append(get_candidate_from_row(row, vote_index))
    
    # Return candidates
    return candidates


# Candidate scraper
def get_candidate_from_row(row, vote_index):
    """
    This method takes a table row and extracts the candidate name, party, and vote tally.
    The name must be in a cell with class "fn" and the party must be in a cell with class "org".
    The vote tally cell must be specified.
    """
    
    # Get candidate name
    name = row.findChild('td', class_='fn')
    if name.findChild('b'):
        name = name.findChild('b')
    if name.findChild('a') and name.findChild('a').parent == name:
        name = name.findChild('a')
    name = str(name.contents[0])
    
    # Get candidate party
    party = row.findChild('td', class_='org')
    if party.findChild('a'):
        party = party.findChild('a')
    party = str(party.contents[0])
    
    # Get votes
    votes = row.findChildren('td')[vote_index]
    if votes.findChild('b'):
        votes = votes.findChild('b')
    votes = votes.contents[0]
    votes = re.sub(',', '', votes)
    votes = int(votes)
    
    # Return candidate dictionary
    return {
        'name': name,
        'party': party,
        'votes': votes
    }

