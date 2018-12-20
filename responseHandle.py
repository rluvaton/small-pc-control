# Imports
import os
import time
from PIL import ImageGrab

# Server name
server_name = None


class ResponseHandler:
    def __init__(self):
        pass

    # Create Directory if not exist
    @staticmethod
    def get_relative_path(dir_path):
        try:
            dir_name = os.path.dirname(__file__)
            return os.path.join(dir_name, '{}'.format(dir_path)), False
        except Exception, err:
            err_msg = 'Error at parse path: ' + dir_path
            print err_msg, err
            return err_msg, True

    # Create Directory if not exist
    @staticmethod
    def create_dir_if_not_exists(dir_path, relative = False):
        if relative:
            dir_path = ResponseHandler.get_relative_path(dir_path)
            if dir_path[1] is True:
                return dir_path

        try:
            if not os.path.exists(dir_path[0]):
                os.makedirs(dir_path[0])
            return 'Created directories successfully', False
        except Exception, err:
            err_msg = 'Error at create directories: '
            print err_msg, err
            return err_msg, True

    @staticmethod
    def server_name_handler(request, response, get_more_data, get_server_name):
        global server_name
        server_name = response

    @staticmethod
    def exit_handler(request, response, get_more_data, get_server_name):
        print ' -- Exiting -- '

    @staticmethod
    def screenshot_handler(request, response, get_more_data, get_server_name):
        global server_name

        fname = 'screenshot-{}.png'.format(time.time())
        save_path = ResponseHandler.get_relative_path(fname)
        if save_path is None:
            return ""

        index = 0

        try:
            # fp = open(fname, 'wb')
            # while True:
            #     index += 1
            #     print 'index ', index
            #     if not response:
            #         print 'no more', response
            #         break
            #     if response == 'image sent!':
            #         break
            #     fp.write(response)
            #
            #     response = get_more_data('')

            fp = open(fname,'w')
            while True:
                if not response or response == 'Image Data':
                    break
                fp.write(response)
                response = get_more_data(512)
            fp.close()
        except Exception, err:
            err_msg = 'Error at saving image accord'
            print err_msg, err
            return err_msg, True

        if server_name is None:
            server_name = get_server_name('name')

        have_dir = ResponseHandler.create_dir_if_not_exists(server_name, True)
        if have_dir[1]:
            print 'Can\'t save image due to directory reading writing problems'
            return False

        new_save_path = ResponseHandler.get_relative_path('{}\\{}'.format(server_name, fname))
        if new_save_path[1]:
            return new_save_path

        try:
            os.rename(save_path[0], new_save_path[0])
        except Exception, err:
            err_msg = 'Error at moving file from temp to wanted path ({} -> {})'.format(save_path, new_save_path)
            print err_msg
            return err_msg

        return 'Success'

    # Handle Requests
    # Return Tuple that (<messages>, <have-error>, <close-client>)
    @staticmethod
    def handle_requests(request, response, get_more_data, get_server_name):
        res = ResponseHandler.get_request_type(request)

        if res is None:
            err_mes = 'Error Accord at get request type'
            print err_mes
            return err_mes, True, False

        if res[0] is None:
            err_mes = res[1] if res[1] is None else 'Error ar get request type'
            print err_mes, res
            return err_mes, True, False

        res = res[0]

        from userActionType import get_action_fn

        # Get action Handler Function
        fn = get_action_fn(res[0])

        # Not Founded
        if fn is None:
            return None, False, False

        res = fn(request, response, get_more_data, get_server_name)

        if isinstance(res, basestring):
            res = res, False, False

        return None

    # Get Request type
    # Return Tuple that (request-type, <error-message>)
    @staticmethod
    def get_request_type(content):
        if content is None:
            err_mes = 'content sent can\'t be null'
            print err_mes, content
            return None, err_mes

        # Split to action type and parameters
        two_parts = content.split(':', 1)

        if len(two_parts) == 0:
            err_mes = 'Content Parsing Error'
            print err_mes, two_parts
            return None, err_mes

        # Remove the leading trailing spaces
        two_parts[0] = str(two_parts[0]).strip().lower()

        if len(two_parts) < 2:
            two_parts.append('')

        two_parts[1] = two_parts[1].strip()
        return two_parts, None
