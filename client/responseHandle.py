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

        reqType = self.get_request_type(request)

        if reqType is None:
            err_mes = 'Error occurred at get request type'
            print err_mes
            return {
                'error': err_mes,
                'close-client': False
            }

        if 'error' in reqType:
            err_mes = reqType['error'] if reqType['error'] is None else 'Error ar get request type'
            print err_mes, reqType
            return {
                'error': err_mes,
                'close-client': False
            }
        from userActionType import UserActionType

        # Get action Handler Function
        user_action = UserActionType(self).get_action_fn(reqType['type'])

        # Not Founded
        if 'fn' not in user_action:
            return {
            }

        res = user_action['fn'](content)

        if isinstance(res, basestring):
            res = {
                'message': res,
                'close-client': False
            }

        if 'close-client' not in res:
            res['close-client'] = False

        if 'message' not in res:
            res['message'] = 'No message provided'

        res['type'] = reqType['type']

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

    def stop_heartbeat(self, content):
        return {
            'stop-heartbeat': True
        }

    def screenshot_handler(self, response):
        global server_name

        fname = 'screenshot-{}.png'.format(time.time())
        save_path = get_relative_path(fname)
        if save_path is None:
            return {
                'error': 'message path can\'t be null'
            }

        if 'error' in save_path:
            return save_path

        if 'error' in response:
            return {
                'error': response
            }

        try:
            fp = open(fname, 'wb')
            while True:
                if response.startswith('Error:'):
                    fp.close()
                    return {
                        'error': response.replace('Error:', '', 1)
                    }
                if not response or response == 'Image Data':
                    break
                fp.write(response)
                response = self.recv(1024)
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
            err_msg = 'Can\'t save image due to directory reading writing problems', have_dir
            print err_msg
            return {
                'error': err_msg
            }

        new_save_path = get_relative_path('{}\\{}'.format(server_name, fname))
        if 'error' in new_save_path:
            return new_save_path

        try:
            os.rename(save_path['path'], new_save_path['path'])
        except Exception, err:
            err_msg = 'Error at moving file from temp to wanted path ({} -> {})'.format(save_path, new_save_path)
            print err_msg
            return {
                'error': err_msg
            }

        return {
            'message': 'Success'
        }
