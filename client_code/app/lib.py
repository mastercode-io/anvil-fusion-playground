import anvil.server
# Helper functions and tools
import sys
import re
import uuid
import datetime


# name string conversions
def print_exception(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    print(f"Exception occurred: {e}, in file: {file_name}, at line: {line_no}")


def camel_to_snake(string):
    """Convert a CamelCase string to snake_case"""
    return '_'.join(re.findall('[A-Z][^A-Z]*', string)).lower()


def camel_to_title(string):
    """Convert a CamelCase string to Title Case"""
    return ' '.join(re.findall('[A-Z][^A-Z]*', string))


def snake_to_camel(string):
    """Convert a snakle_case string to CamelCase"""
    first, *rest = string.split('_')
    return ''.join([first.title(), *map(str.title, rest)])


# compose ui element id
def get_form_field_id(form_id, field_name):
    return f"{form_id}_{field_name}"


def new_el_id():
    return str(uuid.uuid4()).replace('-', '')


# get python module attribute by string name
def str_to_attr(module_name, attr_name):
    attr = getattr(sys.modules[module_name], attr_name) if hasattr(sys.modules[module_name], attr_name) else None
    return attr


def datetime_py_to_js(dt):
    return anvil.js.window.Date(int(dt.strftime('%s')) * 1000)


def datetime_js_to_py(dt):
    return datetime.datetime.fromtimestamp(dt.getTime() / 1000)


def time_js_to_py(time):
    return datetime.datetime(1970, 1, 1, time.getHours(), time.getMinutes())
