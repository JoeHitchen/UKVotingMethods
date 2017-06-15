import json
import re

from wiki_scraper import get_constituency_results
from voting_engines import DirectElectionEngine


# Load settings and data
with open('./data/parties.json') as file:
    parties = json.load(file)
with open('./data/oxfordshire.json') as file:
    groups = json.load(file)
with open('./data/results_2015.json') as file:
    results = json.load(file)


## Prepare and run election
# Loop over voting groups
for key in groups:
    group = groups[key]
    
    # Get candidates
    candidates = []
    for const in group['Constituencies']:
        candidates.extend(results[const])
        
    # Get redistribution matrix
    matrix = {}
    for from_cand in candidates:
        
        # Check for party redistribution
        from_party = from_cand['party']
        if not from_party in parties or 'redistribute' not in parties[from_party]:
            continue
        
        # Create candidate redistribution
        matrix[from_cand['name']] = {}
        for to_cand in candidates:
            if to_cand['party'] in parties[from_party]['redistribute']:
                matrix[from_cand['name']][to_cand['name']] = parties[from_party]['redistribute'][to_cand['party']]
    
    
    # Run election
    election = DirectElectionEngine(
        [candidate['name'] for candidate in candidates],
        seats = 6,
        votes = {candidate['name']: candidate['votes'] for candidate in candidates},
        redistribution_matrix = matrix
    )
    election.run_election()
    print(election.quota)
    print(election.elected)
    