"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def set_peek(s):
    """
    Helper function: return an arbitrary element that is in the given set
    without modifying the set.
    """
    for i in s:
        return i


def dict_peek(d):
    """
    Helper function: return an arbitrary (key, value) tuple from the given
    dictionary without modifying the dictionary.
    """
    for x in d.items():
        return x


def unit_propagation(formula, assignment):
    """
    implement unit propagation: given a formula, look for a clause that
    contains a single variable.  if we find one, add it to our assignments.

    returns a 3-tuple containing an indicator of success, our assignments, and
    the updated formula.
    """
    # unit propagation
    while True:
        for ix, clause in enumerate(formula):
            if len(clause) == 1:
                # here we have a single variable
                # gross hack to look at one element without popping it
                (var, val) = set_peek(clause)
                break  # break the for, continuing the while.
        else:
            # if we get here normally, break the while loop (no more unit
            # literals)
            break

        # we arrive here if we found a value.  propagate.
        result = propagate(formula, var, val, assignment)

        if result[0] is None:
            # we're still going.
            _, assignment, formula = result
        else:
            return result
    return None, assignment, formula


def pure_literal_propagation(formula, assignment):
    """
    implement pure literal propagation: given a formula, look for a variable
    that only shows up in a single polarity across all clauses.  if we find
    one, add it to our assignments.

    returns a 3-tuple containing an indicator of success, our assignments, and
    the updated formula.
    """
    # pure literal propagation
    # (things that can only be in one polarity)
    while True:
        consider = {j[0]: set() for i in formula for j in i}
        for i in formula:
            for j in i:
                consider[j[0]].add(j[1])
        consider = {k: v for k,v in consider.items() if len(v) == 1}
        if not consider:
            break

        var, val = dict_peek(consider)
        val = val.pop()

        # we arrive here if we found a value.  propagate.
        result = propagate(formula, var, val, assignment)

        if result[0] is None:
            # we're still going.
            _, assignment, formula = result
        else:
            return result
    return None, assignment, formula


def propagate(formula, var, val, assignment):
    """
    helper function that simplifies a formula given a new variable and value to
    set.

    returns a 3-tuple containing an indicator of success, our assignments, and
    the updated formula.
    """
    # make a copy of assignment to work with, and set the given variable to the
    # given value in it.
    assignment = dict(assignment)
    assignment[var] = val
    # update the formula based on this assignment.
    # clauses containing (var, val) are satisfied already (so remove them from the formula).
    # clauses containing (var, not val) must be satisfied by another variable,
    # so remove (var, not val) from them but otherwise leave them intact.
    new_form = [clause - {(var, not val)} for clause in formula if (var, val) not in clause]

    # at this point, if any empty clauses exist, they cannot be satisfied.  and
    # if no clauses remain, we have already satisfied the formula.
    if not new_form:
        # if the list is empty, we win
        return True, assignment, []
    if not all(new_form):
        # if any clause is empty, we lose
        return False, {}, []
    # otherwise, we're still going
    return None, assignment, new_form


def sat_helper(formula, assignment):
    """
    helper function that implements the core functionality for the SAT solver.

    returns a 3-tuple containing an indicator of success, our assignments, and
    the updated formula.

    the indicator of success takes one of three values:
       * True: everything has been satisfied
       * False: the formula could not be satisfied
       * None: still in progress.
    """
    # do unit propagation and continue on.
    res = unit_propagation(formula, assignment)
    if res[0] is not None:
        # if unit propagation caused everything to be satisfied (or found that
        # we can't satisfy), return the result.
        return res

    # if we didn't return something, we need to continue on with our updated
    # assignments and formula.
    _, assignment, formula = res

    # do pure literal propagation and continue on.
    res = pure_literal_propagation(formula, assignment)
    if res[0] is not None:
        # if pure literal propagation caused everything to be satisfied (or
        # found that we can't satisfy), return the result.
        return res

    # if we didn't return something, we need to continue on with the updated
    # assignments and formula.
    _, assignment, formula = res

    # neither of the above fully solved the problem.  so we'll pick a variable
    # and try setting it.
    var, _ = set_peek(formula[0])  # grab a variable

    # recurse with set to true
    form_true = propagate(formula, var, True, assignment)
    if form_true[0] is True:
        return form_true
    elif form_true[0] is None:
        rec_result = sat_helper(form_true[2], form_true[1])
        if rec_result[0] is True:
            return rec_result

    # if we get here, setting the variable to True did not work.  try False.
    form_false = propagate(formula, var, False, assignment)
    if form_false[0] is not None:
        return form_false

    # if we are here, those recursive calls suggested that the process is
    # ongoing.  recurse.
    return sat_helper(form_false[2], form_false[1])


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.  Returns that
    assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    {'a': True}
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    # convert the formula to a list of sets.
    formula = [set(i) for i in formula]

    # call the helper starting with the givne formula and an empty assignments
    # dictionary.
    result = sat_helper(formula, {})
    if result[0]:
        return result[1]  # result[1] will be the dictionary of assignments.
    else:
        return None


def make_neighbor_db(data):
    """
    Returns a different mapping that is more conducive to the kinds of
    operations we want to perform.  This new mapping maps each actor id to a
    set of people they have acted with (these sets also contain IDs, not
    names).
    """
    acted_with = {}
    for i, j, _ in data:
        # the setdefault method lets us avoid checking for ourselves whether an
        # actor is aclready in the dictionary.
        # see https://docs.python.org/3/library/stdtypes.html#dict.setdefault
        acted_with.setdefault(i, set()).add(j)
        acted_with.setdefault(j, set()).add(i)
    return acted_with


def make_vars_for_actors(neighbors, K):
    var = 1
    out = {}
    for actor in neighbors:
        out[actor] = [ var + i  for i in range(0, K)]
        var += K
    return out


def unique(varlist):
    result = []
    for v1 in varlist:
        for v2 in varlist:
            if (v1 < v2):
                result.append([(v1,0), (v2,0)])
    result.append([(v,1) for v in varlist])
    return result

def make_one_manager_constraints(vars_for_actors):
    out = []
    for actor in vars_for_actors:
        out += (unique(vars_for_actors[actor]))
    return out

def make_different_constraint(neighbors, vars_for_actors):
    result = []
    for actor in neighbors:
        for coactor in neighbors[actor]:
            if(actor != coactor):
                vars_for_actor = vars_for_actors[actor]
                vars_for_coactor = vars_for_actors[coactor]
                for v1, v2 in zip(vars_for_actor, vars_for_coactor):
                    result.append([(v1,0),(v2,0)])
    return result

def construct_solution(sol, vars_for_actors):
    out = {}
    def get_value(varlist):
        for i,v in enumerate(varlist):
            if sol[v] == 1:
                return i
        return None

    for actor in vars_for_actors:
        out[actor] = get_value(vars_for_actors[actor])
    return out

def managers_for_actors(K, film_db):
    '''
    Input:
       K , number of managers available.
       film_db, a list of [actor, actor, film] triples describing that two
       actors worked together on a film.
    Output:
        An assignment of actors to managers, where
        actors are identified by their numerical id in film_db and
        managers are identified by a number from 0 to K-1.
        The assignment must satisfy the constraint that
        if two actors acted together in a film, they should not have the
        same manager.
        If no such assignment is possible, the function returns None.

    You should write this function in terms of three methods:
        make_vars_for_actors: for each actor in the db, you want an indicator
        variable for every possible manager indicating whether that manager
        is the manager for that actor.

        make_one_manager_constraints: This function should create constraints that
        ensure that each actor has one and only one manager.

        make_different_constraint: This function should create constraints
        that ensure that each actor has a different manager from other actors
        in the same movie.
    '''
    neighbors = make_neighbor_db(film_db)

    vars_for_actors = make_vars_for_actors(neighbors, K)

    only_one_manager = make_one_manager_constraints(vars_for_actors)

    different_from_coactors = make_different_constraint(neighbors, vars_for_actors)

    sol = satisfying_assignment(only_one_manager + different_from_coactors)
    if sol is None:
        print("UNSAT")
        return None
    else:
        print(len(sol))
        return construct_solution(sol, vars_for_actors)

def check_solution(sol, K, film_db):
    '''
    Input:
        K, number of managers
        flim_db, a list of [actor, actor, film] triples describing that two
        actors worked together on a film.
        sol, an assignment of actors to managers.
    Output:
        The function returns True if sol satisfies the constraint that
        if two actors acted together in a film, they should not have the
        same manager and every manager has an ID less than K.
        It returns False otherwise.
    '''
    for actor, coactor, film in film_db:
        if sol[actor] >= K:
            print ("Out of range value " + str(sol[actor]))
            return False
        if actor != coactor and sol[actor] == sol[coactor]:
            print("Actors " + str(actor) + " and " + str(coactor) + " worked together on " + str(film)
            + " they cannot have the same agent " + str(sol[actor]))
            return False
    return True
