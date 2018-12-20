from userActions import UserActions

# User Action Types
UserActionTypes = {
    "connect": UserActions.user_login,
    "register": UserActions.user_register,
    "time": UserActions.time,
    "name": UserActions.get_pc_name,
    "exit": UserActions.exit,
    "screenshot": UserActions.send_screen_shot,
    "run program": UserActions.run_program,
    "open folder": UserActions.open_folder
}


# Get Function based on action type, if no command then None
def get_action_fn(command):
    if command not in UserActionTypes:
        print 'command {} not founded'.format(command)
        return None
    return UserActionTypes[command]
