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
from AnvilFusion.orm_client import utils

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

# stime = datetime.datetime(2023, 2, 11, 0, 0, 0)
# etime = datetime.datetime(2023, 2, 12, 0, 0, 0)
# query = {
#   'start_time': q.all_of(q.greater_than_or_equal_to(stime), q.less_than(etime)),
# }
# events = Event.search(**query)
# print(len([*events]))

# sdate = datetime(2023, 3, 30, 0, 0, 0)
# edate = datetime(2023, 3, 31, 0, 0, 0)
# stime = datetime.now()
# search_query = q.fetch_only('due_date', 'priority', 'notes',
#                             case=q.fetch_only('case_name'),
#                             activity=q.fetch_only('name'),
#                             assigned_staff=q.fetch_only('first_name', 'last_name'), )
# # search_query = q.fetch_only('due_date', 'priority')
# task_list = anvil.server.call('fetch_rows', 'task',
#                               {
#                                   'search_query': search_query,
#                                   'due_date': q.all_of(q.greater_than_or_equal_to(sdate), q.less_than(edate)),
#                               }
#                               )
# task_list = anvil.server.call('fetch_tasks')
# etime = datetime.now()
# print(stime, etime, (etime - stime))
# print('Task List', len(task_list))
# stime = datetime.now()
# for task in task_list:
#     print(task['due_date'], task['activity']['name'], task['assigned_staff'][0]['last_name'])
# etime = datetime.now()
# print(stime, etime, (etime - stime))

# column config: {'name': 'case_name', 'label': 'Case Name', 'width': 200, 'css_class': ''}

# save view config to appGridViews
# view_config = {
#     'model': 'Task',
#     'columns': [
#         # {'name': 'col_name', 'label': 'col_label', 'type': 'button'},
#         {'name': 'case.case_name', 'label': 'Case'},
#         {'name': 'activity.name', 'label': 'Activity'},
#         {'name': 'due_date', 'label': 'Due Date'},
#         {'name': 'priority', 'label': 'Priority'},
#         {'name': 'assigned_staff.full_name', 'label': 'Assigned Staff'},
#         {'name': 'notes', 'label': 'Notes'},
#     ],
# }

view_config = {
    'model': 'Payment',
    'columns': [
        {'name': 'bank_account.account_type.name', 'label': 'Bank Account'},
    ],
}
# data = {'name': 'TaskView', 'config': json.dumps(view_config)}
# appGridViews(**data).save()

# view_obj = appGridViews.get_by('name', 'TaskView')
# print(view_obj['config'])
# self.view_config = json.loads(view_obj['config'].replace("'", "\""))
# sdate = datetime(2023, 3, 30, 0, 0, 0)
# edate = datetime(2023, 3, 31, 0, 0, 0)

# search = {'incident_date': q.all_of(q.greater_than_or_equal_to(datetime(2022, 1, 31, 0, 0, 0)),
#                                     q.less_than(datetime(2022, 12, 31, 0, 0, 0)))}

# qq = q.fetch_only('uid', bank_account=q.fetch_only('uid', account_type=q.fetch_only('uid', 'name')))
# print(dir(qq))
# print(qq.spec)
# {'uid': True, 'bank_account': {'uid': True, 'account_type': {'uid': True, 'name': True}}}
# {'uid': True, 'bank_account': {'uid': True, 'account_type': {'uid': True, 'name': True}}}
# rows = anvil.server.call('fetch_test', qq)
# rows = Payment.get_grid_view(view_config)
# print(len(rows), rows)
# for row in rows:
#     print(row)


def get_model_attribute(class_name, attr_name):
    cls = getattr(sys.modules[__name__], class_name)
    # print(class_name, attr_name, cls)
    attr = None
    if attr_name in cls._attributes:
        attr = cls._attributes[attr_name]
    elif attr_name in cls._computes:
        attr = cls._computes[attr_name]
    elif '.' in attr_name:
        attr_name = attr_name.split('.')
        if attr_name[0] in cls._attributes:
            attr = cls._attributes[attr_name[0]]
        elif attr_name[0] in cls._relationships:
            attr = get_model_attribute(cls._relationships[attr_name[0]].class_name, '.'.join(attr_name[1:]))
    return attr


# for col in view_config['columns']:
#     col_attr = get_model_attribute(view_config['model'], col['name'])
#     print(col_attr, col_attr.field_type.GridType)

# module_name = getattr(sys.modules[__name__], view_config['model']).__module__
# stime = datetime.now()
# cols = [col['name'] for col in view_config['columns']]
# # if 'uid' not in cols:
# #     cols.insert(0, 'uid')
# task_list = anvil.server.call('fetch_view',
#                               view_config['model'],
#                               module_name,
#                               cols,
#                               [], {})
# etime = datetime.now()
# print('Fetch view', etime - stime)
# stime = datetime.now()
# for task in task_list:
#     due_date = task['due_date']
#     activity = task['activity']
#     notes = task['notes']
# etime = datetime.now()
# print('Access time', etime - stime)

# stime = datetime.now()
# task_list = get_grid_view(view_config)
# etime = datetime.now()
# print('Get view', etime - stime)


# view_config['query'] = query
# view_config['search'] = search
# appGridViews(name='Test', config=view_config).save()

# new_contact = Contact(first_name='Adam', last_name='Plumer')
# print(new_contact, new_contact.first_name, new_contact.last_name)
# print(new_contact.full_name)
#
# tasks = anvil.server.call('fetch_tasks')
# print(tasks)
# print(tasks[0], tasks[0]['due_date'], tasks[0]['priority'])
# iter(tasks)
# iter(tasks[0])
# model_name = 'Contact'
# if hasattr(sys.modules[__name__], model_name):
#     model_class = getattr(sys.modules[__name__], model_name)
# else:
#     raise NameError('Model class not found')
# print(model_class)
# print(isinstance(Contact._attributes['first_name'], property))
# print(isinstance(Contact._properties['full_name'], Attribute))
