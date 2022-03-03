def flatten(list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
        return list_of_lists[:1] + flatten(list_of_lists[1:])

def clean_regex(node):
    start = node.get_regex()
    result = start.replace("\s", " ")
    return result.translate({ord(c): None for c in '()|*+'}).strip()
