__version__ = "0.1.0"


from rich.tree import Tree


def dict_to_rich_tree(data, tree=None, parent=None):
    if tree is None:
        tree = Tree(f"{parent}" if parent else "Dict View By Rich Tree")

    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)
    else:
        raise ValueError("Unsupported data type. Must be a dict or list.")

    for key, value in items:
        if isinstance(value, dict) or isinstance(value, list):
            subtree = Tree(f"{key}")
            dict_to_rich_tree(value, subtree, key)
            tree.add(subtree)
        else:
            tree.add(f"{key}: {value}")

    return tree
