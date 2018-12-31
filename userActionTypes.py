# User Action Type
class UserActionType:

    def __init__(self, user):
        self.user = user

        # User Action Types
        self.UserActionTypes = {
            "help": self.user.help,
            "connect": self.user.user_login,
            "login": self.user.user_login,
            "register": self.user.user_register,
            "signup": self.user.user_register,
            "time": self.user.time,
            "name": self.user.get_pc_name,
            "exit": self.user.exit,
            "screenshot": self.user.send_screen_shot,
            "run program": self.user.run_program,
            "get folder": self.user.get_folder,
            "file content": self.user.get_file_content,
            "stop keep alive": self.user.stop_keep_alive,
            "stop heartbeat": self.user.stop_keep_alive,
        }

        self.UserActionTypesHelp = [
            ("help", "Get all commands"),
            ("connect", "Login the user (you can use login request too)\n\t"
                        "format: connect: <user-name> <password>\n\t" +
             "Notes: user must to be register"),
            ("login", "Login the user (you can use connect request too)\n\t"
                      "format: login: <user-name> <password>\n\t"
                      "Notes: user must to be register"),
            ("register", "Register the user (you can use signup request too)\n\t"
                         "format: register: <user-name> <password>"),
            ("signup", "Signup the user (you can use register request too)\n\t"
                       "format: signup: <user-name> <password>"
                       "Notes: user must to be logged in"),
            ("time", "Get current time\n\t"
                     "format: time"),
            ("name", "Name of the computer\n\t"
                     "format: name"),
            ("exit", "Exit from connection\n\t"
                     "format: exit"),
            ("screenshot", "Take screenshot of the server screen\n\t"
                           "format: screenshot"),
            ("run program", ""),
            ("get folder", ""),
            ("file content", ""),
            ("stop keep alive", ""),
            ("stop heartbeat", ""),
        ]

    # Get Function based on action type, if no command then None
    def get_action_fn(self, command):
        # type: (str) -> {'fn': function, 'error': str}
        if command not in self.UserActionTypes:
            err_msg = 'command {} not founded'.format(command)
            print err_msg
            return {
                'error': err_msg
            }
        return {
            'fn': self.UserActionTypes[command]
        }
