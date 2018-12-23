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

    def __init__(self):
        pass

    @staticmethod
    def user_register(content, send = None):
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
        return res[0], not res[1], False

    @staticmethod
    def user_login(content, send = None):
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
        return res[0], not res[1], False

    @staticmethod
    def time(content, send = None):
        """
        Get Time
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """
        return str(time.ctime())

    @staticmethod
    def get_pc_name(content, send = None):
        """
        Get PC Name
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """
        try:
            return os.environ['COMPUTERNAME']
        except Exception, err:
            err_mess = 'Can\'t get computer name, please try again later'
            print err_mess, err
            return err_mess, True, False

    @staticmethod
    def exit(content, send = None):
        """
        Exit connection
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :notes: Returns the message Bye Bye! and pass close connection flag
        """
        return 'Bye Bye!', False, True

    @staticmethod
    def send_screen_shot(content, send):
        """
        Send Screen shot
        :param content: variables in the request (None in this request)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """
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
            send(d_block)
        img_file.close()

        # Delete the file
        os.remove(saving_path)

        return 'Image Data', False, False

    @staticmethod
    def run_program(content, send = None):
        """
        Run Program
        :param content: variables in the request (program name here)
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :notes: If no program return: 'No Program'
        :example: Usage Example
        content = 'Chrome'
        """
        try:
            os.system('start ' + content)
            return 'Program {} opened'.format(content)
        except Exception, err:
            err_mes = 'Error opening program ({}), try again later'.format(content)
            print err_mes, err
            return err_mes, True

    @staticmethod
    def get_folder(content, send = None):
        """
        Open Folder
        :param content: variables in the request (folder path here
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        :example: Usage Example
        content = 'c:\folderName'
        """
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

    @staticmethod
    def handle_requests(content, send):
        """
        Handle Requests
        :param content: content of the message
        :param send: send to client function
        :return: <message>, <have-error>, <close-client>
        """

        res = UserActions.get_request_type(content)

        if res is None:
            err_mes = 'Error occurred at get request type'
            print err_mes
            return err_mes, True, False

        if res[0] is None:
            err_mes = res[1] if res[1] is None else 'Error ar get request type'
            print err_mes, res
            return err_mes, True, False

        res = res[0]

        from userActionTypes import get_action_fn

        # Get action Handler Function
        fn = get_action_fn(res[0])

        # Not Founded
        if fn is None:
            return 'Unknown request: ' + res[0], True, False

        res = fn(res[1], send)

        if isinstance(res, basestring) or len(res) == 1:
            res = res, False, False

        return res[0], \
               (res[1] if res[1] is not None else False), \
               (res[2] if res[2] is not None else False)

    @staticmethod
    def get_request_type(content):
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
