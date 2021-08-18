
# coding: utf-8

# Some instrumentation to help see/show how recursion works. While this needs to be executed, you can ignore the details (unless you're curious!) and skip directly to "Recursive Patterns" below.

# In[1]:

from functools import wraps
import sys
def instrument(f):
    """This is a helpful wrapper, to instrument a function to show the
    call entry and exit from that function.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        call_depth = wrapper.call_count
        wrapper.call_count += 1
        argstr = ', '.join([str(args[i]) for i in range(len(args))])
        sys.stderr.write("   "*call_depth + "call to " + f.__name__ + ": " + argstr + "\n")
        result = f(*args, **kwargs)
        sys.stderr.write("   "*call_depth + f.__name__ + " returns: " +  str(result) + "\n")
        wrapper.call_count -= 1
        return result
    wrapper.call_count = 0
    return wrapper


# # Recursive Patterns
# ## Let's start with some simple functions that recurse on lists...
# ### Walk the list to find the first value satisfying function `f`

# In[2]:

@instrument
def walk_list(L, f):
    """Walk a list -- in a recursive style. Note that this is done as a
    stepping stone toward other recursive functions, and so does not
    use easier/direct built-in list functions.
    
    In this first version -- walk the list just to find/return the
    FIRST item that satisfies some condition, where f(item) is true.
    
    >>> walk_list([1, 2, 3], lambda x: x > 2)
    3
    """
    if L == []:      #base case
        return None
    if f(L[0]):      #another base case
        return L[0]
    return walk_list(L[1:], f) #recursive case


# In[3]:

walk_list([1, 2, 3], lambda x: x > 2)


# ### Walk a list, but now returning a <em>list</em> of items that satisfy `f` -- uses stack

# In[4]:

@instrument
def walk_list_filter1(L, f):
    """ Walk a list, returning a list of items that satisfy the
    condition f.

    This implementation uses the stack to hold intermediate results,
    and completes construction of the return list upon return of
    the recursive call.

    >>> walk_list_filter1([1, 2, 3], lambda x: x % 2 == 1) #odd only
    [1, 3]
    """
    if L == []:
        return []
    if f(L[0]):
        # the following waits to build (and then return) the list
        # until after the recursive call comes back with a sub-result
        return [L[0]] + walk_list_filter1(L[1:], f)
    else:
        return walk_list_filter1(L[1:], f)


# In[5]:

walk_list_filter1([1, 2, 3], lambda x: x % 2 == 1)


# ### Walk a list, returning a list of items that satisfy `f` -- uses helper with a "so_far" argument

# In[6]:

@instrument
def walk_list_filter2(L, f):
    """ Walk a list, returning a list of items that satisfy the
    condition f.

    This implementation uses a helper with an explicit 'so far'
    variable, that holds the return value as it is being built
    up incrementally on each call.

    >>> walk_list_filter2([1, 2, 3], lambda x: x % 2 == 1)
    [1, 3]
    """
    @instrument
    def helper(L, ans_so_far):
        if L == []:
            return ans_so_far
        if f(L[0]):
            ans_so_far.append(L[0])
        return helper(L[1:], ans_so_far) #tail recursive
    
    return helper(L, [])


# In[7]:

walk_list_filter2([1, 2, 3], lambda x: x % 2 == 1)


# Note the difference in how this works. `walk_list_filter2` builds up the result as an evolving argument to `helper`. 
# When we're done, the stack does nothing more than keep passing that result back up the call chain (i.e., is written in 
# a tail-recursive fashion). 
# In contrast, `walk_list_filter1` uses the stack to hold partial results, and then does further work to 
# build or complete the result after each recursive call returns.

# ## Now consider some functions that recurse on trees...
# We want to extend the basic idea of recursive walkers and builders for lists, now to trees. We'll see the same patterns at work, but now often with more base cases and/or more recursive branch cases.
# 
# For these examples, we need a simple tree structure. Here we'll represent a node in a tree as a list with the first element being the node value, and the rest of the list being the children nodes.
# That is to say, our tree structure is a simple nested list structure.
# <center><img src="images/tree1.png" alt="tree [13, [7], [8, [99], [16], [42]]]" width=150></center>

# In[8]:

tree1 = [13,
         [7],
         [8, 
          [99],
          [16, 
           [77]],
          [42]]]
tree1


# In[9]:

@instrument
def tree_max(tree):
    """Walk a tree, returning the maximum value in the (assumed non-empty) tree. """
    val = tree[0]
    children = tree[1:]
    if not children:     #base case
        return val
    # recursive case. Note that the following launches 
    # MULTIPLE recursive calls, one for each child...
    return max(val, max([tree_max(child) for child in children]))


# In[10]:

tree_max(tree1)


# In[11]:

@instrument
def depth_tree(tree):
    """ Walk a tree, returning the depth of the tree
    >>> depth_tree([13, [7], [8, [99], [16, [77]], [42]]])
    """
    if not tree:         #base case
        return 0    

    children = tree[1:]
    if not children:     #base case
        return 1
    
    #recursive case
    return max([1+depth_tree(child) for child in children])


# In[12]:

depth_tree([13, [7], [8, [99], [16, [77]], [42]]])


# Notice that the recursion structure is exactly the same in both cases?  We could generalize to something like a `walk_tree` that took a tree *and* a function `f` (and perhaps some other base case values), and did that operation at each step. We'll leave that as an exercise for the reader. 

# ### Now a "builder" or "maker" function, that recursively creates a tree structure...

# In[13]:

@instrument
def make_tree(L):
    """ Make and return a binary tree corresponding to the list. The
    tree is "binary" in the sense that left and right branches are
    balanced as much as possible, but no condition is imposed on the
    left/right values under each node in the tree.
    
    >>> make_tree([1,2,3])
    [1, 2, 3]
    """
    n = len(L)
    if n == 0:         #base case
        return []

    val = L[0]
    if n == 1:         #another base case -- no children
        return [val]
    
    split = (n-1) // 2
    left = make_tree(L[1:split+1]) #recursive left half of list
    right = make_tree(L[split+1:]) #recursive right half of list

    #return [val, left, right]
    # FIX: left branch might be empty (right branch will never be), so
    # only combine if left is not empty:
    return [val, left, right] if left else [val, right]


# In[14]:

tree2 = make_tree([1, 2, 3])
tree2


# In[15]:

tree3 = make_tree([1, 2]) #unbalanced tree case
tree3


# How many recursive calls do you expect for a list of length `n`?

# In[16]:

tree4 = make_tree(list(range(8)))
tree4


# In[17]:

def show_tree(tree):
    """ Return a formatted string representation to visualize a tree """
    spaces = '   '
    def helper(tree, level):
        if not tree:
            return ""
        val = tree[0]
        children = tree[1:]
        result = spaces*level + str(val) + '\n'
        for child in children:
            result += helper(child, level+1)
        return result
    return helper(tree, 0)


# In[18]:

print("tree4:", tree4, "\n", show_tree(tree4))


# ## Finally, consider some functions that recurse on graphs...
# For this, we need a more sophisticated structure, since a node may be referenced from more than one other node. We'll represent a (directed) graph as a dictionary with node names as keys, and associated with the key is a list holding the node value and a list of children node names. The special name 'root' is the root of the graph.
# 
# <center><img src="images/graph1.png" alt="graph1" width=200></center>

# In[19]:

graph1 = {'root': [13, ['A', 'B']],
          'A': [77, ['B', 'C']],
          'B': [88, []],
          'C': [-32, ['D']],
          'D': [42, []]}


# In[20]:

@instrument
def graph_max(graph):
    """Walk a graph, returning the maximum value in a (non-empty) graph.
    First, we'll assume there are no cycles in the graph. 
    """
    @instrument
    def node_max(node_name):
        val = graph[node_name][0]
        children = graph[node_name][1]
        if children:
            return max(val, max([node_max(child) for child in children]))
        return val
    return node_max('root')


# In[21]:

graph_max(graph1)


# What do we do if there *are* cycles in the graph, e.g.
# 
# <center><img src="images/graph_cycle.png" alt="graph with cycle" width=220></center>

# In[22]:

graph2 = {'root': [13, ['A', 'B']],
          'A': [77, ['B', 'C']],
          'B': [88, []],
          'C': [-32, ['D']],
          'D': [42, ['A']]} #changed; now D -> A


# In[23]:

#graph_max(graph2) # breaks! (need to re-execute def graph_max afterwards for instrumentation)


# In[24]:

@instrument
def graph_max2(graph):
    """Walk a graph, returning the maximum value in a (non-empty) graph.
    Now, however, there might be cycles.
    """
    visited = set()
    @instrument
    def node_max(node_name):
        val = graph[node_name][0]
        children = graph[node_name][1]
        new_children = [c for c in children if c not in visited]
        if new_children:
            visited.update(set(new_children))
            return max(val, max([node_max(child) for child in new_children]))
        return val
    return node_max('root')


# In[25]:

graph_max2(graph2)


# # Recursive Lists
# It's possible to create a simple python list that has itself as an element. In essence, that means that python lists themselves might be "graphs" and have cycles in them, not just have a tree-like structure!

# In[26]:

x = [0, 1, 2]
x[1] = x
print("x:", x)
print("x[1][1][1][1][1][1][1][1][1][1][2]:", x[1][1][1][1][1][1][1][1][1][1][2])


# We'd like a version of deep_copy that could create a (separate standalone) copy of a recursive list, *with the same* structural sharing (including any cycles that might exist!) as in the original recursive list.

# In[27]:

@instrument
def deep_copy(old, copies=None):
    if copies is None:
        copies = {}

    oid = id(old)      #get the unique python object-id for old

    if oid in copies:  #base case: already copied object, just return it
        return copies[oid]

    if not isinstance(old, list):  #base case: not a list, remember & return it
        copies[oid] = old
        return copies[oid]
    
    #recursive case
    copies[oid] = []
    for e in old:
        copies[oid].append(deep_copy(e, copies))
    return copies[oid]


# In[28]:

y = deep_copy(x)
y[0] = 'zero'
print("x:", x)
print("y:", y)
print("y[1][1][1][1][1][1][1][1][1][1][2]:", y[1][1][1][1][1][1][1][1][1][1][2])

