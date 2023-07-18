# Init and maintain user session variables
import anvil.users
import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q
import uuid
from ..orm_client.model import *


@anvil.server.callable
def create_tenant(tenant_name=None):
    if tenant_name is not None:
        tenant = Tenant('name', tenant_name).save(audit=False)
        return tenant


@anvil.server.callable
def signup_user(email=None, password=None, tenant_name=None):
    if not email or not password or not tenant_name:
        return None
    tenant = Tenant.get_by('name', tenant_name)
    user = anvil.users.signup_with_email(email, password)
    user['uid'] = str(uuid.uuid4())
    user['tenant_uid'] = tenant.uid


@anvil.server.callable
def init_user_session():
    print('session a', anvil.server.session)
    user_row = anvil.users.get_user()
    if user_row is None:
        return None

    anvil.server.session['user_uid'] = user_row['uid']
    anvil.server.session['tenant_uid'] = user_row['tenant_uid']
    anvil.server.session['timezone'] = user_row['timezone']
    anvil.server.session['email'] = user_row['email']
    staff = Staff.get_by('work_email', user_row['email'])
    if staff is not None:
        anvil.server.session['staff'] = staff
    else:
        anvil.server.session['staff'] = None

    pm_logged_user = {
        'tenant_uid': anvil.server.session['tenant_uid'],
        'email': anvil.server.session['email'],
        'staff': anvil.server.session['staff'],
        'timezone': anvil.server.session['timezone']
    }
    print('session b', anvil.server.session)

    return pm_logged_user


@anvil.server.callable
def check_session(tag):
    print(f'seesion check {tag}', anvil.server.session)


@anvil.server.callable
def fetch_rows(table_name, search_definition):
    search_query = search_definition.pop("search_query", None)
    if search_query is not None:
        print('with query', search_query, search_definition)
        rows = getattr(app_tables, table_name).search(search_query, **search_definition)
    else:
        print(search_definition)
        rows = getattr(app_tables, table_name).search(**search_definition)
    return rows


@anvil.server.callable
def fetch_test(query):
    rows = app_tables.payment.search(query)
    return rows
