import anvil.server
from ..app_client import models


@anvil.server.callable
def add_dependency():
    anvil.server.session['dependency']['data_models'] = model.__name__
