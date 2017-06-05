from operator import itemgetter as tuple_index
from copy import copy
from math import floor


# Election engine base
class EngineBase():
    """
    This is the base class for voting engines.
    Vote redistribution when electing or eliminating a candidate can be controled by overwriting the "redistribute_winner" and "redistribute_loser" methods.
    It does not currently support proportional or mixed style voting.
    """

    # Initialisation routine
    def __init__(self, candidates, seats = 1, votes = [], redistribution_matrix = {}):
        """
        This method creates an election engine from inputs representing the number of seats and the list of candidates.

        Required Parameters
        ------
        candidates: list <candidate obj>
            The list of candidates standing.

        Optional Parameters
        ------
        seats: int (default = 1)
            The number of seats to be elected.
        votes: dict <candidate: int>
            The first-round votes for each candidate.
        redistribution_matrix: dict <candidate: dict <candidate: int> >
            The redistribution matrix for all candidates.
        """
        ### THIS METHOD IS UNTESTED ###

        # Read candidates and number of seats
        self.candidates = candidates
        self.seats = seats

        # Process votes input
        self.votes = []
        if votes:
            self.add_votes(votes)

        # Process redistribution matrix input
        self.redistribution_matrix = {}
        if redistribution_matrix:
            self.add_redistribution_matrix(redistribution_matrix)


        # Prepare output containers
        self.elected = []
        self.eliminated = []


    # Vote initialisation
    def add_votes(self, votes):
        """
        This method processes the initial votes and any spoilt ballots.
        It then calculates the voting quota using the Droop method.
        """
        for key in votes:
            if not key in self.candidates:
                raise ValueError('Write-in candidates are not supported')
        self.votes = [votes]
        self.quota = floor(sum(votes.values())/(self.seats+1))+1


    # Redistribution matrix initialisation
    def add_redistribution_matrix(self, matrix):
        """
        This method checks that only valid candiates are listed as 'from' and 'to' redistribution keys.
        A 'None' key is also accepted as a 'to' key for votes which are not to be re-allocated.
        It is not necessary to list all candidates in either key list.
        """

        # Check 'from' keys are valid
        for from_key in matrix:
            if not from_key in self.candidates:
                raise ValueError('From-candidate not recognised: "{}"'.format(from_key))

            # Check 'to' keys are valid
            for to_key in matrix[from_key]:
                if not to_key in self.candidates and to_key is not None:
                    raise ValueError('To-candidate not recognised: "{}"'.format(to_key))

        # Add matrix to engine
        self.redistribution_matrix = matrix


    # Main routine
    def run_election(self):
        """
        This method is the main election routine.
        It iterates the following cycle:
            1. Test for "default winners", where the number of remaining seats equals the number of remaining candidates.
            2. Try to find a "winner" who has the most votes and more votes than the quota.
            3. Eliminate the "loser" with the fewest votes.
        Iterations will be performed until all seats are filled or the number of iterations excedes the number of candidates (whichever is first).
        """

        # Loop over voting rounds
        for i in range(0, len(self.candidates)):

            # Get votes for this round
            round_votes = self.votes[-1]

            # Winners by default
            if self.seats - len(self.elected) >= len(round_votes):
                self.elected.extend(round_votes.keys())
                break

            # Elect winner
            winner = self.find_winner(round_votes)
            if winner:
                self.elected.append(winner)
                if self.seats == len(self.elected):
                    break
                self.redistribute_votes(
                    winner,
                    votes_to_share = self.votes[-1][winner] - self.quota
                )
                continue

            # Eliminate loser
            loser = self.find_loser(round_votes)
            self.eliminated.append(loser)
            self.redistribute_votes(loser)


    # Find winner method
    def find_winner(self, round_votes):
        """
        This method sorts the remaining candidates by the number of votes received and returns the candidate with the most votes that excedes the vote quota.
        If no candidate excedes the vote quota, a None value is returned.
        """
        ranked_votes = sorted(
            round_votes.items(),
            key = tuple_index(1),
            reverse = True
        )
        return ranked_votes[0][0] if ranked_votes[0][1] >= self.quota else None


    # Find loser method
    def find_loser(self, round_votes):
        """This method sorts the remaining candidates by the number of votes received and returns the candidate with the least votes."""
        ranked_votes = sorted(
            round_votes.items(),
            key = tuple_index(1),
            reverse = False
        )
        return ranked_votes[0][0]


    # Advance voting method
    def advance_voting_round(self, candidate):
        """This method advances the voting round and eliminates the candidate specified."""
        self.votes.append(copy(self.votes[-1]))
        self.votes[-1].pop(candidate)


    # Redistribute votes method
    def redistribute_votes(self, candidate_to_go, votes_to_share = False):

        # Advance voting round
        self.advance_voting_round(candidate_to_go)

        # Redistribute votes
        if candidate_to_go in self.redistribution_matrix:

            # Get updated redistribution array
            new_redist = {None: self.redistribution_matrix[candidate_to_go][None]} if None in self.redistribution_matrix[candidate_to_go] else {}
            for candidate in self.votes[-1]:
                if candidate in self.redistribution_matrix[candidate_to_go]:
                    new_redist[candidate] = self.redistribution_matrix[candidate_to_go][candidate]

            # Redistribute votes:
            total_weight = sum(new_redist.values())
            new_redist.pop(None, None)
            for candidate in new_redist:
                self.votes[-1][candidate] += (votes_to_share if votes_to_share else self.votes[-2][candidate_to_go]) * new_redist[candidate]/total_weight

