import anvil.server
from ..app_client import model


@anvil.server.callable
def add_server_dependencies():
    anvil.server.session['app_data_model'] = model.__name__
