# Given candidate and talent info, return an optimal list of candidates to
#  select. If no solution exists, return an empty list [].
#
# num_candidates: number of candidates; candidates are numbered 0 to
#  (num_candidates - 1)
#
# num_talents: number of talents; talents are numbered 0 to (num_talents - 1)
#
# candidate_to_talents: list of lists; candidates_to_talents[c] is a list of
#  talents that Candidate c is able to perform
#
# talent_to_candidates: list of lists; talent_to_candidates[t] is a list of
#  candidates who are able to perform Talent t
def select_candidates(num_candidates, num_talents,
                      candidate_to_talents, talent_to_candidates):
    raise NotImplementedError
