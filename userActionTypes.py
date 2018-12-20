# importing enum for enumerations
import enum
from .userActions import *


# creating enumerations using class
class UserActionTypes(enum.Enum):
    login = ('Connect', UserActions.user_login)
    register = ('Register', UserActions.user_register)
    time = ('Time', UserActions.time),
    name = ('Name', UserActions.get_pc_name),
    exit = ('Exit', UserActions.exit),
    screenShot = ('ScreenShot', UserActions.send_screen_shot),
    runProgram = ('Run Program', UserActions.run_program),
    openFolder = ('Open Folder', UserActions.open_folder)
