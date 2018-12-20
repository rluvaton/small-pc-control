
# ##########################
# Request content must be in the following format
# [request name]: [variable1] [variable2] ... [variableN]
#
# Login Example
# content will equal
# Connect: myUserName 123123
#
# ##########################

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
    def user_register(content):
        params = content.split(' ')
        print 'Register\n'
        print 'User Name: ' + params[0]
        print 'Password: ' + params[1]
        return 'Success'

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
    def user_login(content):
        return False

    # Get Time
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def time(content):
        return False

    # Get PC Name
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def get_pc_name(content):
        return False

    # Exit connection
    # It will return: Bye Bye'
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def exit(content):
        return False

    # Send Screen shot
    # -------------
    # content is the variables in the request
    # No variables
    # ------------
    # Example
    # ''
    @staticmethod
    def send_screen_shot(content):
        return False

    # Run Program
    # If no program return: 'No Program'
    # -------------
    # content is the variables in the request
    # 1 variable: Software name
    # ------------
    # Example
    # Chrome
    @staticmethod
    def run_program(content):
        return False

    # Open Folder
    # If no folder return: 'No Folder'
    # -------------
    # content is the variables in the request
    # 1 variable: Absolute folder path
    # ------------
    # Example
    # c:\\folderName
    @staticmethod
    def open_folder(content):
        return False

    # Handle Requests
    # Return the Response
    @staticmethod
    def handle_requests(content):
        if content is None:
            return None

        # Split to action type and parameters
        two_parts = content.split(':')

        two_parts[0] = str(two_parts[0]).strip()
        two_parts[1] = str(two_parts[1]).strip()

        from userActionTypes import get_action_fn

        fn = get_action_fn(two_parts[0])

        # Not Founded
        if fn is None:
            return 'Unknown request: ' + two_parts[0]

        return fn(two_parts[1])
