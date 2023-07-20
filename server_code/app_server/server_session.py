import anvil.server
from ..app_client import model
from AnvilFusion.app_server.server_dependencies import ServerDependencies
from AnvilFusion.orm_server import persistance


@anvil.server.callable
def add_server_dependencies():
    ServerDependencies.add_dependency('model', model)
    print('app server', persistance.APP_DATA_MODEL)
    persistance.APP_DATA_MODEL = model
    print('app_server', persistance.APP_DATA_MODEL)


@anvil.server.callable
def get_server_dependencies():
    ServerDependencies.get_dependencies()
    print('app_server', persistance.APP_DATA_MODEL)
  