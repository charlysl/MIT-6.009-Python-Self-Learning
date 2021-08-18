# NO IMPORTS!

#############
# Problem 1 #
#############

def runs(L):
    """ return a new list where runs of consecutive numbers
        in L have been combined into sublists. """
    last = None
    result = []
    # process the list one-at-a-time
    for x in L:
        # if there's a sequence in progress check if x goes at end
        if last is not None:
            # does x belong at end of current sequence?
            if last[-1]+1 == x:
                # yup, add it and move to next number
                last.append(x)
                continue
            else:
                # otherwise we're done with current sequence.
                # 1-element sequences are inserted as singletons
                result.append(last[0] if len(last)==1 else last)
        # x is potentially the start of a new sequence
        last = [x]

    # deal with the last current sequence
    if last is not None:
        result.append(last[0] if len(last)==1 else last)

    return result

#############
# Problem 2 #
#############

def is_cousin(parent_db, A, B):
    """ Return True if A and B share a grandparent but do
        not share a parent. """

    # process parent_db into a dict that maps a person
    # to a set containing their parents
    parents = {}   # maps person => set of parents
    for parent,child in parent_db:
        parents.setdefault(child,set()).add(parent)
        
    # cousins don't share any parents
    if not parents[A].isdisjoint(parents[B]):
        return None

    # return set of p's grandparents
    def grandparents(p):
        return set(grandparent
                   for parent in parents[p]
                   for grandparent in parents[parent])

    # but cousins do have at least one grandparent in common,
    # so compute intersection of A's and B's grandparents and
    # check that it's non-empty.
    gparents = grandparents(A).intersection(grandparents(B))
    return None if len(gparents)==0 else gparents.pop()

#############
# Problem 3 #
#############

def all_phrases(grammar, root):
    """ Using production rules from grammar expand root into
        all legal phrases. """

    # recursively generate expansion of phrase, stopping when there
    # are no more nonterminals
    def expand(phrase):
        # look for first nonterminal then expand it
        for i,s in enumerate(phrase):
            # is s a non-terminal?
            if s in grammar:
                # replace nonterminal with each of its productions
                for production in grammar[s]:
                    expansion = phrase[:i] + production + phrase[i+1:]
                    # then expand the updated phrase
                    yield from expand(expansion)
                return

        # no nonterminals: its legal!
        yield phrase

    # materialize result of generator
    return list(expand([root]))


## Version without generators
def all_phrases(grammar, root):
    """ Using production rules from grammar expand root into
        all legal phrases. """

    # recursively generate expansion of phrase, stopping when there
    # are no more nonterminals
    def expand(phrase):
        # look for first nonterminal then expand it
        for i,s in enumerate(phrase):
            results = []
            # is s a non-terminal?
            if s in grammar:
                # replace nonterminal with each of its productions
                for production in grammar[s]:
                    expansion = phrase[:i] + production + phrase[i+1:]
                    # then expand the updated phrase
                    results = results + expand(expansion)
                return results

        # no nonterminals: we're done!
        return [phrase]

    # run helper
    return expand([root])
