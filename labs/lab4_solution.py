"""6.009 Lab 4 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def make_nd_board(dims, fill):
    """
    Recursively construct an n-dimensional board filled with a given element.

    Arguments:
        dims: the dimensions of the board to be created
        fill: the element to put in the board
    >>> make_nd_board([1,2], 7)
    [[7, 7]]
    """
    if len(dims) == 1:
        return [fill] * dims[0]
    else:
        return [make_nd_board(dims[1:], fill) for i in range(dims[0])]


def nd_neighbors(loc, dims):
    """
    Generator to yield the neighbors of a given location.
    Note: also yields the given location

    Arguments:
        loc: the location whose neighbors we want to find
        dims: the dimensions of the space
    >>> dims = [1, 2, 3]
    >>> near = nd_neighbors([0, 1, 2], dims)
    >>> set(near) == {(0, 0, 1), (0, 1, 1), (0, 0, 2), (0, 1, 2)}
    True
    """
    if len(loc) == 0:
        # base case is 0-d
        # yield a single tuple so the 1-d case can build on this
        yield tuple()
    else:
        # recursive case.  find the neighbors of loc[1:] in a space of lower
        # dimensionality.  then add x-1, x, and x+1 to the front of each
        # neighbor in the lower-d space, where x is the coordinate in this
        # dimension.
        for j in nd_neighbors(loc[1:], dims[1:]):
            yield from (((x, )+j) for x in (loc[0]-1, loc[0], loc[0]+1) if 0<=x<dims[0])


def nd_get(array, loc):
    """
    Returns the element at the given location in the given array.
    >>> b = make_nd_board([1,2], 7)
    >>> nd_get(b, [0,1])
    7
    """
    if len(loc) == 1:
        return array[loc[0]]
    else:
        return nd_get(array[loc[0]], loc[1:])


def nd_set(array, loc, val):
    """
    Sets the element at the given location in the given array to be the given
    value.
    >>> b = make_nd_board([1,2], 7)
    >>> nd_set(b, [0,1], 77)
    >>> nd_get(b, [0,1])
    77
    """
    if len(loc) == 1:
        array[loc[0]] = val
    else:
        nd_set(array[loc[0]], loc[1:], val)


def all_coords(dims):
    """
    Generator to yield all the coordinates in a space with the given
    dimensionality.
    >>> set(all_coords([3])) == {(0,), (1,), (2,)}
    True
    >>> set(all_coords([1,2])) == {(0,1), (0,0)}
    True
    """
    if len(dims) == 0:
        yield tuple()
    else:
        yield from ((i, )+j for j in all_coords(dims[1:]) for i in range(dims[0]))



class HyperMinesGame:

    def __init__(self, dims, bombs):
        """Start a new game.

        This method should properly initialize the "board" and "mask"
        attributes.

        Args:
           dims (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate

        Returns:
           A game state dictionary

        >>> g = HyperMinesGame([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]])
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, False], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: ongoing
        """
        self.board = make_nd_board(dims, 0)
        for b in bombs:
            nd_set(self.board, b, '.')
            for n in nd_neighbors(b, dims):
                v = nd_get(self.board, n)
                if isinstance(v, int):
                    nd_set(self.board, n, v+1)
        self.mask = make_nd_board(dims, False)
        self.dimensions = dims
        self.state = 'ongoing'


    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))


    def dig(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 3, 0])
        8
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, True], [True, True], [True, True]]
               [[False, False], [False, False], [True, True], [True, True]]
        state: ongoing
        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 0, 1])
        1
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, True], [False, True], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: defeat
        """
        if self.state != 'ongoing' or nd_get(self.mask, coords):
            return 0

        nd_set(self.mask, coords, True)

        this_spot = nd_get(self.board, coords)
        if this_spot == '.':
            self.state = 'defeat'
            return 1

        count = 1
        if this_spot == 0:
            for n in nd_neighbors(coords, self.dimensions):
                count += self.dig(n)

        self.state = 'victory' if self.victory() else 'ongoing'
        return count

    def victory(self):
        """
        Return True if the given game represents a victory condition, and False
        otherwise.
        >>> g = HyperMinesGame([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]])
        >>> g.victory()
        False

        """
        for c in all_coords(self.dimensions):
            brd = nd_get(self.board, c)
            msk = nd_get(self.mask, c)
            # two things mean we have not won:
            if brd == '.' and msk:  # a bomb that has been uncovered.
                return False
            if brd != '.' and not msk:  # a safe square that has not be uncovered.
                return False
        return True

    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
        ...                     [[False, False], [False, False], [True, True], [True, True]]],
        ...            "state": "ongoing"})
        >>> g.render(False)
        [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
         [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

        >>> g.render(True)
        [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
         [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
        """
        out = make_nd_board(self.dimensions, None)
        for c in all_coords(self.dimensions):
            brd = nd_get(self.board, c)
            msk = nd_get(self.mask, c)
            nd_set(out, c, '_' if not xray and not msk else ' ' if brd == 0 else str(brd))
        return out


    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
