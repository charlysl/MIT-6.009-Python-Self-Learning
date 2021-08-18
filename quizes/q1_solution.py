# NO IMPORTS!

##################################################
### Problem 1: batch
##################################################

def batch(inp, size):

    """
    Inputs:
      inp is a tuple of non-zero integers.
      size is a non-zero integer.

    Outputs:
      Return a list of batches, where each batch is a list of elements (in
    order from the beginning) from inp, until the batch is filled, i.e.,
    the sum of the elements in the batch is equal to or greater than
    size, or there are no more elements.

    >>> batch((13, 2, 3, 4, 3, 1, 1, 1, 4, 2, 3), 5)
    [[13], [2, 3], [4, 3], [1, 1, 1, 4], [2, 3]]

    >>> batch((6, 6, 6, 6, 6), 7)
    [[6, 6], [6, 6], [6]]

    """
    out = []

    batch = []
    for elt in inp:
        batch.append(elt)
        if sum(batch) >= size:
            out.append(batch)
            batch = []
    if len(batch) > 0:
        out.append(batch)
    return out


##################################################
### Problem 2: order
##################################################

def order(inp):
    letter = {}
    letter_order = []
    for string in inp:
        first = string[0]
        if first not in letter:
            letter_order.append(first)
            letter[first] = []
        letter[first].append(string)
    output = []
    for start in letter_order:
        output.extend(letter[start])
    return output


##################################################
### Problem 3: path_to_happiness
##################################################

def path_to_happiness(field):
    """ Return a path through field of smiles that maximizes happiness """

    def pick_best(best_partial_path, r, c):
        """ return (happiness, path) for highest happiness path up to this (r, c) """
        options = []
        for rr in (r-1,r,r+1): # up_right, right, down_right
            if rr >= 0 and rr < field["nrows"]:
                options.append(best_partial_path[rr])
        best = sorted(options,reverse=True)[0]
        return best

    # For each column c in turn, keep track of best happiness
    # and path up to the given row r in that column

    best_partial_path = {r: (0, []) for r in range(field["nrows"])}

    # Continue for each column, updating best path for that column as we go
    for c in range(field["ncols"]):
        best_this_c = {}
        for r in range(field["nrows"]):
            prev_h, prev_p = pick_best(best_partial_path, r, c)
            smiles = field["smiles"][r][c]
            best_this_c[r] = (prev_h + smiles, prev_p + [r])
        best_partial_path = best_this_c

    # Pick highest happiness path among rows in final column
    return sorted(best_partial_path.values(), reverse=True)[0][1]



