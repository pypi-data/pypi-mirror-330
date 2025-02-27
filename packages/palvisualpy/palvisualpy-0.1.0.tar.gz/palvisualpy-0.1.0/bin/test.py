from rich.table import Table
from rich.console import Console
import flatdict

console = Console()


def dict_to_rich_table(data: dict, table: Table=None):
    if table is None:
        table = Table('Dict View By Rich Table', show_lines=True)

    flatted_dict = flatdict.FlatDict(data)
    for k, v in flatted_dict.items():
        if isinstance(v, dict):
            sub_table = Table(show_lines=True)
            table.add_row(k, dict_to_rich_table(v, sub_table))
        elif isinstance(v, list):
            for e in v:
                sub_table = Table(show_lines=True)
                table.add_row(k, dict_to_rich_table(e, sub_table))
        else:
            table.add_row(k, f'{v}')

    return table

