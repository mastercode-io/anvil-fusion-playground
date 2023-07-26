import json

import anvil.server
import anvil.users
from anvil.tables import query as q0
import uuid
import anvil.tz
from datetime import datetime

from . import app as pm
from .orm_client.model import *
from .orm_client.lib import *
from .orm_client import enumerations as enums
from .Forms import *
from .Views import *

import AnvilFusion
from AnvilFusion

my_dotdict = utils.DotDict()
print(my_dotdict)

# Add new tenant  
def add_tenant(name):
    new_tenant = Tenant(name=name)
    new_tenant.save(audit=False)
    return new_tenant


# nt = add_tenant('Playwright')
# anvil.server.call('signup_user', email='playwright@mastercode.io', password='6K5bJCNQypjTVQwk', tenant_name='Playwright')

# anvil.server.call('signup_user', email='adam@theplumegroup.com', password='\YnR.1ti)T!eJ77',
#                   tenant_name='LV Criminal Defense')

stime = datetime.now()
pm.session.init_user_session()
etime = datetime.now()
print('Init App', (etime - stime))


view_config = {
    'model': 'Payment',
    'columns': [
        {'name': 'bank_account.account_type.name', 'label': 'Bank Account'},
    ],
}
# data = {'name': 'TaskView', 'config': json.dumps(view_config)}
# appGridViews(**data).save()

