import os


# Get string size
def get_string_size(s):
    # type: (str) -> int
    """
    Get String size
    :param s: string to get his size
    :return: Returns the size in bytes of the string
    :type: (str) -> int
    """
    return len(s.encode('utf-8'))


# Request for valid response
def request_valid_response(request, yes = 'y', no = 'n', case_matters = False):
    # type: (str, str, str, bool) -> bool
    res = None
    request += ' ({}/{})'.format(yes, no)
    while res != no and res != yes:
        res = raw_input(request)
        res = res if case_matters else res.strip().lower()
    return res == yes


# Create Directory if not exist
def get_relative_path(dir_path):
    try:
        dir_name = os.path.dirname(__file__)
        return {
            'path': os.path.join(dir_name, '{}'.format(dir_path))
        }
    except Exception, err:
        err_msg = 'Error at parse path: ' + dir_path
        print err_msg, err
        return {
            'error': err_msg
        }


# Create Directory if not exist
def create_dir_if_not_exists(dir_path, relative = False):
    if relative:
        dir_path = get_relative_path(dir_path)
        if 'error' in dir_path:
            return dir_path
        dir_path = dir_path['path']

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return {'message': 'Created directories successfully'}
    except Exception, err:
        err_msg = 'Error at create directories: '
        print err_msg, err
        return {
            'error': err_msg
        }


def exit_program():
    os._exit(0)
