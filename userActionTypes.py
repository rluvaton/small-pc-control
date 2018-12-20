from userActions import UserActions

# User Action Types
UserActionTypes = {
    "Connect": UserActions.user_login,
    "Register": UserActions.user_register,
    "Time": UserActions.time,
    "Name": UserActions.get_pc_name,
    "Exit": UserActions.exit,
    "ScreenShot": UserActions.send_screen_shot,
    "Run Program": UserActions.run_program,
    "Open Folder": UserActions.open_folder
}


# Get Function based on action type, if no command then None
def get_action_fn(command):
    if command not in UserActionTypes:
        print 'command {} not founded'.format(command)
        return None
    return UserActionTypes[command]
