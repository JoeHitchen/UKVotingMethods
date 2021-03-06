from operator import itemgetter as tuple_index
from copy import copy
from math import floor


# Election engine base
class DirectElectionEngine():
    """
    This class handles direct elections where representatives are elected directly by the electorate.
    The following voting methods are supported:
        1. First-past-the-post
        2. Multi-member first-past-the-post
        3. Alternative vote
        4. Single transferable vote
    Since this is a post-election analysis tool, a redistribution matrix is used to handle lower-preference votes and it is not possible to specify these ballots directly.
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
        # This method is untested because it's behaviour is trivial #

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
        It calls single_voting_round() repeatedly until all seats are filled or the number of iterations excedes the number of candidates (whichever is first).
        """

        # Loop over voting rounds
        for i in range(0, len(self.candidates)):
            complete = self.single_voting_round()
            if complete:
                break


    # Single voting round method
    def single_voting_round(self):
        """
        This method performs a single round of voting by performing the following steps:
            1. Test for "default winners", where the number of remaining seats equals the number of remaining candidates.
            2. Try to find a "winner" who has the most votes and more votes than the quota.
            3. Eliminate the "loser" with the fewest votes.
        """

        # Get votes for the round
        round_votes = self.votes[-1]

        # Winners by default
        if self.seats - len(self.elected) >= len(round_votes):
            self.elected.extend(round_votes.keys())
            return True

        # Elect winner
        winner = self.find_winner(round_votes)
        if winner:
            self.elected.append(winner)
            if self.seats == len(self.elected):
                return True
            self.redistribute_votes(
                winner,
                votes_to_share = round_votes[winner] - self.quota
            )
            return False

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


    # Redistribute votes method
    def redistribute_votes(self, candidate_to_go, votes_to_share = False):
        """
        This method removes a candidate from the voting and redistributes their votes amongst the remaining candidates according to the redistribution matrix.
        By default, all their votes will be distributed, but this can changed by specifying 'votes_to_share'.
        Any votes redistributed to 'None' are removed from the election.
        """

        # Advance voting round
        self.votes.append(copy(self.votes[-1]))
        self.votes[-1].pop(candidate_to_go)

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

