import os
import hashlib
import threading

mutex = threading.Lock()


# Create MD5
def compute_MD5_hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


# Singleton Pattern
singleton = None


class UserManagement(object):

    @staticmethod
    def singleton():
        global singleton
        singleton = singleton if singleton is not None else UserManagement()

    def __init__(self):
        # File path
        dir_name = os.path.dirname(__file__)
        self.file_path = os.path.join(dir_name, './{}'.format('users_data.txt'))

    # Create record format in the DB
    @staticmethod
    def create_record_format(user_name, password):
        return user_name + ' | ' + compute_MD5_hash(password)

    # Update Users File
    # -----------------
    # username must be unique
    # -----------------
    # If Success return success message
    # If user already exists return 'User Already exists for this User Name'
    # If Error at reading file return 'Error occurred, try again later'
    def add_user_record(self, username, password):
        if username is None or password is None:
            return 'Argument Exception', False

        try:
            # Lock the resource
            res = mutex.acquire(False)
            if not res:
                err_msg = 'Error occurred, Stupid mutex (try again later)'
                print err_msg
                return err_msg, False

            # a opening type:
            # Opens a file for appending.
            # The file pointer is at the end of the file if the file exists.
            # That is, the file is in the append mode.
            # If the file does not exist, it creates a new file for writing.
            with open(self.file_path, 'a+') as fp:
                try:
                    # Go to the start of the file
                    fp.seek(0)

                    founded = False

                    cmp_record = UserManagement.create_record_format(username, password)

                    # Search if exist
                    for record in fp:
                        record = record.replace('\n', '')
                        if record == cmp_record:
                            founded = True
                            break

                    if founded:
                        fp.close()
                        return 'User Already exists for this User Name', True

                    fp.writelines(cmp_record + '\n')
                    fp.close()
                except Exception, ex:
                    fp.close()
                    err_msg = 'Error occurred, try again later'
                    print err_msg, ex
                    return err_msg, False

            # Release the lock
            mutex.release()
        except Exception, ex:
            err_msg = 'Error occurred, try again later'
            print err_msg, ex
            return err_msg, False

        return 'User registered successfully', True

    # Search User
    # -----------
    # Return Success message
    # If user not founded return 'Bad connection parameters' message
    # If Error at reading file return 'Error occurred, try again later'
    def search_user_record(self, username, password):
        if username is None or password is None:
            return 'Argument Exception', False

        try:

            # Lock the resource
            res = mutex.acquire(False)
            if not res:
                err_msg = 'Error occurred, Stupid mutex (try again later)'
                print err_msg
                return err_msg, False

            # a opening type:
            # Opens a file for appending.
            # The file pointer is at the end of the file if the file exists.
            # That is, the file is in the append mode.
            # If the file does not exist, it creates a new file for writing.
            with open(self.file_path, 'a+') as fp:
                # Go to the start of the file
                fp.seek(0)

                founded = False

                cmp_record = UserManagement.create_record_format(username, password)

                # Search if exist
                for record in fp:
                    record = record.replace('\n', '')
                    if record == cmp_record:
                        founded = True
                        break

                if founded:
                    # Release the lock
                    mutex.release()

                    fp.close()
                    return 'User logged in successfully', True

                fp.close()

                # Release the lock
                mutex.release()

                return 'Bad connection parameters', False
        except Exception, ex:
            err_msg = 'Error occurred, try again later'
            print err_msg, ex
            return err_msg, False


# Singleton Pattern
UserManagement.singleton()

# if __name__ == '__main__':
