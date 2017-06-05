from unittest import TestCase
from voting_engines import EngineBase



# EngineBase.add_votes() tests
class Add_Votes__Tests(TestCase):
    """This test class checks the behavour of EngineBase.add_votes() for simple voting set ups."""

    # Prepare for tests
    def setUp(self):
        """
        This method creates an election with one seat for one candidate.
        These settings can be altered in the tests
        """
        self.engine = EngineBase(['A'])

    # Invalid candidate
    def test__invalid_candidate(self):
        """A ValueError should be raised."""

        # Add votes and test
        self.assertRaises(
            ValueError,
            self.engine.add_votes,
            {'A': 10, 'I': 34}
        )


    # Single candidate for one seat with an even number of votes
    def test__single_seat__single_candidate__even_votes(self):
        """The quota here should be 6."""

        # Add votes and test
        self.engine.add_votes({'A': 10})
        self.assertEqual(self.engine.votes, [{'A': 10}])
        self.assertEqual(self.engine.quota, 6)


    # Single candidate for one seat with an odd number of votes
    def test__single_seat__single_candidate__odd_votes(self):
        """The quota here should be 6."""

        # Add votes and test
        self.engine.add_votes({'A': 11})
        self.assertEqual(self.engine.votes, [{'A': 11}])
        self.assertEqual(self.engine.quota, 6)


    # Two candidates for one seat with an even number of votes
    def test__single_seat__two_candidates__even_votes(self):
        """The quota here should be 9."""

        # Alter settings
        self.engine.candidates.append('B')

        # Add votes and test
        self.engine.add_votes({'A': 10, 'B': 6})
        self.assertEqual(self.engine.votes, [{'A': 10, 'B': 6}])
        self.assertEqual(self.engine.quota, 9)


    # Two candidates for one seat with an odd number of votes
    def test__single_seat__two_candidates__odd_votes(self):
        """The quota here should be 9."""

        # Alter settings
        self.engine.candidates.append('B')

        # Add votes and test
        self.engine.add_votes({'A': 11, 'B': 6})
        self.assertEqual(self.engine.votes, [{'A': 11, 'B': 6}])
        self.assertEqual(self.engine.quota, 9)


    # Single candidate for two seats with twelve votes
    def test__two_seats__single_candidate__twelve_votes(self):
        """The quota here should be 5."""

        # Alter settings
        self.engine.seats = 2

        # Add votes and test
        self.engine.add_votes({'A': 12})
        self.assertEqual(self.engine.votes, [{'A': 12}])
        self.assertEqual(self.engine.quota, 5)


    # Single candidate for three seats with twelve votes
    def test__three_seats__single_candidate__twelve_votes(self):
        """The quota here should be 4."""

        # Alter settings
        self.engine.seats = 3

        # Add votes and test
        self.engine.add_votes({'A': 12})
        self.assertEqual(self.engine.votes, [{'A': 12}])
        self.assertEqual(self.engine.quota, 4)



# EngineBase.run_election() tests
class Run_Election__Tests(TestCase):
    """This test class checks the behavour of EngineBase.run_election() under conditions which force a single election round."""

    # Prepare for tests
    def setUp(self):
        """
        This method creates an election for one seat, one candidate and a quota of 5 - A single candidate is needed here to limit elections to one round.
        These settings can be altered in tests.
        """
        self.engine = EngineBase(['A'])
        self.engine.quota = 5


    # Single candidate over quota
    def test__single_candidate_over_quota(self):
        """A single candidate over quota should be elected as a winner."""

        # Set votes and run election
        self.engine.votes = [{'A': 10}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # Single candidate on quota
    def test__single_candidate_on_quota(self):
        """A single candidate on quota should be elected as a winner."""

        # Set votes and run election
        self.engine.votes = [{'A': 5}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # Single candidate under quota
    def test__single_candidate_under_quota(self):
        """A single candidate under quota running for a single seat should be elected as a winner by default."""

        # Set votes and run election
        self.engine.votes = [{'A': 3}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # Single candidate for two seats
    def test__single_candidate_two_seats(self):
        """A single candidate under quota running for two seats should be elected as a winner by default."""

        # Set votes and run election
        self.engine.seats = 2
        self.engine.votes = [{'A': 3}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # Two candidates over quota (in vote order)
    def test__two_candidates_over_quota_ordered(self):
        """With two candidates over quota, the one with the highest number of votes should be elected."""

        # Set votes and run election
        self.engine.votes = [{'A': 10, 'B': 8}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # Two candidates over quota (in reverse vote order)
    def test__two_candidates_over_quota_reversed(self):
        """With two candidates over quota, the one with the highest number of votes should be elected."""

        # Set votes and run election
        self.engine.votes = [{'A': 8, 'B': 10}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'B')
        self.assertEqual(0, len( self.engine.eliminated ))


    # One candidate over quota and one under quota (in vote order)
    def test__one_candidates_over_quota_and_one_under_quota_ordered(self):
        """With one candidate over quota and one under quota, the candidate over quota should be elected."""

        # Set votes and run election
        self.engine.votes = [{'A': 10, 'B': 2}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # One candidate over quota and one under quota (in reverse vote order)
    def test__one_candidates_over_quota_and_one_under_quota_reversed(self):
        """With one candidate over quota and one under quota, the candidate over quota should be elected."""

        # Set votes and run election
        self.engine.votes = [{'A': 1, 'B': 8}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'B')
        self.assertEqual(0, len( self.engine.eliminated ))


    # One candidate on quota and one under quota (in vote order)
    def test__one_candidates_on_quota_and_one_under_quota_ordered(self):
        """With one candidate on quota and one under quota, the candidate on quota should be elected."""

        # Set votes and run election
        self.engine.votes = [{'A': 5, 'B': 2}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'A')
        self.assertEqual(0, len( self.engine.eliminated ))


    # One candidate on quota and one under quota (in reverse vote order)
    def test__one_candidates_on_quota_and_one_under_quota_reversed(self):
        """With one candidate on quota and one under quota, the candidate on quota should be elected."""

        # Set votes and run election
        self.engine.votes = [{'A': 1, 'B': 5}]
        self.engine.run_election()

        # Test results
        self.assertEqual(1, len( self.engine.elected ))
        self.assertEqual(self.engine.elected[0], 'B')
        self.assertEqual(0, len( self.engine.eliminated ))


    # Two candidates under quota (in vote order)
    def test__two_candidates_under_quota_ordered(self):
        """With two candidates under quota, the candidate with fewest votes should be eliminated."""

        # Set votes and run election
        self.engine.votes = [{'A': 4, 'B': 1}]
        self.engine.run_election()

        # Test results
        self.assertEqual(0, len( self.engine.elected ))
        self.assertEqual(1, len( self.engine.eliminated ))
        self.assertEqual(self.engine.eliminated[0], 'B')


    # Two candidates under quota (in vote order)
    def test__two_candidates_under_quota_reversed(self):
        """With two candidates under quota, the candidate with fewest votes should be eliminated."""

        # Set votes and run election
        self.engine.votes = [{'A': 2, 'B': 3}]
        self.engine.run_election()

        # Test results
        self.assertEqual(0, len( self.engine.elected ))
        self.assertEqual(1, len( self.engine.eliminated ))
        self.assertEqual(self.engine.eliminated[0], 'A')



# EngineBase.find_winner() tests
class Find_Winner__Tests(TestCase):
    """This test class checks the behavour of EngineBase.find_winner() for votes from a single round."""

    # Prepare for tests
    def setUp(self):
        """
        This method creates an election for one seat, two candidates and a quota of 5.
        These settings can be altered in tests.
        """
        self.engine = EngineBase(['A', 'B'])
        self.engine.quota = 5


    # Single candidate over quota
    def test__single_candidate_over_quota(self):
        """A single candidate over quota should be identified as a winner."""
        winner = self.engine.find_winner({'A': 30})
        self.assertEqual(winner, 'A')


    # Single candidate on quota
    def test__single_candidate_on_quota(self):
        """A single candidate on quota should be identified as a winner."""
        winner = self.engine.find_winner({'A': 5})
        self.assertEqual(winner, 'A')


    # Single candidate under quota
    def test__single_candidate_under_quota(self):
        """A single candidate under quota should not be identified as a winner."""
        winner = self.engine.find_winner({'A': 3})
        self.assertIsNone(winner)


    # Two candidates over quota (in vote order)
    def test__two_candidates_above_quota_ordered(self):
        """If two candidates are over quota, the one with most votes should be identified as the winner."""
        winner = self.engine.find_winner({'A': 30, 'B': 20})
        self.assertEqual(winner, 'A')


    # Two candidates over quota (in reverse vote order)
    def test__two_candidates_above_quota_reversed(self):
        """If two candidates are over quota, the one with most votes should be identified as the winner."""
        winner = self.engine.find_winner({'A': 20, 'B': 30})
        self.assertEqual(winner, 'B')



# EngineBase.find_loser() tests
class Find_Loser__Tests(TestCase):
    """This test class checks the behavour of EngineBase.find_winner() for votes from a single round."""

    # Prepare for tests
    def setUp(self):
        """
        This method creates an election for one seat, one candidate and a quota of 5 - A single candidate is needed here to limit elections to one round.
        These settings can be altered in tests.
        """
        self.engine = EngineBase(['A', 'B'])
        self.engine.quota = 5


    # A single candidate
    def test__single_candidate(self):
        """For a vote with one candidate, the candidate should be returned as a loser."""
        loser = self.engine.find_loser({'A': 3})
        self.assertEqual(loser, 'A')


    # Two candidates (in vote order)
    def test__two_candidates_ordered(self):
        """For a vote with two candidates, the one with fewest votes should be identified as the loser."""
        loser = self.engine.find_loser({'A': 3, 'B': 2})
        self.assertEqual(loser, 'B')


    # Two candidates (in reverse vote order)
    def test___two_candidates_reversed(self):
        """For a vote with two candidates, the one with fewest votes should be identified as the loser."""
        loser = self.engine.find_loser({'A': 2, 'B': 3})
        self.assertEqual(loser, 'A')



# EngineBase.advance_voting_round() tests
class Advance_Voting_Round__Tests(TestCase):
    """This test class checks the behavour of EngineBase.advance_voting_round() when advancing a single round."""

    # Prepare for tests
    def setUp(self):
        """
        This method creates an election for one seat, one candidate and a quota of 5 - A single candidate is needed here to limit elections to one round.
        These settings can be altered in tests.
        """
        self.engine = EngineBase(['A', 'B', 'C'])
        self.engine.quota = 5
        self.engine.votes = [{'A': 10, 'C': 13, 'B': 4}]


    # Eliminate first candidate
    def test__eliminate_first_candidate(self):
        """Candidate A should not appear in the last round of voting."""
        self.engine.advance_voting_round('A')
        self.assertEqual(self.engine.votes[-1], {'B': 4, 'C': 13})


    # Eliminate middle candidate
    def test__eliminate_middle_candidate(self):
        """Candidate B should not appear in the last round of voting."""
        self.engine.advance_voting_round('B')
        self.assertEqual(self.engine.votes[-1], {'A': 10, 'C': 13})


    # Eliminate last candidate
    def test__eliminate_last_candidate(self):
        """Candidate C should not appear in the last round of voting."""
        self.engine.advance_voting_round('C')
        self.assertEqual(self.engine.votes[-1], {'A': 10, 'B': 4})



# EngineBase.redistribute_votes() tests
class Redistribute_Votes__Tests(TestCase):
    """This test class checks the behaviour of the EngineBase.redistribute_votes() method."""

    # Test setup
    def setUp(self):
        """
        This method creates an election with three candidates running for one seat and the first round of voting complete.
        These settings can be altered in the tests.
        """
        self.engine = EngineBase(
            ['A', 'B', 'C'],
            seats = 1,
            votes = {'A': 30, 'B': 10, 'C': 20}
        )


    # No 'from' key
    def test__no_from_key(self):
        """Candidate B's votes should be dropped."""

        # Add redistribution
        self.engine.add_redistribution_matrix({})

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'A': 30, 'B': 10, 'C': 20},
                {'A': 30, 'C': 20}
            ]
        )


    # No 'to' key
    def test__no_to_key(self):
        """Candidate B's votes should be dropped."""

        # Add redistribution
        self.engine.add_redistribution_matrix({'B': {}})

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'A': 30, 'B': 10, 'C': 20},
                {'A': 30, 'C': 20}
            ]
        )


    # All votes to none
    def test__all_votes_to_none(self):
        """Candidate B's votes should be dropped."""

        # Add redistribution
        self.engine.add_redistribution_matrix({'B': {None: 1}})

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'A': 30, 'B': 10, 'C': 20},
                {'A': 30, 'C': 20}
            ]
        )


    # All votes to one candidate
    def test__all_to_one(self):
        """Candidate B's votes should be transferred to A."""

        # Add redistribution
        self.engine.add_redistribution_matrix({'B': {'A': 1}})

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'A': 30, 'B': 10, 'C': 20},
                {'A': 40, 'C': 20}
            ]
        )


    # All votes to eliminated candidate
    def test__all_to_eliminated(self):
        """Candidate B's votes should be dropped."""

        # Add redistribution and eliminate candidate A
        self.engine.add_redistribution_matrix({'B': {'A': 1}})
        self.engine.votes[-1].pop('A')

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'B': 10, 'C': 20},
                {'C': 20}
            ]
        )


    # Split with none
    def test__split_with_none(self):
        """Candidate B's votes should be partially transferred to A."""

        # Add redistribution
        self.engine.add_redistribution_matrix({'B': {'A': 2, None: 3}})

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'A': 30, 'B': 10, 'C': 20},
                {'A': 34, 'C': 20}
            ]
        )


    # Split two candidates
    def test__split_two_candidates(self):
        """Candidate B's votes should be partially transferred to A and partially to C."""

        # Add redistribution
        self.engine.add_redistribution_matrix({'B': {'A': 2, 'C': 3}})

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'A': 30, 'B': 10, 'C': 20},
                {'A': 34, 'C': 26}
            ]
        )


    # Split with eliminated candidate
    def test__split_with_eliminated(self):
        """Candidate B's votes should be fully transferred to C."""

        # Add redistribution
        self.engine.add_redistribution_matrix({'B': {'A': 2, 'C': 3}})
        self.engine.votes[-1].pop('A')

        # Call method and test
        self.engine.redistribute_votes('B', self.engine.votes[-1]['B'])
        self.assertEqual(
            self.engine.votes,
            [
                {'B': 10, 'C': 20},
                {'C': 30}
            ]
        )

