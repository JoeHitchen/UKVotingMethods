from unittest import TestCase
from voting_engines import MFPTP


# Multiple-First-Past-The-Post tests
class MFPTP_Election__Tests(TestCase):
    """This test class checks the behaviour of elections run under the generalised Multiple-First-Past-The-Post."""

    # A single candidate running for a single seat unopposed
    def test__single_seat__single_candidate(self):
        """Candidate A should be elected automatically."""

        # Setup election
        election = MFPTP(['A'], seats = 1)
        election.add_votes({'A': 10})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 6)
        self.assertEqual(election.votes, [{'A': 10}])
        self.assertEqual(election.elected, ['A'])
        self.assertEqual(election.eliminated, [])


    # Two candidates for one seat with the first leading
    def test__single_seat__two_candidates__a_win(self):
        """Candidate A should be elected outright."""

        # Setup election
        election = MFPTP(['A', 'B'], seats = 1)
        election.add_votes({'A': 10, 'B': 5})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 8)
        self.assertEqual(election.votes, [{'A': 10, 'B': 5}])
        self.assertEqual(election.elected, ['A'])
        self.assertEqual(election.eliminated, [])


    # Two candidates for one seat with the second leading
    def test__single_seat__two_candidates__b_win(self):
        """Candidate B should be elected outright."""

        # Setup election
        election = MFPTP(['A', 'B'], seats = 1)
        election.add_votes({'A': 5, 'B': 10})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 8)
        self.assertEqual(election.votes, [{'A': 5, 'B': 10}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, [])


    # Two candidates tied for one seat
    def test__single_seat__two_candidates__a_tie(self):
        """
        Candidate A should be eliminated because they are listed first.
        Candidate B should be elected.
        """

        # Setup election
        election = MFPTP(['A', 'B'], seats = 1)
        election.add_votes({'A': 10, 'B': 10})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 11)
        self.assertEqual(election.votes, [{'B': 10, 'A': 10}, {'B': 10}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, ['A'])


    # Three candidates for one seat, one over quota
    def test__single_seat__three_candidates__over_quota(self):
        """Candidate B is over quota should be elected outright. """

        # Setup election
        election = MFPTP(['A', 'B', 'C'], seats = 1)
        election.add_votes({'A': 3, 'B': 14, 'C': 4})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 11)
        self.assertEqual(election.votes, [{'A': 3, 'B': 14, 'C': 4}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, [])


    # Three candidates for one seat, one on quota
    def test__single_seat__three_candidates__on_quota(self):
        """Candidate B is on quota should be elected outright."""

        # Setup election
        election = MFPTP(['A', 'B', 'C'], seats = 1)
        election.add_votes({'A': 3, 'B': 8, 'C': 4})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 8)
        self.assertEqual(election.votes, [{'A': 3, 'B': 8, 'C': 4}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, [])


    # Three candidates for one seat, all under quota
    def test__single_seat__three_candidates__under_quota(self):
        """Candidate B has the most votes so should be elected after A and C have been eliminated."""

        # Setup election
        election = MFPTP(['A', 'B', 'C'], seats = 1)
        election.add_votes({'A': 3, 'B': 7, 'C': 4})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 8)
        self.assertEqual(election.votes, [{'A': 3, 'B': 7, 'C': 4}, {'B': 7, 'C': 4}, {'B': 7}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, ['A', 'C'])


    # Two candidates for two seats
    def test__two_seats__two_candidates(self):
        """Both candidates should be elected by default."""

        # Setup election
        election = MFPTP(['A', 'B'], seats = 2)
        election.add_votes({'A': 10, 'B': 15})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 9)
        self.assertEqual(election.votes, [{'A': 10, 'B': 15}])
        self.assertEqual(election.elected, ['A', 'B'])
        self.assertEqual(election.eliminated, [])


    # Three candidates for two seats, two over quota
    def test__two_seats__three_candidates__two_over_quota(self):
        """Candidates A and C should be elected outright."""

        # Setup election
        election = MFPTP(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 30, 'B': 3, 'C': 31})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 22)
        self.assertEqual(election.votes, [{'A': 30, 'B': 3, 'C': 31}, {'A': 30, 'B': 3}])
        self.assertEqual(election.elected, ['C', 'A'])
        self.assertEqual(election.eliminated, [])


    # Three candidates for two seats, one over quota
    def test__two_seats__three_candidates__one_over_quota(self):
        """
        Candidate C should be elected outright.
        Candidate A should be elected after B is eliminated
        """

        # Setup election
        election = MFPTP(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 15, 'B': 3, 'C': 31})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 17)
        self.assertEqual(election.votes, [{'A': 15, 'B': 3, 'C': 31}, {'A': 15, 'B': 3}, {'A': 15}])
        self.assertEqual(election.elected, ['C', 'A'])
        self.assertEqual(election.eliminated, ['B'])


    # Four candidates for two seats, all under quota
    def test__two_seats__four_candidates__all_under_quota(self):
        """
        Candidates C then B should be eliminated.
        Candidates A and D should be elected be default.
        """

        # Setup election
        election = MFPTP(['A', 'B', 'C', 'D'], seats = 2)
        election.add_votes({'A': 15, 'B': 14, 'C': 13, 'D': 16})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 20)
        self.assertEqual(election.votes, [{'A': 15, 'B': 14, 'C': 13, 'D': 16}, {'A': 15, 'B': 14, 'D': 16}, {'A': 15, 'D': 16}])
        self.assertEqual(election.elected, ['A', 'D'])
        self.assertEqual(election.eliminated, ['C', 'B'])

