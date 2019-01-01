# User Action Type
class UserActionType:

    def __init__(self, user):
        self.user = user

        # User Action Types
        self.UserActionTypes = {
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
