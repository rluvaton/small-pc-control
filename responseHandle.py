# Imports
import os
import time
from PIL import ImageGrab

from utils import *

# Server name
server_name = None


# Response Handler
class ResponseHandler:

    def __init__(self, recv, send):
        self.send = send
        self.recv = recv

        # Block all request until user will connect (register / login)
        self.user_connected = False
        pass

    def get_request_type(self, content):
        # type: (str) -> {'type': str, 'body': str, 'error': str}
        """
        Get Request type
        :param content: Content of the request
        :return: The type and the body of the request
        """
        if content is None:
            err_mes = 'content sent can\'t be null'
            print err_mes, content
            return {
                'error': err_mes
            }

        # Split to action type and parameters
        two_parts = content.split(':', 1)

        if len(two_parts) == 0:
            err_mes = 'Content Parsing Error'
            print err_mes, two_parts
            return {
                'error': err_mes
            }

        # Remove the leading trailing spaces
        two_parts[0] = str(two_parts[0]).strip().lower()

        if len(two_parts) < 2:
            two_parts.append('')

        two_parts[1] = two_parts[1].strip()
        return {
            'type': two_parts[0],
            'body': two_parts[1]
        }

    def handle_requests(self, request, content):
        # type: (str, str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Handle Requests
        :param request: request
        :param content: content of the message
        :return: Return the result, message in case of success, if to close the client and error message if there is one
        """

        res = self.get_request_type(request)

        if res is None:
            err_mes = 'Error occurred at get request type'
            print err_mes
            return {
                'error': err_mes,
                'close-client': False
            }

        if 'error' in res:
            err_mes = res['error'] if res['error'] is None else 'Error ar get request type'
            print err_mes, res
            return {
                'error': err_mes,
                'close-client': False
            }
        from userActionType import get_action_fn

        # Get action Handler Function
        user_action = get_action_fn(res['type'])

        # Not Founded
        if 'fn' not in user_action:
            return {
            }

        res = user_action['fn'](content)

        if isinstance(res, basestring) or len(res) == 1:
            res = {
                'message': res,
                'close-client': False
            }

        if res['close-client'] is None:
            res['close-client'] = False

        if res['message'] is None:
            res['message'] = 'No message provided'

        return res

    def server_name_handler(self, content):
        global server_name
        server_name = content,
        return {}

    def exit_handler(self, content):
        print ' -- Exiting -- '
        return {
            'close-client': True
        }

    def screenshot_handler(self, response):
        global server_name

        fname = 'screenshot-{}.png'.format(time.time())
        save_path = get_relative_path(fname)
        if save_path is None:
            return {
                'error': 'message path can\'t be null'
            }

        try:
            fp = open(fname,'wb')
            while True:
                if not response or response == 'Image Data':
                    print '-- end image --'
                    break
                fp.write(response)
                response = self.recv(512)
            fp.close()
        except Exception, err:
            err_msg = 'Error at saving image accord'
            print err_msg, err
            return {
                'error': err_msg
            }

        if server_name is None:
            self.send('name')
            server_name = self.recv(None)

        have_dir = create_dir_if_not_exists(server_name, True)
        if 'error' in have_dir:
            err_msg = 'Can\'t save image due to directory reading writing problems'
            print err_msg
            return {
                'error': err_msg
            }

        new_save_path = get_relative_path('{}\\{}'.format(server_name, fname))
        if new_save_path[1]:
            return {
                'path': new_save_path
            }

        try:
            os.rename(save_path[0], new_save_path[0])
        except Exception, err:
            err_msg = 'Error at moving file from temp to wanted path ({} -> {})'.format(save_path, new_save_path)
            print err_msg
            return {
                'error': err_msg
            }

        return {
            'message': 'Success'
        }


class ResponseHandler1:
    def __init__(self):
        pass


    # Handle Requests
    # Return Tuple that (<messages>, <have-error>, <close-client>)
    def handle_requests(self, request, response, get_more_data, get_server_name):
        res = ResponseHandler.get_request_type(request)

        if res is None:
            err_mes = 'Error Accord at get request type'
            print err_mes
            return err_mes, False

        if res[0] is None:
            err_mes = res[1] if res[1] is None else 'Error ar get request type'
            print err_mes, res
            return err_mes, False

        res = res[0]

        from userActionType import get_action_fn

        # Get action Handler Function
        action_fn = get_action_fn(res[0])

        # Not Founded
        if 'error' in action_fn:
            return {
                'error': action_fn['error']
            }

        fn_res = action_fn['fn'](request, response, get_more_data, get_server_name)

        if isinstance(fn_res, basestring):
            fn_res = fn_res, False

        return fn_res[0], fn_res[1]

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

