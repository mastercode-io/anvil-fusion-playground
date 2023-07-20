import anvil.server
from ..app_client import model
from AnvilFusion.app_server import server_session


@anvil.server.callable
def add_app_dependencies():
    dependencies = {
        'app_model': model,
    }
    anvil.server.session['dependecies'] = dependencies
