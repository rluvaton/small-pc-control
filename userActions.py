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
        """
        Get Request type
        :param content: Content of the request
        :return: <request-type>, <error-message>
        """
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

    def handle_requests(self, content):
        """
        Handle Requests
        :param content: content of the message
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """

        res = self.get_request_type(content)

        if res is None:
            err_mes = 'Error occurred at get request type'
            print err_mes
            return err_mes, True, False

        if res[0] is None:
            err_mes = res[1] if res[1] is None else 'Error ar get request type'
            print err_mes, res
            return err_mes, True, False

        res = res[0]

        from userActionTypes import UserActionType

        # Get action Handler Function
        fn = UserActionType(self).get_action_fn(res[0])

        # Not Founded
        if fn is None:
            return 'Unknown request: ' + res[0], True, False

        res = fn(res[1])

        if isinstance(res, basestring) or len(res) == 1:
            res = res, False, False

        return res[0], \
               (res[1] if res[1] is not None else False), \
               (res[2] if res[2] is not None else False)

    def get_folder(self, content):
        """
        Open Folder
        :param content: variables in the request (folder path here
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        content = 'c:\folderName'
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            return 'Login / Register Before doing any action', True, False

        # Check if path exists
        if not os.path.exists(content):
            err_mes = '{} not exists'.format(content)
            print err_mes
            return err_mes, True

        # Check if path is directory
        if not os.path.isdir(content):
            err_mes = '{} isn\'t a folder'.format(content)
            print err_mes
            return err_mes, True

        try:
            folder_content = os.listdir(content)
            return '\n'.join(folder_content)
        except Exception, err:
            err_mes = 'Error getting folder ({}) content, try again later'.format(content)
            print err_mes, err
            return err_mes, True

    def run_program(self, content):
        """
        Run Program
        :param content: variables in the request (program name here)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :notes: If no program return: 'No Program'
        :example: Usage Example
        content = 'Chrome'
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            return 'Login / Register Before doing any action', True, False

        try:
            os.system('start ' + content)
            return 'Program {} opened'.format(content)
        except Exception, err:
            err_mes = 'Error opening program ({}), try again later'.format(content)
            print err_mes, err
            return err_mes, True

    def send_screen_shot(self, content):
        """
        Send Screen shot
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            return 'Login / Register Before doing any action', True, False

        im = ImageGrab.grab()

        dirname = os.path.dirname(__file__)
        saving_path = os.path.join(dirname, './tempFiles/screenshot-{}.png'.format(time.time()))

        # Save Image
        im.save(saving_path)

        # Start reading & sending the image
        img_file = open(saving_path, 'rb')
        while True:
            d_block = img_file.read(512)
            if not d_block:
                break
            self.send_fn(d_block)
        img_file.close()

        # Delete the file
        os.remove(saving_path)

        return 'Image Data', False, False

    def exit(self, content):
        """
        Exit connection
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :notes: Returns the message Bye Bye! and pass close connection flag
        """
        return 'Bye Bye!', False, True

    def get_pc_name(self, content):
        """
        Get PC Name
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            return 'Login / Register Before doing any action', True, False

        try:
            return os.environ['COMPUTERNAME']
        except Exception, err:
            err_mess = 'Can\'t get computer name, please try again later'
            print err_mess, err
            return err_mess, True, False

    def time(self, content):
        """
        Get Time
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """

        # Check if user logged in before doing any actions
        if not self.user_connected:
            return 'Login / Register Before doing any action', True, False

        return str(time.ctime())

    def user_login(self, content):
        """
        User Login
        :param content: variables in the request (user name and password)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        userName 123123
        :notes: If no user returning: 'Bad connection parameters'
        """
        if content is None or content.strip() is '':
            return 'Argument Exception', True, False
        params = content.split(' ')

        if len(params) != 2:
            err_message = 'Parameters count can\'t be different than 2 in user login'
            print err_message
            return err_message, True, False

        from userManagement import search_user_record
        res = search_user_record(params[0], params[1])

        if res[1]:
            self.user_connected = True

        return res[0], not res[1], False

    def user_register(self, content):
        """
        User Register
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        userName 123123
        """
        if content is None or content.strip() is '':
            return 'Argument Exception', True, False

        params = content.split(' ')

        if len(params) != 2:
            err_message = 'Parameters count can\'t be different than 2 in user registration'
            print err_message
            return err_message, True, False

        from userManagement import add_user_record
        res = add_user_record(params[0], params[1])

        if res[1]:
            self.user_connected = True

        return res[0], not res[1], False
