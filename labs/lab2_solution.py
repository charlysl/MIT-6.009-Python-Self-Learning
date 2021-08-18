# NO IMPORTS ALLOWED!

import json

BACON = 4724

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    """
    Returns True if the two given actors acted together (according to the given
    database) and False otherwise.
    """
    these_actors = {actor_id_1, actor_id_2}
    return any({i, j} == these_actors for i, j, _ in data)


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


def expand(acted_with, current_level, parents):
    """
    Run one "expansion", moving to a larger Bacon number.

    Arguments:
       acted_with: a mapping from IDs to the people they have acted with (the
                   output from make_neighbor_db)
       current_level: a set containing the IDs at the 'current' Bacon level (N)
       parents: a dictionary mapping actor IDs to their parents (i.e., the actor
                that led to them while traversing the graph).

    Returns:
       The set of people with Bacon number N+1
    """
    new_level = set()
    # we want to find all the neighbors of everyone at level N who have not
    # already been seen as we work outward from the center.
    for actor in current_level:
        for neighbor in acted_with[actor]:
            # avoid duplicates by ignoring people we have already seen.  every
            # actor we've seen is in the parents dictionary, so we skip any
            # actor that is already in that dictionary.
            if neighbor not in parents:
                # this is a new actor.  add them to our set of people at level
                # N+1, and also add them to the parents dictionary so we don't
                # double-count them later.
                parents[neighbor] = actor
                new_level.add(neighbor)
    return new_level


def get_actors_with_bacon_number(data, n):
    """
    Returns the set of people who have a given Bacon number.
    """
    acted_with = make_neighbor_db(data)
    # Initialize the parents and the first level of the Bacon number (level 0).
    # BACON has no parent, and he is the only member of level 0.
    parents = {BACON: None}
    cur_level = {BACON}
    # Now, expand out N times, so that we end up with the people with Bacon
    # number N in cur_level.
    for i in range(n):
        cur_level = expand(acted_with, cur_level, parents)
        if not cur_level:
            return set()
    return cur_level  # spec requires that we return a set.


def get_bacon_path(data, actor_id):
    """
    Returns the path of actor ids from BACON to the given actor ID.  Uses
    get_path.
    """
    return get_path(data, BACON, actor_id)


def get_path(data, actor_id_1, actor_id_2):
    """
    Return the path of actor IDs connecting actor_id_1 to actor_id_2
    """
    acted_with = make_neighbor_db(data)
    # Intialize the parents and the first level (starting from actor_id_1).
    # actor_id_1 is our root (it has no parent), and it is the only element in
    # the set of things that have 0 distance from
    parents = {actor_id_1: None}
    cur_level = {actor_id_1}
    # Now we continually expand outward.  We stop in one of two conditions:
    # either actor_id_2 is in the current level (we succeeded!) or there are no
    # elements at the current level (we explored the whole space and never
    # found actor_id_2!).
    while actor_id_2 not in cur_level and cur_level:
        cur_level = expand(acted_with, cur_level, parents)
    # If we failed to find a path, we return None.  Otherwise we return the
    # path from actor_id_1 to actor_id_2 (using the trace_path helper).
    return trace_path(actor_id_2, parents) if actor_id_2 in cur_level else None

def trace_path(person, parents):
    """
    Helper function for get_path.  This traces back through the parent
    dictionary from a given point and returns the path from the root to that
    point.
    """
    out = []
    while person is not None:
        out.append(person)
        person = parents[person]
    return out[::-1]  # the list we constructed is in reverse order, so flip it.


def get_actor_name_map():
    """
    Helper function for get_movie_path.  Returns a mapping from actor names to
    ID numbers.
    """
    with open('resources/names.json') as f:
        return json.load(f)


def get_movie_name_map():
    """
    Helper function for get_movie_path.  Returns a mapping from movie names to
    ID numbers.
    """
    with open('resources/movies.json') as f:
        return json.load(f)


def get_actors_to_movie_db(data):
    """
    Helper function for get_movie_path.  Returns a mapping from pairs of actors
    to the ID number of a movie in which they acted together.
    """
    out = {}
    for a1, a2, m in data:
        out[frozenset({a1, a2})] = m
    return out


def get_movie_path(data, actor_name_1, actor_name_2):
    """
    Returns a list of movie names that connect the two given actors (here given
    as names, not as IDs)
    """
    # We start by creating a few useful mappings using the helper functions
    # above.
    movie_db = get_actors_to_movie_db(data)
    movie_name_db = {v: k for k,v in get_movie_name_map().items()}
    id_from_name = get_actor_name_map()
    # Next, determine the ID numbers of the given actors.
    actor_id_1 = id_from_name[actor_name_1]
    actor_id_2 = id_from_name[actor_name_2]
    # Find the path between them in terms of actors normally.
    actor_path = get_path(data, actor_id_1, actor_id_2)
    # Look up the movie ID numbers that connect each successive pair of actors.
    movie_id_path = [movie_db[frozenset(x)] for x in zip(actor_path, actor_path[1:])]
    # And, finally, convert the movie ID numbers into names.
    return [movie_name_db[i] for i in movie_id_path]


if __name__ == '__main__':
    with open('resources/large.json') as f:
        largedb = json.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    print(get_movie_path(largedb, "Anton Radacic", "Sandra Bullock"))
