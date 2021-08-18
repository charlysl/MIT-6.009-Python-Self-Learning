from instrument import instrument

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
    global call_count
    call_count = 0

    # use sets for fast intersections and differences
    c_to_t = [set(candidate_to_talents[c]) for c in range(num_candidates)]

    # return best (smallest) set of candidates that provide the needed talents
    #  needed_talents = set of talents needed
    #  available = list of available candidates
    #  chosen = list of candidates chosen so far
    #  best = best solution found so far (None == no solution)
    #@instrument
    def helper(needed_talents, available, chosen, best):
        global call_count
        call_count += 1

        # have we found a solution?  [base case]
        if len(needed_talents) == 0:
            return chosen if best is None or len(chosen) < len(best) else best
        
        # optimization #1: we already know a better solution
        if best is not None and len(chosen) >= len(best): return best

        # optimization #2: only consider candidates with at least one needed talent
        available = [c for c in available if c_to_t[c] & needed_talents]

        # are we out of candidates?  [base case] 
        if len(available) == 0: return best

        # see which works best: either using the first candidate or not
        first = available[0]   # trial candidate
        rest = available[1:]   # remaining candidates
        
        # try solution without using trail candidate [recursive case]
        if rest:
            best = helper(needed_talents, rest, chosen, best)

        # try solution using trial candidate [recursive case]
        best = helper(needed_talents - c_to_t[first], rest, chosen + [first], best)

        return best

    # initially we need all the talents, all candidates are available,
    # no one has been chosen, and we have no best solution
    needed_talents = set(range(num_talents))
    available = list(range(num_candidates))
    result = helper(needed_talents, available, [], None)

    #print("num_candidates:", num_candidates, "; num recursive calls:", call_count, "; best:", result)

    # put result in desired form
    return result or []


## Brute Force Approach -- try *all* sets of candidates
def brute_select_candidates(num_candidates, num_talents,
                            candidate_to_talents, talent_to_candidates):
    # use sets for fast intersections and differences
    c_to_t = [set(candidate_to_talents[c]) for c in range(num_candidates)]
    
    # does set of candidates cover all the talents?
    def covers(cset):
        talents = set()
        for c in cset:
            talents.update(c_to_t[c])
        return len(talents) == num_talents
    
    call_count = 0    #just instrumentation
    
    # look at all possible candidate sets, and pick best (smallest) one
    all_candidate_sets = all_subsets(list(range(num_candidates)))
    best = None
    best_count = num_candidates + 1
    for cset in all_candidate_sets:
        call_count += 1
        if covers(cset):
            if len(cset) < best_count:
                best_count = len(cset)
                best = list(cset)
    #print("num_candidates:", num_candidates, "; cases considered:", call_count, "; best:", best)
    return best or []


# yield all subset of list L; all elements of L assume to be unique
def all_subsets(L):
    if len(L) == 0:
        yield set()
    else:
        first = set([L[0]])
        for s in all_subsets(L[1:]):
            yield s
            yield first | s


## Try sets of candidates in order of size of sets (smaller sets first).
## By definition, the first one we find will be minimal and be a best result.
def ordered_select_candidates(num_candidates, num_talents,
                              candidate_to_talents, talent_to_candidates):
    # use sets for fast intersections and differences
    c_to_t = [set(candidate_to_talents[c]) for c in range(num_candidates)]

    def covers(candidates):
        talents = set()
        for c in candidates:
            talents.update(c_to_t[c])
        return len(talents) == num_talents

    candidates = list(range(num_candidates))
    case_count = 0
    for size in range(1,num_candidates+1):
        for candidate_set in all_subsets_of_size(candidates, size):
            case_count += 1
            if covers(candidate_set):
                #print("num_candidates:", num_candidates, " num cases:", case_count, "best:", candidate_set)
                return list(candidate_set)
    #print("num_candidates:", num_candidates, " num cases:", case_count, "best:", [])
    return []

def all_subsets_of_size(L, size):
    """ yield all subsets of L equal in size to size """
    pass # Left as an exercise for the reader
            

if __name__ == '__main__':
    import time
    start = time.time()
    num_candidates = 17
    num_talents = 18
    candidate_to_talents = [[0, 3, 6], [3, 4, 5], [6, 7, 8], [9, 10, 11], 
                            [12, 13, 14], [15, 16, 17], [0, 1, 2], [17], 
                            [1, 4], [7, 10], [13, 16], [2], [5], [8], [11], 
                            [14], [9, 12, 15]]
    talent_to_candidates = [[0, 6], [6, 8], [6, 11], [0, 1], [1, 8], [1, 12],
                            [0, 2], [2, 9], [2, 13], [3, 16], [3, 9], [3, 14],
                            [4, 16], [4, 10], [4, 15], [5, 6], [5, 10], [5, 7]]
    select_candidates(num_candidates, num_talents, 
                      candidate_to_talents, talent_to_candidates)
    end = time.time()
    print("time:", end-start, "sec")
    print(2**num_candidates)

