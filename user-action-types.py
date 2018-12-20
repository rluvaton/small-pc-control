# importing enum for enumerations
import enum


# creating enumerations using class
class UserActionTypes(enum.Enum):
    login = 'Connect'
    register = 'Register'
    time = 'Time',
    name = 'Name',
    exit = 'Exit',
    screenShot = 'ScreenShot',
    runProgram = 'Run Program',
    openFolder = 'Open Folder'
