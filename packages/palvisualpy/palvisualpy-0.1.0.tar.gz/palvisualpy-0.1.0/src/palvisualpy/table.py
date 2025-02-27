from rich.table import Table


def dict_to_rich_table(data, table=None, parent=None):
    if table is None:
        table = Table(f"{parent}" if parent else "Dict View By Rich Table")

    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)
    else:
        raise ValueError("Unsupported data type. Must be a dict or list.")

    for key, value in items:
        if isinstance(value, dict) or isinstance(value, list):
            subtable = Table(f'{key}')
            dict_to_rich_table(value, subtable, key)
            table.add_section(subtable)
        else:
            table.add_row(f'{key}', f'{value}')

    return table
