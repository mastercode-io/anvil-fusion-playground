# User session
import anvil.server
from . import constants
from ..orm_client import enumerations as enums


# pm_logged_user = None

def init_user_session():
    anvil.server.call('check_session', 'a')
    constants.pm_logged_user = anvil.server.call('init_user_session')
    if constants.pm_logged_user is None:
        anvil.users.login_with_form()
        constants.pm_logged_user = anvil.server.call('init_user_session')
    print('USER: ', constants.pm_logged_user)
    anvil.server.call('check_session', 'b')

    enums.Models = enums.init_model_enumerations()
