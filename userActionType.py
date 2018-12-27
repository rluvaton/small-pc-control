
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