from unittest import TestCase
from voting_engines import DirectElectionEngine


# Single-Transferable-Vote tests
class STV_Election__Tests(TestCase):
    """This test class checks the behaviour of elections run under Single-Transferable-Vote."""

    # A single candidate running unopposed for a single seat
    def test__single_seat__single_candidate(self):
        """Candidate A should be elected automatically."""

        # Setup election
        election = DirectElectionEngine(['A'])
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
        election = DirectElectionEngine(['A', 'B'])
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
        election = DirectElectionEngine(['A', 'B'])
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
        election = DirectElectionEngine(['A', 'B'])
        election.add_votes({'A': 10, 'B': 10})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 11)
        self.assertEqual(election.votes, [{'B': 10, 'A': 10}, {'B': 10}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, ['A'])


    # Three candidates for one seat, one over quota
    def test__single_seat__three_candidates__over_quota(self):
        """Candidate B is over quota should be elected outright."""

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'])
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
        election = DirectElectionEngine(['A', 'B', 'C'])
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
        election = DirectElectionEngine(['A', 'B', 'C'])
        election.add_votes({'A': 3, 'B': 7, 'C': 4})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 8)
        self.assertEqual(election.votes, [{'A': 3, 'B': 7, 'C': 4}, {'B': 7, 'C': 4}, {'B': 7}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, ['A', 'C'])


    # Three candidates for one seat, with redistribution
    def test__single_seat__three_candidates__with_redistribution(self):
        """
        Candidate A should be eliminated first and their votes transferred to C.
        Candidate C should then be elected.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'])
        election.add_votes({'A': 4, 'B': 7, 'C': 5})
        election.add_redistribution_matrix({'A': {'C': 1}})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 9)
        self.assertEqual(election.votes, [{'A': 4, 'B': 7, 'C': 5}, {'B': 7, 'C': 9}])
        self.assertEqual(election.elected, ['C'])
        self.assertEqual(election.eliminated, ['A'])


    # Three candidates for one seat, with redistribution
    def test__single_seat__three_candidates__with_split_redistribution(self):
        """
        Candidate A should be eliminated first and their votes partially transferred to B and C.
        Candidate B should then be elected.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'])
        election.add_votes({'A': 4, 'B': 7, 'C': 5})
        election.add_redistribution_matrix({'A': {'C': 1, 'B': 3}})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 9)
        self.assertEqual(election.votes, [{'A': 4, 'B': 7, 'C': 5}, {'B': 10, 'C': 6}])
        self.assertEqual(election.elected, ['B'])
        self.assertEqual(election.eliminated, ['A'])


    # Two candidates for two seats
    def test__two_seats__two_candidates(self):
        """Both candidates should be elected by default."""

        # Setup election
        election = DirectElectionEngine(['A', 'B'], seats = 2)
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
        election = DirectElectionEngine(['A', 'B', 'C'], seats = 2)
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
        election = DirectElectionEngine(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 15, 'B': 3, 'C': 31})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 17)
        self.assertEqual(election.votes, [{'A': 15, 'B': 3, 'C': 31}, {'A': 15, 'B': 3}, {'A': 15}])
        self.assertEqual(election.elected, ['C', 'A'])
        self.assertEqual(election.eliminated, ['B'])


    # Three candidates for two seats, with sufficient excess redistribution
    def test__two_seats__three_candidates__sufficient_excess(self):
        """
        Candidate C should be elected outright.
        Candidate C's excess should put B over quota.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 10, 'B': 3, 'C': 31})
        election.add_redistribution_matrix({'C': {'A': 1}})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 15)
        self.assertEqual(election.votes, [{'A': 10, 'B': 3, 'C': 31}, {'A': 26, 'B': 3}])
        self.assertEqual(election.elected, ['C', 'A'])
        self.assertEqual(election.eliminated, [])


    # Three candidates for two seats, with split excess redistribution
    def test__two_seats__three_candidates__split_excess(self):
        """
        Candidate C should be elected outright.
        The contribution from C's excess should put B over quota.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 10, 'B': 3, 'C': 31})
        election.add_redistribution_matrix({'C': {'A': 1, 'B': 3}})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 15)
        self.assertEqual(election.votes, [{'A': 10, 'B': 3, 'C': 31}, {'A': 14, 'B': 15}])
        self.assertEqual(election.elected, ['C', 'B'])
        self.assertEqual(election.eliminated, [])


    # Three candidates for two seats, with dropped excess
    def test__two_seats__three_candidates__dropped_excess(self):
        """
        Candidate C should be elected outright, with the excess dropped.
        Candidate B should then be eliminated and Candidate A elected by default.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 10, 'B': 3, 'C': 31})
        election.add_redistribution_matrix({'C': {None: 1}})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 15)
        self.assertEqual(election.votes, [{'A': 10, 'B': 3, 'C': 31}, {'A': 10, 'B': 3}, {'A': 10}])
        self.assertEqual(election.elected, ['C', 'A'])
        self.assertEqual(election.eliminated, ['B'])


    # Three candidates for two seats, with partially dropped excess
    def test__two_seats__three_candidates__partially_dropped_excess(self):
        """
        Candidate C should be elected outright, with some excess going to B.
        Candidate B should then be eliminated and Candidate A elected by default.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C'], seats = 2)
        election.add_votes({'A': 10, 'B': 3, 'C': 31})
        election.add_redistribution_matrix({'C': {None: 2, 'B': 2}})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 15)
        self.assertEqual(election.votes, [{'A': 10, 'B': 3, 'C': 31}, {'A': 10, 'B': 11}, {'B': 11}])
        self.assertEqual(election.elected, ['C', 'B'])
        self.assertEqual(election.eliminated, ['A'])


    # Four candidates for two seats, all under quota
    def test__two_seats__four_candidates__all_under_quota(self):
        """
        Candidates C then B should be eliminated.
        Candidates A and D should be elected be default.
        """

        # Setup election
        election = DirectElectionEngine(['A', 'B', 'C', 'D'], seats = 2)
        election.add_votes({'A': 15, 'B': 14, 'C': 13, 'D': 16})
        election.run_election()

        # Test election results
        self.assertEqual(election.quota, 20)
        self.assertEqual(election.votes, [{'A': 15, 'B': 14, 'C': 13, 'D': 16}, {'A': 15, 'B': 14, 'D': 16}, {'A': 15, 'D': 16}])
        self.assertEqual(election.elected, ['A', 'D'])
        self.assertEqual(election.eliminated, ['C', 'B'])

