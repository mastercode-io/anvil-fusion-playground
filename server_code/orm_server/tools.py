import anvil.server
from .persistance import get_table


@anvil.server.callable
def check_table(class_name=None):
    try:
        table = get_table(class_name=class_name)
        return table.list_columns()
    except Exception as e:
        return None
