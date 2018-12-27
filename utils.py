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