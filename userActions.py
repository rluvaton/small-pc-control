# Get Computer Name, Folder Content and program starting
import os

# Get Time
import time

# Take Screen Shot
from PIL import ImageGrab


# ########################################################
#                       Request Format
# ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# Request content must be in the following format
# [request name]: [variable1] [variable2] ... [variableN]
#
# Login Example
# content will equal
# Connect: myUserName 123123
# ########################################################


# User Actions
class UserActions:

    def __init__(self, send_fn):
        self.send_fn = send_fn

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

    def handle_requests(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Handle Requests
        :param content: content of the message
        :return: Return the result, message in case of success, if to close the client and error message if there is one
        """

        res = self.get_request_type(content)

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

        from userActionTypes import UserActionType

        # Get action Handler Function
        user_action = UserActionType(self).get_action_fn(res['type'])

        # Not Founded
        if 'error' in user_action:
            return {
                'error': 'Unknown request: ' + res['type'],
                'close-client': False
            }

        res = user_action['fn'](res['body'])

        if isinstance(res, basestring):
            res = {
                'message': res,
                'close-client': False
            }

        if 'close-client' not in res:
            res['close-client'] = False

        if 'error' not in res and 'message' not in res:
            res['message'] = 'No message provided'

        return res

    def stop_keep_alive(self, content):
        # type: (str) -> {'stop-heartbeat': bool, 'message': str, 'error': str, 'close-client': bool}
        """
        Stop Keep Alive
        :param content:
        :return:
        """
        return {
            'message': 'Stopping heartbeat',
            'stop-heartbeat': True
        }

    def get_file_content(self, content):
        """
        Get File Content
        :param content: file path
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        content = 'c:\file.txt'
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            err_mes = 'Login / Register Before doing any action'
            return {
                'error': err_mes
            }

        # Check if path exists
        if not os.path.exists(content):
            err_mes = '{} not exists'.format(content)
            print err_mes
            return {
                'error': err_mes
            }

        # Check if path is a folder
        if os.path.isdir(content):
            err_mes = '{} isn\'t a file'.format(content)
            return {
                'error': err_mes
            }

        # Start reading & sending the image
        fp = open(content, 'rb')
        while True:
            d_block = fp.read(512)
            if not d_block:
                break
            self.send_fn(d_block)
            print d_block
        fp.close()

    def get_folder(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Open Folder
        :param content: variables in the request (folder path here
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        content = 'c:\folderName'
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            err_mes = 'Login / Register Before doing any action'
            return {
                'error': err_mes,
            }

        # Check if path exists
        if not os.path.exists(content):
            err_mes = '{} not exists'.format(content)
            print err_mes
            return {
                'error': err_mes,
            }

        # Check if path is directory
        if not os.path.isdir(content):
            err_mes = '{} isn\'t a folder'.format(content)
            print err_mes
            return {
                'error': err_mes,
            }

        try:
            folder_content = os.listdir(content)
            return '\n'.join(folder_content)
        except Exception, err:
            err_mes = 'Error getting folder ({}) content, try again later'.format(content)
            print err_mes, err
            return {
                'error': err_mes,
            }

    def run_program(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Run Program
        :param content: variables in the request (program name here)
        :return: <message>, <have-error>, <close-client>
        :notes: If no program return: 'No Program'
        :example: Usage Example
        content = 'Chrome'
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            err_mes = 'Login / Register Before doing any action'
            return {
                'error': err_mes,
            }

        if os.path.isfile(content.replace('"', '')):
            try:
                os.system("\"{}\"".format(content))
            except Exception, err:
                err_mes = 'Error opening program ({}), try again later'.format(content)
                print err_mes, err
                return {
                    'error': err_mes,
                }

            return 'Program {} opened'.format(content)

        err_mes = 'Please provide a path to the program'
        print err_mes
        return {
            'error': err_mes,
        }

    def send_screen_shot(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Send Screen shot
        :param content: variables in the request (None in this request)
        :return: <message>, <have-error>, <close-client>
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            err_mes = 'Login / Register Before doing any action'
            return {
                'error': err_mes,
            }

        im = ImageGrab.grab()

        dirname = os.path.dirname(__file__)
        saving_path = os.path.join(dirname, './tempFiles/screenshot-{}.png'.format(time.time()))

        # Save Image
        im.save(saving_path)

        # Start reading & sending the image
        img_file = open(saving_path, 'rb')
        while True:
            d_block = img_file.read(1024)
            if not d_block:
                break
            self.send_fn(d_block)
        img_file.close()

        # Delete the file
        os.remove(saving_path)

        return {
            'message': 'Image Data'
        }

    def exit(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Exit connection
        :param content: variables in the request (None in this request)
        :return: <message>, <have-error>, <close-client>
        :notes: Returns the message Bye Bye! and pass close connection flag
        """
        return {
            'message': 'Bye Bye!',
            'close-client': True
        }

    def get_pc_name(self, content):
        """
        Get PC Name
        :param content: variables in the request (None in this request)
        :return: <message>, <have-error>, <close-client>
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            err_mess = 'Login / Register Before doing any action'
            return {
                'error': err_mess
            }

        try:
            return os.environ['COMPUTERNAME']
        except Exception, err:
            err_mess = 'Can\'t get computer name, please try again later'
            print err_mess, err
            return {
                'error': err_mess
            }

    def time(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        Get Time
        :param content: variables in the request (None in this request)
        :return: <message>, <have-error>, <close-client>
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            err_msg = 'Login / Register Before doing any action'
            return {
                'error': err_msg
            }

        return str(time.ctime())

    def user_login(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        User Login
        :param content: variables in the request (user name and password)
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        userName 123123
        :notes: If no user returning: 'Bad connection parameters'
        """
        if content is None or content.strip() is '':
            err_msg = 'Argument Exception'
            return {
                'error': err_msg
            }

        params = content.split(' ')

        if len(params) != 2:
            err_msg = 'Parameters count can\'t be different than 2 in user login'
            print err_msg
            return {
                'error': err_msg
            }

        from userManagement import singleton

        res = singleton.search_user_record(params[0], params[1])

        if 'error' not in res:
            self.user_connected = True

        return res

    def user_register(self, content):
        # type: (str) -> {'message': str, 'error': str, 'close-client': bool}
        """
        User Register
        :param content: variables in the request (None in this request)
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        userName 123123
        """
        if content is None or content.strip() is '':
            err_msg = 'Argument Exception'
            return {
                'error': err_msg
            }

        params = content.split(' ')

        if len(params) != 2:
            err_msg = 'Parameters count can\'t be different than 2 in user registration'
            print err_msg
            return {
                'error': err_msg
            }

        from userManagement import singleton
        res = singleton.add_user_record(params[0], params[1])

        if 'error' not in res:
            self.user_connected = True

        return res
