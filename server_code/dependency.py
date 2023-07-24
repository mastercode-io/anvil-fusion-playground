import anvil.server
from ..app_client import model


@anvil.server.callable
def add_server_dependencies():
    anvil.server.session['dependency']['data_models'] = model.__name__
