# Get Computer Name
# Get Folder Content
# Start Program
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

    # User Register
    # -------------
    # content is the variables in the request
    # there are 2 variables:
    # 1. user name
    # 2. password
    # ------------
    # Example
    # userName 123123
    @staticmethod
    def user_register(content, send = None):
        params = content.split(' ')

        if len(params) != 2:
            err_message = 'Parameters count can\'t be different than 2 in user registration'
            print err_message
            return err_message, True

        from userManagement import add_user_record
        return add_user_record(params[0], params[1])

    # User Login
    # If no user returning: 'Bad connection parameters'
    # -------------
    # content is the variables in the request
    # there are 2 variables:
    # 1. user name
    # 2. password
    # ------------
    # Example
    # userName 123123
    @staticmethod
    def user_login(content, send = None):
        params = content.split(' ')

        if len(params) != 2:
            err_message = 'Parameters count can\'t be different than 2 in user login'
            print err_message
            return err_message, True

        from userManagement import search_user_record
        return search_user_record(params[0], params[1])

    # Get Time
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def time(content, send = None):
        return str(time.ctime())

    # Get PC Name
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def get_pc_name(content, send = None):
        try:
            return os.environ['COMPUTERNAME']
        except Exception, err:
            err_mess = 'Can\'t get computer name, please try again later'
            print err_mess, err
            return err_mess, True

    # Exit connection
    # Returns the message and if to close connection
    # It will return: 'Bye Bye'
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def exit(content, send = None):
        return 'Bye Bye!', True

    # Send Screen shot
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def send_screen_shot(content, send):
        im = ImageGrab.grab()

        dirname = os.path.dirname(__file__)
        saving_path = os.path.join(dirname, './screenshot-{}.png'.format(time.time()))

        # Save Image
        im.save(saving_path)

        # Start sending the image
        img_file = open(saving_path,'rb')
        while True:
            strng = img_file.read(512)
            if not strng:
                break
            send(strng)
        img_file.close()

        return 'Image Data', False, False

    # Run Program
    # If no program return: 'No Program'
    # -------------
    # content is the variables in the request
    # 1 variable: Software name
    # ------------
    # Example
    # Chrome
    @staticmethod
    def run_program(content, send = None):
        try:
            os.system('start ' + content)
            return 'Program {} opened'.format(content)
        except Exception, err:
            err_mes = 'Error opening program ({}), try again later'.format(content)
            print err_mes, err
            return err_mes, True

    # Open Folder
    # If no folder return: 'No Folder'
    # -------------
    # content is the variables in the request
    # 1 variable: Absolute folder path
    # ------------
    # Example
    # c:\\folderName
    @staticmethod
    def get_folder(content, send = None):
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

    # Handle Requests
    # Return Tuple that (<messages>, <have-error>, <close-client>)
    @staticmethod
    def handle_requests(content, send):
        res = UserActions.get_request_type(content)

        if res is None:
            err_mes = 'Error Accord at get request type'
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

        if isinstance(res, basestring):
            res = res, False, False

        return res[0], res[1], res[2]

    # Get Request type
    # Return Tuple that (request-type, <error-message>
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
