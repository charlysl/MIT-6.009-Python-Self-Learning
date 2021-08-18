# NO IMPORTS!

##############
# Problem 01 #
##############

def find_triple(ilist):
    """ If the list ilist contains three values x, y, and z such that x + y = z
        return a tuple with x and y. Otherwise return None. """
    s = set(ilist)
    for i in range(len(ilist)):
        for j in range(i+1,len(ilist)):
            x = ilist[i]
            y = ilist[j]
            if (x+y) in s:
                # make sure third elements differs from first two!
                z = ilist.index(x+y)
                if z == i or z == j: continue
                return (x,y)
    return None

##############
# Problem 02 #
##############

def is_palindrome(s):
    return s == s[::-1]

def is_quasidrome(s):
    """Check whether s is a quasidrome."""
    if is_palindrome(s):
        return True
    return any(is_palindrome(s[:cut] + s[cut+1:]) for cut in range(len(s)))

##############
# Problem 03 #
##############

def max_subsequence(ilist, is_circular = False):
    """ Return the start and end indices as a tuple of the maximum subsequence
        in the list.  If is_circular = True, imagine the list is circular.
        That is, after the end index comes the start index.  """
    n = len(ilist)
    if is_circular: ilist = ilist + ilist
    maxsum = None
    result = None
    for start in range(n):
        for slen in range(1,n+1):
            if start + slen <= len(ilist):
                test = sum(ilist[start:start+slen])
                if maxsum is None or test > maxsum:
                    maxsum = test
                    result = (start,(start+slen-1) % n)
    return result

##############
# Problem 04 #
##############

# This problem is trickier.  Here are three solutions (they all
# assume that there are no duplicate edges).  We'd left a few
# questions (as comments) here and there; they are a good way to
# test your understanding!

# The first solution is much like in the Bacon lab in that
# we first build a useful mapping of a vertex to its neighbors

def count_triangles(edges):
    """Count the number of triangles in edges."""
    # build adjaceny dict: vertex => set of immediate neighbor vertices
    neighbors = {}
    for source, destination in edges:
        neighbors.setdefault(source,set()).add(destination)
        neighbors.setdefault(destination,set()).add(source)

    count = 0
    for v1 in neighbors:
        for v2 in neighbors[v1]:
            for v3 in neighbors[v2]:
                if v1 in neighbors[v3]:
                    count += 1
    return count // 6 # Think about this part: why do we divide by 6?

# The second solution can be a bit less efficient, but it's
# still reasonable.  Bonus question to think about: in which
# cases is solution 1 much faster than solution 1? In which
# cases is it about the same?  Can it be slower?

def count_triangles_2(edges):
    """Count the number of triangles in edges."""
    edgeset, vertexset = set(), set()
    for v1, v2 in edges:
        vertexset.add(v1)
        vertexset.add(v2)
        edgeset.add((v1, v2))
        edgeset.add((v2, v1))
    vertices = list(vertexset)

    def is_triangle(edges, v1, v2, v3):
        return (v1, v2) in edges and (v2, v3) in edges and (v3, v1) in edges

    count = 0
    for idx1 in range(len(vertices)):
        for idx2 in range(idx1 + 1, len(vertices)):
            for idx3 in range(idx2 + 1, len(vertices)):
                if is_triangle(edgeset, vertices[idx1], vertices[idx2], vertices[idx3]):
                    count += 1
    return count # Why don't we divide by 6 here?

# The third one is much less efficient.  The idea here is to
# iterate over all *edges*, instead of all *vertices*.  In the
# quiz, such a solution would pass almost everything, but on
# examples with many edges it might fail.

def is_triangle_3(e1, e2, e3):
    # Why is it enough to test just this sequence?
    return e1[1] == e2[0] and e2[1] == e3[0] and e3[1] == e1[0]

def all_triangles_3(edges):
    triangles = set()
    for e1 in edges:
        for e2 in edges:
            for e3 in edges:
                if is_triangle_3(e1, e2, e3):
                    # Why do we use tuple() here?
                    triangles.add(tuple(sorted((e1[0], e2[0], e3[0]))))
    return triangles

def count_triangles_3( edges ):
    """Count the number of triangles in edges."""
    all_edges = []
    all_edges.extend(edges)
    all_edges.extend([y, x] for [x, y] in edges)
    return len(all_triangles_3(all_edges)) # Why don't we divide by 6 here?

##############
# Problem 05 #
##############

def is_unique( A ):
    """ return True if no repeated element in list A. """
    A.sort()
    return all(A[i] != A[i-1] for i in range(1,len(A)))

##############
# Problem 06 #
##############

def matrix_product( A, B, m, n, k ):
    """ compute m-by-k product of m-by-n matrix A with n-by-k matrix B. """
    return [sum(A[i + n*r] * B[c + i*k] for i in range(n))
            for r in range(m)
            for c in range(k)]

##############
# Problem 07 #
##############

def mode( A ):
    """ return the most common value in list A. """
    currMode = None
    maxCount = 0
    for a in A:
        count = A.count(a)  # count occurrences of a in A
        if count > maxCount:
            currMode = a
            maxCount = count
    return currMode

##############
# Problem 08 #
##############

def transpose( A, m, n ):
    """ return n-by-m transpose of m-by-n matrix A. """
    # each row of the output is a column of the input
    return [A[c*n + r]
            for r in range(n)
            for c in range(m)]

##############
# Problem 09 #
##############

def check_valid_paren(s):
    """return True if each left parenthesis is closed by exactly one
    right parenthesis later in the string and each right parenthesis
    closes exactly one left parenthesis earlier in the string."""
    diff = 0
    for ch in s:
        diff = diff + 1 if ch == "(" else diff - 1
        if diff < 0:
            # if at any point we've seen more ) than (
            return False
    # if we saw the same number of ( and )
    return diff == 0

##############
# Problem 10 #
##############

def get_all_elements(root):
    """ Return a list of all numbers stored in root, in any order. """
    # generator recursively walks the tree yielding values
    def walk_tree(node):
        if node is not None:
            yield from walk_tree(node["left"])
            yield node["value"]
            yield from walk_tree(node["right"])

    # call to list ensure an actual list as the result
    return list(walk_tree(root))

# here's a straight-forward recursive solution
def get_all_elements_recursive(root):
    """ Return a list of all numbers stored in root, in any order. """
    elements = [root["value"]]
    if root["left"] != None:
        elements.extend(get_all_elements(root["left"]))
    if root["right"] != None:
        elements.extend(get_all_elements(root["right"]))
    return elements

##############
# Problem 11 #
##############

def find_path(grid):
    """ Given a two dimensional n by m grid, with a 0 or a 1 in each cell,
        find a path from the top row (0) to the bottom row (n-1) consisting of
        only ones.  Return the path as a list of coordinate tuples (row, column).
        If there is no path return None. """
    n = len(grid)
    m = len(grid[0])

    def helper(row,col,path):
        if row == n:
            return path
        for i in range(col-1,col+2):
            if 0 <= i < m and grid[row][i]:
                result = helper(row+1,i,path + [(row,i)])
                if result is not None:
                    return result
        return None

    for c in range(0,m):
        if grid[0][c]:
            result = helper(1,c,[(0,c)])
            if result is not None:
                return result
    return None

##############
# Problem 12 #
##############

def longest_sequence(s):
    """ find sequences of a single repeated character in string s.
        Return the length of the longest such sequence. """
    max_len = 0    # length of longest sequence seen so far                                                           
    cur_len = 0    # length of current sequence                                                                       
    last_ch = None # previous character                                                                               
    for ch in s:
        cur_len = cur_len + 1 if ch == last_ch else 1
        max_len = max(cur_len,max_len)
        last_ch = ch
    return max_len

##############
# Problem 13 #
##############

# straightforward enumeration
def integer_right_triangles(p):
    """Let p be the perimeter of a right triangle with integral, non-zero
       length sides of length a, b, and c.  Return a sorted list of                                                          solutions with perimeter p. """
    return [[a,b,p-a-b]
            for a in range(1,p)
            for b in range(a,p)
            if a**2 + b**2 == (p-a-b)**2]

# a mathematician's solution
# this is very fast, but we wouldn't expect you to find this solution
def integer_right_triangles_at_the_speed_of_list(p):
    solutions = []
    # one side will always be shorter than p//2
    for x in range(1, p // 2):   
        # we know x^2 + y^2 = z^2 and x + y + z = p
        # so (p - x - y)^2 = x^2 + y^2
        # so p^2 - 2px - 2py + 2xy = 0                                                                                
        # now solve for y given x and p
        y, r = divmod(p*p - 2*p*x, 2*(p - x))
        if r == 0 and x < y:
            z = p - x - y
            solutions.append([x, y, z])
    return solutions

##############
# Problem 14 #
##############

def encode_nested_list(seq):
    """Encode a sequence of nested lists as a flat list."""
    # use recursive generator to avoid creating a zillion intermediate-level lists
    def encode(L):
        if not isinstance(L, list):
            yield L
        else:
            yield "up"
            for y in L:
                yield from encode(y)
            yield "down"

    return list(encode(seq))

def encode_nested_list_recursive(seq):
    """Encode a sequence of nested lists as a flat list."""
    if not isinstance(seq, list):
        return [seq]
    return ["up"] + [x for y in seq for x in encode_nested_list(y)] + ["down"]
