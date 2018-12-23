# User Action Type
class UserActionType:

    def __init__(self, user):
        self.user = user

        # User Action Types
        self.UserActionTypes = {
            "connect": self.user.user_login,
            "register": self.user.user_register,
            "time": self.user.time,
            "name": self.user.get_pc_name,
            "exit": self.user.exit,
            "screenshot": self.user.send_screen_shot,
            "run program": self.user.run_program,
            "get folder": self.user.get_folder
        }

    # Get Function based on action type, if no command then None
    def get_action_fn(self, command):
        if command not in self.UserActionTypes:
            print 'command {} not founded'.format(command)
            return None
        return self.UserActionTypes[command]
