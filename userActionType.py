from responseHandle import ResponseHandler

# User Action Types
UserActionTypes = {
    "name": ResponseHandler.server_name_handler,
    "exit": ResponseHandler.exit_handler,
    "screenshot": ResponseHandler.screenshot_handler,
}


# Get Function based on action type, if no command then None
def get_action_fn(command):
    if command not in UserActionTypes:
        return None
    return UserActionTypes[command]
