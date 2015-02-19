# Compute the depth of a list of lists
depth = lambda list_: isinstance(list_, list) and max(map(depth, list_)) + 1

# Flatten a list of lists
def flatten(list_):
    flattened = list_
    while isinstance(flattened[0], list):
        flattened = [item for sublist in flattened for item in sublist]
    return flattened

# Flatten a list of lists to a defined depth
def flattenToDepth(list_, depth):
    flattened = list_
    while depth > 1:
        flattened = [item for sublist in flattened for item in sublist]
        depth -= 1
    return flattened

# Sort a list of strings by the length of the string
def sortByLength(list_):
    listLength = map(len, list_)
    return [item for (len_, item) in sorted(zip(listLength, list))]
