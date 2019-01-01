# Explanation on all requests from the server
all_actions_type_help = [
    {
        "name": "connect",
        "description": "Connect the user",
        "format": "connect: <user-name> <password>",
        "example": "connect: myUserName 123123",
        "notes": "user must to be register",
        "alternative": "login"
    },
    {
        "name": "login",
        "description": "Login the user",
        "format": "login: <user-name> <password>",
        "example": "login: myUserName 123123",
        "notes": "user must to be register",
        "alternative": "connect"
    },
    {
        "name": "register",
        "description": "Register user",
        "format": "register: <user-name> <password>",
        "example": "register: myUserName 123123",
        "notes": None,
        "alternative": "signup"
    },
    {
        "name": "signup",
        "description": "Signup user",
        "format": "signup: <user-name> <password>",
        "example": "signup: myUserName 123123",
        "notes": None,
        "alternative": "register"
    },
    {
        "name": "time",
        "description": "Get current time",
        "format": "time",
        "example": "time",
        "notes": "user must be logged in",
        "alternative": None
    },
    {
        "name": "name",
        "description": "Get the name of the computer",
        "format": "name",
        "example": "name",
        "notes": "user must be logged in",
        "alternative": None
    },
    {
        "name": "exit",
        "description": "Exit from the connections",
        "format": "exit",
        "example": "exit",
        "notes": "It will close the program",
        "alternative": None
    },
    {
        "name": "screenshot",
        "description": "Take screenshot of the server screen and save it in the server name folder in the client",
        "format": "screenshot",
        "example": "screenshot",
        "notes": "user must be logged in",
        "alternative": None
    },
    {
        "name": "run program",
        "description": "Run program by path",
        "format": "run program: <program path>",
        "example": "run program: C:\\Program.exe",
        "notes": "user must be logged in",
        "alternative": None
    },
    {
        "name": "get folder",
        "description": "Get Folder content (files and folder) in the server",
        "format": "get folder: <path>",
        "example": "get folder: C:\\",
        "notes": "user must be logged in",
        "alternative": None
    },
    {
        "name": "file content",
        "description": "Get File content in the server",
        "format": "file content: <file url>",
        "example": "file content: C:\\demo.txt",
        "notes": "user must be logged in",
        "alternative": None
    },
    {
        "name": "stop keep alive",
        "description": "Stop keep alive messages",
        "format": "stop keep alive",
        "example": "stop keep alive",
        "notes": "The Server connection will expire after 10 seconds",
        "alternative": "stop heartbeat"
    },
    {
        "name": "stop heartbeat",
        "description": "Stop heartbeat messages",
        "format": "stop heartbeat",
        "example": "stop heartbeat",
        "notes": "The Server connection will expire after 10 seconds",
        "alternative": "stop keep alive"
    },
]


def get_complete_help_message():
    """
    Generate complete help message
    :return: complete help message on all the actions
    """
    print_str = '--------------------'

    for action in all_actions_type_help:
        print_str += '\n{}:\n\t' \
                     'Description: {}\n\t' \
                     'Format: {}\n\t' \
                     'Example: {}' \
            .format(action['name'],
                    action['description'],
                    action['format'],
                    action['example'])

        if action['notes'] is not None:
            print_str += '\n\tNotes: {}'.format(action['notes'])

        if action['alternative'] is not None:
            print_str += '\n\tAlternative: {}'.format(action['alternative'])

        print_str += '\n'

    return print_str


complete_help_message = get_complete_help_message()


# User Action Type
class UserActionType:

    def __init__(self, handler):
        self.handler = handler

        # User Action Types
        self.UserActionTypes = {
            "name": self.handler.server_name_handler,
            "exit": self.handler.exit_handler,
            "screenshot": self.handler.screenshot_handler,
            "stop keep alive": self.handler.stop_heartbeat,
            "stop heartbeat": self.handler.stop_heartbeat,
        }

    # Get Function based on action type, if no command then None
    def get_action_fn(self, command):
        if command not in self.UserActionTypes:
            return {}
        return {
            'fn': self.UserActionTypes[command]
        }
