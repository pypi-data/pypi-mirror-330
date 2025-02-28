import os
import traceback
from datetime import date, datetime
from inspect import getmembers, ismethod


def print_comment(val, space: int = 0, end=''):
    space = space * ' '
    color = '\033[0;38;5;247m'
    print(space + color + val + color, end=end)


def print_property(val, space: int = 0, end=''):
    space = space * ' '
    color = '\033[m'
    print(space + color + val + color, end=end)


def print_const(val, space: int = 0, end=''):
    space = space * ' '
    color = '\033[1;038;5;208m'
    print(space + color + val + color, end=end)


def print_string(val: str, space=0, end='\n', wrap: bool = True):
    space = space * 1 * ' '
    quote = '\033[038;5;208m"' if wrap else ''
    val = '\033[0;38;5;113m' + val + '\033[m'
    print(space + quote + val + quote, end=end)


def print_key(val, space: int = 0, end='\n'):
    space = space * ' '
    val = '\033[1;38;5;38m' + str(val) + '\033[m'
    print(space + val, end=end)


def print_dd_info():
    frame = None
    for current_frame in reversed(traceback.extract_stack()):
        if "dd.py" not in current_frame.filename:
            frame = current_frame
            break
    if not frame:
        return
    filename = frame.filename
    lineno = frame.lineno
    print_comment(f' // {filename}:{str(lineno)}', 0, '\n')


def dump(val, space=0, indent: int = 0, end='', depth=0):
    depth = depth + 1
    if depth > 15:
        print_string("...", space, os.linesep)
        return
    match val:
        case int():
            print_key(val, space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case str():
            print_string(val, space, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case dict():
            print_dict(val, space, indent, depth=depth)
        case list():
            print_list(val, indent)
        case tuple():
            print_list(val, indent)
        case float():
            print_key(val, indent * 2, '')
            print_dd_info() if indent == 0 else print('', end=end)
        case None:
            print_const('None', space, end=end)
        case date():
            print_key(val.strftime("%Y-%m-%d"), indent * 2, end=end)
        case datetime():
            print_key(val.strftime("%Y-%m-%d %H:%M:%S"), indent * 2, end=end)
        case object():
            print_object(val, indent, depth=depth)


def print_object(val, indent: int = 0, depth: int = 0):
    class_name = type(val).__name__
    print_string(class_name, space=min(1, indent), end='', wrap=False)
    print_const('^', space=0, end='')
    print_const('{', space=1, end='')
    # print_comment('#' + hex(id(val)), space=0, end='\n')
    print_dd_info() if indent == 0 else print('', end='\n')
    for _name, member in val.__dict__.items():
        if not callable(member) and not ismethod(member):
            symbol = '+'
            if _name.startswith(f'_{class_name}'):
                symbol = '-'
                _name = _name.replace(f'_{class_name}', '')
            elif _name.startswith('_'):
                symbol = '#'
            print_const(symbol, indent * 2 + 2, end='')
            print_property(_name, 0, '')
            print_const(':', 0)
            dump(member, 1, indent=indent + 1, end='\n', depth=depth)

    print_const('}', space=indent * 2, end='\n')


def print_list(val: list | tuple, indent: int = 0):
    print_string(type(val).__name__ + ':' + str(len(val)), space=indent, end='', wrap=False)
    print_const('[', space=1, end='')
    print_dd_info() if indent == 0 else print('', end='\n')
    for item in range(len(val)):
        value = val[item]
        print_key(item, indent * 2 + 2, '')
        print_const('=>', 1)
        dump(value, 1, indent=indent + 1, end='\n')
    print_const(']', space=indent * 2, end='\n')


def print_dict(val: dict, space=0, indent: int = 0, depth: int = 0):
    print_string(type(val).__name__, space=min(1, indent), end='', wrap=False)
    print_const('{', space=1, end='')

    if indent == 0:
        print_dd_info()
    elif len(val) > 0:
        print('', end='\n')
    else:
        print('', end='')
    for key, value in val.items():
        print_string(key, indent * 2 + 2, end='')
        print_const(':', 0)
        dump(value, 1, indent=indent + 1, end='\n', depth=depth)
    print_const('}', space=indent * 2, end='\n')


def dd(*args):
    for arg in args:
        dump(arg)
    exit('')
