from instrument import instrument

# TENT PACKING
 
# Pack a tent with different sleeping bag shapes leaving no empty squares
#
# INPUTS:
#   tent_size = (rows, cols) for tent grid
#   missing_squares = set of (r, c) tuples giving location of rocks
#   bag_list = list of sets, each decribing a sleeping bag shape
#      Each set contains (r, c) tuples enumerating contiguous grid
#      squares occupied by the bag, coords are relative to the upper-
#      left corner of the bag.  You can assume every bag occupies
#      at least the grid (0,0).
#
# Example bag_list entries:
#      vertical 3x1 bag: { (0,0), (1,0), (2,0) }
#      horizontal 1x3 bag: { (0,0), (0,1), (0,2) }
#      square bag: { (0,0), (0,1), (1,0), (1,1) }
#      L-shaped bag: { (0,0), (1,0), (1,1) }
#      C-shaped bag: { (0,0), (0,1), (1,0), (2,0), (2,1) }
#      reverse-C-shaped bag: { (0,0), (0,1), (1,1), (2,0), (2,1) }
#
# OUTPUT:
#   None if no packing can be found; otherwise a list giving the
#   placement and type for each placed bag expressed as a dictionary
#   with keys
#     "anchor": (r, c) for upper-left corner of bag
#     "shape": index of bag on bag list
def pack(tent_size, missing_squares, bag_list):
    all_squares = set((r, c) for r in range(tent_size[0])
                                 for c in range(tent_size[1]))

    def first_empty(covered_squares):
        """ returns (r, c) for first empty square, else None if no empty squares """
        for row in range(tent_size[0]):
            for col in range(tent_size[1]):
                locn = (row,col)
                if locn not in covered_squares:
                    return locn
        return None

    #@instrument
    def helper(covered_squares):
        """ input: set of covered squares (covered by rocks or bags)
            output: None if no packing can be found, else a list of placed bags"""

        # look for first empty square
        locn = first_empty(covered_squares)

        # base case: no empty squares! We return an empty (successful) packing.
        if locn is None: 
            return []

        # try placing each type of bag at locn: if it fits, mark its 
        # squares as covered and recursively solve resulting problem
        row, col = locn
        for b in range(len(bag_list)):
            # compute set of squares occupied by bag b at locn
            bag_squares = set((r+row, c+col) for r, c in bag_list[b])

            # is bag in-bounds? if not, it doesn't fit here
            if len(bag_squares - all_squares) != 0:
                continue

            # are all of those bag squares free?
            if len(bag_squares & covered_squares) == 0:
                # yes, try packing with bag at this locn
                result = helper(covered_squares | bag_squares)
                if result is not None:
                    # Success! Found packing of subproblem; build solution
                    result.insert(0, {"anchor": locn, "shape": b})
                    return result
                else:
                    # Failure! Need to try another bag
                    continue

        # oops, no valid placement at this locn
        return None

    # get things started
    return helper(missing_squares)


# Alternative version -- do/undo pattern
#
def pack(tent_size, missing_squares, bag_list):
    all_squares = set((r, c) for r in range(tent_size[0])
                                 for c in range(tent_size[1]))
    def first_empty(covered_squares):
        """ returns (r, c) for first empty square, else None if no empty squares """
        for row in range(tent_size[0]):
            for col in range(tent_size[1]):
                locn = (row,col)
                if locn not in covered_squares:
                    return locn
        return None

    #@instrument
    def helper(result_so_far, covered_squares):
        """ result_so_far: list of placed bags
            covered_squares: set of squares covered by rocks or bags
            output: boolean indicating if packing successfully completed """
        # look for first empty square
        locn = first_empty(covered_squares)

        # base case: no empty squares!
        if locn is None: 
            return True #Signal success; results_so_far holds packing

        # try placing each type of bag: if it fits, mark its squares as covered,
        # add it to the results list, and recursively solve resulting problem.
        row, col = locn
        for b in range(len(bag_list)):
            # compute set of squares occupied by bag b at locn
            bag_squares = set((r+row, c+col) for r, c in bag_list[b])

            # is bag in-bounds? if not, it doesn't fit here
            if len(bag_squares - all_squares) != 0:
                continue

            # are all of those bag squares free?
            if len(bag_squares & covered_squares) == 0:
                # yes, try packing with bag at this locn
                bag = {"anchor": locn, "shape": b}
                result_so_far.insert(0, bag)      # mutate result_so_far
                covered_squares |= bag_squares    # mutate covered_squares
                success = helper(result_so_far, covered_squares)
                if success:
                    # SUCCESS -- we're done! result_so_far holds packing
                    return True
                else:
                    # FAILURE! -- need to backtrack. In this case, we need to
                    # UNDO our changes and try other bags (continue for loop)
                    result_so_far.pop(0)
                    covered_squares -= bag_squares

        # oops, no valid placement at this locn
        return False

    # get things started
    result = []
    covered_squares = set(missing_squares)
    success = helper(result, covered_squares)
    return result if success else None


## Another solution -- more subtle control structure
##
#@instrument
def pack(tent_size, missing_squares, bag_list):
    all_squares = set((r, c) for r in range(tent_size[0]) for c in range(tent_size[1]))

    # look for first empty square
    for row in range(tent_size[0]):
        for col in range(tent_size[1]):
            locn = (row, col)
            if locn not in missing_squares:
                # try placing each type of bag: if it fits, mark its squares
                # as covered and recursively solve resulting problem
                for b in range(len(bag_list)):
                    # compute set of squares occupied by bag b at locn
                    bag_squares = set((r+row, c+col) for r, c in bag_list[b])

                    # is bag in-bounds? if not, it doesn't fit here
                    if len(bag_squares - all_squares) != 0:
                        continue

                    # are all of those bag squares free?
                    if len(bag_squares & missing_squares) == 0:
                        # yes, try packing with bag at this locn
                        result = pack(tent_size, missing_squares | bag_squares, bag_list)
                        if result is not None:
                            result.append({"anchor": locn, "shape": b})
                            return result

                # oops, no valid placement at this locn
                return None
    # no empty squares!  we found a packing, so start a list of bags
    return []



## ALL PACKINGS
##  Returns a list of *all* possible packings
##
def all_packings(tent_size, missing_squares, bag_list):
    all_squares = set((r, c) for r in range(tent_size[0])
                                 for c in range(tent_size[1]))

    def first_empty(covered_squares):
        """ returns (r, c) for first empty square, else None if no empty squares """
        for row in range(tent_size[0]):
            for col in range(tent_size[1]):
                locn = (row,col)
                if locn not in covered_squares:
                    return locn
        return None

    def helper(covered_squares):
        """ input: set of covered squares (covered by rocks or bags)
            output: None if no packing can be found, else a list of packings,
            each packing being a list of placed bags
        """
        # look for first empty square
        locn = first_empty(covered_squares)

        # base case: no empty squares! A packing [] is valid; return a list of that
        if locn is None: 
            return [[]]

        ## CHANGED: now build list of all succeeding packings
        packings = None 

        # try placing each type of bag: if it fits, mark its squares
        # as covered and recursively solve resulting problem.
        row, col = locn
        for b in range(len(bag_list)):
            # compute set of squares occupied by bag b at locn
            bag_squares = set((r+row, c+col) for r, c in bag_list[b])

            # is bag in-bounds? if not, it doesn't fit here
            if len(bag_squares - all_squares) != 0:
                continue

            # are all of those bag squares free?
            if len(bag_squares & covered_squares) == 0:
                # yes, try packing with bag at this locn
                result = helper(covered_squares | bag_squares)
                if result:
                    ## CHANGED to record ALL PACKINGS. Don't return; instead
                    ## add to list of packings and continue
                    for r in result:
                        if packings is None:
                            packings = []
                        packings.append([{"anchor": locn, "shape": b}] + r)
            # CHANGED: keep looking for more (continue for loop)
        ## CHANGED: Exhausted bag options. Return packings (might be None)
        return packings 

    # get things started
    return helper(missing_squares)


bag_list = [
  { (0,0), (1,0), (2,0) },  # vertical 3x1 bag
  { (0,0), (0,1), (0,2) },  # horizontal 1x3 bag
  { (0,0), (0,1), (1,0), (1,1) }, # square bag
  { (0,0), (1,0), (1,1) },  # L-shaped bag
  { (0,0), (0,1), (1,0), (2,0), (2,1) },  # C-shaped bag
  { (0,0), (0,1), (1,1), (2,0), (2,1) },  # reverse C-shaped bag
]

if __name__ == '__main__':
    """
    # Succeeds, no backtracking (case 1)
    tent_size = (1,3)
    rocks = set()
    print(pack(tent_size, rocks, bag_list))
    print(all_packings(tent_size, rocks, bag_list))
    
    # Succeeds; more than one packing possible
    tent_size = (3,3)
    rocks = set()
    #print(pack(tent_size, rocks, bag_list))
    res = all_packings(tent_size, rocks, bag_list)
    print("all_packing -- number of packings:", len(res))
    print(res)
    
    # Succeeds, no backtracking (case 10)
    tent_size = (5,2)
    rocks = {(1,0),(3,1)}
    print(pack(tent_size, rocks, bag_list))
    
    # Succeeds, lots of backtracking (case 5)
    # Also interesting in that there are MULTIPLE packings possible
    tent_size = (4,4)
    rocks = set()
    print(pack(tent_size, rocks, bag_list))
    
    res = all_packings(tent_size, rocks, bag_list)
    print("NUMBER PACKINGS:", len(res) if res is not None else 0)
    print("packing:\n", res[0])
    
    for i in range(len(res)):
        print("Packing", i, ":", res[i])
    
    # No packing possible (case 12)
    tent_size = (5,5)
    rocks = {(1,1),(1,3),(3,1),(3,3)}
    print(pack(tent_size, rocks, bag_list))
    """

    
    
    
