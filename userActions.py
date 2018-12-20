from .userActionTypes import UserActionTypes

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
    # request name in content will equal 'Register'
    # there are 2 variables:
    # 1. user name
    # 2. password
    # ------------
    # Example
    # Register: userName 123123
    @staticmethod
    def user_register(content):
        return False

    # User Login
    # If no user returning: 'Bad connection parameters'
    # -------------
    # request name in content will equal 'Connect'
    # there are 2 variables:
    # 1. user name
    # 2. password
    # ------------
    # Example
    # Connect: userName 123123
    @staticmethod
    def user_login(content):
        return False

    # Get Time
    # -------------
    # request name in content will equal 'Time'
    # No variables
    # ------------
    # Example
    # Time:
    @staticmethod
    def time(content):
        return False

    # Get PC Name
    # -------------
    # request name in content will equal 'Name'
    # No variables
    # ------------
    # Example
    # Name:
    @staticmethod
    def get_pc_name(content):
        return False

    # Exit connection
    # It will return: Bye Bye'
    # -------------
    # request name in content will equal 'Exit'
    # No variables
    # ------------
    # Example
    # Exit:
    @staticmethod
    def exit(content):
        return False

    # Send Screen shot
    # -------------
    # request name in content will equal 'ScreenShot'
    # No variables
    # ------------
    # Example
    # ScreenShot:
    @staticmethod
    def send_screen_shot(content):
        return False

    # Run Program
    # If no program return: 'No Program'
    # -------------
    # request name in content will equal 'ScreenShot'
    # 1 variable: Software name
    # ------------
    # Example
    # ScreenShot: Chrome
    @staticmethod
    def run_program(content):
        return False

    # Open Folder
    # If no folder return: 'No Folder'
    # -------------
    # request name in content will equal 'Open Folder'
    # 1 variable: Absolute folder path
    @staticmethod
    def open_folder(content):
        return False

    # Handle Requests
    @staticmethod
    def handle_requests(content):
        # TODO - Algorithm
        # TODO - Request: Register: userName123 123123
        # TODO - Split content based on ':'
        # TODO - First result is the action type
        # TODO - Get the action type function and pass the second result of the split
        # TODO - Example UserActionTypes(split[0])[1](split[1])
        # TODO - Return the value
        if content is None:
            return None

        # Split to action type and parameters
        twoParts = content.split(':')

        # Not Founded
        if UserActionTypes.__getattribute__(twoParts[0]):
            None



        return False
