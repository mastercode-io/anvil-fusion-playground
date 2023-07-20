import anvil.server
from ..app_client import model
from AnvilFusion.app_server.server_dependencies import ServerDependencies


@anvil.server.callable
def add_server_dependencies():
    ServerDependencies.add_dependency('model', model)


@anvil.server.callable
def get_server_dependencies():
    ServerDependencies.get_dependencies()