# Compute the depth of a list of lists
depth = lambda list_: isinstance(list_, list) and max(map(depth, list_)) + 1

# Flatten a list of lists
def flatten(list_):
    flattened = list_
    while isinstance(flattened[0], list):
        flattened = [item for sublist in flattened for item in sublist]
    return flattened

# Sort a list of strings by the length of the string
def sortByLength(list_):
    listLength = map(len, list_)
    return [item for (len_, item) in sorted(zip(listLength, list))]

# Walk a nested list, return the path to each node and its value
def _walk(obj, path=(), memo=None):
    if memo is None:
        memo = set()
    iterator = None
    if isinstance(obj, list):
        iterator = enumerate
    if iterator:
        if id(obj) not in memo:
            memo.add(id(obj))
            for path_component, value in iterator(obj):
                for result in _walk(value, path + (path_component,), memo):
                    yield result
            memo.remove(id(obj))
    else:
        yield path, obj

# Modify strings in a nested list
def _modifyAST(ast, prefix="dictDat['", suffix="']"):
    word = re.compile('\w+')
    for path, value in _walk(ast):
        if isinstance(value, str):
            if word.match(value):
                parent = ast
                for step in path[:-1]:
                    parent = parent[step]
                parent[path[-1]] = prefix + value + suffix
